.. _`gdal.ogr.formats.elasticsearch`:

=========================
OGR ElasticSearch Driver
=========================

ElasticSearch:  Geographically Encoded Objects for ElasticSearch
==================================================================

.. versionadded:: GDAL 1.10 ou plus récent

Ce pilote est en **ÉCRITURE seul**

`ElasticSearch <http://elasticsearch.org/>`_ est un moteur de recherche de niveau 
Entreprise pour diverses sources de données. Il gère l'indexage full-text et les 
requêtes geospatiales de ces données d'une manière rapide et efficace en utilisant 
une API REST pré-définie. Ce pilote sérialise tous les formats de fichiers gérés 
par OGR dans un index ElasticSearch.

Définitions des champs
***********************
Les champs sont dynamiquement mappé à partir de la source de la données OGR. Cependant 
le pilote prendra avantage des options avancées dans ElasticSearch comme définie 
dans un `fichier de mappgin des champq <http://code.google.com/p/ogr2elasticsearch/wiki/ModifyingtheIndex>`_.

Le fichier de mapping vous permet de modifier le mapping en fonction des 
`types spécifiques des champs ElasticSearch <http://www.elasticsearch.org/guide/reference/mapping/core-types.html>`_. 
Il y a plusieurs options à choisir, cependant, la plupart des fonctionnalités 
sont basées sur les différentes choses que vous êtes capable de faire avec 
des champs textes dans ElasticSearch.
::
  
  ogr2ogr -progress --config ES_WRITEMAP /path/to/file/map.txt -f "ElasticSearch" http://localhost:9200 my_shapefile.shp

Le pilote d'écriture d'ElasticSearch gère les options de configuration suivants :

* **ES_WRITEMAP=/chamin/vers/mapfile.txt :** créer un fichier de mapping qui peut 
  être modifié par l'utilisateur avant d'insérer dans l'index.
* **ES_META=/chemin/vers/mapfile.txt :** informe le pilote du mapping de champs 
  définie par l'utilisateur.
* **ES_BULK=10000 :** identifie le nombre d'enregistement à insérer à la fois. 
  Un comptage d'enregistement faible aide à diminuer la consommation de mémoire 
  de ElasticSearch mais prend plus de temps à l'insertion.
* **ES_OVERWRITE=1 :** écrase l'index en cours en supprimant l'existant.

Il est possible d'appliquer plusieurs options à la fois. Le cas d'utilisation 
suivant prend avantage de fichier mapping pré-définie ainsi qu'un comptage 
d'insertion **Bulk** limité.
::
  
  ogr2ogr -progress --config ES_OVERWRITE 1 --config ES_BULK 10000 --config ES_META /path/to/file/map.txt -f "ElasticSearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

Exemples
*********

**Transformation basique :**

::
  
  ogr2ogr -progress -f "ElasticSearch" http://localhost:9200 my_shapefile.shp

**Créer un fichier de Mapping :**

Le fichier de mapping vous permet de modifier le mapping en fonction des 
`types de champs spécifiques ElasticSearch <http://www.elasticsearch.org/guide/reference/mapping/core-types.html>`_. 
Il y a plusieurs options possible, cependant, la plupart des fonctionnalités est 
basé sur toutes les différentes chosques que vous êtes capable de faire avec les 
champs textes.
::
  
  ogr2ogr -progress --config ES_WRITEMAP /path/to/file/map.txt -f "ElasticSearch" http://localhost:9200 my_shapefile.shp

**Lire le fichier de Mapping :**

Lit le fichier de mapping pendant la transformation :
::
  
  ogr2ogr -progress --config ES_META /path/to/file/map.txt -f "ElasticSearch" http://localhost:9200 my_shapefile.shp

**Uploading en bulk (pour les gros jeux de données) :**

L'upload en bulk aide lorsque vous devez charger beaucoup de données. La valeur de l'entier est le nombre de bytes qui sont collecté avant d'être inséré.
::
  
  ogr2ogr -progress --config ES_BULK 10000 -f "ElasticSearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable


**Écraser l'index en court :**

Si cela est définie, cette commande écrasera l'index en court. Autrement les donnée seront ajoutées.
::
  
  ogr2ogr -progress --config ES_OVERWRITE 1 -f "ElasticSearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

**Définir plusieurs à la fois :**

Plusieurs options peuvent être définies en même temps.

::
  
  ogr2ogr -progress --config ES_OVERWRITE 1 --config ES_BULK 10000 --config ES_META /path/to/file/map.txt -f "ElasticSearch" http://localhost:9200 PG:"host=localhost user=postgres dbname=my_db password=password" "my_table" -nln thetable

.. seealso::

* `Page principale pour ElasticSearch <http://elasticsearch.org/>`_
* `Exemples sur le Wiki <http://code.google.com/p/ogr2elasticsearch/w/list>`_
* `Google Group <http://groups.google.com/group/ogr2elasticsearch>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/03/22 (trunk 25229)