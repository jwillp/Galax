#!/usr/bin/python
# -*- coding: utf-8 -*-


class Flotte:
<<<<<<< HEAD
    def __init__(self, planeteDepart, planeteArrive, civilisation, nbVaisseaux, tempsArrivee):
        self.planeteDepart = planeteDepart
        self.planeteArrive = planeteArrive
        self.civilisation = civilisation
        self.nbVaisseaux = nbVaisseaux
        self.tempsArrivee = tempsArrivee

=======
    def __init__(self):
        self.civilisation    # preciser a quelle civilisation appartient la flotte
        self.positionDepart  # planete d'ou partent les vaisseaux
        self.positionArrivee # planete ou vont les vaisseaux
        self.nbVaisseaux     # nombre de vaisseaux en deplacement vers une planete ciblee
        self.tempsDepart     # moment en annees et dixieme x.x du moment du depart des vaisseaux
        self.tempsArrivee    # moment de l'arrivee x.x de l'arrivee sur la planete ciblee
        
    
    def flottePrepar(self, distance, duree):
        if distance <= 2
            duree = distance / 2
        else
            duree = 1 + ((distance- 2) / 3)

    

    
>>>>>>> 50e3a7336c76fde7f04af7f9bfe4990a8f80c5d0
