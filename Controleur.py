#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modele import Modele
from Gui import Gui
from UserActions import UserActions

class Controleur():
    def __init__(self):
        #TODO self.modele = Modele() + inititalisation du modèle
        self.modele = Modele(20, 25, 15)
        self.gui = Gui(self.gameLoop)
        #TODO self.gui.rafraichir(self.modele.anneCourante, self.modele.planetes,
        #                    len(self.modele.getPlanetesHumains),
        #                    len(self.modele.getPlanetesGubru),
        #                    len(self.modele.getPlanetesCzins)
        #)

    def gameLoop(self, userAction, coordinates=None):

        """ the coordiantes should be tuples """
        if userAction == UserActions.VALIDER_DEPLACEMENT:
            self.validationDeplacement()

        elif userAction == UserActions.VALIDER_TOUR:
            self.finTour()

        elif userAction == UserActions.SELECT_PLANETE:
            self.gestionSelectionPlanete()

        elif userAction == UserActions.FLOTTE_CHANGEMEMT:
            self.gestionChangementFlotte()



    def gestionSelectionPlanete(self):
        pass  # TODO Gestion Selection Planete
        # afficher les informations de la planète sélectionnée selon niveau connaissances
        # Si planete == Humain ==> Si on a pas déjà une flotte dans le modèle ==> faire une nouvelle flotte

        #self.gui.getNbVaisseaux()
        #self.gui.inspecterPlanete(planete.nom, planete.capacite, nbVaisseaux)
        pass  # Check coordinates (tuples)

    def validationDeplacement(self):
        pass  # TODO  validation Deplacement

    def finTour(self):
        pass  # TODO Fin d'un tour

    def gestionChangementFlotte(self):
        # TODO mettre flotte même nombre que vaisseaux GUI
        #print(self.gui.getNbVaisseaux())
        pass


    def executer(self):
        self.gui.run()






def main():
    Controleur().executer()


if __name__ == '__main__':
    main()