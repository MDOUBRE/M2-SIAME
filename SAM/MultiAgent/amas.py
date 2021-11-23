from os import environ, terminal_size
from random import seed

import sys
sys.path.extend(['/media/storage/camsi4/pyamak-noyau/'])
import pathlib
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.agent import Agent

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable

class gestionClasse(Amas):
    env = None
    listeLumieres = []
    listeVolets = []
    conso = 0
    heure_termine = False

    def __init__(self, environnement):
        self.env = environnement
        self.set_do_log(True)

    def maj_conso(self):
        for i in range(len(self.listeLumieres)):
            tmp = self.listeLumieres[i].getNiveau()
            self.conso = self.conso + tmp*0.077

    def on_initial_agents_creation(self):
        self.listeLumieres.addAgent(Agent.Lumiere(0, self.env, 69))
        self.listeVolets.addAgent(Agent.Volet(0, self.env, 69))

    
    def on_cycle_begin(self):
        print(self.get_cycle())
        print("Luminosité dans la salle = ", self.env.getLum())
        print("Conso = ", self.conso())
        print("Conso dans l'heure = ", self.conso_heure())
        print("Heure = ", self.env.getHeure())
        print()


    def on_cycle_end(self):
        print("Luminosité dans la salle = ", self.env.getLum())
        print("Conso = ", self.env.getConso())
        print("Conso dans l'heure = ", self.conso_heure())
        print("Heure = ", self.env.getHeure())
        print()

        self.heure_termine = True
        for elem in self.listeLumieres:
            if(elem.getTermine()==False):
                self.heure_termine = False
        if(self.heure_termine==True):
            self.maj_conso()
            self.env.change_heure=True
