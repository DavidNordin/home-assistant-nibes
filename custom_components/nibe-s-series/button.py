"""Button platform for Nibe."""
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import now as hass_now
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NIBE_BUTTONS, BUTTON_CLASS_SET_TIME, BUTTON_CLASS_START
from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup button platform."""
    _LOGGER.debug("Setting up Nibe buttons")
    coordinator = hass.data[DOMAIN]["coordinator"]

    buttons = []
    for button in NIBE_BUTTONS:
        if button["entity_class"] == BUTTON_CLASS_START:
            buttons.append(NibeButtonStart(coordinator, button, entry))
        elif button["entity_class"] == BUTTON_CLASS_SET_TIME:
            buttons.append(NibeButtonSetTime(coordinator, button, entry))
    async_add_devices(buttons)


class NibeButton(NibeEntity, ButtonEntity):
    """Nibe base button class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, entry):
        _LOGGER.debug("Initializing NibeButton: %s", idx["name"])
        super().__init__(coordinator, idx, entry)
        self.coordinator = coordinator
        self.idx = idx
        self._attr_name = idx["name"]


class NibeButtonStart(NibeButton):
    """Nibe start button class."""

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("Pressing NibeButtonStart: %s", self._attr_name)
        result = await self.coordinator.write_coil(self.idx["address"], True)
        _LOGGER.debug("NibeButtonStart result: %s", result)


class NibeButtonSetTime(NibeButton):
    """Nibe set time button class."""

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("Pressing NibeButtonSetTime: %s", self._attr_name)

        now = hass_now()
        try:
            await self.coordinator.write_register(399, now.year)
            await self.coordinator.write_register(400, now.month)
            await self.coordinator.write_register(401, now.day)
            await self.coordinator.write_register(402, now.hour)
            await self.coordinator.write_register(403, now.minute)
            await self.coordinator.write_register(404, now.second)
            _LOGGER.debug("Time set successfully: %s", now.isoformat())
        except Exception as e:
            _LOGGER.error("Failed to set time: %s", e)
