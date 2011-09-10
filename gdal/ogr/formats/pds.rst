.. _`gdal.ogr.formats.pds`:

==================================
PDS - Planetary Data Systems TABLE
==================================

(GDAL/OGR >= 1.8.0)

Ce pilote lit les objets TABLE d'un jeu de données PDS.

Notez qu'il y a un pilote PDS dans GDAL pour lire les objets IMAGE raster à 
partir de jeux de données PDS.

Un fichier label du produit doit être fourni au pilote (même quand les données 
sont placées dans un fichier séparé).

Si le fichier label contient un objet *TABLE*, il sera lu comme la seule couche 
du jeu de données.

Si aucun objet *TABLE* n'est trouvé, le pilote cherchera tous les objets contenant 
la chaîne TABLE et lire chacune d'elle dans une couche.

Les tables ASCII et BINARY sont gérées. Le pilote peut récupéré les descriptions 
de champs à partir d'un objet COLUMN en ligne ou à partir d'un fichier séparé 
pointé par ^STRUCTURE.

Si la table a des colonnes LONGITUDE et LATITUDE de type REAL et avec UNIT=DEGREE, 
elles seront utilisées pour renvoyer les géométries POINT.

Voir également
---------------

* `Description du format PDS <http://pds.nasa.gov/documents/sr/>`_ (voir l'annexe 
  A.29 du fichier StdRef_20090227_v3.8.pdf).

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 19988)