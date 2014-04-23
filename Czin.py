#!/usr/bin/python
# -*- coding: utf-8 -*-
from ModeCzin import *

class Czin:
    def __init__(self,parent):
        self.parent = parent
        self.nbr_vaisseaux_par_attaque = 4
        self.force_attaque_basique = 20
        self.mode = Mode.RASSEMBLEMENT_FORCES
        self.valeur_grappe = []
        self.distance_grappe = 4
        self.valeur_base = []
        self.base = None
        self.planeteMere = None
        
        def initialiserValeurGrappe(self):
            #initialise les valeurs grappe a 0 puis les calcule
            for n in range(0, len(self.parent.listePlanetes)):
                self.valeur_grappe.append(0)
            
            for n in range(0, len(self.parent.listePlanetes)):
                for i in range(0, len(self.parent.listePlanetes)):
                    if self.parent.tempsDeplacement(self.parent.listePlanetes[n], self.parent.listePlanetes[i]) <= self.distance_grappe:
                        self.valeur_grappe[n] += (self.distance_grappe - self.parent.tempsDeplacement(self.parent.listePlanetes[n], self.parent.listePlanetes[i]) + 1)**2
            
        
        def determinerGrappe(self):
            #determine les valeur bases
            for n in range(0, len(self.parent.listePlanetes)):
                if self.valeur_grappe[n] == 0:
                    self.valeur_base.append(0)
                else:
                    self.valeur_base.append(self.valeur_grappe[n]-3*self.parent.tempsDeplacement(self.base, self.parent.listePlanetes[n]))
        
        def determinerBase(self):
            valeurMax = 0
            indexPlanete = None
            for n in range(0,len(self.valeur_base)):
                if valeurMax < self.valeur_base[n]:
                    valeurMax = self.valeur_base[n]
                    indexPlanete = n  
                    
            self.base = self.parent.listePlanetes[indexPlanete]
                    
        #TODO : comprendre comment mettre le tout ensemble
                    
        def forceAttaque(self):
            return self.parent.tempsCourant * self.nbr_vaisseaux_par_attaque * self.force_attaque_basique
        
        
        def choixMode(self):
            if self.mode == Mode.RASSEMBLEMENT_FORCES and self.base.nbVaisseaux == 3*self.forceAttaque():
                #TODO envoyer l'armada a la nouvelle base
                self.mode = Mode.ETABLIR_BASE
            
            #TODO faire le switch entre les modes etablir base et rassemblement de forces
        
    
        
        