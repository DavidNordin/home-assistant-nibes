"""Support for Nibe Climate Thermostats."""
import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NIBE_CLIMATES
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

NIBE_CLIMATES = [
    {
        "name": "Living Room Thermostat",
        "current_temp_address": 2,
        "target_temp_address": 1,
        "hvac_action_address": 28,
        "hvac_mode_address": 0,
        "min_temp": 15,
        "max_temp": 30,
        "step": 0.5,
    },
    # Add more thermostats here if necessary
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup climate platform."""
    _LOGGER.debug("Setting up Nibe climate thermostats")
    coordinator = hass.data[DOMAIN]["coordinator"]

    climates = [
        NibeThermostat(coordinator, climate, entry) for climate in NIBE_CLIMATES
    ]
    async_add_devices(climates)


class NibeThermostat(NibeEntity, ClimateEntity):
    """Representation of a Nibe Climate Thermostat."""

    def __init__(self, coordinator: CoordinatorEntity, idx, config_entry) -> None:
        """Initialize the thermostat."""
        _LOGGER.debug("Initializing NibeThermostat: %s", idx["name"])
        super().__init__(coordinator, idx, config_entry)
        self.coordinator = coordinator
        self.idx = idx

        self._attr_name = idx["name"]
        self._attr_min_temp = idx.get("min_temp", 15)
        self._attr_max_temp = idx.get("max_temp", 30)
        self._attr_target_temperature_step = idx.get("step", 1)
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = PRECISION_WHOLE
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

        self._attr_hvac_mode = self._get_hvac_mode()
        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()

    def _get_current_temperature(self):
        """Get the current temperature from the coordinator."""
        value = self.coordinator.input_registers.get(self.idx["current_temp_address"])
        if value is None:
            _LOGGER.warning("Missing current temperature data for %s", self._attr_name)
            return 0
        return value * 0.1

    def _get_target_temperature(self):
        """Get the target temperature from the coordinator."""
        value = self.coordinator.holding_registers.get(self.idx["target_temp_address"])
        if value is None:
            _LOGGER.warning("Missing target temperature data for %s", self._attr_name)
            return self._attr_min_temp
        return value

    def _get_hvac_action(self):
        """Get the HVAC action from the coordinator."""
        action = self.coordinator.input_registers.get(self.idx["hvac_action_address"])
        if action is None:
            _LOGGER.warning("Missing HVAC action data for %s", self._attr_name)
            return HVACAction.IDLE
        return HVACAction.FAN if action == 0 else HVACAction.HEATING

    def _get_hvac_mode(self):
        """Get the HVAC mode from the coordinator."""
        mode = self.coordinator.coils.get(self.idx["hvac_mode_address"])
        if mode is None:
            _LOGGER.warning("Missing HVAC mode data for %s", self._attr_name)
            return HVACMode.OFF
        return HVACMode.HEAT if mode else HVACMode.OFF

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_temperature = self._get_current_temperature()
        self._attr_target_temperature = self._get_target_temperature()
        self._attr_hvac_action = self._get_hvac_action()
        self._attr_hvac_mode = self._get_hvac_mode()

        _LOGGER.debug(
            "Updated %s: current_temp=%s, target_temp=%s, hvac_action=%s, hvac_mode=%s",
            self._attr_name,
            self._attr_current_temperature,
            self._attr_target_temperature,
            self._attr_hvac_action,
            self._attr_hvac_mode,
        )
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set a new HVAC mode."""
        _LOGGER.debug("Setting HVAC mode for %s to %s", self._attr_name, hvac_mode)
        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.write_coil(self.idx["hvac_mode_address"], True)
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.write_coil(self.idx["hvac_mode_address"], False)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self):
        """Turn the entity on."""
        _LOGGER.debug("Turning on %s", self._attr_name)
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self):
        """Turn the entity off."""
        _LOGGER.debug("Turning off %s", self._attr_name)
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set a new target temperature."""
        target_temperature = int(kwargs[ATTR_TEMPERATURE])
        _LOGGER.debug(
            "Setting target temperature for %s to %s°C", self._attr_name, target_temperature
        )
        await self.coordinator.write_register(
            self.idx["target_temp_address"], target_temperature
        )
