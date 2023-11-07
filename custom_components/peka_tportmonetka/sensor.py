import logging
import subprocess
from datetime import timedelta

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Peka tPortmonetka Sensor"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)

CONF_SENSORS = "sensors"
CONF_RUN_SCRIPT = "/config/custom_components/peka_tportmonetka/get-peka.py" 

SENSOR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required("login"): cv.string,
        vol.Required("password"): cv.string,
        vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SENSORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    sensors = []

    for sensor_config in config.get(CONF_SENSORS):
        name = sensor_config.get(CONF_NAME)
        login = sensor_config.get("login")
        password = sensor_config.get("password")
        scan_interval = sensor_config.get("scan_interval", DEFAULT_SCAN_INTERVAL)

        sensors.append(
            PekaTPortMonetkaSensor(name, login, password, scan_interval)
        )

    add_entities(sensors, True)

class PekaTPortMonetkaSensor(Entity):
    def __init__(self, name, login, password, scan_interval):
        self._name = name
        self._login = login
        self._password = password
        self._state = None
        self._scan_interval = scan_interval

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "PLN"

    @property
    def icon(self):
        return "mdi:wallet"

    @property
    def should_poll(self):
        return True

    def update(self):
        try:
            result = subprocess.check_output(
                ["python3", CONF_RUN_SCRIPT, self._login, self._password]
            ).decode().strip()
            self._state = result
        except subprocess.CalledProcessError as e:
            _LOGGER.error("Error running script: %s", e)
