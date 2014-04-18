#!/usr/bin/python
# -*- coding: utf-8 -*-
#Python 3.x


from GuiGoat import *
from tkinter import *
from tkinter import ttk


class Color():
    GRAY = "#3C3F41"
    LIGHT_GRAY = "#525556"
    DARK_GRAY = "#2B2B2B"
    GREEN = "#3AB35B"
    RED = "#D35F51"
    BLACK = "#27292A"


class Galaxie(Frame):
    """ Galaxie """

    def __init__(self, parent, nbColonnes, nbLignes, tailleTuile, app):
        self.parent = parent
        self.app = app  # La classe principale du GUI
        self.nbColonnes = nbColonnes
        self.nbLignes = nbLignes
        self.tailleTuile = tailleTuile  # taille d'une case en pixel


        # Images
        self.arrierePlan = PhotoImage(file="img/fond.gif")
        self.gubruImage = PhotoImage(file="img/purple.gif")
        self.czinImage = PhotoImage(file="img/fire.gif")
        self.humainImage = PhotoImage(file="img/fire.gif")
        self.indieImage = PhotoImage(file="img/white.gif")

        canvasLargeur = nbColonnes * tailleTuile
        canvasHauteur = nbLignes * tailleTuile

        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=canvasLargeur, height=canvasHauteur, background=Color.DARK_GRAY,
                             highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=TRUE)

        #Dessiner la canvas

        self.canvas.create_image(0, 0, anchor=NW, image=self.arrierePlan)


        #Écouteur d'événements
        self.canvas.bind("<Button-1>", self.app.notifyClick)


    def draw(self, listePlanete):
        self.canvas.delete("planet")
        for planet in listePlanete:
            x = self.tailleTuile*planete.x+self.tailleTuile
            y = self.tailleTuile*planete.y+self.tailleTuile
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
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.title = "Galax"
        #self.wm_iconbitmap("galax.ico")

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
        self.barreInfo = Frame(self.framePrincipal, width=150,  relief=SUNKEN,
                              background=Color.GRAY)
        self.barreInfo.columnconfigure(1, weight=1)
        self.barreInfo.grid(row=0, column=0, sticky=N+W+E+S)

        # LABELS: INFORMATIONS
        Label(self.barreInfo, text="Planètes", anchor=W, justify=LEFT, background=Color.GRAY).grid(row=0, column=0)

        Label(self.barreInfo, text="Humains:", anchor=W, justify=LEFT).grid(row=1, column=0)
        self.labelNbHumains = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=1, column=1)

        Label(self.barreInfo, text="Czin:", anchor=W, justify=LEFT).grid(row=2, column=0)
        self.labelNbCzin = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=2, column=1)

        Label(self.barreInfo, text="Gubru:").grid(row=3, column=0)
        self.labelNbGubru = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=3, column=1)

        Label(self.barreInfo, text="Inspection:").grid(row=4, column=0)

        Label(self.barreInfo, text="Capacité manufacturière:").grid(row=5, column=0)
        self.labelCapManu = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=5, column=1)

        Label(self.barreInfo, text="Nombre de vaisseaux:").grid(row=6, column=0)
        self.labelNbVaisseaux = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=6, column=1)

        Label(self.barreInfo, text="Année courante:", anchor=W, justify=LEFT).grid(row=7, column=0)
        self.labelAnnee = Label(self.barreInfo, text=0,  anchor=W, justify=LEFT).grid(row=7, column=1)




    def initGalaxie(self):

        self.galaxie = Galaxie(self.framePrincipal, 25, 20, 32, self)
        self.galaxie["bd"] = 1
        self.galaxie["background"] = "black"
        self.galaxie.height = 640
        self.galaxie.width = 800
        self.galaxie.grid(row=0, column=1, sticky=N+E+W+S)





    def initBarreCommande(self):
        self.barreCommande = Frame(self.framePrincipal, width=150, height=self.galaxie.height, background=Color.GRAY)
        self.barreCommande.grid(row=0, column=2, sticky=N+W+E+S)









    def initConsoles(self):

        separateur = Frame(self.framePrincipal, height=20, background=Color.GRAY)
        separateur.grid(row=1, column=0, columnspan=3, sticky=N+W+E+S)

        self.consolesFrame = Frame(self.framePrincipal, height=self.galaxie.height, relief=SUNKEN, bd=1, background=Color.BLACK)
        self.consolesFrame.grid(row=2, column=0, columnspan=3, sticky=N+W+E+S)

        self.update_idletasks()

        #Console Humains
        self.consoleHumains = Console(self.consolesFrame, 65, 10)
        self.consoleHumains.console.configure(foreground=Color.GREEN)
        #self.consoleHumains.pack(side=LEFT, fill=X)
        self.consoleHumains.grid(row=0, column=0)

        #Console Ennemis
        self.consoleEnnemis = Console(self.consolesFrame, 67, 10)
        self.consoleEnnemis.console.configure(foreground=Color.RED)
        #self.consoleEnnemis.pack(side=LEFT, fill=X)
        self.consoleEnnemis.grid(row=0, column=1, sticky=N+E+S+W)


    def run(self):
        self.mainloop()

    def refresh(self, listePlanets):
        self.listePlanet
        pass

    def rafraichirJeu(self, anneeCourante, listePlanetes):
        self.galaxie.draw(self, listePlanetes)




    def notifyClick(self, event):
        pass






class Console(Frame):
    def __init__(self, parent, largeur, hauteur):
        Frame.__init__(self,parent)

        self.console = Text(self, width=largeur, height=hauteur)

        #Scroll bar
        scrollbar= ttk.Scrollbar(self, orient=VERTICAL, command=self.console.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.console["yscrollcommand"]=scrollbar.set
        self.console.configure(background=Color.DARK_GRAY)
        self.console.configure(foreground=Color.GREEN)
        self.console.configure(state=DISABLED)

        self.console.pack(side=LEFT, fill=BOTH, expand=YES)

    def insert(self, message):
        self.console.config(state=NORMAL)
        self.console.insert(END, message + "\n" )
        self.console.config(state=DISABLED)

    def victoirePlanete(self, race, planete):
        self.insert(race + " à obtenu la planète " + planete)
















def main():
    gui = Gui(None)
    gui.run()


if __name__ == '__main__':
    main()
