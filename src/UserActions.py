from Enum import *



class UserActions:
    SELECT_PLANETE = Enum.addId()  # Selection d'une planete
    SELECT_PLANETE_2 = Enum.addId()
    VALIDER_DEPLACEMENT = Enum.addId()  # Validation d'un deplacement
    VALIDER_TOUR = Enum.addId()  # Validation d'un tour
    FLOTTE_CHANGEMEMT = Enum.addId() # Augmentation de la flotte


