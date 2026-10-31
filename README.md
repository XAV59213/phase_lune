<p align="center"><img src="custom_components/phase_lune/brand/logo.png" alt="Phase de la Lune" width="400"></p>

# 🌙 Phase de la Lune — Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![Release](https://img.shields.io/github/v/release/XAV59213/phase_lune)](https://github.com/XAV59213/phase_lune/releases)
[![Hassfest](https://github.com/XAV59213/phase_lune/actions/workflows/hassfest.yml/badge.svg)](https://github.com/XAV59213/phase_lune/actions/workflows/hassfest.yml)
[![HACS Validation](https://github.com/XAV59213/phase_lune/actions/workflows/hacs.yml/badge.svg)](https://github.com/XAV59213/phase_lune/actions/workflows/hacs.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Description
Intégration Home Assistant qui calcule **localement** (sans API, sans dépendance) la phase de la lune, son illumination et un texte poétique en français.

## Fonctionnalités
- **2 capteurs** :
  - `sensor.moon_phase` → slug anglais (nom des images PNG) ; attributs `illumination`, `age_days`, `phase_fr`, `poetic`
  - `sensor.phase_de_la_lune` → libellé français ; attributs `illumination`, `age_days`, `phase_slug`, `poetic`
- **Illumination** en % (0–100) et âge lunaire en jours
- **Textes poétiques** pour chaque phase
- Icônes `mdi:moon-*` dynamiques, traductions FR/EN, configuration UI en un clic

## Installation (HACS)

[![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=XAV59213&repository=phase_lune&category=integration)

1. HACS → Intégrations → ⋮ → **Dépôts personnalisés**
2. Ajouter `https://github.com/XAV59213/phase_lune`, catégorie **Intégration**
3. Installer **Phase de la Lune**, puis redémarrer Home Assistant

Installation manuelle : copier `custom_components/phase_lune` dans `config/custom_components/`.

## Configuration
Paramètres → Appareils et services → **Ajouter une intégration** → « Phase de la Lune » → Valider. Aucune option (instance unique).

## Images
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

## Exemple de carte Lovelace (fond sombre)
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

## Calcul
Âge lunaire = jours écoulés depuis une nouvelle lune de référence modulo le mois synodique (29,530588 j). Seuils alignés sur l’intégration Moon du core (échelle 0–28). Illumination ≈ `(1 − cos(2π·âge/29,530588)) / 2 × 100`. Précision : quelques heures.

## À venir
Icônes brand (`brand/icon.png`) pourront être ajoutées dans une version ultérieure.

## Documentation
Guides détaillés dans [`docs/`](docs/) (et le [wiki](https://github.com/XAV59213/phase_lune/wiki)) : [Installation](docs/Installation.md) · [Lovelace](docs/Lovelace.md) · [FAQ](docs/FAQ.md)

## Contribution
Issues et pull requests bienvenues : [ouvrir une issue](https://github.com/XAV59213/phase_lune/issues). Merci de vérifier que les workflows Hassfest et HACS passent.

## Licence
MIT © 2025-2026 XAV59213
