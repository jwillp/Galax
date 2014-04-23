#!/usr/bin/python
# -*- coding: utf-8 -*-


class Planete:
    def __init__(self, x, y, nbManufactures):
        self.nom = None
        self.civilisation = None  # quelle civilisation occupe cette planete (humain, Czins, Gubru ou non-colonisateurs)
        self.isPlaneteMere = False  # booleen si cette planete est  planete mèr4e des civilisations colonisatrices
        self.posX = x  # coordonnee x d'une planete
        self.posY = y  # coordonnee y d'une planete
        self.nbManufactures = nbManufactures  # nombre de manufactures de vaisseaux (1 a 6 actives sur la planete)
        self.nbVisites = 0  # nombre de fois que l'humain a visite cette planete
        self.nbVaisseaux = self.nbManufactures  # nombre de vaisseaux que possede la planete


    def seDefendre(self, flotte):
        pass