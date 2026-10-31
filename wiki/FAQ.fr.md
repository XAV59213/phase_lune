# FAQ

**L'image de la lune ne s'affiche pas.**
- Vérifier que les fichiers sont dans `config/www/moon_phases/` (pas `custom_components`).
- Noms exacts en minuscules, extension `.png` (ex. `waning_gibbous.png`).
- Redémarrer HA si le dossier `www` vient d'être créé.
- Tester l'URL `http://<ha>:8123/local/moon_phases/full_moon.png`.
- Vider le cache du navigateur / de l'app.

**L'état est en anglais.** Utiliser `sensor.phase_de_la_lune` pour le libellé FR ; `sensor.moon_phase` reste en slug pour les images.

**Faut-il une connexion internet ?** Non, le calcul est 100 % local.

**Peut-on l'installer deux fois ?** Non, instance unique.
