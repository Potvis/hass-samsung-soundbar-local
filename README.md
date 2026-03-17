# Samsung Soundbar **Local** – Home Assistant Integration (Fork)

> **This is a fork of [hass-samsung-soundbar-local](https://github.com/ZtF/hass-samsung-soundbar-local) by [@ZtF](https://github.com/ZtF).**
> All credit for the original integration goes to them.

> **Local IP control for 2024-line Samsung Wi-Fi soundbars**
> HW-Q990D · HW-Q800D · HW-QS730D · HW-S800D · HW-S801D · HW-S700D · HW-S60D · HW-S61D · HW-LS60D

---

## What changed in this fork?

- **Customisable input source names** – Rename or hide any input source via the integration's options page.
- **Customisable sound mode names** – Same for sound modes.
- **Subwoofer level slider** – A number entity (`number.soundbar_<ip>_subwoofer_level`) exposed as a slider so you can set the subwoofer level directly from Home Assistant dashboards and automations.

---

## What is it?

`soundbar_local` is a custom Home Assistant component that talks **directly** to your 2024 Samsung soundbar over the LAN (TCP 1516, same JSON-RPC API used by the SmartThings app).
No cloud, no SmartThings integration in Home Assistant – everything stays on your network.

### Key features

| Function | Details |
|----------|---------|
| Power control | `turn_on`, `turn_off` |
| Audio | volume **set / step / mute** |
| Subwoofer | level slider (-12 to +6) + woofer ± buttons |
| Inputs | Configurable – rename or hide any source |
| Sound modes | Configurable – rename or hide any mode |
| Options page | Customise display names for sources and sound modes |

The entity is exposed as `media_player.soundbar_<ipaddr>` and works with dashboards, automations and scripts just like any other media-player device.

---

## Supported models

* HW-Q990D  – HW-Q930F
* HW-Q990D  – HW-Q800D  – HW-QS730D
* HW-S800D  – HW-S801D  – HW-S700D  – HW-S60D  – HW-S61D  – HW-LS60D

> Older (2023 and below) bars do **not** implement the same API and will **not** work.

---

## Requirements

* Home Assistant 2024.3.0 or newer
* Python 3.11 (bundled with HA OS / Container)
* Your soundbar **added to the Samsung SmartThings app, connected to Wi-Fi** and
  **"IP control" enabled** in the device settings.
  This setting allows the bar to produce an *Access Token* that the integration uses.

---

## Installation

### Option 1: HACS (recommended)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations → ⋮ (three dots) → Custom repositories**.
3. Add the URL of this fork repository and select **Integration** as the category.
4. Search for **Samsung Soundbar Local** in HACS and install it.
5. Restart Home Assistant.
6. Go to **Settings → Devices & Services → + Add Integration**, search for
   **"Samsung Soundbar Local"**, enter the soundbar's IP address and confirm.

### Option 2: Manual install from release

1. **Download the latest ZIP** from the [Releases](../../releases) page.
2. Unzip to `<config>/custom_components/` (you should end up with
   `<config>/custom_components/samsung_soundbar_local/`).
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → + Add Integration**, search for
   **"Samsung Soundbar Local"**, enter the soundbar's IP address and confirm.

---

## Configuring display names

After adding the integration, go to **Settings → Devices & Services**, find
**Samsung Soundbar Local**, click **Configure**.

You will see two options:

- **Input sources** – Set a display name for each input. Leave a field blank to
  hide that source from the media player UI.
- **Sound modes** – Same for sound modes.

Changes take effect after saving (the integration reloads automatically).

---

## Subwoofer level

The integration exposes a **number entity** (`number.soundbar_<ip>_subwoofer_level`)
that appears as a slider ranging from -12 to +6.

> **Note:** The Samsung API only supports incremental +/- commands for the
> subwoofer. The integration tracks the level locally and restores it across
> restarts. If you change the level using the physical remote or SmartThings app,
> the slider may become out of sync. Adjust it once via Home Assistant to
> re-calibrate.

---

## Creating a release

Follow these steps to create a new release of this integration:

1. **Update the version** in `custom_components/samsung_soundbar_local/manifest.json`.
2. **Commit and push** your changes.
3. **Create a ZIP archive** of the integration folder:
   ```bash
   cd custom_components
   zip -r samsung_soundbar_local.zip samsung_soundbar_local/
   ```
4. **Create a GitHub release:**
   - Go to your fork on GitHub → **Releases** → **Draft a new release**.
   - Click **Choose a tag**, type a version (e.g. `v1.1.0`), and select
     **Create new tag on publish**.
   - Set the **Release title** (e.g. `v1.1.0`).
   - Write release notes describing the changes.
   - **Attach** the `samsung_soundbar_local.zip` file you created.
   - Click **Publish release**.

---

## Credits

This integration is a fork of the excellent work by **[@ZtF](https://github.com/ZtF)**:
<https://github.com/ZtF/hass-samsung-soundbar-local>

All original design, API reverse-engineering, and implementation credit belongs to them.
