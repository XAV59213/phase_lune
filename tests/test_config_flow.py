from tests.conftest import eid
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.phase_lune.const import DOMAIN, NAME


async def test_user_flow_default_france(hass):
    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert r["type"] is FlowResultType.FORM and r["step_id"] == "user"
    key = next(iter(r["data_schema"].schema))
    assert key.default() == "fr"
    r = await hass.config_entries.flow.async_configure(r["flow_id"], {"country": "au"})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    assert r["title"] == NAME and r["data"] == {"country": "au"}
    assert r["result"].unique_id == DOMAIN


async def test_single_instance(hass):
    MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, data={"country": "fr"}).add_to_hass(hass)
    r = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert r["type"] is FlowResultType.ABORT and r["reason"] == "already_configured"


async def test_options_flow_changes_country_and_reloads(hass):
    e = MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, data={"country": "fr"})
    e.add_to_hass(hass)
    assert await hass.config_entries.async_setup(e.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get(eid(hass, "slug")).attributes["hemisphere"] == "north"
    r = await hass.config_entries.options.async_init(e.entry_id)
    assert r["type"] is FlowResultType.FORM
    assert next(iter(r["data_schema"].schema)).default() == "fr"
    r = await hass.config_entries.options.async_configure(r["flow_id"], {"country": "nz"})
    assert r["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert e.options == {"country": "nz"}
    st = hass.states.get(eid(hass, "slug"))
    assert st.attributes["country"] == "nz" and st.attributes["hemisphere"] == "south"
