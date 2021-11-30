from pyAmakCore.classes.amas import Amas

from my_agent import Lumiere, Volet

class GestionClasse(Amas):
    env = None
    listeLumieres = []
    listeVolets = []
    conso = 0
    conso_heure = 0
    heure_termine = False
    seuil = 69

    def synchronization(self):
        self._Amas__scheduler.give_amas_token()
        super().synchronization()

    def __init__(self, environnement, seuil, execution_policy):
        self.env = environnement
        self.seuil = seuil
        self.set_do_log(True)
        super().__init__(self.env, execution_policy)

    def maj_conso(self):
        for i in range(len(self.listeLumieres)):
            tmp = self.listeLumieres[i].getNiveau()
            self.conso = self.conso + tmp*0.077

    def on_initial_agents_creation(self):
        tmp = Lumiere(0, self.env, self.seuil, self)
        tmp2 = Volet(0, self.env, self.seuil, self)
        liste_agents = [tmp, tmp2]
        self.listeLumieres.append(tmp)
        self.listeVolets.append(tmp2)
        self.add_agents(liste_agents)
    
    def on_cycle_begin(self):
        print("Début cycle")
        #print(self.get_cycle())
        print("niveau volet = ", self.listeVolets[0].getNiveau())
        self.env.majNivVolet(self.listeVolets[0].getNiveau())
        print("Luminosité dans la salle = ", self.env.getLumCaptee())
        print("Conso = ", self.conso)
        print("Conso dans l'heure = ", self.conso_heure)
        print("Heure = ", self.env.getHeure())
        print()

    def on_cycle_end(self):
        lum = 0
        for elem in self.listeLumieres:
            lum += elem.getNiveau()
        lum = lum/ len(self.listeLumieres)         
        self.env.majLumInte(lum)
        print("Fin cycle")
        self.env.majNivVolet(self.listeVolets[0].getNiveau())
        print("Luminosité dans la salle = ", self.env.getLumCaptee())
        print("Conso = ", self.conso)
        print("Conso dans l'heure = ", self.conso_heure)
        print("Heure = ", self.env.getHeure())
        print()
        yo = input()

        if(self.env.getLumCaptee()<self.seuil+5 and self.env.getLumCaptee()>self.seuil-5):
            self.env.change_heure = True
            self.maj_conso()
        else:
            self.env.change_heure = False

        '''
        self.heure_termine = True
        for elem in self.listeLumieres:
            if(elem.getTermine()==False):
                self.heure_termine = False
        if(self.heure_termine==True):
            self.maj_conso()
            self.env.change_heure=True
        '''