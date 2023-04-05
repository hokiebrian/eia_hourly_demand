from homeassistant import config_entries
import voluptuous as vol
import aiohttp
from datetime import timedelta, date
from .const import DOMAIN

class EIAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate the user input
            if not await self._validate_input(user_input):
                errors["base"] = "invalid API Key or Balancing Authority"
            else:
                # If validation is successful, create and return the config entry
                return self.async_create_entry(title=user_input["ba_id"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("ba_id"): str,
                }
            ),
            errors=errors,
        )

    async def _validate_input(self, user_input):
        """Validate the user input."""
        api_key = user_input["api_key"]
        ba_id = user_input["ba_id"]

        # Check if the API key is valid by making a test API call

        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = (f"https://api.eia.gov/v2/electricity/rto/region-data/data/"
               f"?api_key={api_key}&data[]=value&facets[respondent][]={ba_id}"
               f"&facets[type][]=D&frequency=hourly&start={start_date}"
               f"&sort[0][column]=period&sort[0][direction]=desc")

        async with aiohttp.ClientSession() as session:
            try:
                timeout = aiohttp.ClientTimeout(total=5)
                async with session.get(url, timeout=timeout) as response:
                    if response.status != 200:
                        return False
                    data = await response.json()
                    if (data["response"]["total"]) == 0:
                        return False
            except:
                pass

        return True