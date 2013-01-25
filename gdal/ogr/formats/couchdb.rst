.. _`gdal.ogr.formats.couchdb`:

===========================
CouchDB - CouchDB/GeoCouch
===========================

(GDAL/OGR >= 1.9.0)

Ce pilote peut se connecter à un service CouchDB, potentiellement avec l'extension
spatial GeoCouch. GDAL/OGR doit avoir été compilé avec la gestion de Curl pour 
compiler le pilote de CouchDB.

Le pilote gère les opérations en lecture et écriture.

Concepts CouchDB vs OGR
========================

Une base de données CouchDB est considérée comme un couche OGR. Un document 
CouchDB est considéré comme une feature OGR.

OGR prend en charge de préférence les documents CouchDB qui suivent les 
spécifications GeoJSON.

Syntaxe du nom de jeu de données
=================================

La syntaxe pour ouvrir une source de données CouchDB est : ``couchdb:http://example.com[/layername]`` 
où http://example.com pointe vers la racine d'un dépôt CouchDB et, en option, 
*layername* est le nom de la base de données CouchDB.

Il est également possible d'ouvrir directement une vue : 
``couchdb:http://example.com/layername/_design/adesigndoc/_view/aview[?include_docs=true]``
*include_docs=true* peut être nécessaire en fonction de la valeur renvoyée par 
l'appel de *emit()* dans la fonction *map()*.

Authentification
=================

Certaines opérations, en particulier les opérations d'écriture, nécessitent une 
authentification.
L'authentification peut être envoyée avec la variable d'environnement 
*COUCHDB_USERPWD* définie par *user:password* ou directement dans l'URL.

Filtrage
=========

Le pilote transmettra n'importe quel filtre défini avec *SetSpatialFilter()* vers
le serveur quand l'extension GeoCouch est disponible. Il fera de même pour les 
filtres attributaires (très simples) définis avec *SetAttributeFilter()*.
Lorsque l'évaluation des filtres échoue côté serveur, le filtre sera évalué côté client.

Par défaut, le pilote tentera d'utiliser la fonction filtre spatial suivante
"_design/ogr_spatial/_spatial/spatial", qui est la fonction filtre spatial 
valide pour les couches créées par OGR. Si cette fonction filtre n'existe pas, 
mais qu'une autre existe, vous pouvez la définir avec l'option de configuration 
*COUCHDB_SPATIAL_FILTER*.

Notez que la première fois qu'une requête d'attribut est envoyée, il peut être 
nécessaire d'avoir des permissions d'écriture dans la base de données pour créer une 
nouvelle vue d'index.

Pagination
===========

Les features sont récupérées à partir du serveur par tranche de 500 par défaut. 
Ce nombre peut être modifié avec l'option de configuration *COUCHDB_PAGE_SIZE*.

Gestion de l'écriture
=======================

La création et la suppression de table sont possibles.

La gestion de l'écriture est seulement activée lorsque la source de données est 
ouverte en mode update.

Lors de l'insertion d'une nouvelle feature avec *CreateFeature()*, et si la 
commande réussit, OGR ira chercher les champs \_id et \_rev renvoyés et les
utilisera.

Gestion de l'écriture et transactions OGR
==========================================

Les opérations *CreateFeature()* / *SetFeature()* sont par défaut transmises au
serveur en synchronisation avec l'appel de l'API d'OGR. Cela peut cependant 
entrainé des problèmes de performances lorsque de nombreuses commandes sont 
enclenchées à cause d'un surplus d'échanges clients/serveurs..

Il est possible d'entourer les opérations *CreateFeature()* / *SetFeature()* entre 
*OGRLayer::StartTransaction()* et *OGRLayer::CommitTransaction()*. Les opérations 
seront stockées en mémoire et seulement exécutées au moment de l'appel de 
*CommitTransaction()*.

Options de création de couche
==============================

Les options de création de couche suivantes sont gérées :

* **UPDATE_PERMISSIONS = LOGGED_USER|ALL|ADMIN|function(...)|DEFAULT :** Met à 
  jour les permissions pour la nouvelle couche.

  * si définie à LOGGED_USER (défaut), seuls les utilisateurs identifiés
    pourront réaliser des modifications sur la couche.
  * si définie à ALL, tous les utilisateurs pourront faire des modifications sur 
    la couche.
  * si définie à ADMIN, seulement les administrateurs pourront faire des 
    modifications sur la couches.
  * si elle commence par "function(", la valeur de l'option de création sera 
    utilisée comme contenu de la `fonction validate_doc_update <http://guide.couchdb.org/draft/validation.html>`_.
  * sinon, tous les utilisateurs seront autorisés à réaliser des modifications 
    dans les *non-design* documents.

* **GEOJSON = YES|NO :** définissez la à *NO* pour éviter l'écriture de documents 
  comme documents JSON. *Yes* par défaut.
* **COORDINATE_PRECISION = int_number :** nombre maximal de chiffre après le 
  séparateur décimal à écrire pour les coordonnées. 15 par défaut. Une troncature 
  intelligente sera réalisée pour supprimer les zéros inutiles.

  .. note::
    Lors de l'ouverture d'un jeu de données en mode update, l'option de 
    configuration *OGR_COUCHDB_COORDINATE_PRECISION* peut être définie pour avoir
    un rôle similaire.

Exemples
========

Lister les tables d'un répertoire CouchDB :

::
    
    ogrinfo -ro "couchdb:http://some_account.some_couchdb_server.com"


Créer et remplir une table à partir d'un shapefile :

::
    
    ogr2ogr -f couchdb "couchdb:http://some_account.some_couchdb_server.com" shapefile.shp


.. seealso::

  * `Référence de CouchDB <http://wiki.apache.org/couchdb/Reference>`_
  * `Dépôt du code source de GeoCouch <http://github.com/couchbase/geocouch>`_
  * `Documentation pour la fonction 'validate_doc_update' <http://guide.couchdb.org/draft/validation.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/01/23 (trunk 22490)
