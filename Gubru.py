#!/usr/bin/python
# -*- coding: utf-8 -*-
import operator
from Flotte import Flotte
from Modele import Modele
from Races import *


class Gubru:
    FORCE_ATTAQUE_BASIQUE = 10
    NBR_VAISSEAUX_PAR_ATTAQUE = 5

    def __init__(self, modele):
        self.modele = modele
        self.listePlanetesAttaquees = []

    @staticmethod
    def forceAttaque(anneeCourante):
        """ Calcul la force d'attaque des GUBRU """
        force1 = anneeCourante * Gubru.NBR_VAISSEAUX_PAR_ATTAQUE + Gubru.FORCE_ATTAQUE_BASIQUE
        force2 = Gubru.FORCE_ATTAQUE_BASIQUE * 2
        if force1 > force2:
            return force1
        else:
            return force2

    def jouer(self):
        planeteMere = self.modele.getPlaneteMereRace(Races.GUBRU)
        puissanceAttaque = self.forceAttaque(self.modele.anneeCourante) + Gubru.FORCE_ATTAQUE_BASIQUE

        if not planeteMere:
            self.choisirNouvellePlaneteMere()

        if planeteMere.nbVaisseaux > puissanceAttaque:
            self.creerFlottesAssaut(puissanceAttaque)

        self.rapatrierFlottes()




    def creerFlottesAssaut(self, puissanceAttaque):
        """ Gere la formation des flottes des gubrus """

        for planete in self.getPlanetesProches():
            if not self.isFlotteTrajectoire(self.getPlaneteMere(), planete):
                self.modele.ajouterFlotte(self.getPlaneteMere(), planete, Races.GUBRU, puissanceAttaque)

    def rapatrierFlottes(self):
        """ Rapatrie les flottes selon la logique Gubru """
        planetes = self.getPlanetes()
        planetes.remove(self.getPlaneteMere())  # Retirer la planete mere (rapatrier mere vers mere == illogique)

        for planete in planetes:
            if planete.nbVaisseaux > 25:
                # A-t-on deja rapatrie une flotte?
                if not self.isFlotteTrajectoire(planete, self.getPlaneteMere()):
                    vaisseauxRapatrier = 25 - 15
                    self.modele.ajouterFlotte(planete, self.getPlaneteMere(), Races.GUBRU, vaisseauxRapatrier)

    def isFlotteTrajectoire(self, planeteDepart, planeteArrivee):
        """ Retourne true si une flotte à la trajectoire de planeteDepart vers planeteArrivee
        :type planeteDepart: Planete
        :type planeteArrivee: Planete
        """
        for flotte in self.modele.getFlotteRace(Races.GUBRU):
            if planeteDepart == flotte.planeteDepart and planeteArrivee == flotte.planeteArrivee:
                return True
        return False



    def choisirNouvellePlaneteMere(self):
        """ Permet de choisir une nouvelle planete mere """
        planeteMere = self.getPlanetes()[-1]
        planeteMere.isPlaneteMere = True

    # MÉTHODES DE RÉCUPÉRATION #

    def getPlanetesProches(self):
        """ Retourne une liste des planetes les plus proches non Gubru """
        NB_PLANETES = 4  # Le nombre de planete les plus proches
        planetesNonGubru = self.modele.getPlanetesNonRace(Races.GUBRU)
        planetesProximite = []

        for planete in self.modele.getPlanetesNonRace(Races.GUBRU):
            distance = self.modele.calculerDistance(self.getPlaneteMere(), planete)
            planetesProximite.append((planete, distance))

        planetesProximite = sorted(planetesProximite, key=operator.itemgetter(1))

        planetes = []
        for tup in planetesProximite:
            planetes.append(tup[0])

        return planetes[:NB_PLANETES]

    def getPlaneteMere(self):
        return self.modele.getPlaneteMereRace(Races.GUBRU)

    def getPlanetes(self):
        return self.modele.getPlanetesRace(Races.GUBRU)
