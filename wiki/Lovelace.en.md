# Lovelace card

## Dark markdown card
```yaml
type: markdown
card_mod:
  style: |
    ha-card { background: #0b1020; color: #e8e8f0; text-align: center; }
content: |
  <img src="/local/moon_phases/{{ states('sensor.moon_phase') }}.png" width="200">

  ## Current phase: {{ states('sensor.phase_de_la_lune') }}

  *{{ state_attr('sensor.phase_de_la_lune','poetic') }}*

  Illumination: {{ state_attr('sensor.phase_de_la_lune','illumination') }} %
```
`card_mod` is optional (installable via HACS). The phase label and poetic text are in French; use `states('sensor.moon_phase')` for the English slug.

## Simple entities card
```yaml
type: entities
entities:
  - sensor.moon_phase
  - sensor.phase_de_la_lune
  - type: attribute
    entity: sensor.phase_de_la_lune
    attribute: illumination
    name: Illumination (%)
```
