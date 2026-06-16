"""MyLight150 DataUpdateCoordinator."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MyLight150ApiClient, MyLight150ApiError, MyLight150AuthError
from .const import CONF_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyLight150Coordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator MyLight150 — orchestre les appels API périodiques et nocturnes."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MyLight150ApiClient,
        update_interval_minutes: int,
    ) -> None:
        self._api = api
        self.installation_code: str | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval_minutes),
        )


    async def _async_update_data(self) -> dict[str, Any]:
        """Cyclic refresh every N minutes from config."""
        try:
            # Fetch installation code if not already done
            if not self.installation_code:
                self.installation_code = await self._fetch_installation_code()
                _LOGGER.debug("MyLight150: Installation code: %s", self.installation_code)

            parsed_data: dict[str, Any] = {}

            # Fetch realtime home data and parse it for sensors
            parsed_data.update(await self._fetch_home_data())

            # Fetch device data and parse it for sensors
            parsed_data.update(await self._fetch_device_data())

            # Fetch yearly energy totals
            parsed_data.update(await self._fetch_yearly_data())

            return parsed_data

        except MyLight150AuthError as err:
            raise UpdateFailed(f"Erreur d'authentification : {err}") from err
        except MyLight150ApiError as err:
            raise UpdateFailed(f"Erreur API : {err}") from err


    def async_teardown(self) -> None:
        """Cleanup when unloading the integration."""


    async def _fetch_yearly_data(self) -> dict[str, Any]:
        """
        Fetch yearly energy totals from /v3/production?aggregation=Year
        and /v3/consumption?aggregation=Year.

        Keys produced:
          yearly_solar_production_kwh  — énergie totale produite par les panneaux
          yearly_self_consumption_kwh  — énergie auto-consommée (production → maison)
          yearly_grid_injection_kwh    — énergie injectée sur le réseau
          yearly_grid_purchase_kwh     — énergie achetée depuis la grid
        """
        parsed: dict[str, Any] = {}

        # --- Production annuelle ---
        try:
            prod = await self._api.async_get_yearly_production()
            bd = prod.get("breakdown", {})
            total = bd.get("total")
            parsed["yearly_solar_production_kwh"] = total if isinstance(total, (int, float)) else None
            for item in bd.get("destination", []):
                measure = (item.get("measure") or {})
                if item.get("type") == "selfConsumption":
                    parsed["yearly_self_consumption_kwh"] = measure.get("energy")
                elif item.get("type") == "injection":
                    parsed["yearly_grid_injection_kwh"] = measure.get("energy")
        except Exception as err:
            _LOGGER.warning("MyLight150: Yearly production fetch failed: %s", err)

        # --- Consommation annuelle ---
        try:
            conso = await self._api.async_get_yearly_consumption()
            bd = conso.get("breakdown", {})
            for item in (bd.get("global") or {}).get("energies", []):
                if item.get("type") == "paidEnergy":
                    parsed["yearly_grid_purchase_kwh"] = (item.get("measure") or {}).get("energy")
        except Exception as err:
            _LOGGER.warning("MyLight150: Yearly consumption fetch failed: %s", err)

        _LOGGER.debug("MyLight150: Yearly data parsed: %s", parsed)
        return parsed

    # API Calls to MyLight150 endpoints

    async def _fetch_installation_code(self) -> str:
        """Fetch installation code from /v2 endpoint."""
        try:
            v2_data = await self._api.async_call_api("/v2")
            # Searching for "installation" link
            for link in v2_data.get("links", []):
                if link.get("rel") == "installation":
                    href = link.get("href", "")
                    code = href.rstrip("/").split("/")[-1]
                    if code:
                        _LOGGER.debug(f"MyLight150: Installation code '{code}' found.")
                        return code
        except Exception as err:
            _LOGGER.debug("Diagnostics: Error while retrieving /v2 : %s", err)

        raise UpdateFailed("MyLight150: Installation code not found in /v2")
    

    async def _fetch_home_data(self) -> dict[str, Any]:
        """Fetch instant data from /v2/installations/{code}/home?msb=msb01 endpoint."""
        endpoint = f"/v2/installations/{self.installation_code}/home?msb=msb01"
        try:
            data = await self._api.async_call_api(endpoint)
        
            """Parse device data from /v2/installations/{code}/home?msb=msb01 endpoint."""
            parsed: dict[str, Any] = {
                # Live powers (kW)
                "solar_production":  data.get("solarProduction", {}).get("value"),
                "grid":              data.get("grid", {}).get("value"),
                "injection":         data.get("injection", {}).get("value"),
                "load":              data.get("load", {}).get("value"),
                # MySmartBattery (virtual battery)
                "msb_state":         data.get("msb", {}).get("state"),
                "msb_power":         data.get("msb", {}).get("power", {}).get("value"),
                "msb_autonomy":      data.get("msb", {}).get("autonomy", {}).get("value"),
                "msb_capacity":      data.get("msb", {}).get("capacity", {}).get("value"),
                # Saving (weekly display)
                "savings":           data.get("savings", {}).get("amount", {}).get("value"),
                # Timestamp of the data (UTC)
                "timestamp":         data.get("timestamp"),
            }

            _LOGGER.debug("MyLight150: Data parsed for live home: %s", parsed)
            return parsed
        
        except Exception as err:
            _LOGGER.debug("Diagnostics: Error while retrieving %s : %s", endpoint, err)


    async def _fetch_device_data(self) -> dict[str, Any]:
        """Fetch device data from /v3/equipments endpoint."""
        try:
            data = await self._api.async_call_api("/v3/equipments")
        
            """Parse device data from /v3/equipments endpoint."""
            equipments = data.get("equipments", [])

            parsed: dict[str, Any] = {}
            
            for equipment in equipments:
                equipment_type = equipment.get("equipmentType")
                current_mode = equipment.get("currentMode")
                if equipment_type and current_mode:
                    parsed.update({f"{equipment_type}_mode": current_mode})

            _LOGGER.debug("MyLight150: Data parsed for equipments: %s", parsed)
            return parsed
        
        except Exception as err:
            _LOGGER.debug("Diagnostics: Error while retrieving /v3/equipments : %s", err)
