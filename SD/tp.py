import socket
import json
import random

IP_perso="192.168.0.18"
port_perso=1883

Num_noeud=0
Table_hachage=[]
Table_voisinage=[]

# Pour les réponses, dans le json recu
IP_reponse=""
Port_reponse=""


def init():
    Table_voisinage.append([0, "", 0]) # voisin prec
    Table_voisinage.append([0, "", 0]) # voisin suiv


def my_join():
    reponse = False
    while(reponse==False):
        Num_noeud=random.randint(1, 65535)
        #IP et port à donner car à connaitre à la base pour pouvoir se connecter à un noeud
        sendMsg(True,"join", IP, port, IP_perso, port_perso)

        # Attente de la confirmation ou non
        payload=receive()
        if(payload["type"]=="accept" and payload["key"]==Num_noeud):
            reponse=True


# une fois arrivé pour signaler à tout le monde qu'on est la
#def my_new():
    

#def my_put():


def my_get(key):
    # IP et port à remplacer par le suivant dans a liste de voisinage
    sendMsg(True,"get", Table_voisinage[0][1], Table_voisinage[0][2], IP_perso, port_perso, key)
    payload=receive()

#def my_quit():


#def on_join():
#    print("on_join\n")


def sendMsg(my, cmd, IP, port, IP_source, port_source):
    # Creation socket
    tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tpsoc_envoi.bind(('', port_perso))
        
    jsonFrame = { }
    jsonFrame['type'] = json.loads(cmd)
    jsonFrame['ip'] = json.loads(IP_source)
    jsonFrame['port'] = json.loads(port_source)

    if(cmd=="get"):
        # a modifier
        jsonFrame['value_units'] = 'celsius'

    # envoi du message et fermeture de la socket
    tpsoc_envoi.connect((IP, port))
    tpsoc_envoi.send(json.dumps(jsonFrame))
    tpsoc_envoi.close()


def receive():
    tpsoc_rcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tpsoc_rcv.bind(('', port_perso))
    tpsoc_rcv.listen()
    IP_reponse, Port_reponse = tpsoc_rcv.accept()
    msg_recu = tpsoc_rcv.recv(255)
    tpsoc_rcv.close()
    payload = json.loads(msg_recu.payload.decode('utf-8'))
    return payload


init()
my_join()
while(True):
    payload=receive()