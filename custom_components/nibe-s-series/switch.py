"""Switch platform for NIBE."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, COIL, HOLDING_REGISTERS
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

NIBE_SWITCHES = [
    {"name": "Allow Heat (Manual)", "address": 181, "register_type": HOLDING_REGISTERS},
    {"name": "Allow Cooling (Manual)", "address": 182, "register_type": HOLDING_REGISTERS},
    {"name": "Reset Alarm", "address": 22, "register_type": HOLDING_REGISTERS},
    {"name": "Allow Addition (Manual)", "address": 180, "register_type": HOLDING_REGISTERS},
    {"name": "Operating Mode (Manual)", "address": 237, "register_type": HOLDING_REGISTERS},
]

async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup switch platform."""
    _LOGGER.debug("Setting up NIBE switches")

    coordinator = hass.data[DOMAIN]["coordinator"]
    switches = [NibeSwitch(coordinator, switch, entry) for switch in NIBE_SWITCHES]
    async_add_devices(switches)


class NibeSwitch(NibeEntity, SwitchEntity):
    """NIBE switch entity class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("Initializing NibeSwitch: %s", idx["name"])
        super().__init__(coordinator, idx, config_entry)
        self.idx = idx
        self.coordinator = coordinator
        self._attr_is_on = self._get_value()

    def _get_value(self):
        """Get the value from the coordinator."""
        if self.idx["register_type"] == COIL:
            return self.coordinator.coils.get(self.idx["address"], False)
        if self.idx["register_type"] == HOLDING_REGISTERS:
            return bool(self.coordinator.holding_registers.get(self.idx["address"], 0))

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self._get_value()
        _LOGGER.debug("Updated NibeSwitch %s: %s", self._attr_name, self._attr_is_on)
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        _LOGGER.debug("Turning on NibeSwitch: %s", self._attr_name)
        if self.idx["register_type"] == COIL:
            await self.coordinator.write_coil(self.idx["address"], True)
        elif self.idx["register_type"] == HOLDING_REGISTERS:
            await self.coordinator.write_register(self.idx["address"], 1)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        _LOGGER.debug("Turning off NibeSwitch: %s", self._attr_name)
        if self.idx["register_type"] == COIL:
            await self.coordinator.write_coil(self.idx["address"], False)
        elif self.idx["register_type"] == HOLDING_REGISTERS:
            await self.coordinator.write_register(self.idx["address"], 0)
