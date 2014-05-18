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

    def gererFlotte(self, flotte, listeNotif, anneeCourante):
        """ Gere une flotte arrivant en territoire de la planete """

        if flotte.civilisation == Races.HUMAIN:
            self.nbVisites += 1

        if flotte.civilisation == self.civilisation:
            self.accueillirFlotte(flotte)
        else:
            self.seDefendre(flotte, listeNotif, anneeCourante)


    def accueillirFlotte(self, flotte):
        """ Accueille un flotte [amie] au sein de ses rangs """
        self.nbVaisseaux += flotte.nbVaisseaux

    def seDefendre(self, flotte, listeNotif, anneeCourante):
        """ Se défend contre une flotte d'envahisseur"""
        notif = Affrontement(anneeCourante, self, flotte.civilisation, self.civilisation, False)

        effetSurprise = False
        attaquants = flotte.nbVaisseaux
        defenseurs = self.nbVaisseaux

        if defenseurs > 0:
            probSurprise = self.calculEffetSurprise(defenseurs, attaquants)*100

            rnd = random.randrange(0, 1+100)
            if 0 <= rnd < probSurprise:
                effetSurprise = True
                attaquants, defenseurs = defenseurs, attaquants



            while attaquants > 0 and defenseurs > 0:
                rand = random.randrange(0, 10)
                if 0 <= rand <= 7:  # Victoire du defenseur
                    attaquants -= 1
                else:  # Victoire de l'attaquant
                    defenseurs -= 1

            if effetSurprise:  # Rétablir les camps si effet surprise
                attaquants, defenseurs = defenseurs, attaquants

            self.nbVaisseaux = defenseurs
            flotte.nbVaisseaux = attaquants

        if flotte.nbVaisseaux > self.nbVaisseaux:
            self.nbVaisseaux = flotte.nbVaisseaux
            self.civilisation = flotte.civilisation
            self.isPlaneteMere = False
            isDefenseReussie = False
        else:
            isDefenseReussie = True

        notif.isDefenseReussie = isDefenseReussie
        listeNotif.append(notif)

    def produireVaisseaux(self):
        """Produit des vaisseaux selon le nombre de manufactures """
        self.nbVaisseaux += self.nbManufactures

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


