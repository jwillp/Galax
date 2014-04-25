#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import math
from Planete import *
from Flotte import *
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
        self.listePos = []
        self.planeteMereHumains = None
        self.planeteMereGubrus = None
        self.planeteMereCzins = None
        self.gubru = Gubru(self)
        self.czin = Czin(self)
        self.planeteSelectionnee = None
        self.planeteSelectionnee2 = None
        
        
    def creerPlanetes(self):
        for n in range(0,self.nombrePlanetes):
            self.listePlanetes.append(Planete(None, None, None))
            self.listePos = [None, None]
            
        for n in range(0,self.nombrePlanetes):
            self.listePlanetes[n] = self.positionsPlanetesRandom()
            
        self.determinerPlanetesIndependantes()
        self.determinerPlaneteMereHumains()
        self.determinerPlaneteMereGubrus()
        self.determinerPlaneteMereCzins()
        
    def positionsPlanetesRandom(self):
        randomPositionX = random.randrange(self.tailleX) 
        randomPositionY = random.randrange(self.tailleY) 
        randomManufactures = random.randrange(7)
        position = [randomPositionX, randomPositionY]
        
        for n in range(0, len(self.listePos)):
            while self.listePos[n] in position:
                randomPositionX = random.randrange(self.tailleX) 
                randomPositionY = random.randrange(self.tailleY) 
                position = [randomPositionX, randomPositionY]
                
        return Planete(randomPositionX, randomPositionY, randomManufactures) #TODO ajouter import pour les planetes
        
        
        
        
        
    def determinerPlaneteMereHumains(self):
        self.planeteMereHumains = random.randrange(len(self.listePlanetes))
        self.listePlanetes[self.planeteMereHumains].isPlaneteMere = True
        self.listePlanetes[self.planeteMereHumains].civilisation = Races.HUMAIN
        self.listePlanetes[self.planeteMereHumains].nbManufactures = 10
        self.listePlanetes[self.planeteMereHumains].nbVaisseaux = 100
        
    def determinerPlaneteMereGubrus(self):
        #trouve une planete qui n'est pas la planete mere humaine
        self.planeteMereGubrus = random.randrange(len(self.listePlanetes))
        
        if self.planeteMereGubrus == self.planeteMereHumains:
            self.determinerPlaneteMereGubrus()
        else:           
            self.listePlanetes[self.planeteMereGubrus].isPlaneteMere = True
            self.listePlanetes[self.planeteMereGubrus].civilisation = Races.GUBRU
            self.listePlanetes[self.planeteMereGubrus].nbManufactures = 10
            self.listePlanetes[self.planeteMereGubrus].nbVaisseaux = 100
            self.gubru.planeteMere = self.planeteMereGubrus
            
    def determinerPlaneteMereCzins(self):
        #trouve une planete qui n'est pas la planete mere humaine ou Gubru
        self.planeteMereCzins = random.randrange(len(self.listePlanetes))
        if self.planeteMereCzins == self.planeteMereHumains or self.planeteMereCzins == self.planeteMereGubrus:
            self.determinerPlaneteMereCzins()
        else : 
            self.listePlanetes[self.planeteMereCzins].isPlaneteMere = True
            self.listePlanetes[self.planeteMereCzins].civilisation = Races.CZIN
            self.listePlanetes[self.planeteMereCzins].nbManufactures = 10
            self.listePlanetes[self.planeteMereCzins].nbVaisseaux = 100
            self.czin.planeteMere = self.planeteMereCzins
            
    def determinerPlanetesIndependantes(self):
        for n in range(0, len(self.listePlanetes)):
            self.listePlanetes[n].civilisation = Races.INDEPENDANT
    
    def ajoutFlottes(self, planeteDepart, planeteArrivee, civilisation, nbVaisseaux):
        #prends pour aquis que le constructeur de Flotte est : Flotte(planeteDepart, planeteArrivee, civilisation, nbVaisseaux)
        self.listeFlottes.append(Flotte(planeteDepart, planeteArrivee, civilisation, nbVaisseaux, self.tempsCourant + self.tempsDeplacement(planeteDepart, planeteArrivee)))
        for planete in self.listePlanetes:
            if planete == planeteDepart:
                planete.nbVaisseaux -= nbVaisseaux
        
    def arriveeFlottes(self):
        #verifie l'arrivee des flottes et gere le retour des flottes Gubrus d'une nouvelle conquete
        for n in range(0, len(self.listeFlottes)):
            if self.listeFlottes[n].tempsArrivee == self.anneeCourante:
                planeteAttaquee = self.trouverPlaneteAttaquee(self.listeFlottes[n])
                if planeteAttaquee != -1:
                    planeteAttaquee.defense(self.listeFlottes[n])
                    if self.listeFlottes[n].civilisation == Races.GUBRU and planeteAttaquee.civilisation == Races.GUBRU:
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
        
    def tempsDeplacement(self, planeteDepart, planeteArrivee):
        #calcule le temps de deplacement comme si la distance est l'hypothenuse d'un triangle rectangle et arrondit a une decimale
        distanceX = (planeteArrivee.posX - planeteDepart.posX)**2
        distanceY = (planeteArrivee.posY - planeteDepart.posY)**2
        distanceFinale = math.sqrt(distanceX+distanceY)
        return round(distanceFinale,1)
    
    
    def updatePlanetesAttaqueesGubru(self):
        #s'assure que les Gubrus n'envoir pas plusieurs flottes aux memes planetes ( appelee dans choisirPlanetesAttaqueesGubru de la classe Gubru)
        listePlanetesPlusAttaquees = []
        for i in range(0,len(self.gubru.listePlanetesAttaquees)):
            trouve = False
            for n in range(0, len(self.listeFlottes)):
                if self.gubru.listePlanetesAttaquees[i] == self.listeFlottes[n].planeteArrivee:
                    if self.listeFlottes[n].civilisation == Races.GUBRU:
                        trouve = True
            if trouve == False: 
                listePlanetesPlusAttaquees.append(self.gubru.listePlanetesAttaquees[i])
                
        for n in range(0,len(listePlanetesPlusAttaquees)):
            self.gubru.listePlanetesAttaquees.remove(listePlanetesPlusAttaquees[n])
                    
        listePlanetesPlusAttaquees.clear()
       
    def avancerTemps(self):
        #fait les taches d'une annee complete sans inclure les actions humaines
        self.gubru.creerFlottes()
        self.czin.creerFlottes() #TODO : pas mal tout des Czin 
        for n in range(0,9):
            self.arriveeFlottes()
            self.anneeCourante += 0.1
            
        for n in range(0, len(self.listePlanetes)):
            self.listePlanetes[n].nbVaisseaux += self.listePlanetes[n].nbManufactures   

    def isHumainVivant(self):
        resteFlottes = False
        restePlanetes = False
        
        for planete in self.listePlanetes:
            if planete.civilisation == Races.HUMAIN:
                restePlanetes = True
                
        for flotte in self.listeFlottes:
            if flotte.civilisation == Races.HUMAIN:
                resteFlottes = True
                
        if resteFlottes and restePlanetes:
            return True
        else:
            return False
        
    def getPlaneteAt(self, posX, posY):
        planeteRetour = None
        for planete in self.listePlanetes:
            if planete.posX == posX and planete.posY == posY:
                planeteRetour = planete
                
        return planeteRetour
    
    def listePlanetesRace(self, race):
        nombre = 0
        for planete in self.listePlanetes:
            if planete.civilisation == race:
                nombre +=1
                
        return nombre
    
    def selectionnerPlanete(self, planete):
        self.planeteSelectionnee = planete
    
    
        
