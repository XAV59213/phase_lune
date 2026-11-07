# Changelog

## Non publié / Unreleased
- FR : phase et illumination calculées depuis l'élongation vraie Lune−Soleil (Meeus), vérifiées sur 249 instants USNO (voir docs/PRECISION.md) ; anecdote liée à la date du calendrier (29 février = 28 février, plus de doublon 30/31 décembre en année bissextile). Tests Home Assistant (pytest) ajoutés.
- EN: phase and illumination from true Moon−Sun elongation (Meeus), checked against 249 USNO instants (see docs/PRECISION.md); anecdote tied to calendar date (Feb 29 = Feb 28, no Dec 30/31 duplicate in leap years). Home Assistant pytest suite added.

## 1.3.1
- FR : ajout de `quality_scale.yaml` (auto-évaluation Quality Scale, sans niveau officiel revendiqué). Aucun changement fonctionnel.
- EN: added `quality_scale.yaml` (Quality Scale self-assessment, no official tier claimed). No functional changes.

## 1.3.0
- FR : suppression de la boucle qui renommait/supprimait les entrées du registre d’entités au démarrage ; plus aucun `entity_id` codé en dur. `has_entity_name` + appareil « Phase de la Lune » + noms traduits (`translation_key`). Les unique_id sont inchangés : les ids existants (et vos renommages) sont conservés. Aucune migration nécessaire. Carte : `entity` optionnelle, détection automatique des capteurs via leurs attributs.
- EN: removed the setup loop that renamed/removed entity registry entries; no more hardcoded `entity_id`. `has_entity_name` + "Phase de la Lune" device + translated names (`translation_key`). Unique ids unchanged, so existing ids (and user renames) are kept. No migration needed. Card: `entity` optional, sensors auto-detected by attributes.

## 1.2.5
- Correctif hassfest : clés pays en minuscules (compatibilité anciennes configs)
- Captures d’écran dans le README

## 1.2.2
- Nouveaux capteurs `sensor.illumination_lune` (%) et `sensor.anecdote_lune` (anecdote du jour).
- `sensor.moon_phase` renommé « Phase lunaire (image) » (entity_id inchangé).
- Éditeur de carte en français ; chemin images forcé `/phase_lune/moon_phases`.
- Carte : anecdote + illumination toujours affichées (repli via `/phase_lune/anecdotes.json`).

## 1.2.1 — 2026-10-31
- FR : carte — l’anecdote du jour s’affiche juste sous le texte poétique, encadrée et bien visible ; repli sur `sensor.phase_de_la_lune` / `sensor.moon_phase` si l’entité choisie n’a pas `anecdote`/`poetic` ; `image_path` `/local/moon_phases` migré automatiquement vers `/phase_lune/moon_phases` ; `show_anecdote` vrai par défaut ; taille de carte augmentée.
- EN: card — fact of the day shown right under the poetic text, highlighted; fallback to `sensor.phase_de_la_lune` / `sensor.moon_phase` when the chosen entity lacks `anecdote`/`poetic`; `/local/moon_phases` image_path silently migrated to `/phase_lune/moon_phases`; `show_anecdote` defaults to true; larger card size.

## 1.2.0 — 2026-10-31
- FR : choix du **pays** à l’installation (défaut France, modifiable via Options) → hémisphère N/S ; au sud, image miroir (croissant ↔ décroissant). Nouveaux attributs `country`, `hemisphere`, `image_slug` ; `entity_picture` ; la carte utilise `image_slug`.
- EN: **country** selection at setup (default France, editable via Options) → N/S hemisphere; southern hemisphere gets mirrored picture. New attributes `country`, `hemisphere`, `image_slug`; `entity_picture`; card uses `image_slug`.

## 1.1.2 — 2026-10-31
- FR : les 8 PNG des phases sont incluses dans le zip HACS (`custom_components/phase_lune/www/moon_phases/`) et servies par l'intégration via `/phase_lune/moon_phases/<slug>.png` — plus de copie dans `www`. Image par défaut de la carte mise à jour.
- EN: the 8 phase PNGs ship in the HACS zip and are served by the integration at `/phase_lune/moon_phases/<slug>.png` — no more copying to `www`. Card default image path updated.

## 1.1.1 — 2026-10-31
- FR : 365 anecdotes FR/EN **toutes uniques** (plus de recyclage de 73 faits) — science, exploration, mythologie, culture, folklore, nature ; source `tools/anecdotes_extra.txt`.
- EN: 365 **truly unique** FR/EN Moon facts (no more recycling of 73 facts) — science, exploration, mythology, culture, folklore, nature; source `tools/anecdotes_extra.txt`.

## 1.1.0 — 2026-10-31
- FR : carte Lovelace `custom:phase-lune-card` (chargée automatiquement, éditeur visuel) ; 365 anecdotes FR/EN (jour de l’année, `anecdotes.json`) ; 4 textes poétiques FR/EN par phase en rotation quotidienne ; nouveaux attributs `anecdote`, `anecdote_en`, `day_of_year`, `poetic_en`, `poetics`.
- EN: `custom:phase-lune-card` Lovelace card (auto-loaded, visual editor); 365 FR/EN facts (day of year, `anecdotes.json`); 4 FR/EN poetic texts per phase with daily rotation; new attributes.

## 1.0.3 — 2026-10-31

- FR : correction du logo du README dans HACS (URL absolue).
- EN: fix README logo in HACS (absolute URL).

## 1.0.2 — 2026-10-31
- FR: documentation bilingue (README, docs/, wiki/, info.md), traductions enrichies ; images `media/moon_phases/` (crédit papo-o / HA Community)
- EN: bilingual documentation (README, docs/, wiki/, info.md), richer translations; `media/moon_phases/` images (credit papo-o / HA Community)

## 1.0.1 — 2026-10-31
- Ajout des assets brand (icon/logo, clair/sombre, @2x)
- README enrichi (badges, documentation, contribution)
- Documentation `docs/` + pages wiki prêtes à publier

## 1.0.0
- Première version : capteurs `sensor.moon_phase` (slug) et `sensor.phase_de_la_lune` (FR)
- Illumination %, âge lunaire, textes poétiques
- Configuration UI en un clic, traductions FR/EN, calcul 100 % local
