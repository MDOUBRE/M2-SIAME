"""
Environment class
"""
from pyAmakCore.classes.environment import Environment

class Classe_connectee(Environment):
    """
    Environment class
    """

    lum_inte = 1
    lum_inte1 = 1
    lum_inte2 = 1
    lum_exte = 0
    cloison = 0 

    niveauVolet = 0

    heure = 8
    change_heure=False

    captation = 0
    list_lum_heures = [[8,5], [9,20], [10, 40], [11, 70], [12, 100] , [13, 95] , [14, 90] , [15, 85] , [16, 80] , [17, 70] , [18, 60] , [19, 40] , [20, 20] , [21, 5]]

    def __init__(self, lum=0):
        self.lum_inte = lum
        self.lum_inte1 = lum
        self.lum_inte2 = lum
        super().__init__()

    def getLumExte(self, heure):
        lum=0
        if(heure>=8 and heure<=21):
            return self.list_lum_heures[heure-8][1]

    def getLum1(self):
        return self.lum_inte1

    def getLum2(self):
        return self.lum_inte2

    def getLum(self):
        return self.lum_inte

    def getHeure(self):
        return self.heure

    def majNivVolet(self, niveauVolet):
        self.niveauVolet = niveauVolet

    def getLumCaptee(self):
        if((0.7*self.lum_inte) + ((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)>=100):
            print((0.7*self.lum_inte))
            print((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)     
            return 100
        elif((0.7*self.lum_inte) + ((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)<=0):
            print((0.7*self.lum_inte))
            print((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)
            return 0
        else:
            print((0.7*self.lum_inte))
            print((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)
            print(self.niveauVolet)
            return (0.7*self.lum_inte) + ((self.list_lum_heures[self.heure-8][1]*self.niveauVolet)*0.3)

    def majLumInte(self, lum):
        self.lum_inte = lum

    def on_cycle_begin(self):
        if(self.change_heure==True):
            self.heure += 1
            self.change_heure=False
    



    