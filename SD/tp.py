import socket
import json
import random
import sys
import logging as log

#from SD.chord_base import BUFFER_SIZE

BUFFER_SIZE = 2048

IP_perso="192.168.0.18"
port_perso=1883

num_noeud = 0
table_hachage={}
table_voisinage = [[0, "", 0], [0, "", 0]]

ip_resp = ""
port_resp = 0
key_resp = 0

answer_key = 0
answer_val = 0


def my_new():
    print(num_noeud)
    sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, num_noeud)

def my_join(IP, port):
    reponse = False
    global num_noeud
    while(reponse==False):
        num_noeud=random.randint(1, 65535)
        sendMsg(True,"join", IP, port, IP_perso, port_perso, num_noeud)
        # Attente de la confirmation ou non
        payload, ok=receive()
        
        if(payload['type']=="init" and payload['key']==num_noeud):
            print("OKKKK pour la clé ", num_noeud)
            table_hachage = payload['data']
            table_voisinage = receptionTv(payload['tv'])

            reponse = True
        elif(payload['type']=="reject"):
            print("Join refusé")
            print("RE JOIN")
    my_new()

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

def receptionTv(table):
    table_voisinage[0] = table['precedent']
    table_voisinage[1] = table['suivant']
    print(table_voisinage)


def majData(payload):
    table_hachage[payload['key']]= payload['val']

def getData(key):
    return table_hachage[key]

def calcTvData(key):
    tv = []
    data = {}
    print("faire tv + data")
    return tv, data


def sendMsg(my, type, IP, port, IP_source = "", port_source = 0, key = 0, data = {}, tv = [], keyResp = 0, val = 0, idUniq = 0, msgGet = 0, msgPut = 0, msgGest = 0, ok = 0):
       
    jsonFrame = { }
    jsonFrame['type'] = type

    if(type=="join" or type=="get_resp" or type=="resp" or type=="new", type=="put" or type=="get"):
        jsonFrame['ip'] = IP_source
        jsonFrame['port'] = port_source

    if(type=="join" or type=="reject" or type=="init" or type=="get_resp" or type=="resp" or type=="new" or type=="put" or type=="get" or type=="answer" ):
        jsonFrame['key'] = key

    if(type=="init"):
        jsonFrame['data']= data
        jsonFrame['tv']= tv

    if(type=="put" or type=="answer"):
        jsonFrame['val'] = val

    if(type=="put" or type=="ack"):
        jsonFrame['idUniq'] = idUniq

    if(type=="ack"):
        jsonFrame['ok'] = ok

    if(type=="resp"):
        jsonFrame['keyResp'] = keyResp

    if(type=="quit"):
        jsonFrame['msgGet'] = msgGet
        jsonFrame['msgPut'] = msgPut
        jsonFrame['msgGest'] = msgGest

    # envoi du message et fermeture de la socket
    print("Envoi de ", jsonFrame)
    print("vers ", IP, " ", port, "\n")
    tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tpsoc_envoi.connect((IP, port))
    except:
        try:
            tpsoc_envoi.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tpsoc_envoi.connect((IP, port))
        except socket.error as e:
            tpsoc_envoi.close()
            print("ERREUR SEND")
            return    
    tpsoc_envoi.send(bytes(json.dumps(jsonFrame), "utf-8"))
    tpsoc_envoi.close()


def decide(payload):
    global num_noeud
    # OK
    if(payload["type"] == "join"):
        key = payload['key']
        key_prec = table_voisinage[0][0]
        key_suiv = table_voisinage[1][0]      

        if(key==num_noeud or key==key_suiv or key==key_prec):
            sendMsg(False, "reject", payload['ip'], payload['port'], "", 0, payload['key'])
        elif(key_prec<num_noeud):
            if(key>key_prec and key<num_noeud):
                tv, data = calcTvData(key)
                sendMsg(False, "init", payload['ip'], payload['port'], "", 0, payload['key'], tv, data)
            else:
                sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) and (key<num_noeud and key>=0)):
                tv, data = calcTvData(key)
                sendMsg(False, "init", payload['ip'], payload['port'], "", 0, payload['key'], tv, data)
            else:
                sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])

    # OK
    elif(payload["type"] == "get_resp"):
        key = payload['key']
        key_prec = table_voisinage[0][0]
        key_suiv = table_voisinage[1][0]   

        if(key_prec<num_noeud):
            if(key>key_prec and key<num_noeud):
                sendMsg(False, "resp", payload['ip'], payload['port'], IP_perso, port_perso, payload['key'], {}, [], num_noeud)
            else:
                sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) and (key<num_noeud and key>=0)):
                sendMsg(False, "resp", payload['ip'], payload['port'], IP_perso, port_perso, payload['key'], {}, [], num_noeud)
            else:
                sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key==key_prec):
            sendMsg(False, "resp", payload['ip'], payload['port'], table_voisinage[0][1], table_voisinage[0][2], payload['key'], {}, [], table_voisinage[0][0])
        elif(key==key_suiv):
            sendMsg(False, "resp", payload['ip'], payload['port'], table_voisinage[1][1], table_voisinage[1][2], payload['key'], {}, [], table_voisinage[1][0])

    # OK
    elif(payload["type"] == "resp"):
        ip_resp = payload['ip']
        port_resp = payload['port']
        key_resp = payload['keyResp']

    # OK
    elif(payload["type"] == "new"):
        print("New : ", payload['key'], " ", payload['ip'], " ", payload['port'])
        if(payload['ip'] != IP_perso):
            sendMsg(False, "new", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
            if(num_noeud<table_voisinage[1][0]):
                if(payload['key']>num_noeud and payload['key']<table_voisinage[1][0]):
                    majTv(payload)
            elif(num_noeud>table_voisinage[1][0]):
                if((payload['key']>num_noeud and payload['key']<=65535) or (payload['key']<table_voisinage[1][0] and payload['key']>=0)):
                    majTv(payload)
    
    # OK
    elif(payload["type"]== "put"):
        key = payload["key"]
        key_prec = table_voisinage[0][0] 

        if(key_prec<num_noeud):
            if(key>key_prec and key<=num_noeud):
                majData(payload)
                sendMsg(False, "ack", payload['ip'], payload['port'], "", 0, 0, {}, [], 0, 0, payload['idUniq'], 0, 0, 0, "ok")
            else:
                sendMsg(False, "put", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) and (key<=num_noeud and key>=0)):
                majData(payload)
                sendMsg(False, "ack", payload['ip'], payload['port'], "", 0, 0, {}, [], 0, 0, payload['idUniq'], 0, 0, 0, "ok")
            else:
                sendMsg(False, "put", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])

    # OK
    elif(payload["type"]=="ack"):
        print("La valeur du \'put\' ", payload["idUnique"], " a été acceptée")

    # OK
    elif(payload["type"]=="get"):
        key = payload["key"]
        key_prec = table_voisinage[0][0]

        if(key_prec<num_noeud):
            if(key>key_prec and key<=num_noeud):
                val = getData(payload['key'])
                sendMsg(False, "answer", payload['ip'], payload['port'], "", 0, payload['key'], {}, [], 0, val)
            else:
                sendMsg(False, "get", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) and (key<=num_noeud and key>=0)):
                val = getData(payload['key'])
                sendMsg(False, "answer", payload['ip'], payload['port'], "", 0, payload['key'], {}, [], 0, val)
            else:
                sendMsg(False, "get", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])

    # OK
    elif(payload["type"]=="answer"):
        print("La valeur du noeud ", payload["key"], " est ",payload["val"]) 
        answer_key = payload["key"]
        answer_val = payload["val"]   

    elif(payload["type"] == "quit" and payload["msgGest"] == num_noeud):
        return True
    
    return False


def receive():
    tpsoc_rcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tpsoc_rcv.bind(('', port_perso))
    except socket.error as e:
        try:
            tpsoc_rcv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tpsoc_rcv.bind(('', port_perso))
        except socket.error as e:
            tpsoc_rcv.close()
            print("ERREUR ECOUTE")
            return None, 0  
    tpsoc_rcv.listen(2)
    try:
        client, addr = tpsoc_rcv.accept()
    except socket.error as e: 
        print("ERREUR ACCEPT")       
    rec = ''
    allReceived = False
    try:
        while(not allReceived):
            incomingData = client.recv(2048).decode()
            if(incomingData == ''):
                allReceived = True
            else:
                rec += incomingData
    except socket.error as e:
        print("ERREUR RECEPTION DONNEES")
        tpsoc_rcv.close()
        return None, 0 
    payload = json.loads(rec)
    if(payload["type"]!=None):
        tpsoc_rcv.close()
        return payload, 1



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

if(len(sys.argv)==2):
    port_perso = sys.argv[1]
elif(len(sys.argv)==4):
    IP_join = sys.argv[2]
    port_join = int(sys.argv[3])
    print(IP_join)
    print(port_join)
    my_join(IP_join, port_join)
else:
    print("ERROR lors du passage d'arguments!!!\n")
    stop = True


while(stop == False):
    ok=0
    payload, ok = receive()
    if(ok==1):
        decide(payload)
        print(table_voisinage)
