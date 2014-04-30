#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modele import Modele
from Gui import Gui
from Notification import Affrontement, Annihilation
from Races import Races
from UserActions import UserActions


class Controleur():
    def __init__(self):
        self.modele = None
        self.gui = None

        nbCol = 25
        nbLignes = 20
        nbPlanete = 35

        self.initModele(nbCol, nbLignes, nbPlanete)
        self.initGui()

    def initGui(self):
        self.gui = Gui(self.gameLoop)
        self.gui.activerValiderDeplacement(False)
        self.gui.activerBarreAugmentation(False)

        data = {}
        data["anneeCourante"] = self.modele.anneeCourante
        data["listePlanetes"] = self.modele.planetes
        data["nbPlanetesHumain"] = self.modele.getNbPlanetesRace(Races.HUMAIN)
        data["nbPlanetesGubru"] = self.modele.getNbPlanetesRace(Races.GUBRU)
        data["nbPlanetesCzin"] = self.modele.getNbPlanetesRace(Races.CZIN)
        data["selection1"] = None
        data["selection2"] = None
        data["flottesHumaines"] = None
        data["flottes"] = self.modele.flottes

        self.gui.rafraichir(data)

    def initModele(self, nbCols, nbLignes, nbPlanetes):
        self.modele = Modele(nbCols, nbLignes, nbPlanetes)
        self.modele.creerPlanetes()

    def executer(self):
        """ permet de lancer le GUI """
        self.gui.run()

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

        if not planete:  # Si on clique dans le vide
            if userAction is UserActions.SELECT_PLANETE:
                self.modele.planeteSelectionnee = None
                self.gui.resetNombreVaisseaux()
                self.gui.activerBarreAugmentation(False)
                self.gui.activerValiderDeplacement(False)

            else:
                self.modele.planeteSelectionnee2 = None
        else:
            self.inspecterPlanete(planete)
            if userAction is UserActions.SELECT_PLANETE:
                self.gestionSelection1(planete)
            else:
                self.gestionSelection2(planete)
                self.rafraichirFlotte()

        self.rafraichirGui()


    def gestionSelection1(self, planete):
        self.modele.planeteSelectionnee = planete

        if self.modele.planeteSelectionnee.civilisation == Races.HUMAIN:
            self.gui.nbVaisseauxWidget.configure(to_=planete.nbVaisseaux)
            activation = True
        else:
            activation = False
            self.gui.resetNombreVaisseaux()

        self.gui.activerBarreAugmentation(activation)


    def gestionSelection2(self, planete):
        self.modele.planeteSelectionnee2 = planete
        if self.modele.planeteSelectionnee:
            if self.modele.planeteSelectionnee.civilisation == Races.HUMAIN:
                self.gui.nbVaisseauxWidget.configure(to_=self.modele.planeteSelectionnee.nbVaisseaux)
                activation = True
            else:
                activation = False
                self.gui.resetNombreVaisseaux()

            self.gui.activerBarreAugmentation(activation)


    def gestionChangementFlotte(self):
        """ Méthode gérant le cas du changement du nombre de vaisseaux d'une flotte """
        if self.gui.getNbVaisseaux() <= 0 or not self.modele.planeteSelectionnee2:
            activation = False
        else:
            activation = True

        self.gui.activerValiderDeplacement(activation)



    def rafraichirFlotte(self):
        depart = self.modele.planeteSelectionnee
        arrivee = self.modele.planeteSelectionnee2
        data = {"planeteDepart": depart, "planeteArrivee": arrivee}
        if depart and arrivee:
            data["distance"] = self.modele.calculerDistance(depart, arrivee)
        else:
            data["distance"] = None
        self.gui.rafraichirFlotte(data)


    def inspecterPlanete(self, planete):
        """ Inspecte une la planete selon le niveau de connaissance """
        if planete.civilisation == Races.HUMAIN:
            self.gui.inspecterPlanete(planete.nom, planete.posX, planete.posY, planete.nbManufactures,
                                      planete.nbVaisseaux)
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
        # Rafraîchissement du GUI
        self.rafraichirGui()

        planeteDepart = self.modele.planeteSelectionnee
        planeteArrive = self.modele.planeteSelectionnee2
        nbVaisseaux = self.gui.getNbVaisseaux()

        self.modele.ajouterFlotte(planeteDepart, planeteArrive, Races.HUMAIN, nbVaisseaux)

        self.gui.resetNombreVaisseaux()
        self.gui.activerBarreAugmentation(False)
        self.gui.activerValiderDeplacement(False)
        self.rafraichirGui()


    def finTour(self):
        """ Méthode gérant le cas de la fin d'un tour"""
        self.modele.avancerTemps()
        self.gestionNotifications()
        self.rafraichirGui()


    def rafraichirGui(self):
        data = {}
        data["anneeCourante"] = self.modele.anneeCourante
        data["listePlanetes"] = self.modele.planetes
        data["nbPlanetesHumain"] = self.modele.getNbPlanetesRace(Races.HUMAIN)
        data["nbPlanetesGubru"] = self.modele.getNbPlanetesRace(Races.GUBRU)
        data["nbPlanetesCzin"] = self.modele.getNbPlanetesRace(Races.CZIN)
        data["selection1"] = self.modele.planeteSelectionnee
        data["selection2"] = self.modele.planeteSelectionnee2
        data["flottes"] = self.modele.flottes
        self.gui.rafraichir(data)








    def gestionNotifications(self):
        """ Permet de gérer les notifications """

        notifications = self.modele.notifications
        for notif in notifications:
            if isinstance(notif, Affrontement):
                self.gestionNotifAffrontement(notif)
            elif isinstance(notif, Annihilation):
                self.gestionNotifAnnihilation(notif)
        self.modele.notifications = []  # On vide les notifications

    def gestionNotifAnnihilation(self, notif):
        """ Gestion notifications d'annihilation """
        self.gui.consoleHumains.annihilation(notif.annee, notif.race)
        self.gui.consoleEnnemis.annihilation(notif.annee, notif.race)

    def gestionNotifAffrontement(self, notif):
        """ Gestion notifications d'affrontement """

        isHumainConcernes = False
        if notif.attaquant is Races.HUMAIN or notif.defenseur is Races.HUMAIN:
            isHumainConcernes = True

        # il y eu affrontement

        if isHumainConcernes:
            self.gui.consoleHumains.affrontementPlanete(notif.annee, notif.attaquant, notif.defenseur, notif.planete)

        self.gui.consoleEnnemis.affrontementPlanete(notif.annee, notif.attaquant, notif.defenseur, notif.planete)

        if notif.isDefenseReussie:  # Défense réussie

            if isHumainConcernes:
                self.gui.consoleHumains.defensePlanete(notif.annee, notif.defenseur, notif.attaquant, notif.planete)

            self.gui.consoleEnnemis.defensePlanete(notif.annee, notif.defenseur, notif.attaquant, notif.planete)

        else:  # Défense ratée, perte planète gain pour autre
            if isHumainConcernes:
                self.gui.consoleHumains.victoirePlanete(notif.annee, notif.attaquant, notif.planete)
                self.gui.consoleHumains.pertePlanete(notif.annee, notif.defenseur, notif.attaquant, notif.planete)

            self.gui.consoleEnnemis.pertePlanete(notif.annee, notif.defenseur, notif.attaquant, notif.planete)
            self.gui.consoleEnnemis.victoirePlanete(notif.annee, notif.attaquant, notif.planete)


def main():
    Controleur().executer()


if __name__ == '__main__':
    main()
