"""Constantes pour l'intégration Phase de la Lune."""
DOMAIN = "phase_lune"
NAME = "Phase de la Lune"
VERSION = "1.0.0"

SYNODIC_MONTH = 29.530588853
# Nouvelle lune de référence : 6 janvier 2000 18:14 UTC
REFERENCE_NEW_MOON_JD = 2451550.1

PHASES = {
    "new_moon": ("Nouvelle lune", "mdi:moon-new", "La lune se renouvelle dans l’ombre…"),
    "waxing_crescent": ("Premier croissant", "mdi:moon-waxing-crescent", "Un fin croissant apparaît…"),
    "first_quarter": ("Premier quartier", "mdi:moon-first-quarter", "La lune marque le premier quart…"),
    "waxing_gibbous": ("Gibbeuse croissante", "mdi:moon-waxing-gibbous", "La lune grossit vers la pleine lumière…"),
    "full_moon": ("Pleine lune", "mdi:moon-full", "La lune brille de tout son éclat…"),
    "waning_gibbous": ("Gibbeuse décroissante", "mdi:moon-waning-gibbous", "La lune décroît…"),
    "last_quarter": ("Dernier quartier", "mdi:moon-last-quarter", "La moitié de la lune s’efface…"),
    "waning_crescent": ("Dernier croissant", "mdi:moon-waning-crescent", "Un dernier croissant s’éteint…"),
}
