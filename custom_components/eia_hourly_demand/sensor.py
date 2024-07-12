"""
Setup EIA Sensor
"""

import logging
from datetime import timedelta, date
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=1800)

API_KEY = "api_key"
BA_ID = "ba_id"

EIA_URL = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    "?api_key={api_key}&data[]=value&facets[respondent][]={ba_id}"
    "&facets[type][]=D&frequency=hourly&start={start_date}"
    "&sort[0][column]=period&sort[0][direction]=desc"
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the EIA sensor entry."""
    api_key = config_entry.data[API_KEY]
    ba_id = config_entry.data[BA_ID]
    eia_data = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([EIASensor(api_key, ba_id, eia_data)], True)


class EIASensor(SensorEntity):
    """Representation of an EIA Sensor."""

    _attr_icon = "mdi:factory"
    _attr_native_unit_of_measurement = "MWh"
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, api_key: str, ba_id: str, eia_data: dict):
        """Initialize the sensor."""
        self._api_key = api_key
        self._ba_id = ba_id
        self._eia_data = eia_data
        self._state = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Hourly Demand {self._ba_id}"

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the sensor."""
        return f"HourlyMWh{self._ba_id}"

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = EIA_URL.format(
            api_key=self._api_key, ba_id=self._ba_id, start_date=start_date
        )
        _LOGGER.debug(f"Fetching data from URL: {url}")

        async with aiohttp.ClientSession() as session:
            try:
                timeout = aiohttp.ClientTimeout(total=10)
                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()  # Raise an error for bad HTTP status codes
                    data = await response.json()
                    self._state = float(data["response"]["data"][0]["value"])
            except aiohttp.ClientConnectorError as e:
                _LOGGER.error(f"Connection Error: {e}")
                self._state = None
            except (IndexError, KeyError) as e:
                _LOGGER.error("Data Error: Invalid or no data returned")
                _LOGGER.debug(f"Error details: {e}")
                self._state = None
            except aiohttp.TimeoutError as e:
                _LOGGER.error("Timeout Error: Request timed out")
                _LOGGER.debug(f"Error details: {e}")
                self._state = None
            except aiohttp.ClientResponseError as e:
                _LOGGER.error(f"HTTP Error: {e.status} - {e.message}")
                self._state = None
            except Exception as e:
                _LOGGER.error(f"An unexpected error occurred: {e}")
                self._state = None
