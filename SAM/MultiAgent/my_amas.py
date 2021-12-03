from pyAmakCore.classes.amas import Amas
import matplotlib.pyplot as plt

from my_agent import Lumiere, Volet

class GestionClasse(Amas):
    env = None
    listeLumieres = []
    listeVolets = []
    conso = 0
    conso_heure = 0
    heure_termine = False
    seuil = 69

    grapheNiveauVolets_heure = []
    grapheNiveauVolets_niveau = []
    grapheNiveauLumiere_heure = []
    grapheNiveauLumiere_niveau = []

    grapheLuminosite_heure = []
    grapheLumnosite_niveau = []

    graphe_conso_heure = []

    graphe_conso_val = []
    graphe_conso_heure_val = []

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
            if(tmp>=0 and tmp<20):
                conso = 0.05
            elif(tmp>=20 and tmp<40):
                conso = 0.057
            elif(tmp>=40 and tmp<60):
                conso = 0.069
            elif(tmp>=60 and tmp<80):
                conso = 0.081
            else:
                conso = 0.095           
            self.conso = self.conso + tmp*conso

    def on_initial_agents_creation(self):
        liste_agents = []
        for i in range(10):
            tmp = Lumiere(0, self.env, self.seuil, self)
            tmp2 = Volet(0, self.env, self.seuil, self)
            liste_agents.append(tmp)
            liste_agents.append(tmp2)
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
        if(self.env.getLumCaptee()<self.seuil-5):
            if(self.listeVolets[0].getNiveau()<100):
                for elem in self.listeLumieres:
                    elem.setPrio(False)
        elif(self.env.getLumCaptee()>self.seuil+5):
            if(self.listeLumieres[0].getNiveau()>0):
                for elem in self.listeVolets:
                    elem.setPrio(False)

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
        #yo = input()

        if(self.env.getLumCaptee()<=self.seuil+5 and self.env.getLumCaptee()>=self.seuil-5):
            self.env.change_heure = True
            self.maj_conso()

            self.graphe_conso_heure.append(self.env.getHeure())
            if(self.env.getHeure()!=8):
                self.graphe_conso_heure_val.append(self.conso - self.graphe_conso_val[len(self.graphe_conso_val)-1])
            else:
                self.graphe_conso_heure_val.append(self.conso)
            self.graphe_conso_val.append(self.conso)
        else:
            self.env.change_heure = False

        for elem in self.listeVolets:
            elem.setPrio(True)
        for elem in self.listeLumieres:
            elem.setPrio(True)


        self.grapheNiveauLumiere_heure.append(self.env.getHeure())
        self.grapheNiveauLumiere_niveau.append(self.listeLumieres[0].getNiveau())
        self.grapheNiveauVolets_niveau.append(self.listeVolets[0].getNiveau())

        self.grapheLumnosite_niveau.append(self.env.getLumCaptee())

        if(self.env.getHeure()==21):
            #fig1 = plt.figure()
            #fig1.add_
            plt.plot(self.grapheNiveauLumiere_heure, self.grapheNiveauLumiere_niveau)
            plt.title("Niveau des lumières selon l'heure (%)")

            plt.show()

            plt.plot(self.grapheNiveauLumiere_heure, self.grapheNiveauVolets_niveau)
            plt.title("Niveau des volets selon l'heure (%)")

            plt.show()

            plt.plot(self.grapheNiveauLumiere_heure, self.grapheLumnosite_niveau)
            plt.title("Niveau de luminosité selon l'heure (%)")

            plt.show()

            plt.plot(self.graphe_conso_heure, self.graphe_conso_val)
            plt.title("Conso générale selon l'heure (KWh)")

            plt.show()

            plt.plot(self.graphe_conso_heure, self.graphe_conso_heure_val)
            plt.title("Conso/heure (KWh)")

            plt.show()
            yo = input()
            
        

        '''
        self.heure_termine = True
        for elem in self.listeLumieres:
            if(elem.getTermine()==False):
                self.heure_termine = False
        if(self.heure_termine==True):
            self.maj_conso()
            self.env.change_heure=True
        '''