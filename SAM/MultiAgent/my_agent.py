from pyAmakCore.classes.agent import Agent

class Lumiere(Agent):
    partie_salle = 0
    niveau = 0
    etat = 0
    seuil = 0

    chaine = ""
    valeur_captee = 0
    cycle_tmp=0

    env = 0
    termine = False

    prio=False

    def __init__(self, partie, environnement, seuil, amas, niveau=0, valeur_capt=0):
        self.partie_salle = partie
        self.niveau = niveau
        self.valeur_captee = valeur_capt
        self.env = environnement
        self.chaine = ""
        self.seuil = seuil

        super().__init__(amas)

    def getPartieSalle(self):
        return self.partie_salle
        
    def getNiveau(self):
        return self.niveau

    def getTermine(self):
        return self.termine

    def setPrio(self, val):
        self.prio=val

    def on_perceive(self):
        print("LUMIERE : ON_PERCEIVE")
        self.valeur_captee=self.env.getLumCaptee()
        #print("LUMIERE : VALEUR CAPTEE = ", self.valeur_captee)

    def on_decide(self):
        print("LUMIERE : ON_DECIDE")
        self.termine = False
        if(self.prio==True):
            if(self.valeur_captee>self.seuil+5):
                print("LUMIERE : on est dans le if")
                self.chaine="diminuer"
                print(self.chaine)
            elif(self.valeur_captee<self.seuil-5):
                print("LUMIERE : on est dans le elif")
                if(self.cycle_tmp==0):
                    self.cycle_tmp=1
                else:
                    self.chaine="augmenter"
                    print(self.chaine)
            else:
                print("LUMIERE : on est dans le else")
                self.termine = True
                self.chaine = "non"
   
    def on_act(self):
        print("LUMIERE : ON_ACT")
        print("LUMIERE : niveau avant modif = ", self.niveau)
        if(self.chaine=="augmenter" and self.niveau<=95):
            self.niveau += 5
        elif(self.chaine=="diminuer" and self.niveau>=5):
            self.niveau -= 5
        self.chaine=""
        print("LUMIERE : niveau après modif = ", self.niveau)


class Volet(Agent):
    partie_salle = 0
    niveau = 0
    seuil=0

    chaine=""
    valeur_captee = 0
    cycle_tmp=0    

    env=0
    termine = False

    prio = False

    def __init__(self, partie, environnement, seuil, amas, niveau=0, valeur_capt=0):
        self.partie_salle = partie
        self.niveau=niveau
        self.valeur_captee=valeur_capt
        self.seuil = seuil
        self.chaine = ""
        self.env = environnement

        super().__init__(amas)

    def getPartieSalle(self):
        return self.partie_salle

    def getTermine(self):
        return self.termine

    def getNiveau(self):
        return self.niveau

    def setPrio(self, val):
        self.prio=val

    def on_perceive(self):
        print("                                         VOLET : ON_PERCEIVE")
        self.valeur_captee=self.env.getLumCaptee()
        self.chaine = ""
        #print("VOLET : VALEUR CAPTEE = ", self.valeur_captee)

    def on_decide(self):
        print("                                         VOLET : ON_DECIDE")
        self.termine = False
        if(self.prio==True):
            if(self.valeur_captee>self.seuil+5):
                print("                                         VOLET : on est dans le if")
                if(self.cycle_tmp==0):
                    self.cycle_tmp=1
                else:
                    self.chaine="diminuer"
            elif(self.valeur_captee<self.seuil-5):
                print("                                         VOLET : on est dans le elif")
                self.chaine="augmenter"
            else:
                print("                                         VOLET : on est dans le else")
                self.chaine = "non"
                print(self.chaine)
                self.termine = True

    def on_act(self):
        print("                                         VOLET : ON_ACT")
        print("                                         VOLET : niveau avant modif = ", self.niveau)
        print(self.chaine)
        if(self.chaine=="augmenter" and self.niveau<=95):
            print("ah que coucou")
            self.niveau += 5
        elif(self.chaine=="diminuer" and self.niveau>=5):
            print("ah que bonsoir")
            self.niveau -= 5
        self.chaine=""
        print("                                         VOLET : niveau après modif = ", self.niveau)



