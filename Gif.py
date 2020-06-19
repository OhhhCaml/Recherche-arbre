import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

##2 fonctions 'utiles':
##temps_de_parcours(i,j,t): renvoie le temps de parcours pour aller de i à j au moment t (i,j deux voisins)
##ordre(self): renvoie le nombre de sommet
def force_to_temps2(F_vent):
    return(0.1*(np.pi/2 + np.arctan(1-0.1*F_vent)))


class Gif:
    def __init__(self,grib,chemin,nom):
        self.__coordonnées = chemin.list()
        self.__grib = grib
        self.__fig = plt.figure(figsize = [9.8, 7.2], frameon = False)
        self.__nom = nom

    def liste_duree(self):
        #Renvoie la liste duration pour le gif
        coordonnées = self.__coordonnées
        l_c = len(coordonnées)
        l_d = np.zeros(l_c-1)
        duration = np.zeros(l_c-1)
        for i in range(0,l_c-1):
            t = l_d[i-1]
            duration[i] = self.__grib.temps_de_parcours(coordonnées[i],coordonnées[i+1],t)
            l_d[i] = (duration[i] + t)
        duration = np.floor(1000*duration)
        self.duration  = duration
        return duration,l_d

    def image(self,t,n):
        #t : l'instant pour la carte de vecteur du vent
        #n : le nombre de coordonnées déjà affichées
        self.__fig.clf()
        lat = self.__grib.lat()
        lon = self.__grib.lon()
        
        y = np.array([lat[int(self.__coordonnées[i][0])] for i in range(n)])
        x = np.array([lon[int(self.__coordonnées[i][1])] for i in range(n)])

        u_,v_ = self.__grib.grille_vent(t)
        plt.ylim([lat[-1],lat[0]])
        plt.xlim([lon[0],lon[-1]])
        im = plt.quiver(lon,lat,u_,v_)
        im = plt.plot(x,y, c = "r",lw = 2)
    
    def enregistrer_images(self):
        nom = self.__nom
        os.makedirs(nom, exist_ok = True)

        l_c = len(self.__coordonnées)
        _,l_d = self.liste_duree()
        for i in range(l_c-1):
            self.image(l_d[i],i)
            self.__fig.savefig(nom+"/"+str(i)+".png")
        
        
                
    def gif(self):
        nom = self.__nom
        l_c = len(self.__coordonnées)
        duration,l_d = self.liste_duree()
        duration = list(duration)
        images = []
        for i in range(l_c-1):
            image = Image.open(nom+"/"+str(i)+".png")
            images.append(image.copy())
        images[0].save(self.__nom+".gif", save_all = True, append_images = images[1:], optimize = False, duration = duration)

