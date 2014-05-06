#!/usr/bin/python
# -*- coding: utf-8 -*-
from ModeCzin import *
from Races import *

class Czin:
    def __init__(self, parent):
        self.parent = parent
        self.nbr_vaisseaux_par_attaque = 4
        self.force_attaque_basique = 20
        self.mode = Mode.RASSEMBLEMENT_FORCES
        self.valeur_grappe = []
        self.distance_grappe = 4
        self.valeur_base = []
        self.base = None
        self.planeteMere = None
        self.baseOrigine = None
        self.grappeEnCours = []
        self.tempsConquete = None
        
    def initialiserValeurGrappe(self):
        #initialise les valeurs grappe a 0 puis les calcule
        for n in range(0, len(self.parent.listePlanetes)):
            self.valeur_grappe.append(0)

        for n in range(0, len(self.parent.listePlanetes)):
            for i in range(0, len(self.parent.listePlanetes)):
                if self.parent.calculerDistance(self.parent.listePlanetes[n], self.parent.listePlanetes[i]) <= self.distance_grappe:
                    self.valeur_grappe[n] += (self.distance_grappe - self.parent.calculerDistance(self.parent.listePlanetes[n], self.parent.listePlanetes[i]) + 1)**2


    def determinerGrappe(self):
        #determine les valeur bases
        for n in range(0, len(self.parent.listePlanetes)):
            if self.valeur_grappe[n] == 0:
                self.valeur_base.append(0)
            else:
                self.valeur_base.append(self.valeur_grappe[n]-3*self.parent.calculerDistance(self.base, self.parent.listePlanetes[n]))

    def determinerBase(self):
        if self.baseOrigine == None:
            self.baseOrigine = self.planeteMere
        else:
            self.baseOrigine = self.base
        valeurMax = 0
        self.grappeEnCours.clear()
        indexPlanete = None
        for n in range(0,len(self.valeur_base)):
            if valeurMax < self.valeur_base[n] and self.parent.listePlanetes[indexPlanete].civilisation != Races.Czin:
                valeurMax = self.valeur_base[n]
                indexPlanete = n

        self.base = self.parent.listePlanetes[indexPlanete]

    #TODO : comprendre comment mettre le tout ensemble

    def forceAttaque(self):
        return self.parent.tempsCourant * self.nbr_vaisseaux_par_attaque * self.force_attaque_basique

    def choixProchainePlaneteGrappe(self):
        max = 200000000000
        planeteChoisie = None
        for planete in self.parent.listePlanetes:
            flotteEnCours = False
            for flotte in self.parent.listeFlottes:
                if flotte.planeteArrivee == planete:
                    flotteEnCours = True
            if self.parent.calculerDistance(self.base, planete) <=max and not flotteEnCours:
                max = self.parent.calculerDistance(self.base, planete)
                planeteChoisie = planete

        return planeteChoisie



    def choixMode(self):
        if self.mode == Mode.RASSEMBLEMENT_FORCES:
            self.modeRassemblementForces()

        if self.mode == Mode.ETABLIR_BASE:
            self.modeEtablirBase()

        if self.mode == Mode.CONQUERIR_GRAPPE:
            self.modeConquerirGrappe()


    def modeEtablirBasee(self):
        if self.base.civilisation == Races.Czin:
            self.mode = Mode.CONQUERIR_GRAPPE
            for planete in self.parent.listePlanetes:
                if self.parent.calculerDistance(self.base, planete)<=self.distance_grappe:
                    self.grappeEnCours.append(planete)

            while self.baseOrigine.nbVaisseaux >= self.forceAttaque():
                self.parent.ajoutFlotte(self.base, self.choixProchainePlaneteGrappe, Races.Czin, self.parent.calculerDistance(self.base, self.choixProchainePlaneteGrappe))
            self.tempsConquete = self.parent.tempsCourant
            for n in range(0, len(self.grappeEnCours)):
                if self.parent.calculerDistance(self.base, self.choixProchainePlaneteGrappe) > self.tempsConquete:
                    self.tempsConquete += self.parent.calculerDistance(self.base, self.choixProchainePlaneteGrappe)

        else:
            self.mode = Mode.RASSEMBLEMENT_FORCES

    def modeRassemblementForces(self):
        if self.base.nbVaisseaux == 3*self.forceAttaque():
            self.parent.ajoutFlotte(self.baseOrigine, self.base, Races.Czin, 3*self.forceAttaque(), self.parent.calculerDistance(self.base, self.baseOrigine))
            self.mode = Mode.ETABLIR_BASE

    def modeConquerirGrappe(self):
        resteFlottes = False
        for flotte in self.parent.listeFlottes:
            if flotte.civilisation == Races.CZIN:
                resteFlottes = True

        if resteFlottes:
            self.mode = Mode.RASSEMBLEMENT_FORCES
