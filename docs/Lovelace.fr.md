# Carte Lovelace

## Carte markdown sombre
```yaml
type: markdown
card_mod:
  style: |
    ha-card { background: #0b1020; color: #e8e8f0; text-align: center; }
content: |
  <img src="/phase_lune/moon_phases/{{ states('sensor.moon_phase') }}.png" width="200">

  ## Phase actuelle : {{ states('sensor.phase_de_la_lune') }}

  *{{ state_attr('sensor.phase_de_la_lune','poetic') }}*

  Illumination : {{ state_attr('sensor.phase_de_la_lune','illumination') }} %
```
`card_mod` est optionnel (installable via HACS).

## Carte entité simple
```yaml
type: entities
entities:
  - sensor.phase_de_la_lune
  - type: attribute
    entity: sensor.phase_de_la_lune
    attribute: illumination
    name: Illumination (%)
```
