"""Sensor platform for the EIA Hourly Demand integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_LATEST_TIMESTAMP,
    ATTR_LATEST_VALUE,
    CONF_BA_ID,
    DATA_COORDINATOR,
    DATA_SERVICES_REGISTERED,
    DOMAIN,
    SERVICE_REFRESH,
)
from .coordinator import EIAHourlyDemandCoordinator

ENTITY_DESCRIPTION = SensorEntityDescription(
    key="hourly_demand",
    translation_key="hourly_demand",
    device_class=SensorDeviceClass.ENERGY,
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfEnergy.MEGA_WATT_HOUR,
    icon="mdi:factory",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the EIA Hourly Demand sensor entry."""
    coordinator: EIAHourlyDemandCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    async_add_entities([EIAHourlyDemandSensor(coordinator, entry)], True)

    platform = entity_platform.async_get_current_platform()
    if not hass.data[DOMAIN].get(DATA_SERVICES_REGISTERED):
        platform.async_register_entity_service(
            SERVICE_REFRESH,
            {},
            "async_request_refresh",
        )
        hass.data[DOMAIN][DATA_SERVICES_REGISTERED] = True


class EIAHourlyDemandSensor(
    CoordinatorEntity[EIAHourlyDemandCoordinator], SensorEntity
):
    """Representation of an EIA Hourly Demand sensor."""

    entity_description = ENTITY_DESCRIPTION

    _attr_has_entity_name = True

    def __init__(self, coordinator: EIAHourlyDemandCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._ba_id = entry.data[CONF_BA_ID]
        self._attr_unique_id = f"eia_hourly_demand_{self._ba_id.lower()}"

    @property
    def name(self) -> str | None:
        """Return entity name."""
        return f"{self._ba_id} Demand"

    @property
    def native_value(self) -> float | None:
        """Return the latest demand value."""
        data = self.coordinator.data
        if not data:
            return None
        return data.get(ATTR_LATEST_VALUE)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional metadata about the measurement."""
        data = self.coordinator.data or {}
        return {
            ATTR_LATEST_TIMESTAMP: data.get(ATTR_LATEST_TIMESTAMP),
            ATTR_LATEST_VALUE: data.get(ATTR_LATEST_VALUE),
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for this sensor."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._ba_id)},
            manufacturer="U.S. Energy Information Administration",
            name=f"EIA {self._ba_id}",
            configuration_url="https://www.eia.gov/opendata/browser/electricity/rto",
        )

    async def async_request_refresh(self) -> None:
        """Handle manual refresh service call."""
        await self.coordinator.async_request_refresh()
