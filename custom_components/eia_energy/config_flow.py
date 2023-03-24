from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class EIAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
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
