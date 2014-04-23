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
        nbPlanete = 40

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
        self.modele.planeteSelectionnee2 = None # TODO effacer cette ligne lorsque le modele sera modifié

    def gameLoop(self, userAction, coordinates=None):

        """ the coordiantes should be tuples """
        if userAction == UserActions.VALIDER_DEPLACEMENT:
            self.validationDeplacement()

        elif userAction == UserActions.VALIDER_TOUR:
            self.finTour()

        elif userAction is UserActions.SELECT_PLANETE or userAction is UserActions.SELECT_PLANETE_2:
            self.gestionSelectionPlanete(coordinates, userAction)

        elif userAction == UserActions.FLOTTE_CHANGEMEMT:
            self.gestionChangementFlotte()


    # MÉTHODES DE CONTRÔLES PRINCIPALES #
    def gestionSelectionPlanete(self, coordonnee, userAction):
        """ Méthode gérant le cas de la sélection d'une planète """
        planete = self.modele.getPlaneteAt(coordonnee[0], coordonnee[1])
        if not planete:
            return

        # TODO Gestion Selection Planete



        if userAction is UserActions.SELECT_PLANETE:
            self.gestionSelection1(planete)
        else:
            self.gestionSelection2(planete)



        self.gui.rafraichir(self.modele.anneeCourante, self.modele.listePlanetes,
                            self.modele.listePlanetesRace(Races.HUMAIN), self.modele.listePlanetesRace(Races.GUBRU),
                            self.modele.listePlanetesRace(Races.CZIN),
                            self.modele.planeteSelectionnee,
                            self.modele.planeteSelectionnee2
        )






    def gestionSelection1(self, planete):
        self.modele.planeteSelectionnee = planete
        self.inspecterPlanete(planete)

        if self.modele.planeteSelectionnee.civilisation == Races.HUMAIN:
            activation = True
        else:
            activation = False
            self.gui.resetNombreVaisseaux()

        self.gui.activerBarreAugmentation(activation)
        self.gui.activerValiderDeplacement(activation)

    def gestionSelection2(self, planete):
        self.modele.planeteSelectionnee2 = planete
        if self.modele.planeteSelectionnee != self.modele.planeteSelectionnee2:
            self.inspecterPlanete(planete)




    def inspecterPlanete(self, planete):
        """ Inspecte une lpanete selon le niveau de connaissance """
        if planete.civilisation == Races.HUMAIN:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY, planete.nbManufactures, planete.nbVaisseaux)
            return

        if planete.nbVisites == 0:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY)

        if planete.nbVisites == 1:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY, planete.nbManufactures)

        if planete.nbVisites == 2:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY, planete.nbManufactures)

        if planete.nbVisites == 3:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY, planete.nbManufactures)





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

