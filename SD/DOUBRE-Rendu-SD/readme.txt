Ce fichier readme sert simplement à comprendre les deux dossiers.

1er dossier "v1" :
Ce dossier contient les fichiers python tp.py, put.py, get.py, quit.py et sdist.sh.
Tous ces fichiers servent à l'exe mais pour la lancer il suffit de alncer le script bash dans un terminal via la commande "bash sdist.sh"
Ce premier dossier est le programme pour la versio cercle.

2ème dossier "v2" :
Ce dossier contient les mêmes fichiers que le premier mais contenant des codes différents.
Ce deuxième dossier est le programme pour la version chord (du moins le début).
Pour l'exe, comme our le premier programme il suffit de taper "bash sdist.sh" dans un terminal

Pour lancer plus ou moins de noeuds et/ou modifier le nombre de put et get vous pouvez simplement modifier le script sheel.
Si toutefois vous voulez lancer des noeuds sans utiliser les scrpits alors il y a 2 commandes :
1er noeud : python3 tp.py <port_perso>
autres : python3 tp.py <port_perso> <ip_acces> <port_acces>
Il y a des exemples dans les scripts shell si nécessaire.