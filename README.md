<p align="center"><img src="https://raw.githubusercontent.com/XAV59213/phase_lune/main/custom_components/phase_lune/brand/logo.png" alt="Phase de la Lune" width="400"></p>

# 🌙 Phase de la Lune / Moon Phase — Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![Release](https://img.shields.io/github/v/release/XAV59213/phase_lune)](https://github.com/XAV59213/phase_lune/releases)
[![Hassfest](https://github.com/XAV59213/phase_lune/actions/workflows/hassfest.yml/badge.svg)](https://github.com/XAV59213/phase_lune/actions/workflows/hassfest.yml)
[![HACS Validation](https://github.com/XAV59213/phase_lune/actions/workflows/hacs.yml/badge.svg)](https://github.com/XAV59213/phase_lune/actions/workflows/hacs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[🇫🇷 Français](#-français) · [🇬🇧 English](#-english)**

---

## 🇫🇷 Français

### Description
Intégration Home Assistant qui calcule **localement** (sans API, sans dépendance) la phase de la lune, son illumination et un texte poétique en français.

### Fonctionnalités
- **2 capteurs** :
  - `sensor.moon_phase` → slug anglais (nom des images PNG) ; attributs `illumination`, `age_days`, `phase_fr`, `poetic`
  - `sensor.phase_de_la_lune` → libellé français ; attributs `illumination`, `age_days`, `phase_slug`, `poetic`
- **Illumination** en % (0–100) et âge lunaire en jours
- **Textes poétiques** pour chaque phase
- Icônes `mdi:moon-*` dynamiques, traductions FR/EN, configuration UI en un clic

### Carte Lovelace custom (1.1.0)
La carte `custom:phase-lune-card` est **chargée automatiquement** par l’intégration (aucune ressource à ajouter). Fond sombre hexagones, grande image de lune, phase actuelle, texte poétique (4 par phase, rotation quotidienne) et **anecdote du jour** (365 anecdotes FR/EN, une par jour de l’année).

Tableau de bord → Modifier → Ajouter une carte → cherchez « Phase de la Lune », ou en YAML :
```yaml
type: custom:phase-lune-card
title: Phase de la Lune
entity: sensor.phase_de_la_lune
image_path: /local/moon_phases   # PNG à copier dans config/www/moon_phases/
language: fr                     # ou en
show_illumination: true
show_anecdote: true
```
Nouveaux attributs : `anecdote`, `anecdote_en`, `day_of_year`, `poetic_en`, `poetics`.

### Installation (HACS)

[![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=XAV59213&repository=phase_lune&category=integration)

1. HACS → Intégrations → ⋮ → **Dépôts personnalisés**
2. Ajouter `https://github.com/XAV59213/phase_lune`, catégorie **Intégration**
3. Installer **Phase de la Lune**, puis redémarrer Home Assistant

Installation manuelle : copier `custom_components/phase_lune` dans `config/custom_components/`.

### Configuration
Paramètres → Appareils et services → **Ajouter une intégration** → « Phase de la Lune » → Valider. Aucune option (instance unique).

### Images
Placer 8 images PNG dans `config/www/moon_phases/` (accessibles via `/local/moon_phases/`), nommées exactement :

| État `sensor.moon_phase` | `sensor.phase_de_la_lune` | Fichier |
|---|---|---|
| `new_moon` | Nouvelle lune | `new_moon.png` |
| `waxing_crescent` | Premier croissant | `waxing_crescent.png` |
| `first_quarter` | Premier quartier | `first_quarter.png` |
| `waxing_gibbous` | Gibbeuse croissante | `waxing_gibbous.png` |
| `full_moon` | Pleine lune | `full_moon.png` |
| `waning_gibbous` | Gibbeuse décroissante | `waning_gibbous.png` |
| `last_quarter` | Dernier quartier | `last_quarter.png` |
| `waning_crescent` | Dernier croissant | `waning_crescent.png` |

> Le dossier `www` nécessite parfois un redémarrage de HA après sa création.

📦 Les 8 images prêtes à copier sont dans [`media/moon_phases/`](media/moon_phases/) (hors zip HACS). Source/crédit : [papo-o/home-assistant-config](https://github.com/papo-o/home-assistant-config/tree/master/www/moon_phases) · [fil HA Community 86646](https://community.home-assistant.io/t/moon-platform-with-moon-phases-pictures/86646) — licence non précisée par l'auteur, redistribuées avec crédit ([détails](media/moon_phases/README.md)).

### Exemple de carte Lovelace (fond sombre)
```yaml
type: markdown
card_mod:
  style: |
    ha-card { background: #0b1020; color: #e8e8f0; text-align: center; }
content: |
  <img src="/local/moon_phases/{{ states('sensor.moon_phase') }}.png" width="200">

  ## Phase actuelle : {{ states('sensor.phase_de_la_lune') }}

  *{{ state_attr('sensor.phase_de_la_lune','poetic') }}*

  Illumination : {{ state_attr('sensor.phase_de_la_lune','illumination') }} %
```
(`card_mod` est optionnel ; sans lui, utiliser un thème sombre.)

### Calcul
Âge lunaire = jours écoulés depuis une nouvelle lune de référence modulo le mois synodique (29,530588 j). Seuils alignés sur l’intégration Moon du core (échelle 0–28). Illumination ≈ `(1 − cos(2π·âge/29,530588)) / 2 × 100`. Précision : quelques heures.

### Documentation
Guides détaillés dans [`docs/`](docs/) (et le [wiki](https://github.com/XAV59213/phase_lune/wiki)) : [Accueil](docs/Home.fr.md) · [Installation](docs/Installation.fr.md) · [Lovelace](docs/Lovelace.fr.md) · [FAQ](docs/FAQ.fr.md)

### Contribution
Issues et pull requests bienvenues : [ouvrir une issue](https://github.com/XAV59213/phase_lune/issues). Merci de vérifier que les workflows Hassfest et HACS passent.

---

## 🇬🇧 English

### Description
Home Assistant integration that computes the moon phase, its illumination and a French poetic text **locally** (no API, no dependency).

### Features
- **2 sensors**:
  - `sensor.moon_phase` → English slug (PNG image name); attributes `illumination`, `age_days`, `phase_fr`, `poetic`
  - `sensor.phase_de_la_lune` → French label; attributes `illumination`, `age_days`, `phase_slug`, `poetic`
- **Illumination** in % (0–100) and lunar age in days
- **Poetic texts** for each phase (French)
- Dynamic `mdi:moon-*` icons, FR/EN translations, one-click UI setup

### Custom Lovelace card (1.1.0)
The `custom:phase-lune-card` card is **loaded automatically** by the integration (no resource to add). Dark hexagon background, large moon picture, current phase, poetic text (4 per phase, daily rotation) and **fact of the day** (365 FR/EN facts, one per day of the year).

Dashboard → Edit → Add card → search “Phase de la Lune”, or YAML:
```yaml
type: custom:phase-lune-card
entity: sensor.phase_de_la_lune
image_path: /local/moon_phases   # copy PNGs to config/www/moon_phases/
language: en
```
New attributes: `anecdote`, `anecdote_en`, `day_of_year`, `poetic_en`, `poetics`.

### Installation (HACS)

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=XAV59213&repository=phase_lune&category=integration)

1. HACS → Integrations → ⋮ → **Custom repositories**
2. Add `https://github.com/XAV59213/phase_lune`, category **Integration**
3. Install **Phase de la Lune**, then restart Home Assistant

Manual install: copy `custom_components/phase_lune` into `config/custom_components/`.

### Configuration
Settings → Devices & services → **Add integration** → "Phase de la Lune" → Submit. No options (single instance).

### Images
Put 8 PNG images in `config/www/moon_phases/` (served at `/local/moon_phases/`), named exactly:

| `sensor.moon_phase` state | `sensor.phase_de_la_lune` | File |
|---|---|---|
| `new_moon` | Nouvelle lune (New moon) | `new_moon.png` |
| `waxing_crescent` | Premier croissant (Waxing crescent) | `waxing_crescent.png` |
| `first_quarter` | Premier quartier (First quarter) | `first_quarter.png` |
| `waxing_gibbous` | Gibbeuse croissante (Waxing gibbous) | `waxing_gibbous.png` |
| `full_moon` | Pleine lune (Full moon) | `full_moon.png` |
| `waning_gibbous` | Gibbeuse décroissante (Waning gibbous) | `waning_gibbous.png` |
| `last_quarter` | Dernier quartier (Last quarter) | `last_quarter.png` |
| `waning_crescent` | Dernier croissant (Waning crescent) | `waning_crescent.png` |

> The `www` folder may require a HA restart after it is created.

📦 The 8 ready-to-copy images are in [`media/moon_phases/`](media/moon_phases/) (not in the HACS zip). Source/credit: [papo-o/home-assistant-config](https://github.com/papo-o/home-assistant-config/tree/master/www/moon_phases) · [HA Community thread 86646](https://community.home-assistant.io/t/moon-platform-with-moon-phases-pictures/86646) — no license stated by the author, redistributed with credit ([details](media/moon_phases/README.md)).

### Lovelace card example (dark)
```yaml
type: markdown
card_mod:
  style: |
    ha-card { background: #0b1020; color: #e8e8f0; text-align: center; }
content: |
  <img src="/local/moon_phases/{{ states('sensor.moon_phase') }}.png" width="200">

  ## Current phase: {{ states('sensor.phase_de_la_lune') }}

  *{{ state_attr('sensor.phase_de_la_lune','poetic') }}*

  Illumination: {{ state_attr('sensor.phase_de_la_lune','illumination') }} %
```
(`card_mod` is optional; without it, use a dark theme.)

### Calculation
Lunar age = days since a reference new moon modulo the synodic month (29.530588 d). Thresholds match the core Moon integration (0–28 scale). Illumination ≈ `(1 − cos(2π·age/29.530588)) / 2 × 100`. Accuracy: a few hours.

### Documentation
Detailed guides in [`docs/`](docs/Home.md): [Home](docs/Home.en.md) · [Installation](docs/Installation.en.md) · [Lovelace](docs/Lovelace.en.md) · [FAQ](docs/FAQ.en.md)

### Contributing
Issues and pull requests welcome: [open an issue](https://github.com/XAV59213/phase_lune/issues). Please make sure the Hassfest and HACS workflows pass.

---

## Licence / License
MIT © 2025-2026 XAV59213
