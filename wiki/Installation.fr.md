# Installation

## Via HACS (recommandé)
1. HACS → Intégrations → ⋮ → **Dépôts personnalisés**.
2. URL `https://github.com/XAV59213/phase_lune`, catégorie **Intégration**.
3. Rechercher **Phase de la Lune** → Télécharger.
4. Redémarrer Home Assistant.
5. Paramètres → Appareils et services → **Ajouter une intégration** → « Phase de la Lune ».

## Manuelle
1. Télécharger `phase_lune.zip` depuis la [dernière release](https://github.com/XAV59213/phase_lune/releases/latest).
2. Décompresser dans `config/custom_components/phase_lune/`.
3. Redémarrer puis ajouter l'intégration.

## Images des phases
Créer `config/www/moon_phases/` et y déposer 8 PNG : `new_moon.png`, `waxing_crescent.png`, `first_quarter.png`, `waxing_gibbous.png`, `full_moon.png`, `waning_gibbous.png`, `last_quarter.png`, `waning_crescent.png`. Depuis 1.1.2 ce n'est **plus nécessaire** : les PNG sont dans l'intégration et servies via `/phase_lune/moon_phases/<slug>.png`. (Copie manuelle optionnelle pour utiliser `/local/moon_phases/`.)

Images prêtes à copier : [`media/moon_phases/`](https://github.com/XAV59213/phase_lune/tree/main/media/moon_phases) — source : [papo-o](https://github.com/papo-o/home-assistant-config/tree/master/www/moon_phases) / [HA Community 86646](https://community.home-assistant.io/t/moon-platform-with-moon-phases-pictures/86646), redistribuées avec crédit.

## Mise à jour
HACS propose automatiquement les nouvelles versions ; redémarrer après mise à jour.

## Pays / options
À l'ajout : **Pays** (défaut France) → hémisphère (image inversée au sud). Modifiable via **Configurer** (rechargement automatique). Instance unique.

## Suppression
Paramètres → Appareils et services → Phase de la Lune → ⋮ → **Supprimer**. Optionnel : HACS → ⋮ → **Supprimer**, redémarrer, retirer les cartes `custom:phase-lune-card`.

## Précision
Voir [PRECISION.md](https://github.com/XAV59213/phase_lune/blob/main/docs/PRECISION.md) (`age_days` = âge équivalent depuis 1.3.2 ; 29 février = anecdote du 28).
