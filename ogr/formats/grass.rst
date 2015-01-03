.. _`gdal.ogr.formats.grass`:

GRASS
======

Le pilote GRASS peut lire les cartes vectorielles GRASS (version 6.0 et au 
delà). Chaque carte vectorielle GRASS est représentée comme une source de 
données. Une carte vectorielle de GRASS peut avoir 0, 1 ou plusieurs couches.

Les points de GRASS sont représenté comme *wkbPoint*, les lignes et limites 
comme *wkbLineString* et les surfaces comme *wkbPolygon*. *wkbMulti** et 
*wkbGeometryCollection* nesont utilisé. Des objets géométriques peuvent être 
mélangé dans une couche. Si une couche contient seulement des objets d'un seul 
type, il est définie par le type approprié et peut être récupéré par 
*OGRLayer::GetLayerDefn();*

Si une géométrie a plus de catégories de la même couche lié, il est représenté 
en autant d'objet (une pour chaque catégorie).

À la fois les cartes 2D et 3D sont gérées.

Nom de la source de données
----------------------------

Le nom de la source de données est le chemin complet vers le fichier 'head' 
dans le répertoire vector/ de GRASS. En utilisant les noms des variables 
d'environnement de GRASS, cela peut être exprimé par :
::
    
    $GISDBASE/$LOCATION_NAME/$MAPSET/vector/mymap/head

où 'mymap' est le nom d ela carte vectorielle. Par exemple :
::
    
    /home/cimrman/grass_data/jizerky/jara/vector/liptakov/head

Noms de la couche
------------------

Habituellement les numéros de la couche sont utilisé comme noms de couche. Le 
numéro 0 d'une couche est utilisé pour tous les objets sans catégorie. Il est 
possible de donner en option le nom de la couche GRASS lié à la base de données 
cependant ce n'est pas encore géré par les modules GRASS. Un nom de couche peut 
être ajouté dans le fichier vecteur 'dln' comme '/name' après le numéro de 
couche, par exemple à l'enregistrement original :

::
    
    1 rivers cat $GISDBASE/$LOCATION_NAME/$MAPSET/dbf/ dbf

il est possible d'assigner le nom 'rivers'
::
    
    1/rivers rivers cat $GISDBASE/$LOCATION_NAME/$MAPSET/dbf/ dbf

la couche 1 qui sera listée est la couche 'rivers'.

Filtre attributaire
--------------------

Si une couche a des attributs stockés dans une base de données, la requête est 
passée au pilote de la base de données sous-jacente. Ce qui signifie que les 
conditions SQL qui peuvent être utilisées dépendent des pilotes et de la base 
de données à laquelle la couche est liée. Par exemple, le pilote DBF a pour 
l'instant que très peu d'expressions SQL et PostgreSQL offrent un ensemble 
d'expression très riche.

Si une couche n'a pas d'attributs liés et n'a que des catégories, le moteur SQL 
interne à OGR est utilisé pour évaluer l'expression. Les catégories sont des 
nombres entiers attaché à une géométrie, c'est une sorte d'identifiant, mais 
ce n'est pas un FID puisque plusieurs objets géométriques dans une couche 
peuvent avoir la même catégorie.

L'évaluation est réalisée lorsque le filtre des attributs est défini.

Filtre spatial
---------------

Les boites englobantes des objets géométriques stockées dans une structure 
topologique sont utilisées pour évaluer si des géométries correspondent au 
filtre spatial en cours.

L'évaluation est réalisée une fois que le filtre spatial est défini.

GISBASE
--------

*GISBASE* est le chemin complet vers le répertoire où GRASS est installé. Par 
défaut, le pilote GRASS utilise le chemin donné par le script de configuration 
de GDAL. Un répertoire différent peut être forcé en définissant la variable 
d'environnement *GISBASE*. *GISBASE* est utilisé pour trouver les pilotes des 
bases de données GRASS.

Topologie manquante
--------------------

Le pilote GRASS peut lire les fichiers vecteurs de GRASS si la topologie est 
disponible (aka niveau 2). Si une erreur est retournée, disant que la topologie 
n'est pas disponible, il est nécessaire de construire la topologie avec 
le module ``v.build`` de GRASS.

Accès aléatoire
-----------------

Si un accès aléatoire (*GetFeature* au lieu de *GetNextFeature*) est utilisé 
sur une couche avec des attributs, la lecture des géométries peut être assez 
lente. Cela est dû au fait que le pilote doit faire une requête sur les 
attributs par catégorie pour chaque objet géométrique (pour éviter d'utiliser 
beaucoup de mémoire) et l'accès aléatoire à une base de données est 
habituellement lent. Cela peut être amélioré du côté  de GRASS  lors de 
l'optimisation et de l'écriture des fichiers basés sur des pilotes (DBF, SQLite).

Problèmes connus
----------------

À cause d'un bug dans la bibliothèque de GRASS, il est impossible de 
démarrer/arrêter les pilotes des bases de données dans l'ordre FIFO et l'ordre 
FILO doit être utilisé. Le pilote GRASS pour OGR est écrit avec cette 
limitation à l'esprit et les pilotes sont toujours fermés s'ils ne sont pas 
utilisés et si nu pilote reste ouvert, la commande *kill()* est utilisée pour 
l'arrêter. Il peut arriver cependant dans certains cas que le pilote tente 
d'arrêter un pilote de base de données qui n'est pas le dernier ouvert et 
l'application se termine. Cela peut arriver si la lecture séquentielle 
(*GetNextFeature*) d'une couche n'est pas terminée (la lecture est arrêtée 
avant que la dernière géométrie disponible ne soit atteinte), les objets d'une 
autre couche sont lu puis la lecture de la première couche est terminée, parce 
que dans ce cas-là la commande *kill()* n'est pas utilisée.

.. seealso::

  * `Page principale de GRASS <http:*grass.itc.it/>`_

Le développement de ce pilote a été financé par Faunalia (http://www.faunalia.it).

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 21:26 (trunk 10609)
