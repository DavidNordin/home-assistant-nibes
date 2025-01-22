"""Adds config flow for NIBE."""
import logging
from typing import Any, Optional

import voluptuous as vol
from pymodbus.client import AsyncModbusTcpClient

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_HOST_NAME,
    CONF_HOST_PORT,
    CONF_DEVICE_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class NibeIqcConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for NIBE."""

    VERSION = 1
    user_input: Optional[dict[str, Any]]

    def __init__(self):
        """Initialize the config flow."""
        _LOGGER.debug("NibeIqcConfigFlow.__init__")
        self._errors = {}
        self.user_input = {}

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the user configuration step."""
        _LOGGER.debug("NibeIqcConfigFlow.async_step_user")
        self._errors = {}

        if user_input is None:
            user_input = {}
        else:
            # Validate the connection
            error = await self._validate_connection(user_input)
            if error is None:
                self.user_input = user_input
                return self.async_create_entry(
                    title=user_input[CONF_DEVICE_NAME], data=self.user_input
                )
            self._errors[error[0]] = error[1]

        return await self._show_config_form_user(user_input)

    async def _show_config_form_user(self, user_input) -> FlowResult:
        """Show the configuration form."""
        user_schema = {
            vol.Required(CONF_DEVICE_NAME): cv.string,
            vol.Required(CONF_HOST_NAME): cv.string,
            vol.Required(CONF_HOST_PORT, default=502): cv.positive_int,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(user_schema),
            errors=self._errors,
            last_step=True,
        )

    async def _validate_connection(self, user_input: dict) -> Optional[tuple[str, str]]:
        """Validate connection to the Modbus device."""
        host = user_input[CONF_HOST_NAME]
        port = user_input[CONF_HOST_PORT]

        try:
            async with AsyncModbusTcpClient(host, port) as client:
                await client.connect()
                if not client.connected:
                    _LOGGER.error("Failed to connect to Modbus device at %s:%d", host, port)
                    return "base", "cannot_connect"

        except Exception as e:
            _LOGGER.error("Error connecting to Modbus device: %s", e)
            return "base", "cannot_connect"

        return None


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler for NIBE."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry
        self._errors = {}

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Handle options configuration."""
        self._errors = {}

        if user_input is not None:
            # Validate the connection
            error = await self._validate_connection(user_input)
            if error is None:
                return self.async_create_entry(
                    title=self.config_entry.title, data=user_input
                )
            self._errors[error[0]] = error[1]

        return self._show_options_form(user_input)

    def _show_options_form(self, user_input) -> FlowResult:
        """Show the options form."""
        user_schema = {
            vol.Required(
                CONF_HOST_NAME, default=self.config_entry.data.get(CONF_HOST_NAME, "")
            ): cv.string,
            vol.Required(
                CONF_HOST_PORT, default=self.config_entry.data.get(CONF_HOST_PORT, 502)
            ): cv.positive_int,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(user_schema),
            errors=self._errors,
            last_step=True,
        )

    async def _validate_connection(self, user_input: dict) -> Optional[tuple[str, str]]:
        """Validate connection to the Modbus device."""
        host = user_input[CONF_HOST_NAME]
        port = user_input[CONF_HOST_PORT]

        try:
            async with AsyncModbusTcpClient(host, port) as client:
                await client.connect()
                if not client.connected:
                    _LOGGER.error("Failed to connect to Modbus device at %s:%d", host, port)
                    return "base", "cannot_connect"

        except Exception as e:
            _LOGGER.error("Error connecting to Modbus device: %s", e)
            return "base", "cannot_connect"

        return None
