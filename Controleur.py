#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modele import Modele
from Gui import Gui
from Races import Races
from UserActions import UserActions


class Controleur():
    def __init__(self):
        self.modele = None
        self.gui = None
        self.initModele()
        self.initGui()

    def initGui(self):
        self.gui = Gui(self.gameLoop)
        self.gui.activerValiderDeplacement(False)
        self.gui.activerBarreAugmentation(False)
        self.gui.rafraichir(self.modele.anneeCourante, self.modele.listePlanetes,
                            self.modele.listePlanetesRace(Races.HUMAIN), self.modele.listePlanetesRace(Races.GUBRU),
                            self.modele.listePlanetesRace(Races.CZIN))
        self.gui.rafraichir()

    def initModele(self):
        self.modele = Modele(20, 25, 15)
        self.modele.creerPlanetes()

    def gameLoop(self, userAction, coordinates=None):

        """ the coordiantes should be tuples """
        if userAction == UserActions.VALIDER_DEPLACEMENT:
            self.validationDeplacement()

        elif userAction == UserActions.VALIDER_TOUR:
            self.finTour()

        elif userAction == UserActions.SELECT_PLANETE:
            self.gestionSelectionPlanete(coordinates)

        elif userAction == UserActions.FLOTTE_CHANGEMEMT:
            self.gestionChangementFlotte()


    # MÉTHODES DE CONTRÔLES PRINCIPALES #
    def gestionSelectionPlanete(self):
        """ Méthode gérant le cas de la sélection d'une planète """
        pass  # TODO Gestion Selection Planete
        # Si aucune planète ne correspond au coordonnées ==> ne rien faire
        # Sinon obtenir la planète au coordonées visées
        # Si on a aucune planète selection dans le modèle alors mettre celle-ci
        # afficher les informations de la planète sélectionnée selon niveau connaissances
        # Si planete == Humain ==> Si on a pas déjà une flotte dans le modèle ==> faire une nouvelle flotte

        #self.gui.getNbVaisseaux()
        #self.gui.inspecterPlanete(planete.nom, planete.capacite, nbVaisseaux)
        pass  # Check coordinates (tuples)

    def validationDeplacement(self):
        """ Méthode gérant le cas de la validation d'un déplacement """
        pass  # TODO  validation Deplacement

    def finTour(self):
        """ Méthode gérant le cas de la fin d'un tour"""
        pass  # TODO Fin d'un tour

    def gestionChangementFlotte(self):
        """ Méthode gérant le cas du changement du nombre de vaisseaux d'une flotte """
        # TODO mettre flotte même nombre que vaisseaux GUI
        #print(self.gui.getNbVaisseaux())
        pass


    def executer(self):
        """ permet de lancer le GUI """
        self.gui.run()


# TODO Selon les cas, désactiver certains boutons du GUI pour empêcher des problèmes #
# Le contrôleur nécessitera certaine des méthodes suivantes du modèle
# getNbPlanetesGubru() OU getPlanetesGubru()
# getNbPlanetesCzins() OU getPlanetesCzins()
# getNbPlanetesHumaines() OU getPlanetesHumaines()
# getPlaneteAt(x,y) ==> permet d'obtenir une planète selon coordonnée


def main():
    Controleur().executer()


if __name__ == '__main__':
    main()

