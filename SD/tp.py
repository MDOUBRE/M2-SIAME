import socket
import json
import random

IP_perso="192.168.0.18"
port_perso=1883

# Pour les réponses, dans le json recu
IP_reponse=""
Port_reponse=""

num_noeud=0
table_hachage=[]
table_voisinage=[]


def init():
    table_voisinage.append([0, "", 0]) # voisin prec
    table_voisinage.append([0, "", 0]) # voisin suiv


def my_join():
    reponse = False
    IP = input()
    port = int(input())

    while(reponse==False):
        num_noeud=random.randint(1, 65535)
        sendMsg(True,"join", IP, port, IP_perso, port_perso, num_noeud)

        # Attente de la confirmation ou non
        payload=receive()
        if(payload["type"]=="accept" and payload["key"]==num_noeud):
            reponse=True

def my_new():
    sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso)

def my_put(key, val, idUnique):
    sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key, 0, [], 0, val, idUnique)

def my_get(key):
    # IP et port à remplacer par le suivant dans a liste de voisinage
    sendMsg(True,"get", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key)
    payload=receive()

#def my_quit():

def majTv(payload):
    if(payload['key'] > table_voisinage[0][0]):
        table_voisinage[0] = [payload['key'], payload['ip'], payload['port']]
    if(payload['key'] < table_voisinage[1][0]):
        table_voisinage[1] = [payload['key'], payload['ip'], payload['port']]


#def on_join():


def sendMsg(my, cmd, IP, port, IP_source = "", port_source = 0, key = 0, data = 0, tv = [], keyResp = 0, val = 0, idUnique = 0, msgGet = 0, msgPut = 0, msgGest = 0):
    # Creation socket
    tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tpsoc_envoi.bind(('', port_perso))
        
    jsonFrame = { }
    jsonFrame['type'] = json.loads(cmd)

    if(cmd=="join" or cmd=="get_resp" or cmd=="resp" or cmd=="new", cmd=="put" or cmd=="get"):
        jsonFrame['ip'] = json.loads(IP_source)
        jsonFrame['port'] = json.loads(port_source)

    if(cmd=="join" or cmd=="accept" or cmd=="init" or cmd=="get_resp" or cmd=="resp" or cmd=="new" or cmd=="put" or cmd=="get" or cmd=="answer" ):
        jsonFrame['key'] = json.loads(key)

    if(cmd=="init"):
        jsonFrame['data']= json.loads(data)
        jsonFrame['tv']= json.loads(tv)

    if(cmd=="put" or cmd=="answer"):
        jsonFrame['val'] = json.loads(val)

    if(cmd=="put" or cmd=="ack"):
        jsonFrame['idUnique'] = json.loads(idUnique)

    if(cmd=="resp"):
        jsonFrame['keyResp'] = json.loads(keyResp)

    if(cmd=="quit"):
        jsonFrame['msgGet'] = json.loads(msgGet)
        jsonFrame['msgPut'] = json.loads(msgPut)
        jsonFrame['msgGest'] = json.loads(msgGest)

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


def decide(payload):
    if(payload['cmd'] == "join"):
        if(payload['key'] < table_voisinage[0][0]):
            sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'])
        elif(payload['key'] > table_voisinage[1][0]):
            sendMsg(False, "join", table_voisinage[1][1], table_voisinage[1][2], payload['ip'], payload['port'])
        elif(payload['key'] == table_voisinage[0][0] or payload['key'] == table_voisinage[1][0] or payload['key'] == num_noeud):
            sendMsg(False, "reject", payload['ip'], payload['port'])
        else:
            sendMsg(False, "accept", payload['ip'], payload['port'])

    elif(payload['cmd']=="accept"):
        if(payload['key']!=num_noeud):
            print("PROBLEME DE REPONSE DE JOIN, ON REFAIT LE MY_JOIN")
            my_join()
        else:
            print("Join avec key = ", payload['key'], " accepté")
            my_new()

    elif(payload['cmd']=="reject"):
        print("JOIN REJECTED, ON REFAIT LE MY_JOIN")
        my_join()

    elif(payload['cmd'] == "quit" and payload['msgGest'] == num_noeud):
        return True

    elif(payload['cmd'] == "new"):
        if(payload['ip'] != IP_perso):
            sendMsg(False, "new", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'])
            if(payload['key'] > table_voisinage[0][0] or payload['key'] < table_voisinage[1][0]):
                majTv(payload)
    
    elif(payload['cmd'] == "init"):
        print("faut faire l'init mais chelou un peu")


stop = False
init()
my_join()
while(stop == False):
    payload = receive()
    stop = decide(payload)