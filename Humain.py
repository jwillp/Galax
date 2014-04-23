# classe humain
class Humain:
    def __init__(self):
        self.pointage = 0
        self.nombreVaisseaux = 0
        self.nombreManufactures = 0
        self.nombrePlanetesOccupees = 1 # l'etoile-mere est evidemment la 1ere etoile occupee donc initialisee a 1
        self.puissanceAttaque = 0 # a definir selon une fonction random au debut du jeu
        self.etoileMere = 0 # coordonnees pour identifier l'etoile-mere du joueur initialisee au hasard depuis le debut
        getEtoiles() # appel a la methode pour conquerir d'autres planetes    
        Humain.isDead() # methode declarant que le joueur a perdu la partie
