#!/usr/bin/python32
# -*- coding: utf-8 -*-
#Python 3.x
from Races import Races

try: #3.x
    from tkinter import *
    from tkinter import ttk

except (ImportError):
    from Tkinter import * #2.x
    import ttk

from PIL import Image
from PIL import ImageTk

from UserActions import *


class Color():
    def __init__(self):  pass

    GRAY = "#3C3F41"
    LIGHT_GRAY = "#525556"
    DARK_GRAY = "#2B2B2B"
    GREEN = "#3AB35B"
    RED = "#D35F51"
    BLACK = "#27292A"
    MIDNIGHT_BLUE = "#2c3e50"


class Galaxie(Frame):
    """ Galaxie """

    def __init__(self, parent, nbColonnes, nbLignes, tailleTuile, app):
        self.parent = parent
        self.app = app  # La classe principale du GUI
        self.nbColonnes = nbColonnes
        self.nbLignes = nbLignes
        self.tailleTuile = tailleTuile  # taille d'une case en pixel

        # Images
        self.arrierePlan = ImageTk.PhotoImage(Image.open("img/fond.jpg"))

        self.gubruImage = ImageTk.PhotoImage(Image.open("img/fire.png"))
        self.czinImage = ImageTk.PhotoImage(Image.open("img/purple.png"))
        self.humainImage = ImageTk.PhotoImage(Image.open("img/blue.png"))
        self.indieImage = ImageTk.PhotoImage(Image.open("img/white.png"))
        self.selectionImage = ImageTk.PhotoImage(Image.open("img/selection.png"))
        self.selectionImage2 = ImageTk.PhotoImage(Image.open("img/selection2.png"))
        self.canvasLargeur = nbColonnes * tailleTuile
        self.canvasHauteur = nbLignes * tailleTuile

        Frame.__init__(self, parent)

        self.canvas = Canvas(self, width=self.canvasLargeur, height=self.canvasHauteur, background="#000918",
                             highlightthickness=0)

        self.canvas.grid(column=0, row=0, sticky=N + S)

        #Dessiner la canvas
        image = Image.open("img/fond.jpg")
        self.arrierePlan = image.resize(( self.canvas.winfo_width(), self.canvas.winfo_height()), Image.ANTIALIAS)
        self.arrierePlan = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.arrierePlan)

        #Écouteur d'événements
        self.canvas.bind("<Button-1>", self.app.notifyPlanetClick)
        self.canvas.bind("<Button-3>", self.app.notifyPlanetRightClick)


    def draw(self, data):
        listePlanetes = data["listePlanetes"]
        selection1 = data["selection1"]
        selection2 = data["selection2"]
        flottes = data["flottes"]

        self.canvas.delete("planete")
        self.canvas.delete("flotte")

        #Affichage des liens entre les sélections
        self.drawLienSelection(selection1, selection2)


        # Affichage des flottes
        self.drawFlottes(flottes)

        # Affichage des planetes et Selections
        self.drawPlanetes(listePlanetes, selection1, selection2)


    def drawLienSelection(self, selection1, selection2):
        """ Affiche le liens entre les selections """
        if selection1 and selection2:
            x1 = self.tailleTuile * selection1.posX + self.tailleTuile/2
            y1 = self.tailleTuile * selection1.posY + self.tailleTuile/2

            x2 = self.tailleTuile * selection2.posX + self.tailleTuile/2
            y2 = self.tailleTuile * selection2.posY + self.tailleTuile/2
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="#AAD106", tag="planete")

    def drawFlottes(self, flottes):
        """ affiche la trajectoire de toutes les flottes humaines """
        for flotte in flottes:
            x1 = self.tailleTuile * flotte.planeteDepart.posX + self.tailleTuile/2
            y1 = self.tailleTuile * flotte.planeteDepart.posY + self.tailleTuile/2

            x2 = self.tailleTuile * flotte.planeteArrive.posX + self.tailleTuile/2
            y2 = self.tailleTuile * flotte.planeteArrive.posY + self.tailleTuile/2
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="#BF0E0E", tag="planete")


    def drawPlanetes(self, listePlanetes, selection1, selection2):
        """ affiche les planetes plus un marqueur de selection"""
        for planete in listePlanetes:
            x = self.tailleTuile * planete.posX
            y = self.tailleTuile * planete.posY

            # SELECTION
            if planete == selection1:
                self.canvas.create_image(x-8, y-8, anchor=NW, image=self.selectionImage, tag="planete")

            if planete == selection2:
                self.canvas.create_image(x-8, y-8, anchor=NW, image=self.selectionImage2, tag="planete")
            #PLANETE
            if planete.civilisation == Races.HUMAIN:
                self.canvas.create_image(x, y, anchor=NW, image=self.humainImage, tag="planete")

            elif planete.civilisation == Races.GUBRU:
                self.canvas.create_image(x, y, anchor=NW, image=self.gubruImage, tag="planete")

            elif planete.civilisation == Races.CZIN:
                self.canvas.create_image(x, y, anchor=NW, image=self.czinImage, tag="planete")

            elif planete.civilisation == Races.INDEPENDANT:
                self.canvas.create_image(x, y, anchor=NW, image=self.indieImage, tag="planete")










class Gui(Tk):
    def __init__(self, callBack):
        Tk.__init__(self, None)
        self.callBack = callBack
        self.wm_title("Galax")
        #self.wm_iconbitmap("galax.ico")

        self.selectionPlanete = None  # La planète sélectionnée actuellement

        self.initialize()


    def initialize(self):
        self.configure(background=Color.GRAY)
        self.framePrincipal = Frame(self)
        self.framePrincipal.pack(fill=BOTH)
        self.framePrincipal.grid_rowconfigure(1, weight=1)

        self.framePrincipal.grid_columnconfigure(0, weight=2)
        self.framePrincipal.grid_columnconfigure(1, weight=1)
        self.framePrincipal.grid_columnconfigure(2, weight=1)

        self.initGalaxie()
        self.initBarreInfo()
        self.initBarreCommande()
        self.initConsoles()


    def initBarreInfo(self):
        # Barre de GAUCHE
        self.barreInfo = Frame(self.framePrincipal, width=150, relief=SUNKEN,
                               background=Color.GRAY)
        self.barreInfo.configure(padx=10)
        self.barreInfo.columnconfigure(0, weight=1)
        self.barreInfo.grid(row=0, column=0, sticky=N + W + E + S)

        # LABELS: INFORMATIONS
        # SECTION PLANETE

        self.infoBox = Box(self.barreInfo)
        self.infoBox.background = Color.DARK_GRAY
        self.infoBox.titleBackground = Color.MIDNIGHT_BLUE
        self.infoBox.foreground = "white"

        self.infoBox.configure(relief=SUNKEN, bd=1)
        self.infoBox.insertNewTitle("Planètes")


        # Race Images
        image = ImageTk.PhotoImage(Image.open("img/Human.png"))
        labelHumain = Label(self.infoBox, text=":", foreground=self.infoBox.foreground, compound=LEFT, image=image,
                            anchor=W, justify=LEFT, background=self.infoBox.background)
        labelHumain.image = image

        self.infoBox.insertWidget("Humains:", labelHumain, 0)

        image = ImageTk.PhotoImage(Image.open("img/Czin.png"))
        labelCzin = Label(self.infoBox, text=":", foreground=self.infoBox.foreground, compound=LEFT, image=image,
                          anchor=W, justify=LEFT, background=self.infoBox.background)
        labelCzin.image = image

        self.infoBox.insertWidget("Czin:", labelCzin, 0)

        image = ImageTk.PhotoImage(Image.open("img/Gubru.png"))
        labelCzin = Label(self.infoBox, text=":", foreground=self.infoBox.foreground, compound=LEFT, image=image,
                          anchor=W, justify=LEFT, background=self.infoBox.background)
        labelCzin.image = image

        self.infoBox.insertWidget("Gubru:", labelCzin, 0)

        self.infoBox.insertSeperator(7)

        self.infoBox.insertNewTitle("Inspection")
        self.infoBox.insertLabel("Nom de la planète:", "-")
        self.infoBox.insertLabel("Capacité manufacturière:", "-")
        self.infoBox.insertLabel("Nombre de vaisseaux:", "-")
        self.infoBox.insertSeperator(7)

        self.infoBox.background = Color.MIDNIGHT_BLUE
        self.infoBox.foreground = "white"
        self.infoBox.insertLabel("Année courante:", 0)

        self.infoBox.grid(row=0, column=0, sticky=N + W + E + S)
        self.infoBox.grid_columnconfigure(0, weight=2)


    def initGalaxie(self):
        self.galaxie = Galaxie(self.framePrincipal, 25, 20, 32, self)
        self.galaxie["bd"] = 1
        self.galaxie["background"] = "#000918"
        self.galaxie.height = 640
        self.galaxie.width = 800
        self.galaxie.grid_columnconfigure(0, weight=1)
        self.galaxie.grid(row=0, column=1, sticky=N + E + W + S)


    def initBarreCommande(self):
        self.barreCommande = Frame(self.framePrincipal, width=150, height=self.galaxie.height, background=Color.GRAY)
        self.barreCommande.grid(row=0, column=2, sticky=N + W + E + S)

        self.barreCommande.configure(padx=10)
        self.barreCommande.columnconfigure(0, weight=1)

        self.commandBox = Box(self.barreCommande)
        self.commandBox.background = Color.DARK_GRAY
        self.commandBox.titleBackground = Color.MIDNIGHT_BLUE
        self.commandBox.foreground = "white"

        self.commandBox.configure(relief=SUNKEN, bd=1)
        self.commandBox.insertNewTitle("Flottes")
        self.commandBox.insertLabel("Départ:", "-")
        self.commandBox.insertLabel("Destination:", "-")
        self.commandBox.insertLabel("Distance:", "-")
        self.commandBox.insertSeperator()

        self.commandBox.titleBackground = self.commandBox.background
        self.commandBox.insertNewTitle("Nombre de vaisseaux")
        self.nbVaisseauxWidget = BarreAugmentation(self.commandBox, 0)
        self.nbVaisseauxWidget.commande = self.notifyFlotteChange
        self.commandBox.insertWidget("nbVaisseaux", self.nbVaisseauxWidget)
        self.commandBox.insertSeperator(3)

        self.btnValiderDeplacement = Button(self.commandBox, text="Valider le déplacement",
                                            command=self.notifyValiderDeplacement)
        self.commandBox.insertWidget("validerDeplacement", self.btnValiderDeplacement)
        self.commandBox.insertSeperator(3)

        self.btnTerminerTour = Button(self.commandBox, text="Terminer le tour", command=self.notifyTerminerTour)
        self.commandBox.insertWidget("terminerTour", self.btnTerminerTour)
        self.commandBox.grid(row=0, column=0, sticky=N + W + E + S)
        self.commandBox.grid_columnconfigure(0, weight=1)


    def initConsoles(self):
        separateur = Frame(self.framePrincipal, height=20, background=Color.GRAY)
        separateur.grid(row=1, column=0, columnspan=3, sticky=N + W + E + S)

        self.consolesFrame = Frame(self.framePrincipal, height=self.galaxie.height, relief=SUNKEN, bd=1,
                                   background=Color.BLACK)
        self.consolesFrame.grid(row=2, column=0, columnspan=3, sticky=N + W + E + S)

        self.update_idletasks()

        #Console Humains
        self.consoleHumains = Console(self.consolesFrame, 10)
        self.consoleHumains.grid(row=0, column=0, sticky=N + W + E + S)
        self.consoleHumains.configure(background=Color.GRAY)
        self.consolesFrame.grid_columnconfigure(0, weight=1)
        #Console Ennemis
        self.consoleEnnemis = Console(self.consolesFrame, 10)
        self.consoleEnnemis.grid(row=0, column=1, sticky=N + W + E + S)

        self.consolesFrame.grid_columnconfigure(0, weight=1)


    # MÉTHODES POUR LE CONTRÔLEUR
    def run(self):
        """ Permet de lancer la boucle evenementielle principale du GUI """
        self.mainloop()

    def rafraichir(self, data):
        """ rafraichit le panneau des infos des civilisations+la zone de jeu """
        self.galaxie.draw(data)

        self.infoBox.setValue("Humains:", data["nbPlanetesHumain"])
        self.infoBox.setValue("Gubru:",  data["nbPlanetesGubru"])
        self.infoBox.setValue("Czin:",  data["nbPlanetesCzin"])

        self.infoBox.setValue("Année courante:", data["anneeCourante"])


    def inspecterPlanete(self, nom, x, y, capacite=None, nbVaisseaux=None):
        """ Permet d'inspecter une planete grace au "panneau planete" (infoBox)"""
        self.infoBox.setValue("Nom de la planète:", nom)  # TODO inspecter planete

        if not capacite:
            capacite = "-"
        self.infoBox.setValue("Capacité manufacturière:", capacite)

        if not nbVaisseaux:
            nbVaisseaux = "-"
            self.nbVaisseauxWidget.min = 0
            self.nbVaisseauxWidget.max = 0
        # TODO vérification planète humaine ou non
        self.infoBox.setValue("Nombre de vaisseaux:", nbVaisseaux)

    def rafraichirFlotte(self, data):
        """ Raffraichit le panneau Flotte """
        pass  # TODO Rafraichir flotte
        if not data["planeteDepart"]:
            data["planeteDepart"] = "-"
        self.commandBox.setValue("Départ:", data["planeteDepart"]) #TODO mettre le nom

        if not data["planeteArrivee"]:
            data["planeteArrivee"] = "-"
        self.commandBox.setValue("Destination:", data["planeteArrivee"])

        if not data["distance"]:
            data["distance"] = "-"
        self.commandBox.setValue("Distance:", data["distance"])


    def getNbVaisseaux(self):
        """ Retourne le nombre de vaisseaux entres par l'utilisateur """
        return self.nbVaisseauxWidget.valeur.get()

    def resetNombreVaisseaux(self):
        self.nbVaisseauxWidget.valeur.set(0)
        self.nbVaisseauxWidget.labelValeur.configure(text=self.nbVaisseauxWidget.valeur.get())


    # ACTIVATION/DESACTIVATION WIDGET DU GUI #
    def activerFinTour(self, bool):
        """ permet d'activer/desactiver btn fin tour """
        if bool:
            bool = 'active'
        else:
            bool = 'disabled'
        self.btnTerminerTour.configure(state=bool)

    def activerValiderDeplacement(self, bool):
        """ permet d'activer/desactiver btn fin tour """
        if bool:
            bool = 'active'
        else:
            bool = 'disabled'
        self.btnValiderDeplacement.configure(state=bool)

    def activerBarreAugmentation(self, bool):
        """ permet d'activer/desactiver la barre  nb vaisseaux flotte """
        self.nbVaisseauxWidget.activer(bool)



    # NOTIFICATION D'ENTRÉE UTILISATEUR

    def notifyPlanetClick(self, event):
        """ lorsque que l'on clique sur l'aire de jeux """
        x = int(event.x / self.galaxie.tailleTuile)
        y = int(event.y / self.galaxie.tailleTuile)
        coord = (x, y)
        self.callBack(UserActions.SELECT_PLANETE, coord)

    def notifyPlanetRightClick(self, event):
        x = int(event.x / self.galaxie.tailleTuile)
        y = int(event.y / self.galaxie.tailleTuile)
        coord = (x, y)
        self.callBack(UserActions.SELECT_PLANETE_2, coord)



    def notifyValiderDeplacement(self):
        """ lorsque le bouton valider déplacement est termine """
        self.callBack(UserActions.VALIDER_DEPLACEMENT)

    def notifyTerminerTour(self):
        """ lorsque le bouton terminer tour est presse """
        self.callBack(UserActions.VALIDER_TOUR)

    def notifyFlotteChange(self):
        """ si on augmente ou reduit le nombre de vaisseaux """
        self.callBack(UserActions.FLOTTE_CHANGEMEMT)


### CUSTOM WIDGETS #####


class Box(Frame):
    def __init__(self, parent):
        #Default Color values

        self.titleBackground = "red"
        self.titleForeground = "white"
        self.background = "white"
        self.foreground = "black"

        Frame.__init__(self, parent, width=100, height=100)
        self.values = {}  #A dictionnary containing the values for each label
        self.currentRow = 0

    def insertImage(self, labelStr, imagePath, value=None):
        img = ImageTk.PhotoImage(Image.open(imagePath))
        labelHumain = Label(self.infoBox, compound=TOP, image=img, background=self.background)
        labelHumain.image = img
        if (value != None):
            Label(self, text=value, anchor=W, justify=LEFT, background=self.background,
                  foreground=self.foreground).grid(row=self.currentRow, column=1, sticky=N + W + E + S)
        self.values[labelStr] = (value, self.currentRow)
        self.currentRow += 1


    def insertLabel(self, labelStr, value=None):
        Label(self, text=labelStr, anchor=W, justify=LEFT, background=self.background, foreground=self.foreground).grid(
            row=self.currentRow, column=0, sticky=N + W + E + S)
        if (value != None):
            Label(self, text=value, anchor=W, justify=LEFT, background=self.background,
                  foreground=self.foreground).grid(row=self.currentRow, column=1, sticky=N + W + E + S)

        self.values[labelStr] = (value, self.currentRow)
        self.currentRow += 1

    def getValue(self, labelStr):
        return self.values[labelStr][0]

    def setValue(self, labelStr, newValue):
        theRow = self.values[labelStr][1]
        self.values[labelStr] = (newValue, theRow)
        Label(self, text=newValue, anchor=W, justify=LEFT, background=self.background, foreground=self.foreground).grid(
            row=theRow, column=1, sticky=N + W + E + S)


    def insertSeperator(self, number=1):
        for i in range(number):
            Label(self, text="", anchor=W, justify=LEFT, background=self.background).grid(row=self.currentRow, column=0,
                                                                                          columnspan=2,
                                                                                          sticky=N + W + E + S)
            self.currentRow += 1

    def insertWidget(self, widgetName, widget, value=None):
        widget.grid(row=self.currentRow, column=0, columnspan=2, sticky=N + W + E + S)

        if (value != None):
            Label(self, text=value, anchor=W, justify=LEFT, background=self.background,
                  foreground=self.foreground).grid(row=self.currentRow, column=1, sticky=N + W + E + S)

        self.values[widgetName] = (value, self.currentRow)
        self.currentRow += 1

    def insertNewTitle(self, title, hasStyle=True):
        if (hasStyle):
            Label(self, text=title, anchor=W, justify=LEFT, background=self.titleBackground,
                  foreground=self.titleForeground).grid(row=self.currentRow, column=0, columnspan=2,
                                                        sticky=N + W + E + S)
        else:
            Label(self, text=title, anchor=W, justify=LEFT, background=self.background,
                  foreground=self.titleForeground).grid(row=self.currentRow, column=0, columnspan=2,
                                                        sticky=N + W + E + S)
        self.currentRow += 1


class Console(Frame):
    def __init__(self, parent, hauteur):
        Frame.__init__(self, parent)

        self.console = Text(self, height=hauteur)

        #Scroll bar
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.console.yview)
        scrollbar.grid(row=0, column=1, sticky=N + S + E + W)

        self.console["yscrollcommand"] = scrollbar.set
        self.console.configure(background=Color.DARK_GRAY)
        self.console.configure(foreground=Color.GREEN)
        self.console.configure(state=DISABLED)

        self.console.grid(row=0, column=0, sticky=N + E + W + S)


    def insert(self, message):
        self.console.config(state=NORMAL)
        self.console.insert(END, message + "\n")
        self.console.config(state=DISABLED)

    def victoirePlanete(self, annee, race, planete):  # TODO planete
        message = "[Année: %s] Les %s ont obtenu la planète %s" % (annee, race,planete)
        self.insert(message)

    def affrontemenPlanete(self,annee, attanquant, defenseur, planete):
        message = "[Année: %s] Les %s ont attaqué les %s sur %s" % (annee, attanquant, defenseur, planete)
        self.insert(message)

    def defensePlanete(self, annee, defenseur, attaquant, planete):
        message = "[Année: %s] Les %s ont défendu avec succes %s contre les %s" % (annee, defenseur, planete, attaquant)
        self.insert(message)

    def pertePlanete(self, annee, defenseur, attaquant, planete):
        message = "[Année: %s] Les %s ont perdu %s au main des %s" % (annee, defenseur, planete, attaquant)
        self.insert(message)

    def annihilationRace(self, race):
        message = "[Année: %s] Les %s ont été annihilé"
        self.insert(message)

class BarreAugmentation(Frame):
    def __init__(self, parent, max, min=0, step=1):
        Frame.__init__(self, parent, height=60, background="blue")



        #Parameteres
        self.valeur = IntVar()
        self.valeur.set(0)
        self.step = 1
        self.min = 0
        self.max = max

        self.commande = None  #La commande à appaler en cas d'action event



        #GUI
        self.boutonAug = Button(self, text=" + ", command=self.augmenter)  #augmenter
        self.labelValeur = Label(self, text=self.valeur.get())
        self.boutonRed = Button(self, text=" - ", command=self.reduire)  #Réduire

        self.boutonRed.grid(column=0, row=0, sticky=N + W + E + S)
        self.labelValeur.grid(column=1, row=0, sticky=N + W + E + S)
        self.boutonAug.grid(column=2, row=0, sticky=N + W + E + S)
        self.grid_columnconfigure(1, weight=1)


    def augmenter(self):
        self.valeur.set(self.valeur.get() + self.step)
        if (self.valeur.get() > self.max):
            self.valeur.set(self.max)
        self.labelValeur.configure(text=self.valeur.get())
        self.commande()


    def reduire(self):
        self.valeur.set(self.valeur.get() - self.step)
        if (self.valeur.get() < self.min):
            self.valeur.set(self.min)
        self.labelValeur.configure(text=self.valeur.get())
        self.commande()


    def activer(self, bool):
        """ permet d'activer/desactiver le widget """
        if bool:
            bool = 'active'
        else:
            bool = 'disabled'
        self.boutonAug.configure(state=bool)
        self.boutonRed.configure(state=bool)
        self.labelValeur.configure(state=bool)


def main():
    gui = Gui(None)
    gui.run()


if __name__ == '__main__':
    main()

# TODO TESTS
# TESTER SI L'AFFICHAGE FONCTIONNE
# TESTER L'ACTIVATION DÉSACTIVATION DES WIDGETS
