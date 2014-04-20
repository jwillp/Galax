#!/usr/bin/python
# -*- coding: utf-8 -*-


class Gubru:
    def __init__(self,parent):
        self.parent = parent
        force_attaque_basique = 10
        nbr_vaisseaux_par_attaque = 5
        self.planeteMere = parent.modele.planeteMereGubrus
        
    def forceAttaque(self):
        if self.parent.temps_courant * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique > self.force_attaque_basique*2:
            return self.parent.temps_courant * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique
        else : 
            return self.force_attaque_basique*2
        
    def creerFlottes(self):
        