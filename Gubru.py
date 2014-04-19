#!/usr/bin/python
# -*- coding: utf-8 -*-


class Gubru:
    def __init__(self,parent):
        self.parent = parent
        force_attaque_basique = 10
        nbr_vaisseaux_par_attaque = 5
        self.planeteMere = parent.modele.planeteMereGubrus
        self.listePlanetesAttaquees = []
        
    def forceAttaque(self):
        if self.parent.temps_courant * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique > self.force_attaque_basique*2:
            return self.parent.temps_courant * self.nbr_vaisseaux_par_attaque + self.force_attaque_basique
        else : 
            return self.force_attaque_basique*2
        
    def creerFlottes(self):
        self.flottesAttaque()
                
        planetesGubrus = []
        for n in range(0, len(self.parent.listePlanetes)):
            if self.parent.listePlanetes[n].civilisation == "Gubru":# TODO a changer pour Races.GUBRU quand l'enum sera fait
                planetesGubrus.append(self.parent.listePlanetes[n])
                
        for n in range(0, len(planetesGubrus)):
            if planetesGubrus.nbVaisseaux > 25:
                self.parent.ajoutFlotte(planetesGubrus[n], self.planeteMere, "Gubru", planetesGubrus.nbVaisseaux-15)# TODO a changer pour Races.GUBRU quand l'enum sera fait
                
    def flottesAttaque(self):
        if self.planeteMere.nbVaisseaux >= self.forceAttaque()+self.force_attaque_basique:
            while self.planeteMere.nbVaisseaux >= self.forceAttaque():
                planeteChoisie = self.choisirPlaneteAttaquee()
                self.listePlanetesAttaquees.append(planeteChoisie)
                self.parent.ajoutFlotte(self.planeteMere, planeteChoisie, "Gubru") # TODO a changer pour Races.GUBRU quand l'enum sera fait
                
    def retourFlottesConquete(self, planeteConquise):
        if planeteConquise.nbVaisseaux > 25:
            self.parent.ajoutFlotte(planeteConquise, self.planeteMere, "Gubru", planeteConquise.nbVaisseaux-15)# TODO a changer pour Races.GUBRU quand l'enum sera fait
        else:
            self.parent.ajoutFlotte(planeteConquise, self.planeteMere, "Gubru", planeteConquise.nbVaisseaux)# TODO a changer pour Races.GUBRU quand l'enum sera fait
    
    def choisirPlaneteAttaquee(self):
        #trouve la prochaine planete a attaquer en s'assurant qu'il n'y a pas deja une flotte en direction
        self.parent.updatePlanetesAttaqueesGubru()
        distance = 2000000000 #chiffre ridicule pour trouver ce qui est plus proche
        planeteAttaquee = None
        for n in range(0, len(self.parent.listePlanetes)):
            if self.parent.tempsDeplacement(self.planeteMere, self.parent.listePlanetes[n]) < distance and self.parent.listePlanetes[n].civilisation != "Gubru": #TODO changer pour Races.GUBRU quand l'enum est fait 
                for i in range(0, len(self.listePlanetesAttaquees)):
                    if self.parent.listePlanetes[n] != self.listePlanetesAttaquees[i]:
                        distance = self.parent.tempsDeplacement(self.planeteMere, self.parent.listePlanetes[n])
                        planeteAttaquee = self.parent.listePlanete[n]
        return planeteAttaquee
    
    def choisirNouvellePlaneteMere(self):
        #choisit la nouvelle planete mere
        if self.planeteMere.civilisation != "Gubru":
            for n in range(0, len(self.parent.listePlanetes)):
                if self.parent.listePlanetes[n].civilisation == "Gubru":
                    self.planeteMere = self.parent.listePlanetes[n]
                    self.parent.listePlanetes[n].isPlaneteMere = True
                    self.parent.planeteMereGubru = self.parent.listePlanetes[n]
            
    