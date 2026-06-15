---
name: Feature Request / Demande de fonctionnalité
description: Suggest a new feature or proposer une nouvelle fonctionnalité
title: "[FEAT] <short description / description courte>"
labels: ["enhancement", "triage"]
---

body:
  - type: markdown
    attributes:
      value: |
        **English:** Describe the desired feature and its usefulness for the community.
        **Français:** Décrivez la fonctionnalité souhaitée et son utilité pour la communauté.

  - type: textarea
    id: use_case
    attributes:
      label: Use Case / Cas d'usage
      description: |
        **English:** Why is this feature useful?
        **Français:** Pourquoi cette fonctionnalité est-elle utile ?
        **Example / Exemple:** "Allow real-time solar production data retrieval for Lovelace display."
        / "Permettre de récupérer les données de production solaire en temps réel pour les afficher dans Lovelace."
    validations:
      required: true

  - type: textarea
    id: implementation
    attributes:
      label: Implementation Ideas (Optional) / Idées pour l'implémentation (optionnel)
      description: |
        **English:** If you have technical leads (e.g., API endpoint, sensor type, etc.), share them here.
        **Français:** Si vous avez des pistes techniques (ex: endpoint API, type de capteur, etc.), partagez-les ici.
      placeholder: |
        **English:**
        - Use MyLight150's `/api/v1/solar` endpoint
        - Create a `SensorEntity` with `state_class: measurement`
        **Français:**
        - Utiliser l'endpoint `/api/v1/solar` de MyLight150
        - Créer un capteur de type `SensorEntity` avec l'attribut `state_class: measurement`

  - type: dropdown
    id: priority
    attributes:
      label: Priority (Subjective) / Priorité (subjective)
      options:
        - "Low (nice-to-have) / Basse (nice-to-have)"
        - "Medium / Moyenne"
        - "High (blocking for my use) / Haute (blocant pour mon usage)"