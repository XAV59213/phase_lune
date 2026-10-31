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
Créer `config/www/moon_phases/` et y déposer 8 PNG : `new_moon.png`, `waxing_crescent.png`, `first_quarter.png`, `waxing_gibbous.png`, `full_moon.png`, `waning_gibbous.png`, `last_quarter.png`, `waning_crescent.png`. Elles sont servies via `/local/moon_phases/<slug>.png`.

## Mise à jour
HACS propose automatiquement les nouvelles versions ; redémarrer après mise à jour.
