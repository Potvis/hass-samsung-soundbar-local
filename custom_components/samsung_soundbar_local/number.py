"""Number entity for Samsung Soundbar Local – Subwoofer level."""

from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN
from .soundbar import AsyncSoundbar

_LOGGER = logging.getLogger(__name__)

# Samsung soundbars typically expose a subwoofer range of -12 to +6.
_SUB_MIN = -12
_SUB_MAX = 6
_SUB_DEFAULT = 0


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    """Set up number entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    soundbar: AsyncSoundbar = data["soundbar"]
    host = entry.data["host"]

    async_add_entities(
        [SubwooferLevelNumber(coordinator, soundbar, host)],
        True,
    )


class SubwooferLevelNumber(CoordinatorEntity, RestoreEntity, NumberEntity):
    """Subwoofer level controlled via incremental +/- commands.

    The Samsung API does not expose a direct get/set for the subwoofer level,
    so we track the value locally and restore it across restarts.
    Use the physical remote or SmartThings app to verify the initial level,
    then adjust via this entity to keep it in sync.
    """

    _attr_native_min_value = _SUB_MIN
    _attr_native_max_value = _SUB_MAX
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:speaker"

    def __init__(self, coordinator, soundbar: AsyncSoundbar, host: str) -> None:
        super().__init__(coordinator)
        self._soundbar = soundbar
        self._attr_unique_id = f"{host}_subwoofer_level"
        self._attr_name = f"Soundbar {host} Subwoofer Level"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            manufacturer="Samsung",
            model="Soundbar",
            name=f"Soundbar {host}",
        )
        self._level: int = _SUB_DEFAULT

    async def async_added_to_hass(self) -> None:
        """Restore the last known subwoofer level on startup."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._level = int(float(last_state.state))
            except (ValueError, TypeError):
                self._level = _SUB_DEFAULT

    @property
    def native_value(self) -> int:
        return self._level

    async def async_set_native_value(self, value: float) -> None:
        target = int(value)
        target = max(_SUB_MIN, min(_SUB_MAX, target))

        while self._level != target:
            if self._level < target:
                await self._soundbar.sub_plus()
                self._level += 1
            else:
                await self._soundbar.sub_minus()
                self._level -= 1

        self.async_write_ha_state()
