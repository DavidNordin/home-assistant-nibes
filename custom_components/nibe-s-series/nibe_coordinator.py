from datetime import timedelta
import logging
import async_timeout
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SLAVE, NAME

_LOGGER = logging.getLogger(__name__)


class NibeCoordinator(DataUpdateCoordinator):
    """Coordinator to manage Modbus communication for Nibe integration."""

    def __init__(self, hass, client: AsyncModbusTcpClient):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=NAME,  # Name of the coordinator for logging purposes
            update_interval=timedelta(seconds=15),  # Polling interval
        )
        self.client = client
        self.paused = False

        # Registers storage
        self.input_registers = []
        self.holding_registers = []
        self.discrete_inputs = []
        self.coils = []

    async def _async_update_data(self):
        """Fetch data from Modbus device."""
        if self.paused:
            _LOGGER.warning("Coordinator is paused, skipping data update.")
            return

        try:
            async with async_timeout.timeout(10):
                if not self.client.connected:
                    _LOGGER.info("Connecting to Modbus client...")
                    await self.client.connect()

                _LOGGER.debug("Fetching Modbus data...")
                
                # Read coils
                coils_result = await self.client.read_coils(0, count=7, slave=DEFAULT_SLAVE)
                self.coils = coils_result.bits

                # Read discrete inputs
                discrete_inputs_result = await self.client.read_discrete_inputs(
                    0, count=54, slave=DEFAULT_SLAVE
                )
                self.discrete_inputs = discrete_inputs_result.bits

                # Read input registers
                input_registers_result = await self.client.read_input_registers(
                    0, count=33, slave=DEFAULT_SLAVE
                )
                self.input_registers = input_registers_result.registers

                # Read holding registers
                holding_registers_result = await self.client.read_holding_registers(
                    0, count=69, slave=DEFAULT_SLAVE
                )
                self.holding_registers = holding_registers_result.registers

                _LOGGER.debug("Modbus data successfully fetched.")
                return
        except ModbusException as err:
            raise UpdateFailed(f"Modbus error: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def write_register(self, address: int, value: int):
        """Write to a holding register."""
        try:
            _LOGGER.debug("Writing value %s to register %s", value, address)
            result = await self.client.write_register(address, value, slave=DEFAULT_SLAVE)
            await self.async_refresh()
            return result
        except ModbusException as err:
            _LOGGER.error("Failed to write to register %s: %s", address, err)
            raise

    async def write_coil(self, address: int, value: bool):
        """Write to a coil."""
        try:
            _LOGGER.debug("Writing value %s to coil %s", value, address)
            result = await self.client.write_coil(address, value, slave=DEFAULT_SLAVE)
            await self.async_refresh()
            return result
        except ModbusException as err:
            _LOGGER.error("Failed to write to coil %s: %s", address, err)
            raise

    def close(self):
        """Close the Modbus client connection."""
        if self.client.connected:
            _LOGGER.info("Closing Modbus client connection.")
            self.client.close()

    def pause(self):
        """Pause data fetching by disconnecting the client."""
        _LOGGER.info("Pausing Modbus communication.")
        self.paused = True
        if self.client.connected:
            self.client.close()

    async def resume(self):
        """Resume data fetching by reconnecting the client."""
        _LOGGER.info("Resuming Modbus communication.")
        self.paused = False
        return await self.client.connect()
