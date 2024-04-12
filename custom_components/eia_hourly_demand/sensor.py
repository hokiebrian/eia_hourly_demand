""" Setup EIA Sensor """
import logging
from datetime import timedelta, date
import json
import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorStateClass
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


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    api_key = config_entry.data[API_KEY]
    ba_id = config_entry.data[BA_ID]
    eia_data = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([EIASensor(api_key, ba_id, eia_data)], True)


class EIASensor(SensorEntity):
    _attr_icon = "mdi:factory"
    _attr_native_unit_of_measurement = "MWh"
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, api_key, ba_id, eia_data):
        self._api_key = api_key
        self._ba_id = ba_id
        self._eia_data = eia_data
        self._state = None

    @property
    def name(self):
        return f"Hourly Demand {self._ba_id}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"HourlyMWh{self._ba_id}"

    async def async_update(self):
        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = EIA_URL.format(
            api_key=self._api_key, ba_id=self._ba_id, start_date=start_date
        )
        _LOGGER.debug(f"Data {url}")
        async with aiohttp.ClientSession() as session:
            try:
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(url, timeout=timeout) as response:
                    data = await response.json()
                    if data["response"]["data"][0]["value"] is None:
                        value_as_float = 0
                    else:
                        value_as_float = float(data["response"]["data"][0]["value"])
                    self._state = value_as_float
            except aiohttp.ClientConnectorError as e:
                _LOGGER.debug(f"Connection Error: {e}")
                self._state = None
            except (IndexError, KeyError) as e:
                _LOGGER.error("Data Error, no data returned")
                _LOGGER.debug(f"Data Error: {e}")
                self._state = None
            except asyncio.TimeoutError as e:
                _LOGGER.error("Timeout Error, asyncio")
                _LOGGER.debug(f"Data Error: {e}")
                self._state = None
            except Exception as e:
                _LOGGER.error(f"An unexpected error occurred: {e}")
                self._state = None
