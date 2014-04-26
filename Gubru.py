#!/usr/bin/python
# -*- coding: utf-8 -*-
from Races import*

class Gubru:
    def __init__(self, parent):
        self.parent = parent
        self.force_attaque_basique = 10
        self.nbr_vaisseaux_par_attaque = 5
        self.planeteMere = None
        self.listePlanetesAttaquees = []
        
    def forceAttaque(self):
        if self.parent.anneeCourante * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique > self.force_attaque_basique*2:
            return self.parent.anneeCourante * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique
        else : 
            return self.force_attaque_basique*2
        
    def creerFlottes(self):
        self.flottesAttaque() # cree les flottes qui vont attaquer des planetes
        
        planetesGubrus = []
        for n in range(0, len(self.parent.listePlanetes)):
            if self.parent.listePlanetes[n].civilisation == Races.GUBRU:
                planetesGubrus.append(self.parent.listePlanetes[n]) # ajoute a une liste les planetes conquises par les gubrus et en cours d'attaque pour ne pas envoyer plusieurs flottes aux memes planetes
                
        # cree les flottes a partir de planetes avec plus de 25 vaisseaux
        for n in planetesGubrus:
            if n.nbVaisseaux > 25:
                self.parent.ajoutFlottes(n, self.planeteMere, Races.GUBRU, n.nbVaisseaux-15)
                
    def flottesAttaque(self):
        #determine les planetes les plus pres non Gubru non attaquees et les ajoute a une liste de planetes attaquees et cree les flottes
        if self.planeteMere.nbVaisseaux >= self.forceAttaque()+self.force_attaque_basique:
            while self.planeteMere.nbVaisseaux >= self.forceAttaque():
                planeteChoisie = self.choisirPlaneteAttaquee()
                self.listePlanetesAttaquees.append(planeteChoisie)
                self.parent.ajoutFlottes(self.planeteMere, planeteChoisie, Races.GUBRU, 10) # TODO mettre un vrai nombre de vaisseaux
                
    def retourFlottesConquete(self, planeteConquise):
        #gere le retour des flottes apres une conquete ( appellee dans le modele apres l'arrivee des flottes et le combat)
        if planeteConquise.nbVaisseaux > 25:
            self.parent.ajoutFlotte(planeteConquise, self.planeteMere, Races.GUBRU, planeteConquise.nbVaisseaux-15)
        else:
            self.parent.ajoutFlotte(planeteConquise, self.planeteMere, Races.GUBRU, planeteConquise.nbVaisseaux)
    
    def choisirPlaneteAttaquee(self):
        #trouve la prochaine planete a attaquer en s'assurant qu'il n'y a pas deja une flotte en direction
        self.parent.updatePlanetesAttaqueesGubru()
        distance = 2000000000 #chiffre ridicule pour trouver ce qui est plus proche
        planeteAttaquee = None
        for n in range(0, len(self.parent.listePlanetes)):
            if self.parent.tempsDeplacement(self.planeteMere, self.parent.listePlanetes[n]) < distance and self.parent.listePlanetes[n].civilisation != Races.GUBRU: 
                for i in range(0, len(self.listePlanetesAttaquees)):
                    if self.parent.listePlanetes[n] != self.listePlanetesAttaquees[i]:
                        distance = self.parent.tempsDeplacement(self.planeteMere, self.parent.listePlanetes[n])
                        planeteAttaquee = self.parent.listePlanetes[n]
        return planeteAttaquee
    
    def choisirNouvellePlaneteMere(self):
        #choisit la nouvelle planete mere
        if self.planeteMere.civilisation != Races.GUBRU:
            for n in range(0, len(self.parent.listePlanetes)):
                if self.parent.listePlanetes[n].civilisation == Races.GUBRU:
                    self.planeteMere = self.parent.listePlanetes[n]
                    self.parent.listePlanetes[n].isPlaneteMere = True
                    self.parent.planeteMereGubru = self.parent.listePlanetes[n]
            
    