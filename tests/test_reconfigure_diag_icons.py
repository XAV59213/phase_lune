import json
from pathlib import Path
from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.config_entries import UnknownEntry
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.components.diagnostics import get_diagnostics_for_config_entry

from custom_components.phase_lune.const import DOMAIN, PHASES
from custom_components.phase_lune.diagnostics import async_get_config_entry_diagnostics
from tests.conftest import UIDS, eid

ROOT = Path(__file__).parent.parent / "custom_components" / "phase_lune"


async def _setup(hass, **kw):
    e = MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, **kw)
    e.add_to_hass(hass)
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    return e


@pytest.mark.parametrize("kw", [{"options": {"country": "fr"}}, {"data": {"country": "FR"}}],
                         ids=["options", "legacy_data"])
async def test_reconfigure_country_reloads(hass, kw):
    e = await _setup(hass, **kw)
    reg_ids = {k: eid(hass, k) for k in UIDS}
    r = await e.start_reconfigure_flow(hass)
    assert r["type"] is FlowResultType.FORM and r["step_id"] == "reconfigure"
    assert next(iter(r["data_schema"].schema)).default() == "fr"
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {"country": "za"})
    assert r["type"] is FlowResultType.ABORT and r["reason"] == "reconfigure_successful"
    await hass.async_block_till_done()
    assert e.data == {} and e.options == {"country": "za"}
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert {k: eid(hass, k) for k in UIDS} == reg_ids  # entity ids stables
    assert hass.states.get(eid(hass, "slug")).attributes["hemisphere"] == "south"


async def test_reconfigure_rejects_unknown_entry(hass):
    with pytest.raises(UnknownEntry):
        await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_RECONFIGURE, "entry_id": "nope"})


async def test_diagnostics_no_sensitive_data(hass, hass_client):
    e = await _setup(hass, data={"country": "AU"}, title="Ma maison secrète")
    diag = await get_diagnostics_for_config_entry(hass, hass_client, e)
    assert diag["country"] == "au" and diag["hemisphere"] == "south" and diag["country_known"]
    assert diag["legacy_country_in_data"] is True and diag["anecdotes"] == 365
    assert diag["calculation"]["ok"] and diag["calculation"]["slug"] in PHASES
    dump = json.dumps(diag)
    for secret in (e.entry_id, DOMAIN + "_moon_phase", "Ma maison secrète", "latitude", str(hass.config.latitude)):
        assert secret not in dump


async def test_diagnostics_reports_calculation_error(hass):
    e = await _setup(hass, options={"country": "xx"})
    with patch("custom_components.phase_lune.calc.compute", side_effect=ValueError("boom")):
        diag = await async_get_config_entry_diagnostics(hass, e)
    assert diag["calculation"] == {"ok": False, "error": "ValueError"}
    assert diag["country_known"] is False and diag["hemisphere"] == "north"


async def test_icon_translations(hass):
    icons = json.loads((ROOT / "icons.json").read_text())["entity"]["sensor"]
    assert set(icons) == set(UIDS)
    assert set(icons["slug"]["state"]) == set(PHASES)
    assert icons["slug"]["state"]["full_moon"] == "mdi:moon-full"
    await _setup(hass, options={"country": "fr"})
    for k in ("slug", "illumination", "anecdote"):
        assert "icon" not in hass.states.get(eid(hass, k)).attributes  # icône fournie par icons.json
    assert hass.states.get(eid(hass, "phase")).attributes["icon"].startswith("mdi:moon-")


def test_brand_assets_spec():
    from PIL import Image
    b = ROOT / "brand"
    sizes = {"icon.png": (256, 256), "icon@2x.png": (512, 512),
             "dark_icon.png": (256, 256), "dark_icon@2x.png": (512, 512)}
    for f, size in sizes.items():
        assert Image.open(b / f).size == size
    for f, (lo, hi) in {"logo.png": (128, 256), "logo@2x.png": (256, 512)}.items():
        im = Image.open(b / f)
        assert lo <= min(im.size) <= hi and im.size[0] > im.size[1]
        assert im.getchannel("A").getbbox() == (0, 0) + im.size  # recadré
