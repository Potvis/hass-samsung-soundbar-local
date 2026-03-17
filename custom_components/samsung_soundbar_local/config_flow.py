"""Config flow for Samsung Soundbar Local."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import (
    ALL_SOUND_MODES,
    ALL_SOURCES,
    CONF_SOUND_MODE_NAMES,
    CONF_SOURCE_NAMES,
    CONF_VERIFY_SSL,
    DEFAULT_SOUND_MODE_NAMES,
    DEFAULT_SOURCE_NAMES,
    DOMAIN,
)


class SoundbarLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Soundbar."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the step when user initiates a flow via the UI."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Optional(CONF_VERIFY_SSL, default=False): bool,
                }
            ),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return SoundbarLocalOptionsFlow(config_entry)


class SoundbarLocalOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for customising display names."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None) -> FlowResult:
        """Show the main options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["sources", "sound_modes"],
        )

    async def async_step_sources(self, user_input: dict | None = None) -> FlowResult:
        """Configure source display names."""
        current = self._config_entry.options.get(CONF_SOURCE_NAMES, {})

        if user_input is not None:
            new_opts = dict(self._config_entry.options)
            new_opts[CONF_SOURCE_NAMES] = {
                api_name: user_input.get(api_name, "")
                for api_name in ALL_SOURCES
            }
            return self.async_create_entry(title="", data=new_opts)

        schema_fields: dict = {}
        for api_name in ALL_SOURCES:
            default = current.get(api_name, DEFAULT_SOURCE_NAMES.get(api_name, api_name))
            schema_fields[vol.Optional(api_name, default=default)] = str

        return self.async_show_form(
            step_id="sources",
            data_schema=vol.Schema(schema_fields),
            description_placeholders={
                "instructions": "Enter a display name for each input source. Leave blank to hide the source from the UI."
            },
        )

    async def async_step_sound_modes(self, user_input: dict | None = None) -> FlowResult:
        """Configure sound mode display names."""
        current = self._config_entry.options.get(CONF_SOUND_MODE_NAMES, {})

        if user_input is not None:
            new_opts = dict(self._config_entry.options)
            new_opts[CONF_SOUND_MODE_NAMES] = {
                api_name: user_input.get(api_name, "")
                for api_name in ALL_SOUND_MODES
            }
            return self.async_create_entry(title="", data=new_opts)

        schema_fields: dict = {}
        for api_name in ALL_SOUND_MODES:
            default = current.get(api_name, DEFAULT_SOUND_MODE_NAMES.get(api_name, api_name))
            schema_fields[vol.Optional(api_name, default=default)] = str

        return self.async_show_form(
            step_id="sound_modes",
            data_schema=vol.Schema(schema_fields),
            description_placeholders={
                "instructions": "Enter a display name for each sound mode. Leave blank to hide the mode from the UI."
            },
        )
