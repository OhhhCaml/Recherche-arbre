import numpy as np

TAILLE_INIT = 50000

class file_prioritaire :
    ### Classe implémentant une file prioritaire avec un tas, variables :
    ### Primitives :
    def enfile(self, e) :
        self.__taille += 1
        if self.__taille >= len(self.__tas) :
            self.__double_taille()
        self.__tas[(self.__taille - 1)] = e
        e_pos = self.__taille - 1
        while e_pos > 0 and self.__compare(self.__tas[int(e_pos)], self.__tas[int((e_pos-1)//2)]) :
            echange(self.__tas, e_pos, (e_pos-1)//2)
            e_pos = (e_pos-1)/2
        
    def defile(self) :
        if self.__taille == 0 :
            raise Exception("file vide")
        if self.__taille < len(self.__tas)//4 :
            self.__divise_taille()
        r = self.__tas[0]
        self.__taille -= 1
        self.__tas[0] = self.__tas[self.__taille]
        e_pos = 0
        descente(self.__tas, self.__compare, self.__taille, e_pos)
        return r
        
    def est_vide(self) :
        return self.__taille == 0
    
    def taille(self) :
        return self.__taille

    def __double_taille(self) :
        self.__tas = np.concatenate((self.__tas, self.__tas))

    def __divise_taille(self) :
        self.__tas = np.array([self.__tas[i] for i in range(len(self.__tas)//2)])

    ### Fonctions pour Python :
    def __init__(self, fct_comparaison, v) :
        ###### fct_comparaison(e1, e2) renvoie True si e1 est prioritaire par rapport à e2
        self.__taille = 0
        self.__compare = fct_comparaison
        self.__tas = np.array(TAILLE_INIT*[v])

    def copy(self) :
        R = file_prioritaire()
        R.__tas = self.__tas.copy()
        R.__taille = self.__taille
        R.__compare = self.__compare
        
        return R

    def __str__(self) :
        if self.taille == 0 :
            return "Vide"
        s = "["
        for i in range(1, self.__taille +1) :
            s += str(self.__tas[i]) + ", "
        s += "]"
        return s

    def __iter__(self) :
        return iter(self.__tas)

    def __next__(self):
        pass

    
def echange(l, i, j) :
    l[int(i)], l[int(j)] = l[int(j)], l[int(i)]

def descente(tas, compare, taille, pos) :
    fils_prio = []
    fg = 2*pos+1
    fd = 2*pos+2
    if fd < taille :
        if compare(tas[int(fg)], tas[(fd)]) : fils_prio = fg
        else : fils_prio = fd
        if compare(tas[fils_prio], tas[pos]) :
            echange(tas, fils_prio, pos)
            descente(tas, compare, taille, fils_prio)
    elif fd == taille :
        fils_prio = fg
        if compare(tas[fils_prio], tas[pos]) :
            echange(tas, fils_prio, pos)
            descente(tas, compare, taille, fils_prio)

def minx(x , y) :
    return x<y

'''
file = file_prioritaire(minx, etype = int)
file.enfile(6)
file.enfile(0)
file.enfile(5)
file.enfile(3)
file.enfile(1)
file.enfile(4)
file.enfile(10)
file.enfile(12)
file.enfile(2)
file.defile()
file.defile()
print(file)
'''
