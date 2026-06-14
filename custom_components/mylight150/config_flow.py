from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
)


from .api import MyLight150ApiClient, MyLight150AuthError, MyLight150ApiError
from .const import (
    CONF_PASSWORD,
    CONF_UPDATE_INITIAL,
    CONF_UPDATE_INTERVAL,
    CONF_USERNAME,
    DEFAULT_UPDATE_INITIAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    MAX_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def _validate_credentials(hass, username: str, password: str) -> str | None:
    """Try to authenticate. Returns None on success, or an error key string on failure."""
    session = async_get_clientsession(hass)
    api = MyLight150ApiClient(hass,session, username, password)
    try:
        await api.async_login_test()
        return None
    except MyLight150AuthError:
        _LOGGER.debug("MyLight150: invalid_credentials")
        return "invalid_credentials"
    except MyLight150ApiError:
        _LOGGER.debug("MyLight150: cannot_connect")
        return "cannot_connect"
    except Exception:
        _LOGGER.exception("MyLight150 unexpected error during login")
        return "unexpected"


class MyLight150ConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        _errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME].lower())
            self._abort_if_unique_id_configured()

            try:
                error_key = await _validate_credentials(
                    self.hass,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
                if error_key:
                    _errors["base"] = error_key
                else:
                    return self.async_create_entry(
                        title=user_input[CONF_USERNAME],
                        data={
                            CONF_USERNAME: user_input[CONF_USERNAME],
                            CONF_PASSWORD: user_input[CONF_PASSWORD],
                        },
                        options={
                            CONF_UPDATE_INTERVAL: int(max(
                                user_input.get(
                                    CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                                ),
                                MIN_UPDATE_INTERVAL,
                            )),
                            CONF_UPDATE_INITIAL: user_input.get(CONF_UPDATE_INITIAL, DEFAULT_UPDATE_INITIAL),
                        },
                    )
            except Exception:
                _LOGGER.exception("MyLight150: config flow failed")
                _errors["base"] = "unexpected"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(
                        CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                    ): NumberSelector(
                        NumberSelectorConfig(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL, mode="slider", step=1, unit_of_measurement="min")
                    ),
                    vol.Optional(CONF_UPDATE_INITIAL, default=DEFAULT_UPDATE_INITIAL): bool,
                }
            ),
            errors=_errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        _errors: dict[str, str] = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is not None:
            password = user_input[CONF_PASSWORD]

            try:
                error_key = await _validate_credentials(
                    self.hass,
                    reconfigure_entry.data[CONF_USERNAME],
                    password,
                )
                if error_key:
                    _errors["base"] = error_key
                else:
                    return self.async_update_reload_and_abort(
                        reconfigure_entry,
                        data_updates={
                            CONF_PASSWORD: password,
                        },
                    )
            except Exception:
                _LOGGER.exception("MyLight150: reconfigure flow failed!")
                _errors["base"] = "unexpected"

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PASSWORD,
                        default=reconfigure_entry.data.get(CONF_PASSWORD, ""),
                    ): str,
                }
            ),
            description_placeholders={
                "username": reconfigure_entry.data[CONF_USERNAME],
            },
            errors=_errors,
        )

    @staticmethod
    def async_get_options_flow(configentry: ConfigEntry) -> MyLight150OptionsFlowHandler:
        return MyLight150OptionsFlowHandler()


class MyLight150OptionsFlowHandler(OptionsFlow):
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            user_input[CONF_UPDATE_INTERVAL] = max(
                int(user_input[CONF_UPDATE_INTERVAL]), MIN_UPDATE_INTERVAL
            )
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL,
                            self.config_entry.data.get(
                                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                            ),
                        ),
                    ): NumberSelector(
                        NumberSelectorConfig(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL, mode="slider", step=1, unit_of_measurement="min")
                    ),
                    vol.Optional(
                        CONF_UPDATE_INITIAL,
                        default=self.config_entry.options.get(CONF_UPDATE_INITIAL, DEFAULT_UPDATE_INITIAL),
                    ): bool,
                }
            ),
        )


__all__ = ["MyLight150ConfigFlow", "MyLight150OptionsFlowHandler"]
