import socket
import json
import random
import sys
import logging as log

BUFFER_SIZE = 2048

IP_perso = "192.168.0.35" #macbook
IP_perso = "192.168.1.14" #pc windows
#IP_perso="192.168.0.18"
port_perso=1883

num_noeud = 0
table_hachage={}
table_voisinage = []

ip_resp = ""
port_resp = 0
key_resp = 0

answer_key = 0
answer_val = 0

cptGet = 0
cptPut = 0
cptGest = 0
cptGetrec = 0
cptPutrec = 0
cptGestrec = 0

join_en_cours = False
join_pallier = 0
data_join = {}
tv_join = []
key_join = 0


def creationChord():
    global num_noeud
    global table_voisinage
    num_noeud = 1
    for i in range(17):
        table_voisinage.append([num_noeud, IP_perso, port_perso])


def afficheMoi():
    print()
    print("-----------------------------------------")
    print("                    MOI                  ")
    print("Key : ", num_noeud)
    print("IP : ", IP_perso)
    print("Port : ", port_perso)
    print("-----------------------------------------")
    print()



def afficheVoisins():
    global table_voisinage

    print("-----------------------------------------")
    print("                PRECEDENT                ")
    print(table_voisinage[0])
    print("Key : ", table_voisinage[0][0])
    print("IP : ", table_voisinage[0][1])
    print("Port : ", table_voisinage[0][2])
    print()
    print("                 SUIVANT                 ")
    for i in range(1, 16):
        print("Key : ", table_voisinage[i][0])
        print("IP : ", table_voisinage[i][1])
        print("Port : ", table_voisinage[i][2])
        print()
    print("-----------------------------------------")
    print()


def afficheData():
    global table_hachage
    prec = table_voisinage[0][0]

    print("-----------------------------------------")
    print("                  DATAS                  ")
    if(prec < num_noeud):
        for i in range(prec, num_noeud+1):
            if(i in table_hachage):
                print("Key ", i, " = ", table_hachage[i])
    elif(prec > num_noeud):
        for i in range(prec, 65536):
            if(i in table_hachage):
                print("Key ", i, " = ", table_hachage[i])
        for i in range(0, num_noeud+1):
            if(i in table_hachage):
                print("Key ", i, " = ", table_hachage[i])
        
    print("-----------------------------------------")
    print()


def my_new():
    if(table_voisinage[0][0]!=num_noeud):
        envoi = 0
        while(envoi != 1):
            envoi = sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, num_noeud)

def receptionTv(table):
    global table_voisinage
    table_voisinage.append(table['precedent'])
    table_voisinage.append(table['suivant'])

def my_join(IP, port):
    global num_noeud
    global table_hachage
    global table_voisinage

    reponse = False
    while(reponse==False):
        num_noeud=random.randint(1, 65535)
        sendMsg(True,"join", IP, port, IP_perso, port_perso, num_noeud)
        # Attente de la confirmation ou non
        payload, ok=receive()
        
        if(payload['type']=="init" and payload['key']==num_noeud):
            print("OKKKK pour la cl?? ", num_noeud)
            print(payload)
            table_voisinage = payload['tv']
            liste_key = []
            liste_value = []
            datas = payload['data']
            for key in datas.keys():
                liste_key.append(key)
            for elem in liste_key:
                liste_value.append(datas[elem])
            for i in range(len(liste_key)):
                table_hachage[int(liste_key[i])] = liste_value[i]
            print(table_hachage)

            reponse = True
        elif(payload['type']=="reject"):
            print("Join refus??")
            print("RE JOIN")

    afficheMoi()
    afficheVoisins()

    my_new()

def my_put(key, val, idUnique):
    envoi = 0
    while(envoi != 1):
        sendMsg(True,"new", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key, 0, [], 0, val, idUnique)

def quit(pkey):
    global cptGestrec, cptGetrec, cptPutrec, cptGet, cptPut, cptGest
    sendMsg(True, "quit", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, pkey, {}, [], 0, 0, 0, cptGet + cptGetrec, cptPut + cptPutrec, cptGest + cptGestrec, 0)

def majTv(payload):
    if(payload['key'] > table_voisinage[0][0]):
        table_voisinage[0] = [payload['key'], payload['ip'], payload['port']]

def majData(payload):
    table_hachage[payload['key']] = payload['val']

def getData(key):
    if(key in table_hachage):
        return table_hachage[key]
    else:
        return -35536

def calcTvData(key):
    data = {}
    prec = table_voisinage[0][0]
    if(prec < key):
        for i in range(prec, key+1):
            if(i in table_hachage):
                data[i] = table_hachage[i]
    elif(prec > key):
        for i in range(prec, 65536):
            if(i in table_hachage):
                data[i] = table_hachage[i]
        for i in range(0, key+1):
            if(i in table_hachage):
                data[i] = table_hachage[i]
    return data


def sendMsg(my, type, IP, port, IP_source = "", port_source = 0, key = 0, data = {}, tv = [], keyResp = 0, val = 0, idUnique = 0, msgGet = 0, msgPut = 0, msgGest = 0, ok = 0):       
    jsonFrame = { }
    jsonFrame['type'] = type

    if(type=="join" or type=="get_resp" or type=="resp" or type=="new", type=="put" or type=="get"):
        jsonFrame['ip'] = IP_source
        jsonFrame['port'] = port_source

    if(type=="join" or type=="reject" or type=="init" or type=="get_resp" or type=="resp" or type=="new" or type=="put" or type=="get" or type=="answer" or type=="quit"):
        jsonFrame['key'] = key

    if(type=="init"):
        jsonFrame['data']= data
        jsonFrame['tv']= tv

    if(type=="put" or type=="answer"):
        jsonFrame['val'] = val

    if(type=="put" or type=="ack"):
        jsonFrame['idUnique'] = idUnique

    if(type=="ack"):
        jsonFrame['ok'] = ok

    if(type=="resp"):
        jsonFrame['keyResp'] = keyResp

    if(type=="quit"):
        jsonFrame['msgGet'] = msgGet
        jsonFrame['msgPut'] = msgPut
        jsonFrame['msgGest'] = msgGest

    # envoi du message et fermeture de la socket
    print("\nEnvoi de ", jsonFrame)
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
    return 1


def decide(payload):
    global num_noeud, IP_perso, port_perso
    global answer_key, answer_val
    global ip_resp, port_resp, key_resp
    global cptGet, cptPut, cptGest
    global cptGestrec, cptGetrec, cptPutrec
    global tv_join, data_join, key_join, join_pallier, join_en_cours

    # OK
    if(payload["type"] == "join"):
        key_join = payload['key']
        key_prec = table_voisinage[0][0]
        key_suiv = table_voisinage[1][0]      

        if(key_join==num_noeud or key_join==key_suiv or key_join==key_prec):
            sendMsg(False, "reject", payload['ip'], payload['port'], "", 0, payload['key'])
        elif(key_prec<num_noeud):
            if(key_join>key_prec and key_join<num_noeud):
                ### ici on doit lancer les 16 requ??tes
                join_en_cours = True
                data_join = calcTvData(key_join)
                tv_join.append(table_voisinage[0])
                table_voisinage[0] = [payload['key'], payload['ip'], payload['port']]
                sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, int(key_join + 1))
            else:
                sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key_prec>num_noeud):
            if((key_join>key_prec and key_join<=65535) or (key_join<num_noeud and key_join>=0)):
                ### ici on doit lancer les 16 requ??tes
                join_en_cours = True
                data_join = calcTvData(key_join)
                tv_join.append(table_voisinage[0])
                table_voisinage[0] = [payload['key'], payload['ip'], payload['port']]
                sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, int(key_join + 1))
            else:
                sendMsg(False, "join", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        else:
            if(key_join < num_noeud):
                for i in range(16):
                    val = (key_join + pow(2, i))%35535
                    if(val <=num_noeud and val>key_join):
                        tv_join.append([num_noeud, IP_perso, port_perso])
                    else:
                        tv_join.append([key_join, payload["ip"], payload["port"]])
            else:
                for i in range(16):
                    val = (key_join + pow(2, i))%35535
                    if(val <=key_join and val>num_noeud):
                        tv_join.append([key_join, payload["ip"], payload["port"]])
                    else:                        
                        tv_join.append([num_noeud, IP_perso, port_perso])
            sendMsg(False, "init", payload["ip"], payload["port"], IP_perso, port_perso, payload["key"], data_join, tv_join)

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
            if((key>key_prec and key<=65535) or (key<num_noeud and key>=0)):
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
        tmp = []
        tmp.append(key_resp)
        tmp.append(ip_resp)
        tmp.append(port_resp)
        tv_join.append(tmp)
        join_pallier+=1
        if(join_pallier==16):
            join_pallier = 0
            join_en_cours = False
            sendMsg(False, "init", payload['ip'], payload['port'], "", 0, payload['key'], data_join, tv_join)
        else:
            sendMsg(False, "get_resp", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, int(key_join + pow(2, join_pallier)))


    # OK
    elif(payload["type"] == "new"):
        print("New : ", payload['key'], " ", payload['ip'], " ", payload['port'])
        if((payload['ip'] != IP_perso) or (payload['port'] != port_perso)):
            if(num_noeud<table_voisinage[1][0]):
                if(payload['key']>num_noeud and payload['key']<table_voisinage[1][0]):
                    table_voisinage[1] = [payload['key'], payload['ip'], payload['port']]
            elif(num_noeud>table_voisinage[1][0]):
                if((payload['key']>num_noeud and payload['key']<=65535) or (payload['key']<table_voisinage[1][0] and payload['key']>=0)):
                    table_voisinage[1] = [payload['key'], payload['ip'], payload['port']]
            else:
                if((payload['key']>num_noeud and payload['key']<=65535) or (payload['key']<table_voisinage[1][0] and payload['key']>=0)):
                    table_voisinage[1] = [payload['key'], payload['ip'], payload['port']]
                #majTv(payload)
            envoi = sendMsg(False, "new", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
            while(envoi != 1):
                envoi = sendMsg(False, "new", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])

    # OK
    elif(payload["type"]== "put"):
        cptPut += 1
        cptGest += 1
        key = payload["key"]
        key_prec = table_voisinage[0][0] 

        if(key_prec<num_noeud):
            if(key>key_prec and key<=num_noeud):
                majData(payload)
                sendMsg(False, "ack", payload['ip'], payload['port'], "", 0, 0, {}, [], 0, 0, payload['idUnique'], 0, 0, 0, "ok")
            else:
                sendMsg(False, "put", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) or (key<=num_noeud and key>=0)):
                majData(payload)
                sendMsg(False, "ack", payload['ip'], payload['port'], "", 0, 0, {}, [], 0, 0, payload['idUnique'], 0, 0, 0, "ok")
            else:
                sendMsg(False, "put", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'], {}, [], 0, payload['val'], payload['idUnique'])

    # OK
    elif(payload["type"]=="ack"):
        print("La valeur du \'put\' ", payload["idUnique"], " a ??t?? accept??e")

    # OK
    elif(payload["type"]=="get"):
        cptGet += 1
        cptGest += 1
        key = payload["key"]
        key_prec = table_voisinage[0][0]

        if(key_prec<num_noeud):
            if(key>key_prec and key<=num_noeud):
                val = getData(payload['key'])
                sendMsg(False, "answer", payload['ip'], payload['port'], "", 0, payload['key'], {}, [], 0, val)
            else:
                sendMsg(False, "get", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])
        elif(key_prec>num_noeud):
            if((key>key_prec and key<=65535) or (key<=num_noeud and key>=0)):
                val = getData(payload['key'])
                sendMsg(False, "answer", payload['ip'], payload['port'], "", 0, payload['key'], {}, [], 0, val)
            else:
                sendMsg(False, "get", table_voisinage[0][1], table_voisinage[0][2], payload['ip'], payload['port'], payload['key'])

    # OK
    elif(payload["type"]=="answer"):
        if(payload["key"]==-35536):
            print("Le noeud ", payload["key"], " n'a pas de valeur") 
        else:
            print("La valeur du noeud ", payload["key"], " est ",payload["val"]) 
        answer_key = payload["key"]
        answer_val = payload["val"]   

    # OK
    elif(payload["type"] == "quit"):
        cptGetrec = payload["msgGet"]
        cptPutrec = payload["msgPut"]
        cptGestrec = payload["msgGest"]
        if(payload["key"]==num_noeud):
            print("--------------------------------")
            print("         Compteur final         ")
            print("msgPut = ", cptPutrec + cptPut)
            print("msgGet = ", cptGetrec + cptGet)
            print("msgGest = ", cptGestrec + cptGest)
            print("--------------------------------")
        else:
            quit(payload["key"])
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
            #print("ERREUR ECOUTE")
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
            incomingData = client.recv(BUFFER_SIZE).decode()
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


def put():
    key = random.randint(1, 65535)
    val = random.randint(1, 100)
    id = random.randint(1, 1000)
    envoi = 0
    while(envoi != 1):
        envoi = sendMsg(True, "put", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key, {}, [], 0, val, id)
    return key

def get():
    key = random.randint(1, 65535)
    envoi = 0
    while(envoi != 1):
        envoi = sendMsg(True, "put", table_voisinage[0][1], table_voisinage[0][2], IP_perso, port_perso, key)


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

IP_perso = socket.gethostbyname(socket.gethostname())

if(len(sys.argv)==2):
    port_perso = int(sys.argv[1])
    creationChord()  
    afficheMoi()  
    afficheVoisins()
elif(len(sys.argv)==4):
    port_perso = int(sys.argv[1])
    IP_join = sys.argv[2]
    port_join = int(sys.argv[3])
    print(port_perso)
    print(IP_join)
    print(port_join)
    my_join(IP_join, port_join)
    afficheMoi()
    afficheVoisins()
    afficheData()
else:
    print("ERREUR ARGUMENTS")
    print("STOP = TRUE\n")
    stop = True


while(stop == False):
    ok=0
    payload, ok = receive()
    if(ok==1):
        print(payload)
        stop = decide(payload)
        afficheMoi()
        afficheVoisins()
        afficheData()
        print(table_hachage)