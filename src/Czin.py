#!/usr/bin/python
# -*- coding: utf-8 -*-

from Races import *

from Enum import *

import operator

class Mode:
    RASSEMBLEMENT_FORCES = Enum.addId()
    ETABLIR_BASE = Enum.addId()
    CONQUERIR_GRAPPE = Enum.addId()





class Czin:
    DISTANCE_GRAPPE = 10
    NB_VAISSEAUX_PAR_ATTAQUE = 4
    FORCE_ATTAQUE_BASIQUE = 20

    def __init__(self, modele):

        self.modele = modele
        self.mode = Mode.ETABLIR_BASE
        self.grappe = []
        self.base = self.getPlaneteMere()

    def jouer(self):

        if not self.getPlaneteMere():
            self.determinerNouvellePlaneteMere()

        self.gererModes()





    def forceAttaque(self):
        """ Calcul la force d'attaque des Czins """
        return self.modele.anneeCourante * Czin.NB_VAISSEAUX_PAR_ATTAQUE * Czin.FORCE_ATTAQUE_BASIQUE


    # GESTION DES MODES #

    def gererModes(self):
        if self.mode == Mode.RASSEMBLEMENT_FORCES:
            self.gererModeRassemblement()

        elif self.mode == Mode.ETABLIR_BASE:
            self.gererModeEtablirBase()

        elif self.mode == Mode.CONQUERIR_GRAPPE:
            self.gererModeConquerirGrappe()



    def gererModeRassemblement(self):
        """ Gestion du mode Rassemblement de force """
        # S'il reste uniquement la base Centrale
        if self.base:
            if self.grappe.baseCentrale.nbVaisseaux >= 6:

                if not self.isFlotteTrajectoire(self.grappe.baseCentrale, self.getPlaneteMere()):
                    self.modele.ajouterFlotte(self.grappe.baseCentrale, self.getPlaneteMere(), Races.CZIN,
                                              self.grappe.baseCentrale.nbVaisseaux - 3)

            elif self.grappe.baseCentrale.nbVaisseaux >= 3 * self.forceAttaque():
                self.mode = Mode.ETABLIR_BASE


    def gererModeEtablirBase(self):
        if not self.grappe:
            self.determinerGrappe()
            self.determinerBaseGrappe()

        elif self.grappe.baseCentrale:
            self.mode = Mode.CONQUERIR_GRAPPE


    def gererModeConquerirGrappe(self):
        for planete in self.modele.getPlanetesNonRace(Races.CZIN):
            if planete.civilisation != Races.CZIN and self.modele.calculerDistance(planete, self.grappe.baseCentrale) <= Czin.DISTANCE_GRAPPE:
                if not self.isFlotteTrajectoire(self.grappe.baseCentrale, planete):
                    self.modele.ajouterFlotte(self.grappe.baseCentrale, planete, Races.CZIN, self.forceAttaque())

        self.mode = Mode.RASSEMBLEMENT_FORCES




    def determinerGrappe(self):
        """ Détermine une grappe """

        for planete in self.modele.planetes:
            planete.valeurGrappe = 0

        for i in self.modele.getPlanetesNonRace(Races.CZIN):
            for j in self.modele.getPlanetesNonRace(Races.CZIN):
                if i != j:
                    distance = self.modele.calculerDistance(i, j)
                    if distance <= Czin.DISTANCE_GRAPPE:
                        s = Czin.DISTANCE_GRAPPE - distance + 1
                        j.valeurGrappe += s * s


    def determinerBaseGrappe(self):
        max = 0
        base = None
        for planete in self.modele.planetes:
            if planete.valeurGrappe == 0:
                planete.valeurBase = 0
            else:
                planete.valeurBase = planete.valeurGrappe - 3 * self.modele.calculerDistance(planete,
                                                                                             self.base)
            if planete.valeurBase >= max:
                base = planete

        self.base = base





    def determinerNouvellePlaneteMere(self):
        """ Permet de déterminer une planete mère """
        if self.base:
            self.base.isMere = True
        else:
            self.getPlanetes()[-1].isMere = True


    # MÉTHODES DE RÉCUPÉRATION #

    def getPlaneteMere(self):
        return self.modele.getPlaneteMereRace(Races.CZIN)

    def getPlanetes(self):
        return self.modele.getPlanetesRace(Races.CZIN)

    def getPlanetesProches(self, planeteCible):
        """ Retourne une liste des planetes les plus proches non Gubru """
        planetes = []

        for planete in self.modele.getPlanetesNonRace(Races.CZIN):
            distance = self.modele.calculerDistance(planeteCible, planete)
            planetes.append((planete, distance))

        planetes = sorted(planetes, key=operator.itemgetter(1))

        planetesProximite = []
        for tup in planetes:
            planetesProximite.append(tup[0])

        return planetesProximite



    def isFlotteTrajectoire(self, planeteDepart, planeteArrivee):
        """ Retourne true si une flotte à la trajectoire de planeteDepart vers planeteArrivee
        :type planeteDepart: Planete
        :type planeteArrivee: Planete
        """
        for flotte in self.modele.getFlotteRace(Races.CZIN):
            if planeteDepart == flotte.planeteDepart and planeteArrivee == flotte.planeteArrivee:
                return True
        return False
