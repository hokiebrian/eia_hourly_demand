"""Config flow for the EIA Hourly Demand integration."""

from __future__ import annotations

import asyncio
from datetime import date, timedelta
from typing import Any

from aiohttp import ClientError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import aiohttp_client, selector

from .const import CONF_API_KEY, CONF_BA_ID, DOMAIN

EIA_URL = (
    "https://api.eia.gov/v2/electricity/rto/region-data/data/"
    "?api_key={api_key}&data[]=value&facets[respondent][]={ba_id}"
    "&facets[type][]=D&frequency=hourly&start={start_date}"
    "&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1"
)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate invalid API key or BA ID."""


async def _async_validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate user input by reaching out to the EIA API."""

    session = aiohttp_client.async_get_clientsession(hass)
    start_date = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = EIA_URL.format(
        api_key=data[CONF_API_KEY],
        ba_id=data[CONF_BA_ID],
        start_date=start_date,
    )

    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status in (401, 403):
                raise InvalidAuth
            if resp.status == 404:
                raise InvalidAuth
            resp.raise_for_status()
            payload = await resp.json()
    except asyncio.TimeoutError as err:
        raise CannotConnect from err
    except ClientError as err:
        raise CannotConnect from err

    if not payload.get("response", {}).get("data"):
        raise InvalidAuth

    return {"title": data[CONF_BA_ID]}


class EIAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the EIA Hourly Demand integration."""

    VERSION = 1

    def __init__(self) -> None:
        self._reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_BA_ID].lower())
            self._abort_if_unique_id_configured()

            try:
                info = await _async_validate_input(self.hass, user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self._build_schema(user_input),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> FlowResult:
        """Handle re-authentication when credentials fail."""

        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Prompt for updated credentials during reauth."""

        assert self._reauth_entry is not None
        errors: dict[str, str] = {}

        if user_input is not None:
            new_data = {
                **self._reauth_entry.data,
                CONF_API_KEY: user_input[CONF_API_KEY],
            }

            try:
                await _async_validate_input(self.hass, new_data)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                self.hass.config_entries.async_update_entry(
                    self._reauth_entry, data=new_data
                )
                await self.hass.config_entries.async_reload(self._reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_API_KEY,
                        default=self._reauth_entry.data[CONF_API_KEY],
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                    ),
                }
            ),
            errors=errors,
        )

    def _build_schema(self, user_input: dict[str, Any] | None) -> vol.Schema:
        user_input = user_input or {}
        return vol.Schema(
            {
                vol.Required(
                    CONF_API_KEY,
                    default=user_input.get(CONF_API_KEY, ""),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                ),
                vol.Required(
                    CONF_BA_ID,
                    default=user_input.get(CONF_BA_ID, ""),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
                ),
            }
        )
