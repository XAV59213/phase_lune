# Précision du calcul / Calculation accuracy

**FR** — Depuis la version de développement suivant 1.3.1, la phase est déduite de l'élongation
écliptique vraie Lune − Soleil, calculée localement (sans réseau ni dépendance) avec les séries
basse précision de J. Meeus, *Astronomical Algorithms* (2e éd., ch. 25 et 47 ; illumination ch. 48).
- Vérifié contre 249 instants officiels de l'US Naval Observatory (2020, 2024, 2025, 2026, 2030) :
  écart max 0,015° d'élongation (≈ 2 min, arrondi à la minute USNO compris).
- Catégories : même convention que l'intégration core *Moon* (échelle 0–28, quartier/pleine/nouvelle
  = ±0,5 autour de la valeur exacte, soit ±6,43° d'élongation ≈ 10,7 à 14,3 h selon la vitesse de la Lune).
  Contrairement au core (calcul par jour entier), le calcul est fait à l'instant (rafraîchi toutes les 15 min).
- Illumination : (1 − cos élongation) / 2. Approximation (angle de phase ≈ 180° − élongation,
  latitude lunaire ignorée) : erreur typique < 0,5 point ; à la nouvelle lune réelle la valeur affichée est ≈ 0 %.
- `age_days` est un âge « équivalent » (élongation / 360 × mois synodique moyen), pas le temps écoulé
  depuis la dernière nouvelle lune.
- Hémisphère sud : seule l'image est inversée ; la phase est identique partout sur Terre.
- Validité : ΔT fixé à 69 s, conçu pour ~1950–2050.
- Avant ce changement (cycle moyen), 44 des 249 instants de référence USNO tombaient dans la mauvaise catégorie.

**EN** — The phase now comes from the true ecliptic Moon−Sun elongation computed locally with Meeus'
low-precision series. Checked against 249 USNO principal-phase instants (max error 0.015°, ≈2 min).
Categories follow the core Moon convention (±0.5 on the 0–28 scale, ±6.43°), evaluated at the current instant.
Illumination uses (1 − cos elongation)/2 (typical error < 0.5 pt). `age_days` is an equivalent age.
Southern hemisphere only mirrors the image. Designed for ~1950–2050. The former mean-cycle model put
44 of the 249 USNO reference instants in the wrong category.
