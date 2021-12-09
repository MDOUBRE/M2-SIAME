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
    taux = 1
    list_lum_heures = [[8,taux*5], [9,taux*20], [10, taux*35], [11, taux*60], [12, taux*90] , [13, taux*100] , [14, taux*100] , [15, taux*90] , [16, taux*82] , [17, taux*71] , [18, taux*60] , [19, taux*40] , [20, taux*20] , [21, taux*5]]
    list_importance_exte = [[8, 0.8, 0.2], [9, 0.64, 0.36], [10, 0.5, 0.5], [11, 0.4, 0.6], [12, 0.3, 0.7], [13, 0.25, 0.75], [14, 0.2, 0.8], [15, 0.3, 0.7], [16, 0.43, 0.57], [17, 0.55, 0.45], [18, 0.7, 0.3], [19, 0.8, 0.2], [15, 0.9, 0.1],[21, 0.95, 0.05]]

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
        niv_exte_heure = self.list_lum_heures[self.heure-8][1]
        niv_import_inte = self.list_importance_exte[self.heure-8][1]
        niv_import_exte = self.list_importance_exte[self.heure-8][2]

        if((niv_import_inte*self.lum_inte) + ((niv_exte_heure*(self.niveauVolet/100))*niv_import_exte)>=100):
            return 100
        elif((niv_import_inte*self.lum_inte) + ((niv_exte_heure*(self.niveauVolet/100))*niv_import_exte)<=0):
            return 0
        else:
            return (niv_import_inte*self.lum_inte) + ((niv_exte_heure*(self.niveauVolet/100))*niv_import_exte)

    def majLumInte(self, lum):
        self.lum_inte = lum

    def on_cycle_begin(self):
        if(self.change_heure==True):
            self.heure += 1
            self.change_heure=False
    



    