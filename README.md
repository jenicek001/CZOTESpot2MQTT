# CZOTESpot2MQTT
Daemon to download and publish Czech Republic OTE electric energy hourly spot prices in EUR and in CZK

This Python project sniffs hourly spot electricity prices from OTE-CR and the current CZK/EUR exchange rate from Czech National Bank. It then publishes the hourly spot electricity prices in CZK via MQTT. The MQTT communication also supports get functions to receive the current hourly price and lists for the whole day and the next day whenever available.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetches hourly spot electricity prices from OTE-CR API in CZK.
- Retrieves the current CZK/EUR exchange rate from Czech National Bank.
- Publishes the fetched electricity prices in CZK via MQTT.
- Supports get functions to receive the current hourly price and lists for the whole day and the next day.

## Requirements

- Python 3.6+
- `paho-mqtt` library (install via `pip install paho-mqtt`)

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/electricity-price-sniffer.git
cd electricity-price-sniffer
