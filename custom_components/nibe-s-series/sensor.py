"""Sensor platform for NIBE."""
import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    EntityCategory,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from pymodbus.client.mixin import ModbusClientMixin

from .const import DOMAIN, INPUT_REGISTERS, HOLDING_REGISTERS
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

NIBE_SENSORS = [
    # Temperature sensors
    {"name": "Outdoor Temperature (BT1)", "address": 1, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Supply Temperature (BT2)", "address": 5, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Return Temperature (BT3)", "address": 7, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Hot Water Start (BT5)", "address": 2014, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Hot Water Top (BT7)", "address": 8, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Hot Water Charging (BT6)", "address": 9, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Cold Carrier In (BT10)", "address": 10, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Cold Carrier Out (BT11)", "address": 11, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Temperature (BT12)", "address": 12, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Hot Gas Temperature (BT14)", "address": 13, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Liquid Line Temperature (BT15)", "address": 14, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Suction Gas Temperature (BT17)", "address": 16, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Room Temperature 1 (BT50)", "address": 26, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "External Flow Temperature (BT25)", "address": 39, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Compressor Temperature (BT29)", "address": 86, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},

    # Flow and current sensors
    {"name": "Flow Sensor (BF1)", "address": 40, "register_type": INPUT_REGISTERS, "unit_of_measurement": "l/m", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Current BE3", "address": 46, "register_type": INPUT_REGISTERS, "unit_of_measurement": "A", "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Current BE2", "address": 48, "register_type": INPUT_REGISTERS, "unit_of_measurement": "A", "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Current BE1", "address": 50, "register_type": INPUT_REGISTERS, "unit_of_measurement": "A", "device_class": SensorDeviceClass.CURRENT, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},

    # Calculated and runtime measurements
    {"name": "Calculated Flow Temp (Heating)", "address": 1017, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Calculated Flow Temp (Cooling)", "address": 1567, "register_type": INPUT_REGISTERS, "unit_of_measurement": "°C", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Total Runtime Additions", "address": 1025, "register_type": INPUT_REGISTERS, "unit_of_measurement": "h", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Meter Hot Water", "address": 1575, "register_type": INPUT_REGISTERS, "unit_of_measurement": "kWh", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Meter Heat", "address": 1577, "register_type": INPUT_REGISTERS, "unit_of_measurement": "kWh", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Meter Pool", "address": 1581, "register_type": INPUT_REGISTERS, "unit_of_measurement": "kWh", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Meter Hot Water Compressor", "address": 1583, "register_type": INPUT_REGISTERS, "unit_of_measurement": "kWh", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
    {"name": "Flow Meter Heat Compressor", "address": 1585, "register_type": INPUT_REGISTERS, "unit_of_measurement": "kWh", "device_class": None, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},

    # Alarms and operational states
    {"name": "Active Alarm", "address": 2195, "register_type": INPUT_REGISTERS, "unit_of_measurement": None, "device_class": None, "state_class": None, "scale": 1},
    {"name": "Alarm Number", "address": 1975, "register_type": INPUT_REGISTERS, "unit_of_measurement": None, "device_class": None, "state_class": None, "scale": 1},
    {"name": "Momentary Power Usage", "address": 2166, "register_type": INPUT_REGISTERS, "unit_of_measurement": "W", "device_class": SensorDeviceClass.POWER, "state_class": SensorStateClass.MEASUREMENT, "scale": 0.1},
]

async def async_setup_entry(
    hass: HomeAssistant, entry, async_add_devices: AddEntitiesCallback
):
    """Setup NIBE platform."""
    _LOGGER.debug("Setting up NIBE sensors and controls")
    coordinator = hass.data[DOMAIN]["coordinator"]

    # Add sensors
    sensors = [NibeSensor(coordinator, sensor, entry) for sensor in NIBE_SENSORS]

class NibeSensor(NibeEntity, SensorEntity):
    """NIBE sensor class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry):
        _LOGGER.debug("Initializing sensor: %s", idx["name"])
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx
        self._attr_native_unit_of_measurement = idx["unit_of_measurement"]
        self._attr_device_class = idx["device_class"]
        self._attr_state_class = idx["state_class"]
        self._attr_native_value = self._get_value()

def _get_value(self):
    """Get the value from the coordinator."""
    value = self.coordinator.input_registers.get(self.idx["address"])
    if value is None:
        _LOGGER.warning("Missing data for address: %s", self.idx["address"])
        return None
    scaled_value = ModbusClientMixin.convert_from_registers([value], ModbusClientMixin.DATATYPE.INT16)
    return round(scaled_value * self.idx["scale"], 2)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._get_value()
        _LOGGER.debug(
            "Updated sensor %s: %s %s",
            self._attr_name,
            self._attr_native_value,
            self._attr_native_unit_of_measurement,
        )
        self.async_write_ha_state()
