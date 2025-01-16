"""Button platform for Nibe."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import now as hass_now
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BUTTON_CLASS_SET_TIME,
    BUTTON_CLASS_START,
    DOMAIN,
    NIBE_BUTTONS,
)

from .entity import NibeEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Setup button platform."""
    _LOGGER.debug("NibeS.button.py")
    coordinator = hass.data[DOMAIN]["coordinator"]

    buttons = []
    for button in NIBES_BUTTONS:
        if button["entity_class"] == BUTTON_CLASS_START:
            buttons.append(NibeSButtonStart(coordinator, button, entry))
        elif button["entity_class"] == BUTTON_CLASS_SET_TIME:
            buttons.append(NibeButtonSetTime(coordinator, button, entry))
    async_add_devices(buttons)


class NibeButton(NibeEntity, ButtonEntity):
    """Nibe button class."""

    def __init__(self, coordinator: CoordinatorEntity, idx, entry):
        _LOGGER.debug("NibeButton.__init__()")
        super().__init__(coordinator, idx, entry)
        self.coordinator = coordinator
        self.idx = idx


class NibeButtonStart(NibeButton):
    """Nibe start button class."""

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("NibeButtonStart.async_press()")
        result = await self.coordinator.write_coil(self.idx["address"], True)
        _LOGGER.debug("async_press: %s", result)


class NibeButtonSetTime(NibeButton):
    """Nibe start button class."""

    async def async_press(self) -> None:
        """Press the button."""
        _LOGGER.debug("NibeButtonSetTime.async_press()")

        now = hass_now()
        await self.coordinator.write_register(399, now.year)
        await self.coordinator.write_register(400, now.month)
        await self.coordinator.write_register(401, now.day)
        await self.coordinator.write_register(402, now.hour)
        await self.coordinator.write_register(403, now.minute)
        await self.coordinator.write_register(404, now.second)
