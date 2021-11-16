"""
Environment class
"""
from random import seed

import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib
from pyAmakCore.classes.environment import Environment

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable


class Volet():
    etat = 0
    partie_salle = 0

    def __init__(self, partie, etat=0):
        self.etat = etat
        self.partie_salle = partie

    def getEtat(self):
        return self.etat

    def getPartieSalle(self):
        return self.partie_salle

    def ouvrir(self):
        self.etat = 1

    def fermer(self):
        self.etat = 0   


class Lumiere():
    etat = 0
    partie_salle = 0
    niveau = 0

    def __init__(self, partie, etat=0, niveau = 0):
        self.etat = etat
        self.partie_salle = partie
        self.niveau = niveau

    def getEtat(self):
        return self.etat

    def getPartieSalle(self):
        return self.partie_salle

    def allume(self, niveau):
        self.etat = 1
        self.niveau = niveau

    def eteint(self):
        self.etat = 0
        self.niveau = 0

    def getNiveau(self):
        return self.niveau


class Capteur():
    captation = 0

    def getValeur(self):
        return self.captation


class Controlleur():
    list_actionneurs_volets = []
    list_actionneurs_lumieres = []

    def __init__(self, list_actionneurs_volets, list_actionneurs_lumieres):
        self.list_actionneurs_volets = list_actionneurs_volets
        self.list_actionneurs_lumieres = list_actionneurs_lumieres

    def ouvrirVolet(self, indice):
        self.list_actionneurs_volets[indice].augmenter()

    def ouvrirVolet(self, indice):
        self.list_actionneurs_volets[indice].diminuer()

    def allumerLumiere(self, indice, niveau):
        self.list_actionneurs_lumieres[indice].augmenter(niveau)

    def eteindreLumiere(self, indice):
        self.list_actionneurs_lumieres[indice].diminuer()


class Actionneur():
    def augmenter(self):
        return None

    def diminuer(self):
        return None


class ActionneurLumiere(Actionneur):
    lumiere = None
    
    def __init__(self, lumiere):
        self.lumiere = lumiere

    def augmenter(self, niveau):
        self.lumiere.alume(niveau)

    def diminuer(self):
        self.lumiere.eteint()



class ActionneurVolet(Actionneur):
    volet = None

    def __init__(self, volet):
        self.volet = volet

    def augmenter(self):
        self.volet.ouvrir()

    def diminuer(self):
        self.volet.fermer()


class classe_connectee(Environnement):
    """
    Environment class
    """
    list_volets = []
    list_lumieres = []
    list_capteurs = []
    list_controlleurs = []
    list_actionneurs_lumieres = []
    list_actionneurs_volets = []

    lum_base = 1
    lum_base1 = 1
    lum_base2 = 1
    cloison = 0

    nbControlleurs = 2
    nbActionneurs = 0
    nbLumieres = 0
    nbVolets = 0
    
    moitierLumieres = 0
    moitierVolets = 0

    conso=0

    list_lum_heures = [[8,0.05], [9,0.2], [10, 0.4], [11, 0.7], [12, 1] , [13, 0.95] , [14, 0.9] , [15, 0.85] , [16, 0.8] , [17, 0.7] , [18, 0.6] , [19, 0.4] , [20, 0.2] , [21, 0.05]]

    def __init__(self, lum_base, nbVolets, nbLumieres, nbCapteurs):
        self.lum_base = lum_base
        self.lum_base1 = lum_base
        self.lum_base2 = lum_base
        self.nbLumieres = nbLumieres
        self.nbVolets = nbVolets
        self.nbActionneurs = nbVolets + nbLumieres
        self.moitierLumieres = self.nbLumieres // 2
        self.moitierVolets = self.nbVolets // 2

        for i in range(nbVolets):
            if i < self.moitierVolets:
                self.list_volets.append(Volet(0))
            else:
                self.list_volets.append(Volet(1))
            self.list_actionneurs_volets.append(ActionneurVolet(self.list_volets[i]))
        for i in range(nbLumieres):
            if i < self.moitierLumieres:
                self.list_lumieres.append(Lumiere(0))
            else:
                self.list_lumieres.append(Lumiere(1))
            self.list_actionneurs_lumieres.append(ActionneurLumiere(self.list_lumieres[i]))        
        for i in range(nbCapteurs):
            self.list_capteurs.append(Capteur)        
        super().__init__()

    def on_initialization(self): 
        for i in range(self.nbControlleurs):
            if(i==0):
                self.list_controlleurs.append(Controlleur(self.list_actionneurs_volets[:self.moitierVolets-1], self.list_actionneurs_lumieres[:self.moitierLumieres-1]))
            else:
                self.list_controlleurs.append(Controlleur(self.list_actionneurs_volets[self.moitierVolets:], self.list_actionneurs_lumieres[self.moitierLumieres:]))        
        

    def getLum(self):
        return self.lum_base

    def getLum1(self):
        return self.lum_base1

    def getLum2(self):
        return self.lum_base2


    def allumeLumiere(self, numLum, niveau):
        if(numLum<=self.moitierLumieres):
            self.list_controlleurs[0].allumerLumiere(numLum-1, niveau)
        else:
            self.list_controlleurs[1].allumerLumiere(numLum-self.moitierLumieres-1, niveau)
        if(self.cloison==1):
            if(numLum<=self.moitierLumieres):
                self.lum_base1+=niveau
            else:
                self.lum_base2+=niveau
        else:
            self.lum_base=(self.lum_base1 + self.lum_base2)/2

    def eteintLumiere(self, numLum, niveau):
        if(numLum<=self.moitierLumieres):
            self.list_controlleurs[0].eteindreLumiere(numLum-1)
        else:
            self.list_controlleurs[1].eteindreLumiere(numLum-self.moitierLumieres-1)
        if(self.cloison==1):
            if(numLum<=self.moitierLumieres):
                self.lum_base1-=self.list_controlleurs[0].list_actionneurs_lumieres(numLum-1).lumiere.getNiveau()
            else:
                self.lum_base2-=self.list_controlleurs[0].list_actionneurs_lumieres(numLum-1-self.moitierLumieres).lumiere.getNiveau()
        else:
            self.lum_base=(self.lum_base1 + self.lum_base2)/2

    def ouvreVolet(self, numLum, heure):
        if(numLum<=self.moitierVolets):
            self.list_controlleurs[0].ouvrirVolet(numLum-1)
        else:
            self.list_controlleurs[1].ouvrirVolet(numLum-self.moitierVolets-1)
        if(self.cloison==1):
            if(numLum<=self.moitierVolets):
                if(heure>=8 and heure<22):
                    self.lum_base1+=self.list_lum_heures[heure-8][1]
            else:
                if(heure>=8 and heure<22):
                    self.lum_base2+=self.list_lum_heures[heure-8][1]
        else:
            if(heure>=8 and heure<22):
                self.lum_base=(self.lum_base1 + self.lum_base2)/2


    def fermeVolet(self, numLum, heure):
        if(numLum<=self.moitierVolets):
            self.list_controlleurs[0].fermerVolet(numLum-1)
        else:
            self.list_controlleurs[1].fermerVolet(numLum-self.moitierVolets-1)
        if(self.cloison==1):
            if(numLum<=self.moitierVolets):
                if(heure>=8 and heure<22):
                    self.lum_base1-=self.list_lum_heures[heure-8][1]
            else:
                if(heure>=8 and heure<22):
                    self.lum_base2-=self.list_lum_heures[heure-8][1]
        else:
            if(heure>=8 and heure<22):
                    self.lum_base=(self.lum_base1 + self.lum_base2)/2

    def majLum(self, heure):
        if(heure>=8 and heure<22):
            self.lum_base1-=self.list_lum_heures[heure-8-1][1]
            self.lum_base2-=self.list_lum_heures[heure-8-1][1]
            self.lum_base1+=self.list_lum_heures[heure-8][1]
            self.lum_base2+=self.list_lum_heures[heure-8][1]
            self.lum_base=(self.lum_base1 + self.lum_base2)/2


    '''
    def consommation(self, cmd, heure, partie=0, lum):
        if(cmd=="augmenter"):
            if(self.cloison==0):
                if(self.lum_base==1):
                    print("On ne peut pas augmenter la luminosité\n")
                else:
                    for i in range(len(self.list_volets)):
                        if(self.list_volets[i].getEtat()!=1):
                            self.ouvreVolet(i+1, heure)
            else:
                if(partie==1):
                    if(self.lum_base1==1):
                        print("On ne peut pas augmenter la luminosité de la partie 1 de la salle\n")
                    else:
                        for i in range(self.moitierVolets):
                            if(self.list_volets[i].getEtat()!=1):
                                self.ouvreVolet(i+1, heure)
                else:
                    if(self.lum_base2==1):
                        print("On ne peut pas augmenter la luminosité de la partie 2 de la salle\n")
                    else:
                        for i in range(self.moitierVolets+1,len(self.list_volets)):
                            if(self.list_volets[i].getEtat()!=1):
                                self.ouvreVolet(i+1, heure)
        #elif(cmd=="diminuer"):
    '''