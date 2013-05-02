.. _`gdal.ogr.formats.FMEObjects`:

====================
FMEObjects Gateway
====================

Les sources d'objet gérées par FMEObjects sont gérés en lecture par OGR si le 
pont FMEObjects est configuré, et si une copie d'une licence de FMEObject est 
installée et accessible.

Pour utiliser les lecteurs basés sur FMEObjects le nom de la source de données 
passé doit être le nom du lecteur de FME à utiliser, deux points (:) puis le 
véritable nom de la source de donnés (c'est à dire le nom du fichier). Par 
exemple *NTF:F:\DATA\NTF\2144.NTF* indiquera que le lecteur NTF doit être 
utilisé pour lire le fichier. Il y a un certain  nombre de cas spéciaux.

* une source de données se terminant par .fdd sera supposée être un fichier 
  d'une <<Définition de source de données FME>> (*FME Datasource Definition*) 
  qui contiendra le nom du lecteur, le nom de la source de données puis une 
  définition de paire de ligne  nom/valeur pour les macros qui conviennent pour 
  passer l'appel à *createReader()*.
* Une source de données nommée *PROMPT* résultera à demander à l'utilisateur 
  les informations en utilisant une boite de dialogue FME. Cela ne fonctionne 
  que sous Windows.
* Une source de données nommée <<*PROMPT:filename*>> résultera à demander, puis 
  d'avoir la définition résultante sauvée dans le fichier au format .fdd indiqué. 
  L'extension .fdd sera ajouté au nom du fichier. Cela ne fonctionne que sous 
  Windows.

Chaque objet FME sera traité comme une couche à traver OGR, nommé par le type de 
l'objet. Avec certaines limitations les systèmes de coordonnées FME sont gérés. 
Toutes les types de géométries de FME devraient être proprement gérés. Les 
attributs graphiques de FME (couleur, largeur de ligne, etc) ne sont pas 
convertie dans les informations de Style des objets d'OGR (OGR Feature Style).

Cache
========

Dans le but d'activer l'accès rapide à de large jeux de données sans avoir à 
les traduire à chaque fois qu'ils sont accédés, le pont FMEObjects gère un 
mécanisme de cache d'objet lu à partir du lecteur FME dans un "Fast Feature 
Stores", un format vectoriel natif pour FME avec un index spatial pour la 
recherche spatiale rapide. Ces fichiers en cache sont gardés dans le répertoire 
indiqué par la variable d'environnement *OGRFME_TMPDIR* (ou *TMPDIR* ou */tmp* 
ou *C:\\* si cela n'est pas disponible).

Le fichiers d'objet en cache aura un préfixe *FME\_OLEDB\_* et un index maitre est 
laissé dans le fichier *ogrfmeds.ind*. Pour enlever l'index supprimez tout ces 
fichiers. N'en enlevez pas juste quelques-uns.

Par défaut les objets dans le cache sont relus après 3 600 s (60 minutes). Le 
temps de rétention du cache est altéré au moment de la compilation en modifiant 
le fichier d'include *fme2ogr.h*.

Les entrées à partir des lecteurs de SDE et d'ORACLE ne sont pas en cache. Ces 
sources sont traitées spécialement de différentes manières également.

Avertissements
================

- Établir une session FME est une opération assez dispendieuse sur un système 
  Linux à 350Mhz, cela peut excéder 10 s.
- Les anciens fichiers dans le cache des objets sont nettoyés, mais seulement 
  lors de visite ultérieure au code du pont de FMEObjects dans OGR. Cela signifie 
  que même non utilisé, le pont FMEObjects laissera les anciens objets en cache 
  indéfiniment.

Configuration/compilation
===========================

Pour inclure un pont avec FMEObjects dans une compilation OGR il est nécessaire 
d'avoir chargé FME sur le système. Le paramètre de configuration 
*--with-fme=$FME_HOME* doit être fournie pour la configuration. Le pont 
FMEObjects n'est pas explicitement lié (il est chargé plus tard quand cela est 
nécessaire) il est donc pratique de distribuer un binaire compilé d'OGR avec la 
gestion de FMEObjects sans distribuer FMEObjects. Il fonctionnera seulement pour 
les personnes qui possèdent FMEObjects dans leur *path*.

Le pont FMEObjects a été testé sur Linux et Windows.

Plus d'information sur le produit FME et comment acheté une licence pour le 
logiciel FME (permettant la gestion de FMEObjects) peut être trouvé sur le site 
Internet de Safe Software à http://www.safe.com. Le développement de ce 
pilote a été financé par Safe Software.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 20:02 (trunk 3701)