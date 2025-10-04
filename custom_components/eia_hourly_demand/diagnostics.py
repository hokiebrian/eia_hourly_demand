"""Diagnostics support for the EIA Hourly Demand integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    ATTR_LATEST_TIMESTAMP,
    ATTR_LATEST_VALUE,
    CONF_API_KEY,
    CONF_BA_ID,
    DATA_COORDINATOR,
    DOMAIN,
)
from .coordinator import EIAHourlyDemandCoordinator


def _mask_api_key(key: str) -> str:
    if len(key) <= 4:
        return "****"
    return f"****{key[-4:]}"


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    coordinator: EIAHourlyDemandCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]
    data = coordinator.data or {}

    return {
        "entry": {
            CONF_BA_ID: entry.data[CONF_BA_ID],
            CONF_API_KEY: _mask_api_key(entry.data[CONF_API_KEY]),
        },
        "latest": {
            ATTR_LATEST_TIMESTAMP: data.get(ATTR_LATEST_TIMESTAMP),
            ATTR_LATEST_VALUE: data.get(ATTR_LATEST_VALUE),
        },
    }
