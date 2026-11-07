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
Create `config/www/moon_phases/` and put 8 PNG files there: `new_moon.png`, `waxing_crescent.png`, `first_quarter.png`, `waxing_gibbous.png`, `full_moon.png`, `waning_gibbous.png`, `last_quarter.png`, `waning_crescent.png`. Since 1.1.2 this is **no longer needed**: PNGs ship with the integration at `/phase_lune/moon_phases/<slug>.png`. (Manual copy optional to use `/local/moon_phases/`.)

Ready-to-copy images: [`media/moon_phases/`](https://github.com/XAV59213/phase_lune/tree/main/media/moon_phases) — source: [papo-o](https://github.com/papo-o/home-assistant-config/tree/master/www/moon_phases) / [HA Community 86646](https://community.home-assistant.io/t/moon-platform-with-moon-phases-pictures/86646), redistributed with credit.

## Updating
HACS offers new versions automatically; restart after updating.

## Country / options
At setup: **Country** (default France) → hemisphere (picture mirrored in the south). Change via **Configure** (automatic reload). Single instance.

## Removal
Settings → Devices & services → Phase de la Lune → ⋮ → **Delete**. Optional: HACS → ⋮ → **Remove**, restart, remove `custom:phase-lune-card` cards.

## Accuracy
See [PRECISION.md](https://github.com/XAV59213/phase_lune/blob/main/docs/PRECISION.md) (`age_days` = equivalent age since 1.3.2; Feb 29 = Feb 28 fact).
