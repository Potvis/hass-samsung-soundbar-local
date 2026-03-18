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
    CONF_SOUND_MODE_ORDER,
    CONF_SOURCE_NAMES,
    CONF_SOURCE_ORDER,
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

    # ---- sources ----

    async def async_step_sources(self, user_input: dict | None = None) -> FlowResult:
        """Configure source display names and order."""
        current_names = self._config_entry.options.get(CONF_SOURCE_NAMES, {})
        current_order = self._config_entry.options.get(CONF_SOURCE_ORDER, "")

        if user_input is not None:
            new_opts = dict(self._config_entry.options)
            new_opts[CONF_SOURCE_NAMES] = {
                api_name: user_input.get(api_name, "").strip()
                for api_name in ALL_SOURCES
            }
            new_opts[CONF_SOURCE_ORDER] = user_input.get(CONF_SOURCE_ORDER, "").strip()
            return self.async_create_entry(title="", data=new_opts)

        # Build schema with suggested_value so clearing a field actually blanks it
        schema_fields: dict = {}

        # Order field first
        default_order = current_order or ", ".join(ALL_SOURCES)
        schema_fields[
            vol.Optional(
                CONF_SOURCE_ORDER,
                description={"suggested_value": default_order},
            )
        ] = str

        # Individual name fields
        for api_name in ALL_SOURCES:
            current = current_names.get(
                api_name, DEFAULT_SOURCE_NAMES.get(api_name, "")
            )
            schema_fields[
                vol.Optional(
                    api_name,
                    description={"suggested_value": current},
                )
            ] = str

        return self.async_show_form(
            step_id="sources",
            data_schema=vol.Schema(schema_fields),
        )

    # ---- sound modes ----

    async def async_step_sound_modes(self, user_input: dict | None = None) -> FlowResult:
        """Configure sound mode display names and order."""
        current_names = self._config_entry.options.get(CONF_SOUND_MODE_NAMES, {})
        current_order = self._config_entry.options.get(CONF_SOUND_MODE_ORDER, "")

        if user_input is not None:
            new_opts = dict(self._config_entry.options)
            new_opts[CONF_SOUND_MODE_NAMES] = {
                api_name: user_input.get(api_name, "").strip()
                for api_name in ALL_SOUND_MODES
            }
            new_opts[CONF_SOUND_MODE_ORDER] = user_input.get(
                CONF_SOUND_MODE_ORDER, ""
            ).strip()
            return self.async_create_entry(title="", data=new_opts)

        schema_fields: dict = {}

        # Order field first
        default_order = current_order or ", ".join(ALL_SOUND_MODES)
        schema_fields[
            vol.Optional(
                CONF_SOUND_MODE_ORDER,
                description={"suggested_value": default_order},
            )
        ] = str

        for api_name in ALL_SOUND_MODES:
            current = current_names.get(
                api_name, DEFAULT_SOUND_MODE_NAMES.get(api_name, "")
            )
            schema_fields[
                vol.Optional(
                    api_name,
                    description={"suggested_value": current},
                )
            ] = str

        return self.async_show_form(
            step_id="sound_modes",
            data_schema=vol.Schema(schema_fields),
        )
