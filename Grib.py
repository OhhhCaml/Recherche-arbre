import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import os
import force_to_temps as ftt

##2 fonctions 'utiles':
##temps_de_parcours(i,j,t): renvoie le temps de parcours pour aller de i à j au moment t (i,j deux voisins)
##ordre(self): renvoie le nombre de sommet


class Grib:    
    def __init__(self,force_to_temps = ftt.force_to_temps, type_d_interpolation = 'linear'):
        self.__u = np.genfromtxt('u-component_of_wind_height_above_ground.csv', delimiter = ',')
        self.__v = np.genfromtxt('v-component_of_wind_height_above_ground.csv', delimiter = ',')
        self.__type_intepolation = type_d_interpolation
        self.__time = np.genfromtxt('time.csv', delimiter = ',')
        self.__duree = len(self.__time)
        self.__lon = np.genfromtxt('lon.csv', delimiter = ',')
        self.__lat = np.genfromtxt('lat.csv', delimiter = ',')
        self.__longueur = len(self.__lon)
        self.__hauteur = len(self.__lat)
        self.__u_extr = np.zeros([2,self.__hauteur,self.__longueur])
        self.__v_extr = np.zeros([2,self.__hauteur,self.__longueur])
        self.__ftp = force_to_temps
        self.__matfu = [[-1  for y in range(self.__longueur)] for x in range(self.__hauteur)]
        self.__matfv = [[-1  for y in range(self.__longueur)] for x in range(self.__hauteur)]
    
    def u_min(self):
        #Pour A*
        lu = len(self.__u)
        c = np.transpose(self.__u)[0:self.__longueur]
        for i in range(self.__hauteur):
            for j in range(self.__longueur):
                # c[0:longueur][i] : i-ième colonne
                # c[0:longueur][i][0:lu:hauteur] : toutes les valeurs de la case i j
                tab = c[0:self.__longueur][j][i:lu:self.__hauteur]
                self.__u_extr[0,i,j] = np.min(tab)
                self.__u_extr[1,i,j] = np.max(tab)

    def v_min(self):
        #Pour A*
        lv = len(self.__v)
        c = np.transpose(self.__v)[0:self.__longueur]
        for i in range(self.__hauteur):
            for j in range(self.__longueur):
                # c[0:longueur][j] : i-ième colonne
                # c[0:longueur][j][i:lu:hauteur] : toutes les valeurs de la case i j
                tab = c[0:self.__longueur][j][i:lv:self.__hauteur]
                self.__v_extr[0,i,j] = np.min(tab)
                self.__v_extr[1,i,j] = np.max(tab)


    def ordre(self):
        ##Renvoie le nombre de sommet
        return(self.__hauteur * self.__longueur)

    def hauteur_(self):
        ##Renvoie le nombre de coordonnée de latitude
        return(self.__hauteur)

    def longueur_(self):
        ##Renvoie le nombre de coordonée de longitude
        return(self.__longueur)

    def maxima(self):
        #Renvoie les maxima de partout
        u = max(np.abs(np.min(self.__u)), np.max(self.__u))
        v = max(np.abs(np.min(self.__v)), np.max(self.__v))
        return(u,v)

    def vent(self,point):
        #Renvoie deux tableaux de vent selon u et v de la force
        (i,j) = point
        c1 = np.transpose(self.__v)[0:self.__longueur]
        tab1 = c1[0:self.__longueur][j][i:len(self.__v):self.__hauteur]
        c2 = np.transpose(self.__u)[0:self.__longueur]
        tab2 = c2[0:self.__longueur][j][i:len(self.__u):self.__hauteur]
        return(tab2,tab1)
    
    def voisin(self, p):
        #p : couple (i,j)
        #renvoie la liste des tuples correspondant aux voisins de p
        l = []
        (i,j) = p
        if i > 0:
            l.append( (i-1,j))
        if  i < self.__hauteur-1:
            l.append((i+1,j))
        if j > 0:
            l.append((i,j-1))
        if j < self.__longueur-1:
            l.append((i,j+1))
        return(l)

    def interpol(self,point):
            #Si l'interpolation en ce point n'est pas faite, elle la fait, sinon elle ne fait rien
            #Point où on effectue l'interpolation en fonction du tps
            #t : on cherche le vent a ce moment là
            #Force_vers_temps : prend en argument les coordonnées (i,j) d'un point et le temps t pour renvoyer la valeur de u et v sur ce point au moment t

        (i,j) = point
        tdp = self.__matfu[i][j]
        if tdp == -1 :
            matu, matv = self.vent(point)
            i_u = interpolate.interp1d(self.__time, matu, self.__type_intepolation)
            i_v = interpolate.interp1d(self.__time, matv, self.__type_intepolation)
            self.__matfu[i][j] =  i_u
            self.__matfv[i][j] =  i_v


    def temps_de_parcours(self,depart,arrive,t):
        ##Renvoie le temps de parcours pour aller de i à j au moment t
        (i_d,j_d) = depart
        (i_a,j_a) = arrive
        self.interpol(depart)
    
        if i_a == (i_d - 1) and j_a == j_d:
                #---
                #-d-
                #-a-
            return( float( self.__ftp(-self.__matfv[i_d][j_d](t))))

        if i_a == (i_d + 1) and j_a == j_d:
                #-a-
                #-d-
                #---
            return( float( self.__ftp( self.__matfv[i_d][j_d](t))))
        if i_a == i_d and j_a == (j_d+1):
                #---
                #-da
                #---
            return( float( self.__ftp( self.__matfu[i_d][j_d](t))))
        if i_a == i_d and j_a == (j_d-1):
                #---
                #ad-
                #---
            return( float( self.__ftp(-self.__matfu[i_d][j_d](t))))
        print('Erreur Grib.py, temps de parcours')
    def lat(self):
        return(self.__lat)

    def lon(self):
        return(self.__lon)

    def grille_vent(self,t):
        t1 = int(t)
        u_ = self.__u[self.__hauteur*t1:self.__hauteur*(t1+1),:]
        v_ = self.__v[self.__hauteur*t1:self.__hauteur*(t1+1),:]
        return(u_,v_)
    
    def resultat(self,liste,t,nom,lw1 =2):
        fig = plt.figure(figsize = [9.8, 7.2], frameon = False)
        #Liste : liste de couple des coordonées du point
        os.makedirs('C:/Users/Etienne/Desktop/TIPE/7 mars/resultat', exist_ok=True)
        n = len(liste)
        y = [self.__lat[int(liste[i][0])] for i in range(n)]
        x = [self.__lon[int(liste[i][1])] for i in range(n)]
        t1 = int(t)
        u_ = self.__u[self.__hauteur*t1:self.__hauteur*(t1+1),:]
        v_ = self.__v[self.__hauteur*t1:self.__hauteur*(t1+1),:]
        plt.ylim([self.__lat[-1],self.__lat[0]])
        plt.xlim([self.__lon[0],self.__lon[-1]])
        im = plt.quiver(self.__lon,self.__lat,u_,v_)
        im = plt.plot(x,y, c = "r",lw = lw1)
        fig.savefig('C:/Users/Etienne/Desktop/TIPE/7 mars/resultat/'+nom+'.png')
