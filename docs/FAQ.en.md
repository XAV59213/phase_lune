# FAQ

**The moon image does not show.**
- Check the files are in `config/www/moon_phases/` (not `custom_components`).
- Exact lowercase names, `.png` extension (e.g. `waning_gibbous.png`).
- Restart HA if the `www` folder was just created.
- Test the URL `http://<ha>:8123/local/moon_phases/full_moon.png`.
- Clear the browser / app cache.

**I want the state in English.** Use `sensor.moon_phase` (slug such as `full_moon`); `sensor.phase_de_la_lune` gives the French label.

**Is an internet connection needed?** No, computation is 100% local.

**Can it be installed twice?** No, single instance.
