from __future__ import annotations
from datetime import timedelta

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform

DOMAIN = "mylight150"
DEFAULT_NAME = "MyLight150"

# --- API ---
API_SUBSCRIPTION_KEY = "40aadf2a4bed4231a70c5bb45790a5ed"
API_URL = "https://mltcore-prd-apim.azure-api.net/me"

# --- OAuth/JWT ---
OAUTH_TENANT_NAME = "mylightb2cprd"
OAUTH_TENANT_ID = "94e468fb-4eba-45a2-a895-5c0524b19d56"
OAUTH_CLIENT_ID = "13cb2062-2b0f-4b72-a84c-a5bcb998e714"
OAUTH_SCOPE = f"{CLIENT_ID} openid profile offline_access"
OAUTH_POLICY_NAME = "B2C_1A_MYLIGHTSYSTEMS_signup_signin"
OAUTH_URL = f"https://{TENANT_NAME}.b2clogin.com/{TENANT_NAME}.onmicrosoft.com/{POLICY_NAME}"
OAUTH_REDIRECT_URI = "https://client.mylight150.com/"

# --- Defaults ---
DEFAULT_SCAN_INTERVAL = timedelta(seconds=900)
DEFAULT_RETRY_DELAY = timedelta(seconds=5)

