# TP7: home/building automation #
_________________________________

Nous avons deux possibilités pour la gestion de notre application ambiante.
Soit via python soit via domoticz.

---------------------------------
Python

Il faut 4 terminaux :
T1 ==> "python3 connect.py" (le programme qui gère les volets)
T2 ==> "python3 presence.py" (le programme qui gère les boutons pour la présence et le changement de mode entre fréquence (de base) et interuption)
T3 ==> "python3 mqtt_capt.py" (le programme qui gère les captures de données de luminosité et de température)
T4 ==> "python3 appli.py <seuil>" (le programme qui gère l'application ambiante)

Attention!! => pour l'évaluation le seuil testé était de 1000 et les interruptions sont codés avec un seuil bas de 1000 et un seuil haut de 2000 (+1000).
donc si on fait un test avec autre chose que 1000 en seuil le programme marchera sans problème en mode fréquence mais pourra avoir des intervalles ou il ne fonctionne pas en interruption.
ex : avec un seuil de 1500 la luminosité devra rester entre 1500 et 2500 mais avec les interruptions toute valeur entre 1000 et 1500 ne fera pas d'interruption et donc ne sera pas gérer alors qu'il y a un manque de lumière.
---------------------------------

---------------------------------
Domoticz

Il faut 2 terminaux :
T1 ==> "python3 connect.py" (le programme qui gère les volets)
T2 ==> "python3 mqtt_capt.py" (le programme qui gère les captures de données de lumlinosité et de température)
T3 ==> "python3 LED.py" (le programme qui gère l'allumage de notre led simulant la lumière)

Une fois ces deux programmes lancés il suffit de faire des actions dans domoticz comme allumer ou éteindre la lumière ou encore monter ou baisser un volet.
C'est actions sont montrées en capture d'écran dans notre rapport de TP.