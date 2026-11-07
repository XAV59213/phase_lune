from datetime import datetime, timezone

from freezegun.api import freeze_time
from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers import device_registry as dr, entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.phase_lune.const import CARD_URL, DOMAIN, IMAGES_URL
from tests.conftest import UIDS, eid

FULL = datetime(2024, 1, 25, 17, 54, tzinfo=timezone.utc)  # pleine lune réelle


def _entry(hass, country="fr"):
    e = MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, data={"country": country})
    e.add_to_hass(hass)
    return e


async def test_setup_unload_reload(hass):
    e = _entry(hass)
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    assert e.state is ConfigEntryState.LOADED
    assert len(hass.states.async_entity_ids("sensor")) == 4
    assert await hass.config_entries.async_reload(e.entry_id)
    await hass.async_block_till_done()
    assert e.state is ConfigEntryState.LOADED
    assert await hass.config_entries.async_unload(e.entry_id)
    await hass.async_block_till_done()
    assert e.state is ConfigEntryState.NOT_LOADED


async def test_four_sensors_full_moon(hass):
    with freeze_time(FULL):
        e = _entry(hass)
        assert await hass.config_entries.async_setup(e.entry_id)
        await hass.async_block_till_done()
    reg = er.async_get(hass)
    for k, uid in UIDS.items():
        ent = reg.async_get(eid(hass, k))
        assert ent.unique_id == uid and ent.has_entity_name and ent.translation_key == k
    slug = hass.states.get(eid(hass, "slug"))
    assert slug.state == "full_moon"
    assert slug.attributes["entity_picture"] == f"{IMAGES_URL}/full_moon.png"
    assert slug.attributes["phase_fr"] == "Pleine lune"
    assert slug.attributes["illumination"] > 95
    assert slug.attributes["day_of_year"] == 25
    assert slug.attributes["anecdote"] and slug.attributes["anecdote_en"]
    assert hass.states.get(eid(hass, "phase")).state == "Pleine lune"
    ill = hass.states.get(eid(hass, "illumination"))
    assert 95 < float(ill.state) <= 100 and ill.attributes["unit_of_measurement"] == "%"
    an = hass.states.get(eid(hass, "anecdote"))
    assert an.state == an.attributes["anecdote"][:255]
    assert "entity_picture" not in an.attributes
    devs = dr.async_entries_for_config_entry(dr.async_get(hass), e.entry_id)
    assert len(devs) == 1 and devs[0].name == "Phase de la Lune"


async def test_southern_hemisphere_mirrors_image(hass):
    with freeze_time(datetime(2024, 1, 18, 3, 53, tzinfo=timezone.utc)):  # premier quartier
        e = _entry(hass, "au")
        assert await hass.config_entries.async_setup(e.entry_id)
        await hass.async_block_till_done()
    st = hass.states.get(eid(hass, "slug"))
    assert st.state == "first_quarter"
    assert st.attributes["image_slug"] == "last_quarter"
    assert st.attributes["entity_picture"].endswith("/last_quarter.png")


async def test_renamed_entity_id_preserved(hass):
    e = _entry(hass)
    er.async_get(hass).async_get_or_create(
        "sensor", DOMAIN, UIDS["phase"], config_entry=e, suggested_object_id="ma_lune")
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    assert eid(hass, "phase") == "sensor.ma_lune"
    assert hass.states.get("sensor.ma_lune") is not None
    assert len(hass.states.async_entity_ids("sensor")) == 4


async def test_card_and_static_paths_registered(hass):
    from homeassistant.setup import async_setup_component
    assert await async_setup_component(hass, "http", {})
    e = _entry(hass)
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    assert hass.data[DOMAIN]["_card_registered"] is True
    from homeassistant.components.frontend import DATA_EXTRA_JS_URL_ES5  # noqa: F401
    urls = hass.data["frontend_extra_module_url"].urls
    assert any(u.startswith(CARD_URL + "?v=") for u in urls)
