[![GitHub Release][releases-shield]][releases]
[![Total downloads][total-downloads-shield]][total-downloads]
[![Latest release downloads][latest-release-downloads-shield]][latest-release-downloads]

<p align="right">
<img width="250" alt="Logo" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-NibeS/master/assets/logo.png">
</p>

# Nibe S-series component for Home Assistant

Control and monitor your Nibe S-series unit from Home Assistant via ModbusTCP.

<p align="center">
<img width="250" alt="Sensors" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/sensors.png">
<img width="250" alt="Controls" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/controls.png">
<img width="250" alt="Diagnostic" src="https://raw.githubusercontent.com/DavidNordin/home-assistant-nibes/master/assets/diagnostic.png">
</p>

---

## Features

### Sensors
| Sensor                           | Modbus Register  |
|----------------------------------|------------------|
| Outdoor Temperature (BT1)        | 3x00001          |
| Supply Temperature (BT2)         | 3x00005          |
| Return Temperature (BT3)         | 3x00007          |
| Hot Water Start (BT5)            | 3x02014          |
| Hot Water Top (BT7)              | 3x00008          |
| Hot Water Charging (BT6)         | 3x00009          |
| Cold Carrier In (BT10)           | 3x00010          |
| Cold Carrier Out (BT11)          | 3x00011          |
| Flow Temperature (BT12)          | 3x00012          |
| Hot Gas Temperature (BT14)       | 3x00013          |
| Liquid Line Temperature (BT15)   | 3x00014          |
| Suction Gas Temperature (BT17)   | 3x00016          |
| Room Temperature 1 (BT50)        | 3x00026          |
| External Flow Temperature (BT25) | 3x00039          |
| Compressor Temperature (BT29)    | 3x00086          |
| Flow Sensor (BF1)                | 3x00040          |
| Current BE3                      | 3x00046          |
| Current BE2                      | 3x00048          |
| Current BE1                      | 3x00050          |
| Calculated Flow Temp (Heating)   | 3x01017          |
| Calculated Flow Temp (Cooling)   | 3x01567          |
| Total Runtime Additions           | 3x01025          |
| Flow Meter Hot Water             | 3x01575          |
| Flow Meter Heat                  | 3x01577          |
| Flow Meter Pool                  | 3x01581          |
| Flow Meter Hot Water Compressor  | 3x01583          |
| Flow Meter Heat Compressor       | 3x01585          |
| Active Alarm                     | 3x02195          |
| Alarm Number                     | 3x01975          |
| Momentary Power Usage            | 3x02166          |

---

### Buttons
| Button                | Modbus Register      |
|-----------------------|----------------------|
| Reset Alarm           | 4x00022             |
| Sync Date and Time    | 4x00400 - 4x00405   |

---

### Switches
| Switch                          | Modbus Register  |
|---------------------------------|------------------|
| Allow Heat (Manual)             | 4x00181          |
| Allow Cooling (Manual)          | 4x00182          |
| Allow Addition (Manual)         | 4x00180          |
| Operating Mode (Manual)         | 4x00237          |

---

### Numbers
| Number                                  | Modbus Register |
|----------------------------------------|-----------------|
| Degree Minutes                         | 4x00011         |
| Cooling Degree Minutes                 | 4x00020         |
| Heating Curve                          | 4x00026         |
| Heating Curve Offset                   | 4x00030         |
| Minimum Flow Temp                      | 4x00034         |
| Maximum Flow Temp                      | 4x00038         |
| Start Temp Hot Water (Normal)          | 4x00059         |
| Stop Temp Hot Water (Normal)           | 4x00063         |
| Period Time Heating                    | 4x00092         |
| Period Time Hot Water                  | 4x00093         |
| Period Time Cooling                    | 4x00094         |
| Degree Minutes Start Addition          | 4x00679         |
| Degree Minutes Start Compressor        | 4x00097         |
| Control Calculated Flow Temp (Heat)    | 4x05009         |
| Control Calculated Flow Temp (Cooling) | 4x05017         |

---

### Selects
| Select                                  | Modbus Register |
|----------------------------------------|-----------------|
| Hot Water Demand                        | 4x00056         |
| Operating Mode                          | 4x00237         |
| Brine Pump Mode                         | 4x00096         |
| Heating Pump Mode                       | 4x00853         |
| Operational Priority                    | 3x01028         |

---

## Installation

### HACS
1. In Home Assistant go to HACS -> Integrations. Click on "+ Explore & Download Repositories" and search for "Nibe S-series".

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DavidNordin&repository=home-assistant-nibes&category=integration)

2. In Home Assistant go to Settings -> Devices & Services -> Integrations. Click on "+ Add integration" and search for "Nibe S-series".

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=nibes)

---

## Configuration Nibe Unit

Enable Modbus and network on the Nibe unit.

---

[releases-shield]: https://img.shields.io/github/v/release/DavidNordin/home-assistant-nibes?style=flat-square
[releases]: https://github.com/DavidNordin/home-assistant-nibes/releases
[total-downloads-shield]: https://img.shields.io/github/downloads/DavidNordin/home-assistant-nibes/total?style=flat-square
[total-downloads]: https://github.com/DavidNordin/home-assistant-nibes
[latest-release-downloads-shield]: https://img.shields.io/github/downloads/DavidNordin/home-assistant-nibes/latest/total?style=flat-square
[latest-release-downloads]: https://github.com/DavidNordin/home-assistant-nibes
