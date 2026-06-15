---
name: Bug Report / Signalement de bug
description: Report a bug or signaler un bug dans l'intégration MyLight150
title: "[BUG] <short description / description courte>"
labels: ["bug", "triage"]
assignees: ""
---

body:
  - type: markdown
    attributes:
      value: |
        **English:** Please check if the bug has already been reported before creating a new issue.
        **Français:** Merci de vérifier que le bug n'a pas déjà été signalé avant de créer une nouvelle issue.

  - type: input
    id: ha_version
    attributes:
      label: Home Assistant Version / Version de Home Assistant
      description: Example: 2024.6.3 / Exemple : 2024.6.3
      placeholder: 2024.x.x
    validations:
      required: true

  - type: input
    id: integration_version
    attributes:
      label: MyLight150 Integration Version / Version de l'intégration MyLight150
      description: Installed version (via HACS or manual) / Version installée (via HACS ou manuelle)
      placeholder: v1.0.0
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description / Description du bug
      description: |
        **English:** Clearly describe the issue, steps to reproduce, and expected behavior.
        **Français:** Décrivez clairement le problème, les étapes pour le reproduire, et le comportement attendu.
      placeholder: |
        **English:**
        1. Go to Settings > Devices & Services
        2. Add MyLight150 integration
        3. ...
        **Français:**
        1. Aller dans Paramètres > Appareils et services
        2. Ajouter l'intégration MyLight150
        3. ...

  - type: textarea
    id: logs
    attributes:
      label: Relevant Logs / Logs pertinents
      description: |
        **English:** Paste filtered log extracts (use the "Filter" button in HA logs) to avoid sensitive info. Use backticks (```) for formatting.
        **Français:** Collez les extraits de logs **filtrés** (via le bouton "Filter" dans les logs HA) pour éviter les infos sensibles. Utilisez des backticks (```) pour formater le code.
      placeholder: |
        ```
        2024-06-15 10:00:00 ERROR (MainThread) [custom_components.mylight150] ...
        ```

  - type: dropdown
    id: severity
    attributes:
      label: Severity / Sévérité
      options:
        - "Minor (cosmetic, UI) / Mineure (cosmétique, UI)"
        - "Moderate (partial functionality) / Modérée (fonctionnalité partielle)"
        - "Critical (total blockage) / Critique (blocage total)"
    validations:
      required: true