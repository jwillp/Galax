#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import math
from Planete import *
from Flotte import *
from Humain import *
from Gubru import *
from Czin import *
from Races import *

class Modele:
    def __init__(self, tailleX, tailleY, nombrePlanetes):
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
        self.humain = None
        self.gubru = None
        self.czin = None
        
        
    def creerPlanetes(self):
        for n in range(0,self.nombrePlanetes):
            self.listePlanetes.append(Planete(None, None, None)) #TODO ajouter import pour les planetes
            
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
        
        self.determinerPlanetesIndependantes()
        self.determinerPlaneteMereHumains()
        self.determinerPlaneteMereGubrus()
        self.determinerPlaneteMereCzins()
        
        
        
    def determinerPlaneteMereHumains(self):
        self.planeteMereHumains = random.randrange(self.listePlanetes)
        self.listePlanetes[self.planeteMereHumains].isPlaneteMere = True
        self.listePlanetes[self.planeteMereHumains].civilisation = "Humains" #TODO remplacer par Races.HUMAIN quand le Enum est fait
        self.listePlanetes[self.planeteMereHumains].manufactures = 10
        
    def determinerPlaneteMereGubrus(self):
        #trouve une planete qui n'est pas la planete mere humaine
        self.planeteMereGubrus = random.randrange(self.listePlanetes)
        
        if self.planeteMereGubrus == self.planeteMereHumains:
            self.determinerPlaneteMereGubru()
        else:           
            self.listePlanetes[self.planeteMereGubrus].isPlaneteMere = True
            self.listePlanetes[self.planeteMereGubrus].civilisation = "Gubrus" #TODO remplacer par Races.GUBRU quand le Enum est fait
            self.listePlanetes[self.planeteMereGubrus].manufactures = 10
            
    def determinerPlaneteMereCzins(self):
        #trouve une planete qui n'est pas la planete mere humaine ou Gubru
        self.planeteMereCzins = random.randrange(self.listePlanetes)
        if self.planeteMereCzins == self.planeteMereHumains or self.planeteMereCzins == self.planeteMereGubrus:
            self.determinerPlaneteMereCzins()
        else : 
            self.listePlanetes[self.planeteMereCzins].isPlaneteMere = True
            self.listePlanetes[self.planeteMereCzins].civilisation = "Czins" #TODO remplacer par Races.CZIN quand le Enum est fait
            self.listePlanetes[self.planeteMereCzins].manufactures = 10
            
    def determinerPlanetesIndependantes(self):
        for n in range(0, len(self.listePlanetes)):
            self.listePlanetes[n].civilisation = "Indépendants"  #TODO remplacer par Races.INDEPENDANT quand le Enum est fait
    
    def ajoutFlottes(self, planeteDepart, planeteArrivee, civilisation, nbVaisseaux):
        #prends pour aquis que le constructeur de Flotte est : Flotte(planeteDepart, planeteArrivee, civilisation, nbVaisseaux)
        self.listeFlottes.append(Flotte(planeteDepart, planeteArrivee, civilisation, nbVaisseaux))
        
    def arriveeFlottes(self):
        #verifie l'arrivee des flottes et gere le retour des flottes Gubrus d'une nouvelle conquete
        for n in range(0, len(self.listeFlottes)):
            if self.listeFlottes[n].tempsArrivee == self.anneeCourante:
                planeteAttaquee = self.trouverPlaneteAttaquee(self.listeFlottes[n])
                if planeteAttaquee != -1:
                    planeteAttaquee.defense(self.listeFlottes[n])
                    if self.listeFlottes[n].civilisation == "Gubru" and planeteAttaquee.civilisation == "Gubru":
                        self.gubru.retourFlottesConquete(planeteAttaquee) 
                        
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
            self.listeFlottes.remove(self.listeFlottesSuprimmees[n])
                    
        self.listeFlottesSuprimmees.clear()
        
    def creerCivilisations(self):
        self.humain = Humain()
        self.gubru = Gubru()
        self.czin = Czin()
        
    def tempsDeplacement(self, planeteDepart, planeteArrivee):
        #calcule le temps de deplacement comme si la distance est l'hypothenuse d'un triangle rectangle et arrondit a une decimale
        distanceX = (planeteArrivee.posX - planeteDepart.posX)**2
        distanceY = (planeteArrivee.poY - planeteDepart.posY)**2
        distanceFinale = math.sqrt(distanceX+distanceY)
        return round(distanceFinale,1)
    
    
    def updatePlanetesAttaqueesGubru(self):
        #s'assure que les Gubrus n'envoir pas plusieurs flottes aux memes planetes
        listePlanetesPlusAttaquees = []
        for i in range(0,len(self.gubru.listePlanetesAttaquees)):
            trouve = False
            for n in range(0, len(self.listeFlottes)):
                if self.gubru.listePlanetesAttaquees[i] == self.listeFlottes[n].planeteArrivee:
                    if self.listeFlottes[n].civilisation == "Gubru": #TODO changer pour Races.GUBRU quand l'enum est fait
                        trouve = True
            if trouve == False: 
                listePlanetesPlusAttaquees.append(self.gubru.listePlanetesAttaquees[i])
                
        for n in range(0,len(listePlanetesPlusAttaquees)):
            self.gubru.listePlanetesAttaquees.remove(listePlanetesPlusAttaquees[n])
                    
        listePlanetesPlusAttaquees.clear()
                

        
    
    
        
