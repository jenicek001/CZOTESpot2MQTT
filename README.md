# CZOTESpot2MQTT - Work in Progress
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

- Fetches hourly spot electricity prices from OTE-CR in EUR / MWh.
- Retrieves the current CZK/EUR exchange rate from Czech National Bank.
- Publishes the fetched electricity prices in CZK via MQTT.
- Supports get functions to receive the current hourly price and lists for the whole day and the next day.

## Requirements

- Python 3.6+
- `paho-mqtt` library (install via `pip install paho-mqtt`)
- `aiomqtt` library
- `aiohttp` library

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/jenicek001/CZOTESpot2MQTT.git
cd CZOTESpot2MQTT
```

2. Set up a virtual environment (optional but recommended):
```python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required libraries:
```pip install -r requirements.txt
```

## Usage

1. Ensure you have filled in the config.ini file with your MQTT server details and logging preferences.

2. To run manually:
```python src/main.py
```
The script will run indefinitely, fetching and publishing hourly electricity prices every hour.

3. To start automatically from systemd:
```sudo cp systemd/czote2mqtt.service /etc/systemd/system
```

## Configuration

In the config.ini file, you must provide the following information:

OTE-CR: OTE-CR API key.
CzechNationalBank: URL to fetch the CZK/EUR exchange rate.
MQTT: MQTT broker URL and port to establish the connection, and the topic to publish electricity prices.

# Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request. Make sure to follow the code style and provide tests for new functionalities.

1. Fork the repository.

2. Create a new branch for your changes:
```git checkout -b feature/new-feature
```

3. Commit your changes and push to the branch:
```git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

4. Open a pull request with a detailed description of your changes.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.