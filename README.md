# WAWA Transport Api
Simple app to try out the Warsaw UM Open Api for public transportation.
## Table of contents
- [WAWA Transport Api](#wawa-transport-api)
  - [Table of contents](#table-of-contents)
  - [General information](#general-information)
  - [Technologies](#technologies)
  - [Setup](#setup)
    - [Local environment](#local-environment)
    - [Configuration - the api key](#configuration---the-api-key)
    - [Application usage](#application-usage)
    - [Additional api calls](#additional-api-calls)
  - [Status](#status)
  - [License](#license)

## General information
This repository is created mainly for testing purposes of the Warsaw UM Open API (https://api.um.warszawa.pl/).
This may come in handy in some future projects
## Technologies
You may expect the following technologies used in this repo:
- Python (^3.10)
- Rest API (Requests)
- Poetry
- For any additional python packages please investigate the [pyproject](pyproject.toml) file
## Setup
### Local environment
To setup your local environment start by creating a virtualenv with `python 3.10` or higher.
In your activated virtual environment install `poetry 1.1.12` or higher:
```shell
$ pip install poetry
```
And install all packages using the provided `pyproject.toml` and `poetry.lock` files, like so:
```shell
$ poetry install
```
### Configuration - the api key
This application uses an `api key` which can be requested for free on https://api.um.warszawa.pl/ after creating the developer account.

After obtaining the api key create a `config.ini` file in the root dir of the repository and copy-paste your api key there, like so:
```ini
[OPENAPI]
api_key = YOUR_API_KEY_HERE
```
and you are done!
### Application usage
This application has been written as a prototype api and a short demo script showing an example of use.

To try out the application simply run:
```shell
$ python wawa_transport_api/main.py
```
Which will produce output similar to this one:
```shell
Closest stop name Grenadierów 04
This stop is located 0.04 km from you
Schedule:
Line: 24 -> Gocławek
Arrives at: 22:22:00
Distance from the stop: 2.91 km
Line: 9 -> Wiatraczna
Arrives at: 22:28:00
Distance from the stop: 4.19 km
```
### Additional api calls
Examples of raw api calls are located in `dev_tools/api_examples.http` file.

The file is written in [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) plugin compatible http format and can be used to send requests directly from `VS Code` or `Pycharm`.

## Status
| Milestone               | Status |
| ----------------------- | ------ |
| Api examples            | ✅      |
| Domain models           | ✅      |
| Api requests module     | ✅      |
| Abstraction layer       | ✅      |
| Unit testing & bugfixes | 🏃‍♂️      |
| Documentation           | 🏃‍♂️      |

## License
This software is distributed under [MIT license](LICENSE.md)
