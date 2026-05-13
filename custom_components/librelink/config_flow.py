"""Adds config flow for LibreLink."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_UNIT_OF_MEASUREMENT, CONF_USERNAME
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.config_entries import ConfigEntry

from .api import (
    LibreLinkApiAuthenticationError,
    LibreLinkApiCommunicationError,
    LibreLinkApiError,
    LibreLinkApiLogin,
)
from .const import BASE_URL_LIST, COUNTRY, COUNTRY_LIST, DOMAIN, LOGGER, MG_DL, MMOL_L

# GVS: Init logger
_LOGGER = logging.getLogger(__name__)


class LibreLinkFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for LibreLink."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    base_url=BASE_URL_LIST.get(user_input[COUNTRY]),
                )
            except LibreLinkApiAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except LibreLinkApiCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except LibreLinkApiError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                    vol.Required(
                        COUNTRY,
                        description="Country",
                        default=(COUNTRY_LIST[0]),
                    ): vol.In(COUNTRY_LIST),
                    vol.Required(
                        CONF_UNIT_OF_MEASUREMENT,
                        default=(MG_DL),
                    ): vol.In({MG_DL, MMOL_L}),
                }
            ),
            errors=_errors,
        )

    async def async_step_reauth(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle re-authentication when credentials or T&S change."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle re-authentication confirmation."""
        _errors = {}
        reauth_entry: ConfigEntry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        if user_input is not None:
            try:
                await self._test_credentials(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    base_url=BASE_URL_LIST.get(reauth_entry.data[COUNTRY]),
                )
            except LibreLinkApiAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except LibreLinkApiCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except LibreLinkApiError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                self.hass.config_entries.async_update_entry(
                    reauth_entry,
                    data={**reauth_entry.data, **user_input},
                )
                await self.hass.config_entries.async_reload(reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=reauth_entry.data.get(CONF_USERNAME, ""),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            description_placeholders={
                "username": reauth_entry.data.get(CONF_USERNAME, ""),
            },
            errors=_errors,
        )

    async def _test_credentials(
        self, username: str, password: str, base_url: str
    ) -> None:
        """Validate credentials."""
        client = LibreLinkApiLogin(
            username=username,
            password=password,
            base_url=base_url,
            session=async_create_clientsession(self.hass),
        )

        await client.async_get_token()

