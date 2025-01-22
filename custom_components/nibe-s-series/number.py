"""Number platform for Nibe."""
import logging

from homeassistant.components.number import NumberEntity, NumberDeviceClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NIBE_NUMBERS
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

NIBE_NUMBERS = [
    {"name": "Degree Minutes", "address": 11, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 0.1, "min_value": -300, "max_value": 300, "step": 1},
    {"name": "Cooling Degree Minutes", "address": 20, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 1, "min_value": -300, "max_value": 300, "step": 1},
    {"name": "Heating Curve", "address": 26, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 1, "min_value": 0, "max_value": 100, "step": 1},
    {"name": "Heating Curve Offset", "address": 30, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 1, "min_value": -10, "max_value": 10, "step": 0.5},
    {"name": "Minimum Flow Temp", "address": 34, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 20, "max_value": 60, "step": 0.1},
    {"name": "Maximum Flow Temp", "address": 38, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 30, "max_value": 80, "step": 0.1},
    {"name": "Start Temp Hot Water (Normal)", "address": 59, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 35, "max_value": 60, "step": 0.1},
    {"name": "Stop Temp Hot Water (Normal)", "address": 63, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 40, "max_value": 65, "step": 0.1},
    {"name": "Period Time Heating", "address": 92, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "s", "scale": 1, "min_value": 10, "max_value": 300, "step": 1},
    {"name": "Period Time Hot Water", "address": 93, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "s", "scale": 1, "min_value": 10, "max_value": 300, "step": 1},
    {"name": "Period Time Cooling", "address": 94, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "s", "scale": 1, "min_value": 10, "max_value": 300, "step": 1},
    {"name": "Degree Minutes Start Addition", "address": 679, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 1, "min_value": -500, "max_value": 0, "step": 1},
    {"name": "Degree Minutes Start Compressor", "address": 97, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": None, "scale": 1, "min_value": -500, "max_value": 0, "step": 1},
    {"name": "Control Calculated Flow Temp (Heat)", "address": 5009, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 10, "max_value": 50, "step": 0.1},
    {"name": "Control Calculated Flow Temp (Cooling)", "address": 5017, "register_type": "HOLDING_REGISTERS", "unit_of_measurement": "°C", "scale": 0.1, "min_value": 10, "max_value": 50, "step": 0.1},
]

async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup number platform."""
    _LOGGER.debug("Setting up Nibe numbers")
    coordinator = hass.data[DOMAIN]["coordinator"]

    numbers = [NibeNumber(coordinator, number, entry) for number in NIBE_NUMBERS]
    async_add_devices(numbers)


class NibeNumber(NibeEntity, NumberEntity):
    """Nibe number entity class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("Initializing NibeNumber: %s", idx["name"])
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.address = idx["address"]
        self.scale = idx.get("scale", 1)
        self._attr_device_class = idx.get("device_class", None)
        self._attr_native_unit_of_measurement = idx.get("unit_of_measurement", None)
        self._attr_native_min_value = idx.get("min_value", 0)
        self._attr_native_max_value = idx.get("max_value", 100)
        self._attr_native_step = idx.get("step", 1)
        self._attr_native_value = self._get_value()

    def _get_value(self):
        """Retrieve the scaled value from the coordinator."""
        raw_value = self.coordinator.holding_registers.get(self.address, 0)
        return round(raw_value * self.scale, 2)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "Updated NibeNumber %s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Set the new value."""
        _LOGGER.debug("Setting NibeNumber value: %s", value)
        raw_value = int(value / self.scale)
        await self.coordinator.write_register(self.address, raw_value)
