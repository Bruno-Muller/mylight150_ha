from __future__ import annotations
from datetime import timedelta

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "mylight150"
DEFAULT_NAME = "MyLight150"

# --- API ---
API_URL = "https://mltcore-prd-apim.azure-api.net/me"
API_SUBSCRIPTION_KEY = "40aadf2a4bed4231a70c5bb45790a5ed"

# --- OAuth/JWT ---
OAUTH_TENANT_NAME = "mylightb2cprd"
OAUTH_TENANT_ID = "94e468fb-4eba-45a2-a895-5c0524b19d56"
OAUTH_CLIENT_ID = "13cb2062-2b0f-4b72-a84c-a5bcb998e714"
OAUTH_SCOPE = f"{OAUTH_CLIENT_ID} openid profile offline_access"
OAUTH_POLICY_NAME = "B2C_1A_MYLIGHTSYSTEMS_signup_signin"
OAUTH_URL = f"https://{OAUTH_TENANT_NAME}.b2clogin.com/{OAUTH_TENANT_NAME}.onmicrosoft.com/{OAUTH_POLICY_NAME}"
OAUTH_REDIRECT_URI = "https://client.mylight150.com/"


CONF_DEVICE_ID = "device_id"
CONF_UPDATE_INITIAL = "update_initial"
CONF_UPDATE_INTERVAL = "update_interval"

REFRESH_DATA_FAILED_EVENT = "refresh_failed"
REFRESH_DATA_COMPLETED_EVENT = "refresh_completed"

MIN_UPDATE_INTERVAL = 10
MAX_UPDATE_INTERVAL = 60
DEFAULT_UPDATE_INTERVAL = 15
DEFAULT_UPDATE_INITIAL = True

PLATFORMS: list[Platform] = [
#    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


__all__ = [
    "CONF_DEVICE_ID",
    "CONF_PASSWORD",
    "CONF_UPDATE_INTERVAL",
    "CONF_UPDATE_INITIAL",
    "CONF_USERNAME",
    "DEFAULT_UPDATE_INTERVAL",
    "DOMAIN",
    "MAX_UPDATE_INTERVAL",
    "MIN_UPDATE_INTERVAL",
    "PLATFORMS",
    "REFRESH_DATA_COMPLETED_EVENT",
    "REFRESH_DATA_FAILED_EVENT",
]
