import logging
from pathlib import Path
from unittest.mock import patch

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_component import async_update_entity
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.phase_lune import frontend, sensor
from custom_components.phase_lune.const import CARD_URL, DOMAIN, PHASES
from tests.conftest import UIDS, eid


async def _setup(hass, country="fr"):
    e = MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, options={"country": country})
    e.add_to_hass(hass)
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    return e


async def test_unavailable_logged_once_then_recovers(hass, caplog):
    await _setup(hass)
    ids = [eid(hass, k) for k in UIDS]
    caplog.set_level(logging.INFO, logger="custom_components.phase_lune")
    with patch("custom_components.phase_lune.calc.compute", side_effect=OSError("boom")):
        for _ in range(2):
            for i in ids:
                await async_update_entity(hass, i)
    assert all(hass.states.get(i).state == STATE_UNAVAILABLE for i in ids)
    assert caplog.text.count("calcul impossible") == 4  # une fois par entité, pas à chaque essai
    for i in ids:
        await async_update_entity(hass, i)
    assert all(hass.states.get(i).state != STATE_UNAVAILABLE for i in ids)
    assert caplog.text.count("calcul rétabli") == 4


async def test_enum_device_class_and_service_device(hass):
    e = await _setup(hass)
    st = hass.states.get(eid(hass, "slug"))
    assert st.attributes["device_class"] == SensorDeviceClass.ENUM
    assert st.attributes["options"] == list(PHASES) and st.state in PHASES
    dev = dr.async_entries_for_config_entry(dr.async_get(hass), e.entry_id)[0]
    assert dev.entry_type is dr.DeviceEntryType.SERVICE and dev.sw_version
    assert sensor.PARALLEL_UPDATES == 0


async def test_setup_survives_card_registration_error(hass, caplog):
    with patch("custom_components.phase_lune.async_register_card", side_effect=RuntimeError("x")):
        await _setup(hass)
    assert "Carte Lovelace non enregistrée" in caplog.text
    assert DOMAIN in hass.data and not hass.data[DOMAIN].get("_card_registered")
    assert len(hass.states.async_entity_ids("sensor")) == 4


async def test_card_missing_file_is_skipped(hass, caplog, tmp_path):
    with patch.object(frontend, "Path") as p:
        p.return_value.parent = tmp_path
        await frontend.async_register_card(hass)
    assert "Fichier de carte introuvable" in caplog.text


async def test_register_without_images_and_duplicate_paths(hass, tmp_path):
    assert await async_setup_component(hass, "http", {})
    assert await async_setup_component(hass, "frontend", {})
    pkg = tmp_path / "pkg"
    (pkg / "frontend").mkdir(parents=True)
    (pkg / "frontend" / "phase-lune-card.js").write_text("//")
    with patch.object(frontend, "__file__", str(pkg / "frontend" / "__init__.py")):
        with patch.object(hass.http, "async_register_static_paths") as reg:
            await frontend.async_register_card(hass)
            urls = [c.url_path for c in reg.call_args.args[0]]
            assert urls == ["/phase_lune_frontend"]  # pas d'images ni anecdotes absentes
            reg.side_effect = RuntimeError("already")
            await frontend.async_register_card(hass)  # doublon toléré
    assert any(u.startswith(CARD_URL) for u in hass.data["frontend_extra_module_url"].urls)


def test_version_fallback_on_unreadable_manifest():
    from custom_components.phase_lune.const import VERSION
    assert frontend._version() == VERSION
    with patch.object(Path, "read_text", side_effect=OSError):
        assert frontend._version() == "0"


async def test_async_setup_does_not_register_card_twice(hass):
    from custom_components import phase_lune
    hass.data[DOMAIN] = {"_card_registered": True}
    with patch("custom_components.phase_lune.async_register_card") as reg:
        assert await phase_lune.async_setup(hass, {})
    reg.assert_not_called()
