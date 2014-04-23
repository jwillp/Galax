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

        nbCol = 25
        nbLignes = 20
        nbPlanete = 25

        self.initModele(nbCol, nbLignes, nbPlanete)
        self.initGui(nbCol, nbLignes, nbPlanete)

    def initGui(self, nbCols, nbLignes, nbPlanetes):
        self.gui = Gui(self.gameLoop)
        self.gui.activerValiderDeplacement(False)
        self.gui.activerBarreAugmentation(False)
        self.gui.rafraichir(self.modele.anneeCourante, self.modele.listePlanetes,
                            self.modele.listePlanetesRace(Races.HUMAIN), self.modele.listePlanetesRace(Races.GUBRU),
                            self.modele.listePlanetesRace(Races.CZIN))


    def initModele(self, nbCols, nbLignes, nbPlanetes):
        self.modele = Modele(nbCols, nbLignes, nbPlanetes)
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
    def gestionSelectionPlanete(self, coordonnee):
        """ Méthode gérant le cas de la sélection d'une planète """
        planete = self.modele.getPlaneteAt(coordonnee[0], coordonnee[1])
        if not planete:
            return



        # TODO Gestion Selection Planete

        self.gui.inspecterPlanete(planete.nom, planete.nbManufactures, planete.nbVaisseaux)





        if not self.modele.planeteSelectionnee:
            self.modele.selectionnerPlanete(planete)



        if self.modele.planeteSelectionnee.civilisation == Races.HUMAIN:
            self.gui.activerBarreAugmentation(True)
            self.gui.activerValiderDeplacement(True)

        # Si planete == Humain ==> Si on a pas déjà une flotte dans le modèle ==> faire une nouvelle flotte

         # Check coordinates (tuples)

    def validationDeplacement(self):
        """ Méthode gérant le cas de la validation d'un déplacement """
        pass  # TODO  validation Deplacement




    def finTour(self):
        """ Méthode gérant le cas de la fin d'un tour"""
        self.modele.avancerTemps()
        pass  # TODO Fin d'un tour


    def gestionChangementFlotte(self):
        """ Méthode gérant le cas du changement du nombre de vaisseaux d'une flotte """
        # TODO mettre flotte même nombre que vaisseaux GUI
        #print(self.gui.getNbVaisseaux())
        self.gui.nbVaisseauxWidget.max = self.modele.planeteSelectionnee.nbVaisseaux




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

