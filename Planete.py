#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import Modele
from Notification import Affrontement
from Races import Races


class Planete:
    def __init__(self, x, y, nbManufactures, nom):

        self.nom = nom
        self.civilisation = None  # quelle civilisation occupe cette planete (humain, Czins, Gubru ou non-colonisateurs)
        self.isPlaneteMere = False  # booleen si cette planete est  planete mèr4e des civilisations colonisatrices
        self.posX = x  # coordonnee x d'une planete
        self.posY = y  # coordonnee y d'une planete
        self.nbManufactures = nbManufactures  # nombre de manufactures de vaisseaux (1 a 6 actives sur la planete)
        self.nbVisites = 0  # nombre de fois que l'humain a visite cette planete
        self.nbVaisseaux = self.nbManufactures  # nombre de vaisseaux que possede la planete


    def seDefendre(self, flotte, listeNotif, anneeCourante):

        if flotte.civilisation == Races.HUMAIN:
            self.nbVisites += 1

        effetSurprise = False
        attaquants = flotte.nbVaisseaux
        defenseurs = self.nbVaisseaux

        if defenseurs > 0:
            probSurprise = self.calculEffetSurprise(defenseurs, attaquants)*100

            rnd = random.randrange(0, 100)
            if 0 <= rnd < probSurprise:
                effetSurprise = True
                attaquants, defenseur = defenseurs, attaquants

                indexAttanquant = attaquants
                indexDefenseur = defenseurs

                while attaquants != 0 and defenseurs != 0:
                    rand = random.randrange(0, 10)
                    if 0 <= rand <= 7:  # Victoire du defenseur
                        indexAttanquant -= 1
                    else:  # Victoire de l'attaquant
                        indexDefenseur -= 1

                if effetSurprise:
                    attaquants, defenseur = defenseurs, attaquants

                self.nbVaisseaux = defenseurs
                flotte.nbVaisseaux = attaquants

        if flotte.nbVaisseaux > self.nbVaisseaux:
            self.nbVaisseaux = flotte.nbVaisseaux
            self.civilisation = flotte.civilisation
            isDefenseReussie = False
        else:
            isDefenseReussie = True

        #TODO notification de affrontement selon issue du combat
            notif = Affrontement(anneeCourante, self, flotte.civilisation, self.civilisation, isDefenseReussie)
            listeNotif.append(notif)





    @staticmethod
    def calculEffetSurprise(nbDefenseurs, nbEnvahisseurs):
        r = nbDefenseurs / nbEnvahisseurs
        if r < 5:
            p = r/10
        elif r < 20:
            p = (3*r + 35) / 100
        else:
            p = 0.95

        return p

