"""Select platform for NIBE."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NIBE_SELECTS
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

NIBE_SELECTS = [
    {"name": "Hot Water Demand", "address": 56, "register_type": "HOLDING_REGISTERS", "options": ["Small", "Medium", "Large", "Unused", "Smart Control"]},
    {"name": "Operating Mode", "address": 237, "register_type": "HOLDING_REGISTERS", "options": ["Auto", "Manual", "Addition Only"]},
    {"name": "Brine Pump Mode", "address": 96, "register_type": "HOLDING_REGISTERS", "options": ["Auto", "Manual"]},
    {"name": "Heating Pump Mode", "address": 853, "register_type": "HOLDING_REGISTERS", "options": ["Auto", "Manual"]},
    {"name": "Operational Priority", "address": 1028, "register_type": "INPUT_REGISTERS", "options": ["Off", "Hot Water", "Heating", "Pool", "Cooling"]},
]

async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup select platform."""
    _LOGGER.debug("Setting up NIBE selects")

    coordinator = hass.data[DOMAIN]["coordinator"]
    selects = [NibeSelect(coordinator, select, entry) for select in NIBE_SELECTS]
    async_add_devices(selects)


class NibeSelect(NibeEntity, SelectEntity):
    """NIBE select entity class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("Initializing NibeSelect: %s", idx["name"])
        super().__init__(coordinator, idx, config_entry)
        self.idx = idx
        self.coordinator = coordinator
        self._attr_options = idx["options"]
        self._attr_current_option = self._get_value()

    def _get_value(self):
        """Retrieve the current value from the coordinator."""
        raw_value = self.coordinator.holding_registers.get(self.idx["address"], 0)
        return self.idx["options"][raw_value] if raw_value < len(self.idx["options"]) else None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_option = self._get_value()
        _LOGGER.debug("Updated NibeSelect %s: %s", self._attr_name, self._attr_current_option)
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        _LOGGER.debug("Setting NibeSelect option: %s", option)
        if option in self._attr_options:
            value = self._attr_options.index(option)
            await self.coordinator.write_register(self.idx["address"], value)
