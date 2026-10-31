"""Constantes pour l'intégration Phase de la Lune."""
DOMAIN = "phase_lune"
NAME = "Phase de la Lune"
VERSION = "1.2.4"

URL_BASE = "/phase_lune_frontend"
CARD_FILENAME = "phase-lune-card.js"
CARD_URL = f"{URL_BASE}/{CARD_FILENAME}"

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

# Textes poétiques par phase (FR, EN) — rotation quotidienne.
POETICS = {
    "new_moon": [
        ("La lune se renouvelle dans l’ombre. Temps de poser ses intentions.", "The moon renews in darkness. Time to set intentions."),
        ("Nuit sans lune : les étoiles reprennent la scène.", "Moonless night: the stars take the stage."),
        ("Tout recommence en silence. Semez vos projets.", "Everything begins again in silence. Sow your plans."),
        ("Invisible mais présente, la lune prépare son retour.", "Unseen yet present, the moon prepares its return."),
    ],
    "waxing_crescent": [
        ("Un fin croissant apparaît. L’élan des débuts.", "A thin crescent appears. The momentum of beginnings."),
        ("Le croissant sourit au crépuscule. Osez le premier pas.", "The crescent smiles at dusk. Dare the first step."),
        ("La lumière revient doucement. Nourrissez vos envies.", "Light slowly returns. Nurture your desires."),
        ("Petit à petit, la lune se dévoile.", "Little by little, the moon reveals itself."),
    ],
    "first_quarter": [
        ("Premier quartier : moitié d’ombre, moitié de lumière. Temps d’agir.", "First quarter: half shadow, half light. Time to act."),
        ("La lune se dresse comme un arc tendu. Décidez.", "The moon stands like a drawn bow. Decide."),
        ("Les obstacles se montrent pour être franchis.", "Obstacles show up to be overcome."),
        ("À mi-chemin de la pleine lune, gardez le cap.", "Halfway to full moon, hold your course."),
    ],
    "waxing_gibbous": [
        ("La lune grossit vers la pleine lumière. Peaufinez.", "The moon swells toward full light. Refine."),
        ("Presque pleine, elle invite à la patience.", "Almost full, it invites patience."),
        ("Les efforts mûrissent sous une lumière croissante.", "Efforts ripen under growing light."),
        ("Encore un peu : la plénitude approche.", "Just a little more: fullness is near."),
    ],
    "full_moon": [
        ("La lune brille de tout son éclat. Temps de célébrer.", "The moon shines in full glory. Time to celebrate."),
        ("Pleine lune : tout est révélé, rien n’est caché.", "Full moon: everything revealed, nothing hidden."),
        ("Les nuits sont claires, les émotions aussi.", "Nights are bright, and so are emotions."),
        ("Récoltez ce que vous avez semé.", "Harvest what you have sown."),
    ],
    "waning_gibbous": [
        ("La lune décroît. Temps de relâcher et de se recentrer.", "The moon wanes. Time to release and refocus."),
        ("Partagez ce que la pleine lune vous a appris.", "Share what the full moon taught you."),
        ("La lumière recule doucement. Gratitude.", "Light gently recedes. Gratitude."),
        ("Ralentissez : la lune vous montre l’exemple.", "Slow down: the moon leads by example."),
    ],
    "last_quarter": [
        ("La moitié de la lune s’efface. Faites le tri.", "Half the moon fades. Time to sort things out."),
        ("Dernier quartier : pardonner, alléger, conclure.", "Last quarter: forgive, lighten, conclude."),
        ("Ce qui ne sert plus peut partir.", "What no longer serves can go."),
        ("La lune se lève tard. Prenez le temps.", "The moon rises late. Take your time."),
    ],
    "waning_crescent": [
        ("Un dernier croissant s’éteint. Temps du repos.", "A last crescent fades. Time to rest."),
        ("Le croissant de l’aube murmure la fin d’un cycle.", "The dawn crescent whispers a cycle’s end."),
        ("Écoutez le silence avant le renouveau.", "Listen to the silence before renewal."),
        ("Lâchez prise : la nouvelle lune approche.", "Let go: the new moon is coming."),
    ],
}

IMAGES_URL = "/phase_lune/moon_phases"
IMAGES_DIR = "www/moon_phases"

CONF_COUNTRY = "country"
DEFAULT_COUNTRY = "FR"
# Pays -> hémisphère (N/S). Les phases sont identiques partout ; seul l'aspect (côté éclairé) s'inverse au sud.
COUNTRIES = {
    "FR": "N", "BE": "N", "CH": "N", "LU": "N", "MC": "N", "CA": "N", "US": "N",
    "GB": "N", "DE": "N", "ES": "N", "IT": "N", "PT": "N", "NL": "N", "MA": "N",
    "DZ": "N", "TN": "N", "SN": "N", "CI": "N", "GP": "N", "MQ": "N", "GF": "N",
    "RE": "S", "YT": "S", "NC": "S", "PF": "S", "MG": "S", "MU": "S", "AU": "S",
    "NZ": "S", "ZA": "S", "BR": "S", "AR": "S", "CL": "S",
}
MIRROR = {
    "waxing_crescent": "waning_crescent", "waning_crescent": "waxing_crescent",
    "first_quarter": "last_quarter", "last_quarter": "first_quarter",
    "waxing_gibbous": "waning_gibbous", "waning_gibbous": "waxing_gibbous",
}
