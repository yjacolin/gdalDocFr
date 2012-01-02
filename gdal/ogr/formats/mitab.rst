.. _`gdal.ogr.formats.mitab`:

MapInfo TAB et MIF/MID
=======================

Les jeux de données Mapinfo aux formats natif (TAB) ou interchangeable (MIF/MID) 
sont gérés en lecture et écriture. La mise à jour de fichiers existants n'est 
pas gérée pour le moment.

<note>Dans le reste de ce document, on utilisera l'expression "fichier MIF/MID" 
pour désigner une paire de fichiers .MIF + .MID, et "fichier .TAB" renverra au 
jeu de fichiers d'une table Mapinfo dans sa forme binaire (généralement, les 
fichiers .TAB, .DAT, .MAP, .ID et .IND).</note>

Le pilote Mapinfo considère un dossier entier comme un *jeu de données*, et 
un fichier unique dans ce dossier comme une *couche*. Le nom du dossier doit 
donc être choisi pour nommer le jeu de données. Il est néanmoins tout à fait 
possible d'utiliser le nom d'un seul fichier (.TAB ou .MIF) du dossier pour 
nommer le jeu de données ; ce dernier sera alors considéré comme ne comprenant 
qu'une seule couche.

Les informations de système de coordonnées de Mapinfo sont gérées en lecture et 
écriture.

Problèmes de création
----------------------

Le format des fichiers .TAB nécessite que les limites (l'extension géographique) 
d'un nouveau fichier soient indiquées avant l'écriture des premières 
caractéristiques. Il n'y a toutefois pour le moment pas de mécanisme propre pour 
paramétrer les limites par défaut d'un nouveau fichier avec l'interface 
*OGRDataSource*. Nous comptons corriger le pilote pour être en mesure d'indiquer 
des limites par défaut pour chaque projection, mais actuellement, le pilote 
Mapinfo règle les limites par défaut d'un nouveau fichier comme suit :

* Pour un fichier en coordonnées géographiques (Lat/Lon) : ``LIMITES (-180, -90) (180, 90)``
* Pour toute autre projection : ``LIMITES (-30000000, -15000000) (30000000, 15000000)`` 

Si aucun système de coordonnées n'est fourni à la création de la couche, c'est 
la *projection* qui est utilisée par défaut, pas le système *géographique*, ce 
qui peut entraîner une précision très grossière si les coordonnées sont vraiment 
géographiques. Vous pouvez ajouter *-a_srs WGS84* à la ligne de commande 
``ogr2ogr`` pendant la conversion pour forcer le mode géographique.

Les données attributaires de Mapinfo connaissent un certain nombre de 
limitations :

* Seuls les champs *Integer*, *Real* et *String* (chaîne de caractère) peuvent 
  être créés. La liste variée et les champs de type binaire ne peuvent pas être 
  créés.
* Pour les champs de type *Chaîne de caractères*, la taille du champ est 
  utilisée pour établir la taille du stockage dans le fichier .DAT. Cela signifie 
  que les chaînes plus longues que la longueur du champ seront tronquées.
* Les champs de type *Chaîne de caractères* sans longueur assignée sont 
  considérés comme ayant 254 caractères.


Options de création de jeux de données
---------------------------------------

* **FORMAT=MIF :** Pour créer des fichiers .MIF/.MID au lieu de fichiers .TAB 
  (la sortie est en .TAB par défaut).

Options de création de couche
------------------------------

* **SPATIAL_INDEX_MODE=QUICK :** A utiliser pour activer le "mode d'indexation 
  spatiale rapide".

Le comportement par défaut de MITAB depuis GDAL v1.5.0 est de générer un index 
spatial optimisé par défaut, mais cela provoque une moins grande vitesse 
d'écriture que celle que donnaient GDAL 1.4.X et précédents. Les applications 
qui nécessitent une plus grande vitesse d'écriture et qui ne se soucient pas de 
la performance des requêtes spatiales sur le fichier de sortie peuvent utiliser 
cette option pour demander la création d'un index spatial non-optimal (qui émule 
en fait le type d'index spatial produit par le pilote .TAB d'OGR avant GDAL 
1.5.0). Dans ce mode, l'écriture de fichiers peut être environ 5 fois plus 
rapide, mais les requêtes spatiales peuvent être jusqu'à 30 fois plus lentes.

Compatibilité
**************
 
Avant la v1.8.0, le pilote utilisait d'une manière incorrect un "." comme 
délimiteur pour les paramètres id: et à partir de v1.8.0 le pilote utilise une 
virgule comme délimiteur comme le prévoie la spécification Feature Style d'OGR.

Voir aussi
----------

* `MITAB <http://mitab.maptools.org/>`_

.. j.garniaux at free.fr, Jeremy Garniaux, yjacolin at free.fr, Yves Jacolin - 2011/08/02 (trunk 20882)