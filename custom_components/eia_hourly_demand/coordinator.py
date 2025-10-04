"""Data update coordinator for the EIA Hourly Demand integration."""

from __future__ import annotations

import asyncio
import logging
from datetime import date, timedelta
from typing import Any

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ATTR_LATEST_TIMESTAMP,
    ATTR_LATEST_VALUE,
    CONF_API_KEY,
    CONF_BA_ID,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

EIA_URL = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    "?api_key={api_key}&data[]=value&facets[respondent][]={ba_id}"
    "&facets[type][]=D&frequency=hourly&start={start_date}"
    "&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1"
)


class EIAHourlyDemandCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to retrieve the most recent demand value."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._api_key = entry.data[CONF_API_KEY]
        self._ba_id = entry.data[CONF_BA_ID]
        self._session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=f"EIA Hourly Demand ({self._ba_id})",
            update_interval=DEFAULT_UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = EIA_URL.format(
            api_key=self._api_key, ba_id=self._ba_id, start_date=start_date
        )

        try:
            async with self._session.get(url, timeout=10) as response:
                if response.status == 401:
                    raise UpdateFailed("Invalid API key")
                if response.status == 404:
                    raise UpdateFailed("Balancing Authority not found")
                response.raise_for_status()

                payload = await response.json()
        except ClientError as err:
            raise UpdateFailed(f"Error communicating with EIA API: {err}") from err
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout communicating with EIA API") from err

        data = payload.get("response", {}).get("data", [])
        if not data:
            raise UpdateFailed("No data returned from EIA API")

        latest = data[0]
        try:
            latest_value = float(latest["value"])
        except (KeyError, TypeError, ValueError) as err:
            raise UpdateFailed("Malformed data from EIA API") from err

        return {
            ATTR_LATEST_TIMESTAMP: latest.get("period"),
            ATTR_LATEST_VALUE: latest_value,
        }
