#!/usr/bin/python32
# -*- coding: utf-8 -*-
#Python 3.x


try:
    from tkinter import *
    from tkinter import ttk

except (ImportError):
    from Tkinter import *
    import ttk




try:
    from PIL import Image
    from PIL import ImageTk

    BASIC_MODE = False
except(ImportError):
    BASIC_MODE = True

from UserActions import *


class Color():
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
        if (BASIC_MODE):
            self.arrierePlan = PhotoImage(file="img/fond.gif")
            self.gubruImage = PhotoImage(file="img/purple.gif")
            self.czinImage = PhotoImage(file="img/fire.gif")
            self.humainImage = PhotoImage(file="img/blue.gif")
            self.indieImage = PhotoImage(file="img/white.gif")
        else:
            self.arrierePlan = ImageTk.PhotoImage(Image.open("img/fond.jpg"))

            self.gubruImage = ImageTk.PhotoImage(Image.open("img/purple.png"))
            self.czinImage = ImageTk.PhotoImage(Image.open("img/fire.png"))
            self.humainImage = ImageTk.PhotoImage(Image.open("img/blue.gif"))
            self.indieImage = ImageTk.PhotoImage(Image.open("img/white.png"))

        self.canvasLargeur = nbColonnes * tailleTuile
        self.canvasHauteur = nbLignes * tailleTuile

        Frame.__init__(self, parent)

        self.canvas = Canvas(self, width=self.canvasLargeur, height=self.canvasHauteur, background="#000918",
                             highlightthickness=0)

        self.canvas.grid(column=0, row=0, sticky=N+S)

        #Dessiner la canvas






        #Écouteur d'événements
        self.canvas.bind("<Configure>", self.raffraichirArrierePlan)
        self.canvas.bind("<Button-1>", self.app.notifyPlanetClick)

    def raffraichirArrierePlan(self, event):
        print(( self.canvas.winfo_width(),self.canvas.winfo_height()))
        image = Image.open("img/fond.jpg")
        self.arrierePlan = image.resize(( self.canvas.winfo_width(),self.canvas.winfo_height()), Image.ANTIALIAS)
        self.arrierePlan = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.arrierePlan)


    def draw(self, listePlanete):
        self.canvas.delete("planet")
        for planet in listePlanete: # TODO afficher les planètes
            x = self.tailleTuile * planete.x + self.tailleTuile
            y = self.tailleTuile * planete.y + self.tailleTuile
            if planet.race == Race.HUMAINS:
                self.canvas.create_image(x, y, self.humainImage)
            elif planet.race == Race.GUBRU:
                self.canvas.create_image(x, y, self.gubruImage)
            elif planet.race == Race.CZIN:
                self.canvas.create_image(x, y, self.czinImage)
            elif planet.race == Race.INDEPENDANT:
                self.canvas.create_image(x, y, self.indieImage)



                #for ligne in range(0, self.nbLignes):
                #for colonne in range(0, self.nbColonnes):
                # x1 = colonne * self.tailleTuile
                #y1 = (ligne * self.tailleTuile)
                #x2 = x1 + self.tailleTuile
                #y2 = y1 + self.tailleTuile

                # Dessiner les différentes planètes avec leurs nom
                # self.canvas.create_text()


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

        self.infoBox.insertWidget("Gurbu:", labelCzin, 0)





        self.infoBox.insertSeperator(10)

        self.infoBox.insertNewTitle("Inspection")
        self.infoBox.insertLabel("Nom de la planète:", "-")
        self.infoBox.insertLabel("Capacité manufacturière:", "-")
        self.infoBox.insertLabel("Nombre de vaisseaux:", "-")
        self.infoBox.insertSeperator(10)

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
        self.galaxie.grid(row=0, column=1, sticky=N+E+W+S)


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
        self.commandBox.insertSeperator(5)

        self.commandBox.insertWidget("validerDeplacement", Button(self.commandBox, text="Valider le déplacement",
                                                                  command=self.notifyValiderDeplacement))
        self.commandBox.insertSeperator(5)
        self.commandBox.insertWidget("terminerTour",
                                     Button(self.commandBox, text="Terminer le tour", command=self.notifyTerminerTour))
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
        self.mainloop()

    def rafraichir(self, anneeCourante, listePlanetes, nbPlaneteHumains, nbPlaneteGubru, nbPlaneteCzin):
        self.galaxie.draw(self, listePlanetes)

        self.infoBox.setValue("Nom de la planète:", self.selectionPlanete.nom)
        self.infoBox.setValue("Capacité manufacturière:", self.selectionPlanete.capacite)
        self.infoBox.setValue("Nombre de vaisseaux:", self.selectionPlanete.nbVaisseaux)
        self.infoBox.setValue("Année courante:", anneeCourante)


    def inspecterPlanete(self, nom, capacite, nbVaisseaux):
        self.infoBox.setValue("Nom de la planète:", nom) # TODO inspecter planète

        if not capacite:
            capacite = "-"
        self.infoBox.setValue("Capacité manufacturière:", capacite)

        if not nbVaisseaux:
            nbVaisseaux = "-"
            self.nbVaisseauxWidget.min = 0
            self.nbVaisseauxWidget.max = 0
        self.infoBox.setValue("Nombre de vaisseaux:", nbVaisseaux)

    def rafraichirFlotte(self, flotte):
        pass # TODO Rafraichir flotte


    def getNbVaisseaux(self):
        return self.nbVaisseauxWidget.valeur.get()





    # NOTIFICATION D'ENTRÉE UTILISATEUR

    def notifyPlanetClick(self, event):
        x = int(event.x/self.galaxie.tailleTuile)
        y = int(event.y/self.galaxie.tailleTuile)
        coord = (x,y)
        self.callBack(UserActions.SELECT_PLANETE, coord)

    def notifyValiderDeplacement(self):
        self.callBack(UserActions.VALIDER_DEPLACEMENT)

    def notifyTerminerTour(self):
        self.callBack(UserActions.VALIDER_TOUR)

    def notifyFlotteChange(self):
        """ si on augmente ou réduit le nombre de vaisseaux """
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

    def victoirePlanete(self, race, planete): # TODO planete
        self.insert(race + " à obtenu la planète " + planete)


class BarreAugmentation(Frame):
    def __init__(self, parent, max, min=0, step=1):
        Frame.__init__(self, parent, height=60, background="blue")



        #Parameteres
        self.valeur = IntVar()
        self.valeur.set(0)
        self.step = 1
        self.min = 0
        self.max = max

        self.commande = None #La commande à appaler en cas d'action event



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



def main():
    gui = Gui(None)
    gui.run()


if __name__ == '__main__':
    main()
