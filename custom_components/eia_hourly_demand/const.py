"""Constants for the EIA Hourly Demand integration."""

from datetime import timedelta

DOMAIN = "eia_hourly_demand"

CONF_API_KEY = "api_key"
CONF_BA_ID = "ba_id"

ATTR_LATEST_TIMESTAMP = "latest_timestamp"
ATTR_LATEST_VALUE = "latest_value"

DATA_COORDINATOR = "coordinator"
DATA_SERVICES_REGISTERED = "services_registered"

DEFAULT_UPDATE_INTERVAL = timedelta(minutes=30)

SERVICE_REFRESH = "refresh"
