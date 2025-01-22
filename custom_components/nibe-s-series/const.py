"""Constants for the Nibe integration."""

from homeassistant.const import Platform

# Integration metadata
NAME = "Nibe"
DOMAIN = "nibe"
VERSION = "0.1.0"

# Supported platforms
PLATFORMS = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.CLIMATE,
]

# Modbus register types
INPUT_REGISTERS = "input_registers"
HOLDING_REGISTERS = "holding_registers"
COIL = "coil"
DISCRETE_INPUTS = "discrete_inputs"

# Button classes
BUTTON_CLASS_START = "button_class_start"
BUTTON_CLASS_SET_TIME = "button_class_set_time"

# Icon definitions
ICON_FAN = "mdi:fan"
ICON_THERMOMETER = "mdi:thermometer"
ICON_SWITCH = "mdi:toggle-switch-variant"
ICON_TIME_SYNC = "mdi:timer-sync"
ICON_ALARM = "mdi:bell"
ICON_CALENDAR = "mdi:calendar"
ICON_COOLING = "mdi:snowflake"
ICON_THERMOSTAT = "mdi:home-thermometer"
ICON_PLAY = "mdi:play-circle-outline"
ICON_START = "mdi:ray-start-arrow"

# Configuration keys
CONF_HOST_NAME = "host_name"
CONF_HOST_PORT = "host_port"
CONF_DEVICE_NAME = "device_name"

# Default values
DEFAULT_SLAVE = 1
