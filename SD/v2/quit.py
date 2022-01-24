import socket
import json
import random
import sys
import logging as log

liste_port = [10000, 20000, 30000]

IP = socket.gethostbyname(socket.gethostname())
port = liste_port[random.randint(0, 2)]

jsonFrame = { }
jsonFrame['type'] = "quit"
jsonFrame['key'] = 1
jsonFrame['msgGet'] = 0
jsonFrame['msgPut'] = 0
jsonFrame['msgGest'] = 0

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
           
tpsoc_envoi.send(bytes(json.dumps(jsonFrame), "utf-8"))
tpsoc_envoi.close()

