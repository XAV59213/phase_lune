import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


from homeassistant.helpers import entity_registry as er  # noqa: E402

UIDS = {
    "slug": "phase_lune_moon_phase",
    "phase": "phase_lune_phase_de_la_lune",
    "illumination": "phase_lune_illumination",
    "anecdote": "phase_lune_anecdote",
}


def eid(hass, key):
    return er.async_get(hass).async_get_entity_id("sensor", "phase_lune", UIDS[key])
