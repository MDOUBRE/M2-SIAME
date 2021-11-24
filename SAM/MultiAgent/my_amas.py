from pyAmakCore.classes.amas import Amas

from my_agent import Lumiere, Volet

class GestionClasse(Amas):
    env = None
    listeLumieres = []
    listeVolets = []
    conso = 0
    conso_heure = 0
    heure_termine = False

    def synchronization(self):
        self._Amas__scheduler.give_amas_token()
        super().synchronization()

    def __init__(self, environnement, execution_policy):
        self.env = environnement
        self.set_do_log(True)
        super().__init__(self.env, execution_policy)

    def maj_conso(self):
        for i in range(len(self.listeLumieres)):
            tmp = self.listeLumieres[i].getNiveau()
            self.conso = self.conso + tmp*0.077

    def on_initial_agents_creation(self):
        tmp = Lumiere(0, self.env, 69, self)
        tmp2 = Volet(0, self.env, 69, self)
        liste_agents = [tmp, tmp2]
        self.listeLumieres.append(tmp)
        self.listeVolets.append(tmp2)
        self.add_agents(liste_agents)
    
    def on_cycle_begin(self):
        print("Début cycle")
        #print(self.get_cycle())
        print("Luminosité dans la salle = ", self.env.getLum())
        print("Conso = ", self.conso)
        print("Conso dans l'heure = ", self.conso_heure)
        print("Heure = ", self.env.getHeure())
        print()

    def on_cycle_end(self):
        print("Fin cycle")
        print("Luminosité dans la salle = ", self.env.getLum())
        print("Conso = ", self.conso)
        print("Conso dans l'heure = ", self.conso_heure)
        print("Heure = ", self.env.getHeure())
        print()
        yo = int(input())

        self.heure_termine = True
        for elem in self.listeLumieres:
            if(elem.getTermine()==False):
                self.heure_termine = False
        if(self.heure_termine==True):
            self.maj_conso()
            self.env.change_heure=True
