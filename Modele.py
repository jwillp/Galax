#!/usr/bin/python
# -*- coding: utf-8 -*-
from decimal import Decimal
import random
import math
from Planete import *
from Flotte import *
from Gubru import *
from Czin import *
from Races import *


class Modele:
    """ Gestionnaire des données du programme """

    def __init__(self, tailleX, tailleY, nombrePlanetes):
        # Taille de la logique en terme de positions
        self.tailleX = tailleX
        self.tailleY = tailleY

        self.anneeCourante = 0


        # Données planètes
        self.nombreInitialPlanetes = nombrePlanetes  # NombreInitial de planète
        self.nomPlanetes = []  # Une liste contenant tous les noms attribuables aux planètes
        self.planetes = []  # Une liste contenant toutes les planetes
        self.planeteSelectionnee = None
        self.planeteSelectionnee2 = None

        self.flottes = []  # Une liste contenant toutes les flottes

        # Civilisation
        self.gubru = Gubru(self)
        self.czin = Czin(self)

        self.notifications = []

    def chargerNomPlanetes(self):
        fichier = open('noms_planetes.data', 'r')
        self.nomPlanetes = fichier.readlines()
        fichier.close()

    def obtenirNom(self):
        return random.choice(self.nomPlanetes)

    # INITIALISATION DES PLANETES

    def creerPlanetes(self):
        """Initialise toutes les planetes """
        self.chargerNomPlanetes()

        positionsPossibles = []
        for y in range(0, self.tailleY):
            for x in range(0, self.tailleX):
                positionsPossibles.append((x, y))  # Ajout d'un tuple

        for n in range(0, self.nombreInitialPlanetes):
            # On choisit une position au hasard et on l'enlève des positions possibles
            pos = random.choice(positionsPossibles)
            positionsPossibles.remove(pos)

            x = pos[0]
            y = pos[1]
            nbManufactures = random.randrange(0, 7)  # entre 0 et 6
            nom = self.obtenirNom()

            self.planetes.append(Planete(x, y, nbManufactures, nom))

        self.determinerPlaneteMere(Races.HUMAIN)
        self.determinerPlaneteMere(Races.GUBRU)
        self.determinerPlaneteMere(Races.CZIN)
        self.initialiserPlanetesIndependantes()

    def determinerPlaneteMere(self, race):
        """Attribu une planete mere aleatoirement a une race"""
        planete = random.choice(self.planetes)
        if planete.civilisation:
            self.determinerPlaneteMere(race)
        else:
            planete.isPlaneteMere = True
            planete.civilisation = race
            planete.nbManufactures = 10
            planete.nbVaisseaux = 100

    def initialiserPlanetesIndependantes(self):
        """Initialise les planetes independantes"""
        for planete in self.planetes:
            if not planete.civilisation:
                planete.civilisation = Races.INDEPENDANT

    def ajouterFlotte(self, planeteDepart, planeteArrivee, civilisation, nbVaisseaux):
        """Permet d'ajouter une flotte au modele """
        self.flottes.append(Flotte(planeteDepart, planeteArrivee, civilisation, nbVaisseaux, self.anneeCourante,
                                   self.anneeCourante + self.calculerDistance(planeteDepart, planeteArrivee)))
        planeteDepart.nbVaisseaux -= nbVaisseaux

    def arriveeFlottes(self):
        """ Verifie l'arrivee des flottes et les supprimes le cas échéant """

        for flotte in self.flottes:
            if round(flotte.anneeArrivee, 1) == round(self.anneeCourante, 1):

                flotte.planeteArrivee.gererFlotte(flotte, self.notifications, self.anneeCourante)
                self.flottes.remove(flotte)


    @staticmethod
    def calculerDistance(planeteDepart, planeteArrivee):
        """ Calcul le temps de déplacement nécessaire entre deux planètes """
        if not planeteDepart or not planeteArrivee:
            return 0
        #calcule le temps de deplacement comme si la distance est l'hypothenuse d'un triangle rectangle et arrondit a
        # une decimale
        distanceX = (planeteArrivee.posX - planeteDepart.posX) ** 2
        distanceY = (planeteArrivee.posY - planeteDepart.posY) ** 2
        distanceFinale = math.sqrt(distanceX + distanceY)
        return round(distanceFinale, 1)

    def avancerTemps(self):
        #fait les taches d'une annee complete sans inclure les actions humaines
        if self.isRaceVivante(Races.GUBRU):
            self.gubru.jouer()

        if self.isRaceVivante(Races.CZIN):
            pass
            #self.czin.creerFlottes()

        for n in range(10):
            self.arriveeFlottes()
            self.anneeCourante += 0.1

        for planete in self.planetes:
            planete.produireVaisseaux()

    # Méthode de Récupération
    def getPlaneteAt(self, posX, posY):
        """ Retourne une planete a une coordonnée donnée """
        planeteRetour = None
        for planete in self.planetes:
            if planete.posX == posX and planete.posY == posY:
                planeteRetour = planete

        return planeteRetour

    def getNbPlanetesRace(self, race):
        """ Retourne une liste contenant toutes les planetes d'une race """
        nombre = 0
        for planete in self.planetes:
            if planete.civilisation == race:
                nombre += 1
        return nombre

    def getPlanetesRace(self, race):
        """ Retourne une liste des planete pour une race """
        planetesRace = []
        for planete in self.planetes:
            if planete.civilisation == race:
                planetesRace.append(planete)
        return planetesRace

    def getPlanetesNonRace(self, race):
        """ Retourne une liste des planetes qui n'appartiennent pas à une race """
        planetesRace = []
        for planete in self.planetes:
            if planete.civilisation != race:
                planetesRace.append(planete)
        return planetesRace

    def getPlaneteMereRace(self, race):
        """ Retourne la planete mere d'une race """
        for planete in self.planetes:
            if planete.civilisation == race and planete.isPlaneteMere:
                    return planete
        return None

    def getFlotteRace(self, race):
        """ Retourne les flottes d'une race """
        flotteRace = []
        for flotte in self.flottes:
            if flotte.civilisation == race:
                flotteRace.append(flotte)
        return flotteRace

    def isRaceVivante(self, race):
        """Renvoie true si une race possède encore une planete ou une flotte """
        for planete in self.planetes:
            if planete.civilisation == race:
                return True  # Il reste des planetes

        for flotte in self.flottes:
            if flotte.civilisation == race:
                return True  # Il reste des flottes

        return False  # Il ne reste plus rien