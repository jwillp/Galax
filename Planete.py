# classe Planete
class Planete:
    def __init__(self):
        self.nomPlanete
        self.civilisation # quelle civilisation occupe cette planete (humain, Czins, Gubru ou non-colonisateurs)
        self.isPlaneteMere # methode qui definit par un booleen si cette planete est une planete d'origine des civilisations colonisatrices 
        self.positionX # coordonnee x d'une planete
        self.positionY # coordonnee y d'une planete
        self.nbManufactures  # nombre de manufactures de vaisseaux (1 a 6 actives sur la planete)
        self.capaciteManufacturiere # nombre de vaisseaux qu'une manufacture peut faire par annee * nombre de manufactures 
        self.niveauConnaissance  # le niveau de connaissance de l'humain pour cette planète (1,2 ou 3)
        self.nbvisites # nombre de fois que l'humain a visite cette planete
        self.Vaisseaux # nombre de vaisseaux que possede la planete


