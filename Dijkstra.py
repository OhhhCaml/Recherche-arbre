import numpy as np
import Grib as grib
import file_prioritaire as fp
##Approximations :
##  Interpolation est faite à chaque coordonnée en fonction du temps et selon un axe
##  Force du vent et non force du vent relative (il suffit de décaler les fonctions)

class chemin :
    def __init__(self) :
        self.__cout = -1
        self.__liste = []
        self.__tab = []

    def longueurMax(self, grib) :
        self.__tab = [[False for j in range(grib.longueur_())] for i in range(grib.hauteur_())]

    def longueur(self) :
        return len(self.__liste)

    def ajouter_point(self, point, cout) :
        if self.__cout == -1 :
            self.__cout = 0
        else :
            self.__cout += cout
        self.__liste.append(point)
        self.__tab[point[0]][point[1]] = True

    def dernier_point(self) :
        return self.__liste[-1]

    def contient(self, point) :
        return self.__tab[point[0]][point[1]]

    def cout(self) :
        return self.__cout

    def list(self) :
        return(self.__liste)
    
    def __str__(self) :
        s = ""
        s += "[" + str(self.__cout) + "] " + str(self.__liste)
        return s

    def compare_chemin(c1, c2) :
        return c1.__cout < c2.__cout

    def copy(self) :
        r = chemin()
        r.__cout = self.__cout
        r.__liste = self.__liste.copy()
        r.__tab = self.__tab.copy()
        return r


chemin_base = chemin()

def dijkstra(grib, depart, arrive) :
    n = grib.ordre()
    file = fp.file_prioritaire(chemin.compare_chemin, chemin_base)
    c = chemin()
    c.longueurMax(grib)
    c.ajouter_point(depart, 0)
    file.enfile(c)
    i = depart
    c = file.defile()
    while i != arrive :
        for j in grib.voisin(i):
            nc = c.copy()
            if not nc.contient(j):
                if nc.cout() > 72 : print("Trop tard ")
                nc.ajouter_point(j, (grib.temps_de_parcours(i,j,nc.cout())))
                file.enfile(nc)
        c = file.defile()
        i = c.dernier_point()
    return c
