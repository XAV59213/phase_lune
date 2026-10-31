# Installation

## Via HACS (recommended)
1. HACS → Integrations → ⋮ → **Custom repositories**.
2. URL `https://github.com/XAV59213/phase_lune`, category **Integration**.
3. Search **Phase de la Lune** → Download.
4. Restart Home Assistant.
5. Settings → Devices & services → **Add integration** → "Phase de la Lune".

## Manual
1. Download `phase_lune.zip` from the [latest release](https://github.com/XAV59213/phase_lune/releases/latest).
2. Unzip into `config/custom_components/phase_lune/`.
3. Restart, then add the integration.

## Phase images
Create `config/www/moon_phases/` and put 8 PNG files there: `new_moon.png`, `waxing_crescent.png`, `first_quarter.png`, `waxing_gibbous.png`, `full_moon.png`, `waning_gibbous.png`, `last_quarter.png`, `waning_crescent.png`. They are served at `/local/moon_phases/<slug>.png`.

## Updating
HACS offers new versions automatically; restart after updating.
