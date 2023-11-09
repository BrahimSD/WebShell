Projet de programmation système L2 info / math-info

Sujet 2021-2022 : Serveur de web shells


*********
Serveur : 
*********
Utilisation : ./serveur.py traitant.py port
D’abord on a créé une fonction controlPort() pour avoir que des port supérieur strict a 2000.
On fait le premier handler pour crée des fils, après si on veut les tuer on peut envoyer un signal SIGINT qui sert dans notre cas à fermer toutes les connections
Pour le deuxième handler c’est pour supprimer un fils a chaque fois .
Apres on associe au serveur socket notre Host et Port dans notre cas c’est le localhost
On fait un serversocket.listen(4) pour accepter que 4 connexion simultanés max
On fait un while true pour que le serveur ne se termine pas et puisse accepter plusieurs connexions, après on a fait une redirection de l’entrée et la sortie standard : 
serveursocket c’est l’entré standard et clientsocket c’est la sortie standard et pour exécuter le fichier en utilise :
os.execvp("python3", ["python3",sys.argv[1]]),  on fait tout cela dans le fils , si on est le père on ajoute les fils a la liste childList 
et on fait un print pour afficher la connexion avec le pid de fils qui représente le numéro de chaque nouvelle session et le numero de port.

**********
Traitant1:
**********

Ce traitant il a comme unique but de vérifier si la requête lue sur l'entrée standard est bien
Celle attendu (HTTP/1.1) et GET pour récupérer des données, ensuite il affiche sur la sortie d'erreur : 
"request not supported" si la requête n’est pas un (HTTP/1.1) et GET et les donnes de la requete si
elle est valide.

**********
Traitant2:
**********

On lit 100Ko sur l'entrée standard avec la variable dataIN qui sera décodé pour pouvoir afficher les informations
Dans une variable on crée la structure HTML qui va nous permettre d'afficher la requête GET HTTP directement 
dans le navigateur avec le os.write
Et dans le body on encapsule la requête initiale avec la correct longueur du contenu

**********
Traitant3:
**********

Pour ce 3eme traitant on a utilisé aussi nos skills de technoweb, on a ajouté une zone de saisie et un bouton 
qui recharge la page , Ensuite on a décodé la saisie avec la fonction escaped_utf8_to_utf8(s) .
Pour la fonction get_param_from_url() c’est une fonction principale dans ce projet son rôle est de récupère la saisie de l’utilisateur, 
on prend le paramètre PARAMS comme une liste pour stocker à chaque fois la saisie de l’utilisateur , 
et pour récupérer le lien on a utiliser un split pour récupérer tout le lien avec la variable PATH , 
après on fait un split pour les ? avec la variable ARGS pour récupérer tous ce qui est après le ? cad la saisie ,
il nous reste maintenant que faire un split pour & et prendre le deuxième élément de la liste , 
et comme ca on arrive a choper le paramètre entrer par l’utilisateur.

**********
Traitant4:
**********

Pour le traitant 4, on veut que notre page web contient toujours une zone de saisie et un bouton 
pour la validation et en haut de page s'affichent les saisies déjà réalisées : chaque nouvelle 
saisie s'ajoute aux précédentes.

Pour réaliser cela, on a créé une variable fHist en mode open, et à chaque fois on écrit dedans 
en utilisant  la saisie de ‘l’utilisateur ,aves os.write , et pour lire le contenu on a utiliser une 
variable fHistR pour la lecture des donnés , et en sotck tous cela dans la varible histdata pour 
l’afficher dans la sortie standard 1 (navigateur) , et pour mettre des espaces on a utiliser un 
replace('\n','<br>').

**********
Traitant5:
**********

Pour le traitant 5 , c’est pareil que précèdent , on a juste ajouter le PID pour avoir des nouvelles 
session a chaque fois , on récupère le PID depuis la fonction get_param_from_url() s’il existe déjà 
sinon on le crée par os.getpid()

**********
Webshell1:
**********

Pour le webshell1 on créer un tube pour la lecture et l’écriture , on vérifier les commandes 
taper par le dup(w,2) , et en les affichent avec dup(w,1) , et pour les commandes qui 
n’affichent rien on a utiliser MARKER , et on lit caractère par caractère jusque arriver a 
MARKER et on stock ces caractères dans la variable result a chaque fois jusqu’à la fin , 
après dans le os.write on remplace le MARKER par un espace et on fait result[ :-6] pour 
recouper que les commande sans le MARKER ,et pour exécuter la commande on a 
utilisé : os.execvp('sh', ['sh','-c', f"{commande}"]).

Ainsi pour la mise en forme on a utiliser une balise style avec l’arrière plant en vert et 
les h3 sans marge , et la ligne de saisie on un utiliser un flex pour l’aligner avec la date 
qu’on a défini avec la fonction getDate().

***********
Webshell2 :
***********

Pour le webshell2 , on a créé une fonction generateReponseString () pour générer la 
réponse html , il prend deux paramètres historique et pid , après on a fait la fonction 
send_reponse() qui prend 4 paramètres traitantShell on l’ouvre en mode écriture et 
shellTraitant on l’ouvre en mode lecture pour le père , pour param c’est pour récupérer 
la saisie , après l’idée c’est créé des fifo une pour le traitantShell et l’autre pour 
shellTraitant , et c’est on est le fils on fait l’inverse on ouvre le traitantShel en lecture et 
shellTraitant en ecriture , a la fin en fait des dup2 pour vérifier dans le shell les 
commandes taper et les affichées dans le navigateur , et pour exécuter les commandes 
en utilisent un os.execvp('sh', ['sh'])



