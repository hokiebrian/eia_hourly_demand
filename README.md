## EIA Hourly Demand Data

![release_badge](https://img.shields.io/github/v/release/hokiebrian/eia_hourly_demand?style=for-the-badge)
![release_date](https://img.shields.io/github/release-date/hokiebrian/eia_hourly_demand?style=for-the-badge)
[![License](https://img.shields.io/github/license/hokiebrian/eia_hourly_demand?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

You will need a EIA API Key (free). Register here: https://www.eia.gov/opendata/register.php

## Installation

This provides the hourly demand data (in MWh) for a specified Balancing Authority.

### Install Custom Components

1) Make sure that [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) is setup.
2) Go to integrations in HACS
3) Click the 3 dots in the top right corner and choose `Custom repositories`
4) Paste the following into the repository input field `https://github.com/hokiebrian/eia_hourly_demand` and choose category of `Integration`
5) Click add and restart HA to let the integration load
6) Go to settings and choose `Devices & Services`
7) Click `Add Integration` and search for `EIA Demand Data by Balancing Authority`
8) Configure the integration by copying your `EIA API Key` and `EIA BA Code` (see below) when prompted

## Notes

This data is self-reported by the Balancing Authority on an hourly basis. It is a manual process and vulnerable to data input errors, submission errors or neglect.

Multiple instances can be created if you want to track more than one BA. More info on what a BA is and does can be found here: https://www.eia.gov/todayinenergy/detail.php?id=27152

## BA Codes as of March 2023

| BA Code | BA Name                                                            | Region/Country Name |
|---------|--------------------------------------------------------------------|---------------------|
| AEC     | PowerSouth Energy Cooperative                                      | Southeast           |
| AECI    | Associated Electric Cooperative, Inc.                              | Midwest             |
| AVA     | Avista Corporation                                                 | Northwest           |
| AVRN    | Avangrid Renewables, LLC                                           | Northwest           |
| AZPS    | Arizona Public Service Company                                     | Southwest           |
| BANC    | Balancing Authority of Northern California                         | California          |
| BPAT    | Bonneville Power Administration                                    | Northwest           |
| CHPD    | Public Utility District No. 1 of Chelan County                     | Northwest           |
| CISO    | California Independent System Operator                             | California          |
| CPLE    | Duke Energy Progress East                                          | Carolinas           |
| CPLW    | Duke Energy Progress West                                          | Carolinas           |
| DEAA    | Arlington Valley, LLC                                              | Southwest           |
| DOPD    | PUD No. 1 of Douglas County                                        | Northwest           |
| DUK     | Duke Energy Carolinas                                              | Carolinas           |
| EEI     | Electric Energy, Inc.                                              | Midwest             |
| EPE     | El Paso Electric Company                                           | Southwest           |
| ERCO    | Electric Reliability Council of Texas, Inc.                        | Texas               |
| FMPP    | Florida Municipal Power Pool                                       | Florida             |
| FPC     | Duke Energy Florida, Inc.                                          | Florida             |
| FPL     | Florida Power & Light Co.                                          | Florida             |
| GCPD    | Public Utility District No. 2 of Grant County, Washington          | Northwest           |
| GLHB    | GridLiance                                                         | Midwest             |
| GRID    | Gridforce Energy Management, LLC                                   | Northwest           |
| GRIF    | Griffith Energy, LLC                                               | Southwest           |
| GRMA    | Gila River Power, LLC                                              | Southwest           |
| GVL     | Gainesville Regional Utilities                                     | Florida             |
| GWA     | NaturEner Power Watch, LLC                                         | Northwest           |
| HGMA    | New Harquahala Generating Company, LLC                             | Southwest           |
| HST     | City of Homestead                                                  | Florida             |
| IID     | Imperial Irrigation District                                       | California          |
| IPCO    | Idaho Power Company                                                | Northwest           |
| ISNE    | ISO New England                                                    | New England         |
| JEA     | JEA                                                                | Florida             |
| LDWP    | Los Angeles Department of Water and Power                          | California          |
| LGEE    | Louisville Gas and Electric Company and Kentucky Utilities Company | Midwest             |
| MISO    | Midcontinent Independent System Operator, Inc.                     | Midwest             |
| NEVP    | Nevada Power Company                                               | Northwest           |
| NWMT    | NorthWestern Corporation                                           | Northwest           |
| NYIS    | New York Independent System Operator                               | New York            |
| PACE    | PacifiCorp East                                                    | Northwest           |
| PACW    | PacifiCorp West                                                    | Northwest           |
| PGE     | Portland General Electric Company                                  | Northwest           |
| PJM     | PJM Interconnection, LLC                                           | Mid-Atlantic        |
| PNM     | Public Service Company of New Mexico                               | Southwest           |
| PSCO    | Public Service Company of Colorado                                 | Northwest           |
| PSEI    | Puget Sound Energy, Inc.                                           | Northwest           |
| SC      | South Carolina Public Service Authority                            | Carolinas           |
| SCEG    | Dominion Energy South Carolina, Inc.                               | Carolinas           |
| SCL     | Seattle City Light                                                 | Northwest           |
| SEC     | Seminole Electric Cooperative                                      | Florida             |
| SEPA    | Southeastern Power Administration                                  | Southeast           |
| SOCO    | Southern Company Services, Inc. - Trans                            | Southeast           |
| SPA     | Southwestern Power Administration                                  | Central             |
| SRP     | Salt River Project Agricultural Improvement and Power District     | Southwest           |
| SWPP    | Southwest Power Pool                                               | Central             |
| TAL     | City of Tallahassee                                                | Florida             |
| TEC     | Tampa Electric Company                                             | Florida             |
| TEPC    | Tucson Electric Power                                              | Southwest           |
| TIDC    | Turlock Irrigation District                                        | California          |
| TPWR    | City of Tacoma, Department of Public Utilities, Light Division     | Northwest           |
| TVA     | Tennessee Valley Authority                                         | Tennessee           |
| WACM    | Western Area Power Administration - Rocky Mountain Region          | Northwest           |
| WALC    | Western Area Power Administration - Desert Southwest Region        | Southwest           |
| WAUW    | Western Area Power Administration - Upper Great Plains West        | Northwest           |
| WWA     | NaturEner Wind Watch, LLC                                          | Northwest           |
| YAD     | Alcoa Power Generating, Inc. - Yadkin Division                     | Carolinas           |
| AESO    | Alberta Electric System Operator                                   | Canada              |
| BCHA    | British Columbia Hydro and Power Authority                         | Canada              |
| HQT     | Hydro-Quebec TransEnergie                                          | Canada              |
| IESO    | Ontario IESO                                                       | Canada              |
| MHEB    | Manitoba Hydro                                                     | Canada              |
| NBSO    | New Brunswick System Operator                                      | Canada              |
| SPC     | Saskatchewan Power Corporation                                     | Canada              |
| CEN     | Centro Nacional de Control de Energia                              | Mexico              |

