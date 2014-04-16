#!/usr/bin/python
# -*- coding: utf-8 -*-
#Python 3.x


from GuiGoat import *
from tkinter import *


class Color():
    GRAY = "#3C3F41"
    LIGHT_GRAY = "#525556"
    DARK_GRAY = "#2B2B2B"


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
        self.framePrincipal.grid_rowconfigure(0, weight=1)
        self.framePrincipal.grid_columnconfigure(1, weight=1)


        self.initGalaxie()
        self.initBarreInfo()
        self.initBarreCommande()
        self.initConsoles()



    def initBarreInfo(self):
        self.barreInfo = Frame(self.framePrincipal, width=120, height=self.galaxie.height, relief=SUNKEN,
                               background=Color.GRAY)
        self.barreInfo.grid(row=0, column=1, sticky=N+E)


    def initBarreCommande(self):
        self.barreCommande = Frame(self.framePrincipal, height=120, width=self.galaxie.width,
                                   background=Color.GRAY)
        self.barreCommande.grid(row=1, column=0)


    def initGalaxie(self):
        self.galaxie = Galaxie(self.framePrincipal, 25, 20, 32, self)
        self.galaxie["bd"] = 1
        self.galaxie["background"] = Color.LIGHT_GRAY
        self.galaxie.height = 640
        self.galaxie.width = 800
        self.galaxie.grid(row=0, column=0)

    def initConsoles(self):

        self.consolesFrame = Frame(self.framePrincipal, width=120, height=self.galaxie.height, background="green")
        self.consolesFrame.grid(row=0, column=2, sticky=N+E)


        self.initConsoleHumains()
        self.initConsoleEnnemis()




    def initConsoleHumains(self):
        self.consoleHumainsFrame = Frame(self.consolesFrame, width=120, height=self.galaxie.height, background="green")

        self.consoleHumains = Text(self.consoleHumainsFrame, width=25)

        scrollbar=Scrollbar(self.consoleHumainsFrame, orient=VERTICAL, command=self.consoleHumains.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.consoleHumains["yscrollcommand"]=scrollbar.set
        self.consoleHumains.configure(background="#000000")
        self.consoleHumains.configure(foreground="green")

        self.consoleHumains.pack(side=LEFT, fill=BOTH, expand=YES)

        self.consoleHumainsFrame.pack(side=LEFT)

    def initConsoleEnnemis(self):
        self.consoleEnnemisFrame = Frame(self.consolesFrame, width=120, height=self.galaxie.height, background="red")
        self.consoleEnnemisFrame.grid_propagate(False)

        self.consoleEnnemis = Text(self.consoleEnnemisFrame, width=25, height=0)
        scrollbar=Scrollbar(self.consoleEnnemisFrame, orient=VERTICAL, command=self.consoleEnnemis.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.consoleEnnemis["yscrollcommand"]=scrollbar.set
        self.consoleEnnemis.configure(background="#000000")
        self.consoleEnnemis.configure(foreground="green")


        self.consoleEnnemis.pack(side=LEFT, fill=BOTH, expand=YES)

        self.consoleEnnemisFrame.pack(side=LEFT)





    def run(self):
        self.mainloop()

    def refresh(self, listePlanets):
        self.listePlanet
        pass

    def raffraichirJeu(self, listePlanetes):
        self.galaxie.draw(self, listePlanetes)



    def notifyClick(self):
        pass


def main():
    gui = Gui(None)
    gui.run()


if __name__ == '__main__':
    main()
