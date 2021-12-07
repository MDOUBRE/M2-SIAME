import json
import socket

IP_perso="192.168.0.18"
port_perso=1883

IP_envoi="192.168.0.13"
port_envoi=10001

def sendMsg():        
    jsonFrame = { }
    jsonFrame['type'] = "test"
    jsonFrame['contenu'] = "On ets la"

    # envoi du message et fermeture de la socket
    print("\n")
    print("Envoi de ", type)

    tpsoc_envoi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #co = False
    tpsoc_envoi.connect((IP_envoi, port_envoi))
    #while(co==False):
        #try:
            #tpsoc_envoi.connect((IP, port))
            #co=True
        #except:
            #print("fuck")
    tpsoc_envoi.send(bytes(json.dumps(jsonFrame), "utf-8"))
    tpsoc_envoi.close()  


def receive():
    tpsoc_rcv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tpsoc_rcv.bind(('', port_perso))
    except socket.error as e:
        print("ERREUR COUTE SUR LE PORT DE BASE")
    tpsoc_rcv.listen(2)
    try:
        client, addr = tpsoc_rcv.accept()
    except socket.error : 
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
        return
    payload = json.loads(rec)
    #tpsoc_rcv.close()
    return payload


while(1):
    sendMsg()
    payload=receive()
    print(payload['type'])