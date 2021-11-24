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

    def __init__(self, partie, environnement, seuil, amas, etat=0, niveau=0, valeur_capt=0):
        self.etat = etat
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

    def getEtat(self):
        return self.etat 

    def getTermine(self):
        return self.termine

    def on_perceive(self):
        print("ON EST DANS ON_PERCEIVE LUMIERE")
        self.valeur_captee=self.env.getLum()
        print("VALEUR CAPTEE = ", self.env.getLumCaptee())

    def on_decide(self):
        print("ON EST DANS ON_DECIDE LUMIERE")
        self.termine = False
        if(self.valeur_captee>self.seuil+5):
            self.chaine="diminuer"
        elif(self.valeur_captee<self.seuil-5):
            if(self.cycle_tmp==0):
                self.cycle_tmp=1
            else:
                self.chaine="augmenter"
        else:
            self.termine = True
   
    def on_act(self):
        print("ON EST DANS ON_ACT LUMIERE")
        if(self.chaine=="augmenter"):
            self.niveau += 5
        elif(self.chaine=="diminuer"):
            self.niveau -= 5


class Volet(Agent):
    partie_salle = 0
    niveau = 0
    etat = 0
    seuil=0

    chaine=""
    valeur_captee = 0
    cycle_tmp=0    

    env=0
    termine = False

    def __init__(self, partie, environnement, seuil, amas, etat=0, niveau=0, valeur_capt=0):
        self.etat = etat
        self.partie_salle = partie
        self.niveau=niveau
        self.valeur_captee=valeur_capt
        self.seuil = seuil
        self.chaine = ""
        self.env = environnement

        super().__init__(amas)

    def getEtat(self):
        return self.etat

    def getPartieSalle(self):
        return self.partie_salle

    def ouvrir(self):
        self.etat = 1

    def fermer(self):
        self.etat = 0  

    def getTermine(self):
        return self.termine
    
    def on_perceive(self):
        print("ON EST DANS ON_PERCEIVE VOLET")
        self.valeur_captee=self.env.getLumCaptee()
        print("VALEUR CAPTEE = ", self.env.getLumCaptee())

    def on_decide(self):
        print("ON EST DANS ON_DECIDE VOLET")
        self.termine = False
        if(self.valeur_captee>self.seuil+5):
            if(self.cycle_tmp==0):
                self.cycle_tmp=1
            else:
                self.chaine="diminuer"
        elif(self.valeur_captee<self.seuil-5):
            self.chaine="augmenter"
        else:
            self.termine = True

    def on_act(self):
        print("ON EST DANS ON_ACT VOLET")
        if(self.chaine=="augmenter"):
            self.niveau += 5
        elif(self.chaine=="diminuer"):
            self.niveau -= 5


