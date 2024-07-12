"""The EIA Energy Data component."""

from .const import DOMAIN

CONF_API_KEY = "api_key"
CONF_ID = "ba_id"


def setup(hass, config):
    """Set up the EIA Energy component."""
    return True


async def async_setup_entry(hass, entry):
    """Set up EIA Energy Data from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True


async def async_unload_entry(hass, entry):
    """Unload the EIA Energy sensor platform."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Clean up the entry from hass.data
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return True
