import socket
import json
import random

IP_perso="192.168.0.18"
port_perso=1883

num_noeud=0
table_hachage={}
table_voisinage=[]

ip_resp = ""
port_resp = 0
key_resp = 0

answer_key = 0
answer_val = 0


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
            payload = receive()
        else:
            print("PROBLEME DE JOIN, RETRY")

        payload = receive()
        if(payload['type']=="init" and payload['key']==num_noeud):
            table_hachage = payload['data']
            table_voisinage = payload['tv']


def my_new():
    sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso)

def my_put(key, val, idUnique):
    sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key, 0, [], 0, val, idUnique)

def my_get(key):
    # IP et port à remplacer par le suivant dans a liste de voisinage
    sendMsg(True,"get", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key)
    #payload=receive()

#def my_quit():

def majTv(payload):
    if(payload['key'] > table_voisinage[0][0]):
        table_voisinage[0] = [payload['key'], payload['ip'], payload['port']]

def majData(payload):
    table_hachage[payload['key']]= payload['val']

def getData(key):
    return payload['key']

def calcTvData(key):
    tv = []
    data = {}
    print("faire tv + data")
    return tv, data


def sendMsg(my, type, IP, port, IP_source = "", port_source = 0, key = 0, data = {}, tv = [], keyResp = 0, val = 0, idUnique = 0, msgGet = 0, msgPut = 0, msgGest = 0, ok = 0):
    # Creation socket
    tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tpsoc_envoi.bind(('', port_perso))
        
    jsonFrame = { }
    jsonFrame['type'] = json.loads(type)

    if(type=="join" or type=="get_resp" or type=="resp" or type=="new", type=="put" or type=="get"):
        jsonFrame['ip'] = json.loads(IP_source)
        jsonFrame['port'] = json.loads(port_source)

    if(type=="join" or type=="accept" or type=="init" or type=="get_resp" or type=="resp" or type=="new" or type=="put" or type=="get" or type=="answer" ):
        jsonFrame['key'] = json.loads(key)

    if(type=="init"):
        jsonFrame['data']= json.loads(data)
        jsonFrame['tv']= json.loads(tv)

    if(type=="put" or type=="answer"):
        jsonFrame['val'] = json.loads(val)

    if(type=="put" or type=="ack"):
        jsonFrame['idUnique'] = json.loads(idUnique)

    if(type=="ack"):
        jsonFrame['ok'] = json.loads(ok)

    if(type=="resp"):
        jsonFrame['keyResp'] = json.loads(keyResp)

    if(type=="quit"):
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
    if(payload['type'] == "join"):
        if(payload['key'] < num_noeud):
            sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(payload['key'] > table_voisinage[1][0]):
            sendMsg(False, "join", table_voisinage[1][1], table_voisinage[1][2], payload['ip'], payload['port'], payload['key'])
        elif(payload['key'] == table_voisinage[0][0] or payload['key'] == table_voisinage[1][0] or payload['key'] == num_noeud):
            sendMsg(False, "reject", payload['ip'], payload['port'], "", 0, payload['key'])
        else:
            sendMsg(False, "accept", payload['ip'], payload['port'], "", 0, payload['key'])
            tv, data = calcTvData(payload['key'])
            sendMsg(False, "init", payload['ip'], payload['port'], "", 0, payload['key'], tv, data)

    elif(payload['type'] == "get_resp"):
        if(payload['key']>=num_noeud and payload['key']<table_voisinage[1][0]):
            sendMsg(False, "resp", payload['ip'], payload['port'], IP_perso, port_perso, payload['key'], {}, [], num_noeud)
        elif(payload['key']>=table_voisinage[1][0]):
            sendMsg(False, "get_resp", table_voisinage[1][1], table_voisinage[1][2], payload['ip'], payload['port'], payload['key'])
        elif(payload['key']<num_noeud):
            sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])

    elif(payload['type'] == "resp"):
        ip_resp = payload['ip']
        port_resp = payload['port']
        key_resp = payload['keyResp']

    elif(payload['type'] == "new"):
        if(payload['ip'] != IP_perso):
            sendMsg(False, "new", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'])
            if(payload['key'] > table_voisinage[0][0] and payload['key'] < num_noeud):
                majTv(payload)
    
    elif(payload['type']== "put"):
        if(payload['key'] > table_voisinage[0][0] or payload['key'] < table_voisinage[1][0] or payload['key']==num_noeud):
            majData(payload)
            sendMsg(False, "ack", payload['ip'], payload['port'], "", 0, 0, {}, [], 0, 0, payload['idUnique'], 0, 0, 0, "ok")
        else:
            if(payload['key'] < table_voisinage[0][0]):
                sendMsg(False, "put", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])
            elif(payload['key'] > table_voisinage[1][0]):
                sendMsg(False, "put", table_voisinage[1][1], table_voisinage[1][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])
    
    elif(payload['ack']):
        print("La valeur du \'put\' ", payload['idUnique'], " a été acceptée")

    elif(payload['type']=="get"):
        if(payload['key'] > table_voisinage[0][0] or payload['key'] < table_voisinage[1][0] or payload['key']==num_noeud):
            val = getData(payload['key'])
            sendMsg(False, "answer", payload['ip'], payload['port'], "", 0, payload['key'], {}, [], 0, val)
        else:
            if(payload['key'] < table_voisinage[0][0]):
                sendMsg(False, "get", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
            elif(payload['key'] > table_voisinage[1][0]):
                sendMsg(False, "get", table_voisinage[1][1], table_voisinage[1][2], payload['ip'], payload['port'], payload['key'])

    elif(payload['type']=="answer"):
        print("La valeur du noeud ", payload['key'], " est ",payload['val']) 
        answer_key = payload['key']
        answer_val = payload['val']   

    elif(payload['type'] == "quit" and payload['msgGest'] == num_noeud):
        return True
    
    return False


##########################################################################################################################
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                            MAIN                                                        #
#                                                                                                                        #
#                                                                                                                        #
#                                                                                                                        #
##########################################################################################################################

stop = False
init()
my_join()
while(stop == False):
    payload = receive()
    stop = decide(payload)