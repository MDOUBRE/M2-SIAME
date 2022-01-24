import socket
import json
import random
import sys
import logging as log

liste_port = [1883, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
#liste_port = [1883, 10000, 20000, 30000]

IP = socket.gethostbyname(socket.gethostname())
port = liste_port[random.randint(0, 15)]

jsonFrame = { }
jsonFrame['type'] = "put"
jsonFrame['ip'] = IP
jsonFrame['port'] = port
jsonFrame['key'] = random.randint(0, 65534)
jsonFrame['val'] = random.randint(0, 500)
jsonFrame['idUnique'] = random.randint(0, 1000)

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

