# Jeu de la vie avancé

## Table des matières
- [Jeu de la vie avancé](#jeu-de-la-vie-avancé)
  - [Table des matières](#table-des-matières)
  - [Description](#description)
  - [Packages utilisés](#packages-utilisés)
  - [Paramètres](#paramètres)
  - [Règles](#règles)
  - [Créatures](#créatures)
  - [Installation \& exécution](#installation--exécution)

## Description

Ce projet est une version avancée du Jeu de la vie. Un jeu créé pour observer le comportement et les instincts naturels des espèces.

## Packages utilisés

- Tkinter

## Paramètres

Chaque espèce est décrite par un ensemble de paramètres modulables. Ces paramètres influencent le comportement, la survie et les interactions entre espèces.

- Nom
  - Identifiant lisible de l'espèce.

- Vitalité / Énergie
  - Valeur actuelle et valeur maximale (ex. 0–100).
  - Impact :
    - Comportement (plus ou moins agressif selon niveau).
    - Capacité à chasser/fuir.
    - Taux d'épuisement à l'effort.
  - Récupération :
    - Récupération passive par repos.
    - Récupération active par alimentation.

- Métabolisme
  - Consommation d'énergie par unité de temps (ex. points/min).
  - Influence la vitesse à laquelle la nourriture est consommée et la nécessité de rechercher de la nourriture.

- Alimentation
  - Type de régime : herbivore / carnivore / omnivore / nécrophage.
  - Types de nourriture préférés (plantes, petits animaux, carcasses, etc.).
  - Capacité de stockage : quantité maximale de nourriture avant surpoids.
  - Effets du surpoids :
    - Réduction de la vitesse, augmentation de la vulnérabilité.
    - Perte graduelle de points si la nourriture excède la capacité.
  - Durée de survie sans nourriture (temps avant perte critique de vitalité).

- Vitesse et locomotion
  - Vitesse de base (cases/tick).
  - Vitesse selon le milieu (coefficients par type de terrain : eau, forêt, plaine, montagne).
  - Vitesse influencée par l'état (fatigue, surpoids, blessure).
  - Capacité à voler (booléen + paramètres si vrai) :
    - Altitude maximale, consommation d'énergie en vol, vitesse de vol.
    - Restrictions (obstacles, conditions météo, terrains interdits).
    - Avantages : ignore certains obstacles, meilleur repérage.

- Sens et perception
  - Champ de vision (distance en cases).
  - Angle de vision (ex. 360° pour certains, 120° pour d'autres).
  - Sensibilité aux sons/odeurs (détection à distance des proies/prédators).
  - Précision de détection (probabilité de repérer une cible).

- Taille et masse
  - Influence la capacité à attaquer/être attaqué, la vitesse et la consommation d'énergie.
  - Détermine quelles proies peuvent être chassées/consommées.

- Comportement social
  - Territorialité (territoire défini ou nomade).
  - Sociabilité (solitaire, groupe, meute).
  - Coopération en chasse, partage de nourriture, protection mutuelle.

- Reproduction
  - Age de maturité sexuelle.
  - Fréquence / cooldown de reproduction.
  - Taille de la portée.
  - Conditions nécessaires (énergie minimale, proximité d'un partenaire, saison).
  - Hérédité/mutation : probabilité de variations aléatoires des paramètres chez les descendants.

- Défense et attaque
  - Force d'attaque (dommages).
  - Résistance/défense (réduction de dégâts).
  - Comportements d'évitement (fuite) vs confrontation (attaque).
  - Initiation d'agression dépendante de l'énergie, faim et taille relative de la cible.

- Cycle de vie et vieillissement
  - Espérance de vie / durée de vie maximale.
  - Dégradation progressive des capacités avec l'âge (vitesse, vision, fertilité).
  - Mort naturelle vs mort par prédation/famine.

- Comportements spécifiques / IA
  - Priorités (ex. survie > reproduction > exploration).
  - Stratégies de recherche de nourriture (patrouille, affût, poursuite).
  - Évasion (distance de fuite, manœuvres).
  - Comportement d'apprentissage ou adaptation si souhaité (mémoire d'emplacements riches en nourriture).

- Variables environnementales influentes
  - Sensibilité au climat (froid/chaleur) : effet sur vitalité et comportement.
  - Effet de la météo sur vol (vent, pluie) si vol implémenté.
  - Disponibilité saisonnière de ressources.

- Paramètres techniques / gameplay
  - Priorité CPU : fréquence de mise à jour par espèce (pour optimiser perf).
  - Valeurs par défaut recommandées et plages acceptables pour l'équilibrage.
  - Identifiants pour la sauvegarde/chargement d'instances.

Exemple résumé d'une fiche d'espèce (suggestion de structure JSON) :
- name: "Nom"
- max_health: 100
- energy: 100
- metabolism: 1.2
- diet: ["plants", "small_animals"]
- food_capacity: 30
- starvation_time: 300
- base_speed: 1.0
- terrain_speed: {plaine:1.0, foret:0.8, eau:0.2}
- can_fly: true
- fly_speed: 2.0
- vision_range: 6
- social: "meute"
- reproduction: {maturity:50, cooldown:120, litter:3}
- aggression: 0.4
- lifespan: 200

Ces paramètres permettent de créer des espèces variées (volantes ou non), équilibrer interactions et simuler un écosystème riche et dynamique.

## Règles

- Toutes les espèces ont un niveau de nourriture maximal
  - Si elle mange quelque chose, elle gagne des points de nourriture.
  - Si elle arrive à 0 point de nourriture :
    - Si la créature était en surpois, elle perds progressivement ces points de surpoids en même temps que sa vitalité.
    - Si ce n'est pas le cas alors elle ne perds que sa vitalité.

## Créatures

|Nom|Vitalité|Nourriture|
|---|--------|----------|
|Herbivore # 1|5|20|

## Installation & exécution