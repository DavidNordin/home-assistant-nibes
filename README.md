[![GitHub Release][releases-shield]][releases]
[![Total downloads][total-downloads-shield]][total-downloads]
[![Latest release downloads][latest-release-downloads-shield]][latest-release-downloads]

<p align="right">
<img width="250" alt="Logo" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-NibeS/master/assets/logo.png">
</p>

# Nibe S-series component for Home Assistant


Control and monitor your Nibe S-series unit from Home Assistant via ModbusTCP.

<p align="center">
<img width="250" alt="Sensors" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/sensors.png"><img width="250" alt="Controls" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/controls.png"><img width="250" alt="Diagnostic" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/diagnostic.png">
</p>




### Sensors
| Sensor  | Modbus register |
| ------------- | ------------- |
|Boost input|1x00002|
|Current exhaust fan power|3x00026|
|Current exhaust fan step|3x00024|
|Current heating power|3x00029|
|Current heat/cold recovery power|3x00030|
|Current supply fan power|3x00025|
|Current supply fan step|3x00023|
|Exhaust air temperature|3x00005|
|Exhaust fan alarm|1x00022|
|Extract air temperature|3x00004|
|Filter days left|3x00020|
|Filter timer alarm|1x00025|
|Fire alarm|1x00010|
|Heat recovery temperature|3x00007|
|Last seen|_Calculated_|
|Night cooling active|1x00038|
|Outdoor temperature | 3x00002  |
|Overpressure input|1x00003|
|Recycle efficiency|_Calculated_|
|Rotor alarm|1x00011|
|Startup 1st phase|1x00028|
|Startup 2nd phase|1x00029|
|Supply air temperature|3x00003|
|Supply fan alarm|1x00021|


### Buttons
| Button  | Modbus register |
| ------------- | ------------- |
| Clear Alarms |0x00005|
|Reset filter timer|0x00006|
|Sync date and time|4x00400 - 4x00405|


### Switches
| Switch  | Modbus register |
| ------------- | ------------- |
|Away mode|0x00004|
|Boost mode|0x00003|
|Heater enabled|4x00067|
|Night cooling enabled|4x00019|
|Overpressure mode|0x00002|
|Power|0x00001|
|Preheater enabled|4x00064|

### Numbers
| Number  | Modbus register |
| ------------- | ------------- |
|Night cooling exhaust high limit|4x00021|
|Night cooling exhaust low limit|4x00022|
|Night cooling indoor-outdoor diff. limit|4x00020|

## Installation

### HACS
1. In Home Assistant go to HACS -> Integrations. Click on "+ Explore & Download Repositories" and search for "Nibe S-series".

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DavidNordin&repository=home-assistant-nibes&category=integration)

2. In Home Assistant go to Settings -> Devices & Services -> Integrations. Click on "+ Add integration" and search for "Nibe S-series".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=nibes)


## Configuration Nibe unit

Enable modbus and network on the Nibe unit.



[releases-shield]: https://img.shields.io/github/v/release/DavidNordin/home-assistant-nibes?style=flat-square
[releases]: https://github.com/DavidNordin/home-assistant-nibes/releases
[total-downloads-shield]: https://img.shields.io/github/downloads/DavidNordin/home-assistant-nibes/total?style=flat-square
[total-downloads]: https://github.com/DavidNordin/home-assistant-nibes
[latest-release-downloads-shield]: https://img.shields.io/github/downloads/DavidNordin/home-assistant-nibes/latest/total?style=flat-square
[latest-release-downloads]: https://github.com/DavidNordin/home-assistant-nibes