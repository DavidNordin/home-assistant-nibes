"""Nibe integration"""
import logging
import asyncio
from custom_components.nibe.helpers.general import get_parameter
from custom_components.nibe.nibe_coordinator import NibeCoordinator

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from pymodbus.client import AsyncModbusTcpClient

from .const import (
    CONF_HOST_NAME,
    CONF_HOST_PORT,
    DOMAIN,
    PLATFORMS,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration using YAML (not supported)."""
    _LOGGER.debug("async_setup: YAML configuration is not supported")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration from a configuration entry."""
    _LOGGER.debug("Setting up entry: %s", entry.title)

    host_name = entry.data.get(CONF_HOST_NAME)
    host_port = int(entry.data.get(CONF_HOST_PORT))
    client = AsyncModbusTcpClient(host_name, port=host_port)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = NibeCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN]["coordinator"] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a configuration entry."""
    _LOGGER.debug("Unloading entry: %s", entry.title)

    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unloaded:
        coordinator = hass.data[DOMAIN].pop("coordinator", None)
        if coordinator is not None:
            coordinator.close()

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload a configuration entry."""
    _LOGGER.debug("Reloading entry: %s", entry.title)
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
