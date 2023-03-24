from datetime import timedelta, date
import json
import aiohttp

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import CONF_API_KEY, CONF_ID
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=1800)

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data[CONF_API_KEY]
    ba_id = config_entry.data[CONF_ID]
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
        return "Hourly Demand " + self._ba_id

    @property
    def state(self):
        return self._state
    
    @property
    def unique_id(self):
        return "HourlyMWh" + self._ba_id

    async def async_update(self):
        start_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        url = (f"https://api.eia.gov/v2/electricity/rto/region-data/data/"
               f"?api_key={self._api_key}&data[]=value&facets[respondent][]={self._ba_id}"
               f"&facets[type][]=D&frequency=hourly&start={start_date}"
               f"&sort[0][column]=period&sort[0][direction]=desc")

        async with aiohttp.ClientSession() as session:
            try:
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(url, timeout=timeout) as response:
                    data = await response.json()
                    self._state = json.dumps(data["response"]["data"][0]["value"])
            except:
                self._state = -1

