DOMAIN = "soundbar_local"

PLATFORMS = ["button", "media_player", "number"]

DEFAULT_POLL_INTERVAL = 10  # seconds

CONF_VERIFY_SSL = "verify_ssl"
CONF_SOURCE_NAMES = "source_names"
CONF_SOUND_MODE_NAMES = "sound_mode_names"

# All possible API source identifiers
ALL_SOURCES = [
    "HDMI_IN1",
    "HDMI_IN2",
    "E_ARC",
    "ARC",
    "D_IN",
    "BT",
    "WIFI_IDLE",
]

# All possible API sound mode identifiers
ALL_SOUND_MODES = [
    "STANDARD",
    "SURROUND",
    "GAME",
    "MOVIE",
    "MUSIC",
    "CLEARVOICE",
    "DTS_VIRTUAL_X",
    "ADAPTIVE",
]

# Default display names (empty string = hidden from UI)
DEFAULT_SOURCE_NAMES: dict[str, str] = {
    "HDMI_IN1": "HDMI 1",
    "HDMI_IN2": "HDMI 2",
    "E_ARC": "eARC",
    "ARC": "ARC",
    "D_IN": "Digital In",
    "BT": "Bluetooth",
    "WIFI_IDLE": "Wi-Fi",
}

DEFAULT_SOUND_MODE_NAMES: dict[str, str] = {
    "STANDARD": "Standard",
    "SURROUND": "Surround",
    "GAME": "Game",
    "MOVIE": "Movie",
    "MUSIC": "Music",
    "CLEARVOICE": "Clear Voice",
    "DTS_VIRTUAL_X": "DTS Virtual X",
    "ADAPTIVE": "Adaptive Sound",
}
