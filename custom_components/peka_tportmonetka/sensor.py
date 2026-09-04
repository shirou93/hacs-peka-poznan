"""PEKA balance sensor."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .api import async_get_balance
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the balance sensor from a config entry."""
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    if not isinstance(scan_interval, timedelta):
        scan_interval = timedelta(minutes=float(scan_interval))

    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name="PEKA balance",
        update_method=lambda: async_get_balance(hass, entry.data),
        update_interval=scan_interval,
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([PekaBalanceSensor(coordinator, entry)])


class PekaBalanceSensor(CoordinatorEntity, SensorEntity):
    """Expose the PEKA balance as a Home Assistant sensor."""

    _attr_native_unit_of_measurement = "PLN"
    _attr_icon = "mdi:wallet"
    _attr_should_poll = False

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_name = entry.title
        self._attr_unique_id = f"{entry.entry_id}_balance"

    @property
    def native_value(self):
        """Return the latest balance."""
        return self.coordinator.data
