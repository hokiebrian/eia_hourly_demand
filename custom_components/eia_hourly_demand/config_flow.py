"""Config Flow for EIA Integration"""

from datetime import timedelta, date
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

API_KEY = "api_key"
BA_ID = "ba_id"

EIA_URL = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    "?api_key={api_key}&data[]=value&facets[respondent][]={ba_id}"
    "&facets[type][]=D&frequency=hourly&start={start_date}"
    "&sort[0][column]=period&sort[0][direction]=desc"
)


class EIAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EIA integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the user input
            valid = await self._validate_input(user_input)
            if not valid:
                errors["base"] = "invalid_api_key_or_ba_id"
            else:
                # If validation is successful, create and return the config entry
                return self.async_create_entry(title=user_input[BA_ID], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(API_KEY): str,
                    vol.Required(BA_ID): str,
                }
            ),
            errors=errors,
        )

    async def _validate_input(self, user_input):
        """Validate the user input."""
        api_key = user_input[API_KEY]
        ba_id = user_input[BA_ID]

        # Check if the API key and BA ID are valid by making a test API call
        start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
        url = EIA_URL.format(api_key=api_key, ba_id=ba_id, start_date=start_date)

        async with aiohttp.ClientSession() as session:
            try:
                timeout = aiohttp.ClientTimeout(
                    total=10
                )  # Adjusted timeout for reliability
                async with session.get(url, timeout=timeout) as response:
                    if response.status != 200:
                        return False
                    data = await response.json()
                    if not data["response"]["data"]:
                        return False
            except aiohttp.ClientConnectorError:
                return False
            except aiohttp.ClientResponseError as e:
                return False
            except aiohttp.TimeoutError:
                return False
            except Exception as e:
                return False

        return True
