#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

class Modele:
    def __init__(self, parent, tailleX, tailleY, nombrePlanetes):
        self.parent = parent
        self.tailleX = tailleX
        self.tailleY = tailleY
        self.nombrePlanetes = nombrePlanetes
        self.listePlanetes = []
        self.listeFlottes = []
        self.anneeCourante = 0
        self.listeFlottesSuprimmees = []
        self.planeteMereHumains = None
        self.planeteMereGubrus = None
        self.planeteMereCzins = None
        
        
    def creerPlanetes(self):
        for n in range(0,self.nombrePlanetes):
            self.listePlanetes.append(Planete(None, None, None, None)) #TODO ajouter import pour les planetes
            
        for n in range(0,self.nombrePlanetes):
            self.listePlanetes[n] = self.positionsPlanetesRandom()
        
    def positionsPlanetesRandom(self):
        randomPositionX = random.randrange(self.tailleX) #TODO trouver la variable pour la taille en X du jeu
        randomPositionY = random.randrange(self.tailleY) #TODO trouver la variable pour la taille en Y du jeu
        randomManufactures = random.randrange(6)
        
        for n in range(0,len(self.listePlanetes)):
            while self.listePlanetes[n].posX == randomPositionX and self.listePlanetes[n].posY == randomPositionY:
                randomPositionX = random.randrange(self.tailleX)
                randomPositionY = random.randrange(self.tailleY)
            return Planete(randomPositionX, randomPositionY, randomManufactures) #TODO ajouter import pour les planetes
        
        self.determinerPlaneteMereHumains()
        self.determinerPlaneteMereGubrus()
        self.determinerPlaneteMereCzins()
        self.determinerPlanetesIndependantes()
        
        
    def determinerPlaneteMereHumains(self):
        self.planeteMereHumains = random.randrange(self.listePlanetes)
        self.listePlanetes[self.planeteMereHumains].isPlaneteMere = True
        self.listePlanetes[self.planeteMereHumains].civilisation = "Humains"
        self.listePlanetes[self.planeteMereHumains].manufactures = 10
        
    def determinerPlaneteMereGubrus(self):
        self.planeteMereGubrus = random.randrange(self.listePlanetes)
        
        if self.planeteMereGubrus == random.randrange(self.listePlanetes):
            self.determinerPlaneteMereGubru()
        else:           
            self.listePlanetes[self.planeteMereGubrus].isPlaneteMere = True
            self.listePlanetes[self.planeteMereGubrus].civilisation = "Gubrus"
            self.listePlanetes[self.planeteMereGubrus].manufactures = 10
            
    def determinerPlaneteMereCzins(self):
        self.planeteMereCzins = random.randrange(self.listePlanetes)
        if self.planeteMereCzins == self.planeteMereHumains or self.planeteMereCzins == self.planeteMereGubrus:
            self.determinerPlaneteMereCzins()
        else : 
            self.listePlanetes[self.planeteMereCzins].isPlaneteMere = True
            self.listePlanetes[self.planeteMereCzins].civilisation = "Czins"
            self.listePlanetes[self.planeteMereCzins].manufactures = 10
            
    def determinerPlanetesIndependantes(self):
        for n in range(0, len(self.listePlanetes)):
            if n != self.planeteMereHumains and n != self.planeteMereGubrus and n != self.planeteMereCzins:
                self.listePlanetes[n].civilisation = "Indépendants"  
    
    def ajoutFlottes(self, flotteAjoutee):
        self.listeFlottes.append(flotteAjoutee)
        
    def arriveeFlottes(self):
        #verifie l'arrivee des flottes
        for n in range(0, len(self.listeFlottes)):
            if self.listeFlottes[n].tempsArrivee == self.anneeCourante:
                planeteAttaquee = self.trouverPlaneteAttaquee(self.listeFlottes[n])
                planeteAttaquee.defense(self.listeFlottes[n])
                self.listeFlottesSuprimmees.append(self.listeFlottes[n])
                           
    def trouverPlaneteAttaquee(self, flotte):
        #trouve la planete attaquee
        for n in range(0, len(self.listePlanetes)):
            if self.listePlanetes[n] == flotte.positionArrivee:
                return self.listePlanetes[n]
            else:
                return -1
            
    def supprimerFlottes(self):
        #trouve les flottes qui doivent etre supprimes et les supprime
        for n in range(0,len(self.listeFlottesSuprimmees)):
            for i in range(0, len(self.listeFlottes)):
                if self.listeFlottesSuprimmees[n] == self.listeFlottes[i]:
                    self.listeFlottes.pop(i)
                    
        self.listeFlottesSuprimmees.clear()