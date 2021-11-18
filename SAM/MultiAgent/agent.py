from random import seed

import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.environment import Agent

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable


class Volet(Agent):
    etat = 0
    partie_salle = 0
    niveau = 0

    capteur = 0
    valeur_captee = 0
    cycle_tmp=0
    seuil=0
    chaine=""

    env=0

    def __init__(self, partie, capteur, environnement, etat=0, niveau=0, valeur_capt=0, seuil=0):
        self.etat = etat
        self.partie_salle = partie
        self.capteur = capteur
        self.niveau=niveau
        self.valeur_captee=valeur_capt
        self.seuil = seuil
        self.chaine = ""
        self.env = environnement

    def getEtat(self):
        return self.etat

    def getPartieSalle(self):
        return self.partie_salle

    def ouvrir(self):
        self.etat = 1

    def fermer(self):
        self.etat = 0  
    
    def on_perceive(self):
        self.valeur_captee=self.env.capteur.getValeur()

    def on_decide(self):
        if(self.valeur_captee>self.seuil+5):
            if(self.cycle_tmp==0):
                self.cycle_tmp=1
            else:
                self.chaine="diminuer"
        elif(self.valeur_captee<self.seuil-5):
                self.chaine="augmenter"

    def on_act(self):
        if(self.chaine=="augmenter"):
            self.niveau += 5
        elif(self.chaine=="diminuer"):
            self.niveau -= 5




class Lumiere(Agent):
    partie_salle = 0
    niveau = 0
    etat = 0

    capteur = 0
    valeur_captee = 0
    cycle_tmp=0

    env = 0

    def __init__(self, partie, capteur, environnement, etat=0, niveau=0, valeur_capt=0):
        self.etat = etat
        self.partie_salle = partie
        self.niveau = niveau
        self.valeur_captee = valeur_capt
        self.capteur = capteur
        self.env=environnement

    def getPartieSalle(self):
        return self.partie_salle
        
    def getNiveau(self):
        return self.niveau

    def getEtat(self):
        return self.etat 

    def on_perceive(self):
        self.valeur_captee=self.env.capteur.getValeur()

    def on_decide(self):
        if(self.valeur_captee>self.seuil+5):
            self.chaine="diminuer"
        elif(self.valeur_captee<self.seuil-5):
            if(self.cycle_tmp==0):
                self.cycle_tmp=1
            else:
                self.chaine="augmenter"
   
    def on_act(self, chaine):
        if(self.chaine=="augmenter"):
            self.niveau += 5
        elif(self.chaine=="diminuer"):
            self.niveau -= 5

    


