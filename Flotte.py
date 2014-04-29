#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO enlever la valeur par défaut de anneeDepart et l'inverser avec anneeArriver et modifier le modele en conséquence

class Flotte:

    def __init__(self, planeteDepart, planeteArrive, civilisation, nbVaisseaux, anneeArrivee, anneeDepart):
        self.planeteDepart = planeteDepart
        self.planeteArrivee = planeteArrive
        self.civilisation = civilisation
        self.nbVaisseaux = nbVaisseaux
        self.anneeArrivee = anneeArrivee
        self.anneeDepart = anneeDepart



