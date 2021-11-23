"""
Environment class
"""
from random import seed

import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.agent import Agent

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable


class classe_connectee(Environnement):
    """
    Environment class
    """

    class Capteur():
        captation = 0
        lumiere=0

        def __init__(self):
            self.captation=0

        def getValeur(self):
            return self.captation

        def maj(self):
            self.captation = (self.lum_exte + self.lumiere.getNiveau())/2

        def on_act(self):
            self.maj()


    lum_inte = 1
    lum_inte1 = 1
    lum_inte2 = 1
    lum_exte = 0
    cloison = 0 

    heure = 8
    change_heure=False

    capteur = Capteur()
    list_lum_heures = [[8,5], [9,20], [10, 40], [11, 70], [12, 100] , [13, 95] , [14, 90] , [15, 85] , [16, 80] , [17, 70] , [18, 60] , [19, 40] , [20, 20] , [21, 5]]

    def __init__(self, lum):
        self.lum_inte = lum
        self.lum_inte1 = lum
        self.lum_inte2 = lum

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

    def on_cycle_begin(self):
        if(self.change_heure==True):
            self.heure += 1
            self.change_heure=False
    



    