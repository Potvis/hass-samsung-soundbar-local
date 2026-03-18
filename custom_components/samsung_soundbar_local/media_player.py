"""Media Player entity for Samsung Soundbar Local."""

from __future__ import annotations

import logging

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry

from .const import (
    ALL_SOUND_MODES,
    ALL_SOURCES,
    CONF_SOUND_MODE_NAMES,
    CONF_SOUND_MODE_ORDER,
    CONF_SOURCE_NAMES,
    CONF_SOURCE_ORDER,
    DEFAULT_SOUND_MODE_NAMES,
    DEFAULT_SOURCE_NAMES,
    DOMAIN,
)
from .soundbar import AsyncSoundbar

_LOGGER = logging.getLogger(__name__)

_SUPPORTED: MediaPlayerEntityFeature = (
    MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
    | MediaPlayerEntityFeature.SELECT_SOUND_MODE
)


def _parse_order(order_str: str, all_names: list[str]) -> list[str]:
    """Parse a comma-separated order string into a list of valid API names."""
    if not order_str or not order_str.strip():
        return list(all_names)
    valid = set(all_names)
    return [n.strip() for n in order_str.split(",") if n.strip() in valid]


def _build_mapping(
    api_names: list[str],
    defaults: dict[str, str],
    overrides: dict[str, str],
    order: list[str],
) -> dict[str, str]:
    """Build ordered {api_name: display_name} mapping, dropping empty display names."""
    # Only include sources that appear in the order list
    ordered = order if order else api_names
    mapping: dict[str, str] = {}
    for api_name in ordered:
        if api_name not in defaults and api_name not in overrides:
            continue
        display = overrides.get(api_name, defaults.get(api_name, api_name))
        if display:  # empty string = hidden
            mapping[api_name] = display
    return mapping


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    """Set up the soundbar platform from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    soundbar: AsyncSoundbar = data["soundbar"]

    async_add_entities([SoundbarLocalEntity(coordinator, soundbar, entry)], True)


class SoundbarLocalEntity(CoordinatorEntity, MediaPlayerEntity):
    """Representation of the soundbar as a Media Player entity."""

    _attr_supported_features = _SUPPORTED
    _attr_device_class = MediaPlayerDeviceClass.SPEAKER

    def __init__(self, coordinator, soundbar: AsyncSoundbar, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._soundbar = soundbar
        self._entry = entry

        host = entry.data["host"]
        self._attr_unique_id = host
        self._attr_name = f"Soundbar {host}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            manufacturer="Samsung",
            model="Soundbar",
            name=self._attr_name,
        )

        self._refresh_mappings()

    def _refresh_mappings(self) -> None:
        """Rebuild display-name mappings from current options."""
        opts = self._entry.options

        source_order = _parse_order(
            opts.get(CONF_SOURCE_ORDER, ""), ALL_SOURCES
        )
        sound_mode_order = _parse_order(
            opts.get(CONF_SOUND_MODE_ORDER, ""), ALL_SOUND_MODES
        )

        self._source_map = _build_mapping(
            ALL_SOURCES,
            DEFAULT_SOURCE_NAMES,
            opts.get(CONF_SOURCE_NAMES, {}),
            source_order,
        )
        self._sound_mode_map = _build_mapping(
            ALL_SOUND_MODES,
            DEFAULT_SOUND_MODE_NAMES,
            opts.get(CONF_SOUND_MODE_NAMES, {}),
            sound_mode_order,
        )

        # Reverse maps: display_name -> api_name
        self._source_reverse = {v: k for k, v in self._source_map.items()}
        self._sound_mode_reverse = {v: k for k, v in self._sound_mode_map.items()}

        self._attr_source_list = list(self._source_map.values())
        self._attr_sound_mode_list = list(self._sound_mode_map.values())

    # ---------- control ----------
    async def async_turn_on(self) -> None:
        await self._soundbar.power_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        await self._soundbar.power_off()
        await self.coordinator.async_request_refresh()

    async def async_volume_up(self) -> None:
        await self._soundbar.volume_up()
        await self.coordinator.async_request_refresh()

    async def async_volume_down(self) -> None:
        await self._soundbar.volume_down()
        await self.coordinator.async_request_refresh()

    async def async_set_volume_level(self, volume: float) -> None:
        await self._soundbar.set_volume(int(volume * 100))
        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        if mute != self.is_volume_muted:
            await self._soundbar.mute_toggle()
            await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str) -> None:
        api_name = self._source_reverse.get(source, source)
        await self._soundbar.select_input(api_name)
        await self.coordinator.async_request_refresh()

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        api_name = self._sound_mode_reverse.get(sound_mode, sound_mode)
        await self._soundbar.set_sound_mode(api_name)
        await self.coordinator.async_request_refresh()

    # ---------- properties ----------
    @property
    def state(self):
        power = self.coordinator.data.get("power")
        return STATE_ON if power == "powerOn" else STATE_OFF

    @property
    def volume_level(self):
        return self.coordinator.data.get("volume", 0) / 100

    @property
    def is_volume_muted(self):
        return self.coordinator.data.get("mute", False)

    @property
    def source(self):
        api_val = self.coordinator.data.get("input")
        return self._source_map.get(api_val, api_val)

    @property
    def sound_mode(self):
        api_val = self.coordinator.data.get("sound_mode")
        return self._sound_mode_map.get(api_val, api_val)

    # ---------- coordinator / options update ----------
    @callback
    def _handle_coordinator_update(self) -> None:
        self._refresh_mappings()
        self.async_write_ha_state()
