#!/usr/bin/python
# -*- coding: utf-8 -*-

# C'EST CLASSE SERVE AU MODEL POUR GARDER UNE LOG
# DES DIFFÉRENTS ÉVÈNEMENTS DU JEU
# CES NOTIFICATIONS SERONT UTILISÉES POUR
# AVERTIR LE JOUEUR DU DÉROULEMENT D'UN ANNÉE


class Affrontement:
    def __init__(self, anneeCourante, planete, attaquant, defenseur, isDefenseReussie):
        self.planete = planete
        self.attaquant = attaquant
        self.defenseur = defenseur
        self.isDefenseReussie = isDefenseReussie
        self.annee = anneeCourante


class Annihilation:
    def __init__(self, anneeCourante, race):
        self.race = race
        self.annee = anneeCourante