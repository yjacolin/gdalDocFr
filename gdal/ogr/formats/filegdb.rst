.. _`gdal.ogr.formats.filegdb`:

=================================================
Pilote des fichiers Geodatabase d'ESRI (FileGDB)
=================================================

Le pilote FileGDB fournie un accès en lecture et écriture vers les fichiers 
géodatabase (répertoire .gdb) créés par ArcGIS 10 et supérieur.

Dépendances
============

* `SDK de l'API FileGDB <http://resources.arcgis.com/fr/content/geodatabases/10.0/file-gdb-api>`_
.. versionadded:: OGR >= 1.9.0

Chargement d'entités par lot
=============================

.. versionadded:: OGR >= 1.10

L'option de configuration FGDB_BULK_LOAD peut être définie à YES pour accélerer 
l'insertion d'entité (ou parfois pour résoudre des problèmes lors de l'insertion 
un lot d'entités - voir `Ticket #4420 <http://trac.osgeo.org/gdal/ticket/4420>`_). 
L'effet de cette option de configuration est d'écrire un blocage d'écriture et une 
désactivation temporaire des indexes. Ceux-ci sont restorés lorsque le jeu de données 
est fermé ou quand une opération de lecture est réalisée.

Requêtes SQL spéciales
=======================

.. versionadded:: OGR >= 1.10

"GetLayerDefinition a_layer_name" et "GetLayerMetadata a_layer_name" peuvent être utilisé 
comme requêtes SQL spéciales pour obtenir respectivement la définition et les métadonnées 
de la table FileGDB comme contenu XML.

Options de création des jeux de données
========================================

Aucun.

Options de création des couches
================================

* **FEATURE_DATASET :** quand cette option est définie, la nouvelle couche sera créé 
  dans le répertoire nommé FeatureDataset. Si le répertoire n'existe pas déjà, celui-ci 
  sera créé.
* **GEOMETRY_NAME :** définie le nom de la colonne géométrique dans la nouvelle couche. 
  "SHAPE" par défaut.
* **OID_NAME :** nom de la colonne OID à créer. "OBJECTID" par défaut.
* **XORIGIN, YORIGIN, ZORIGIN, XYSCALE, ZSCALE :** ces paramètres contrôlent la 
  `grille de précision des coordonnées <http://help.arcgis.com/en/sdk/10.0/java_ao_adf/conceptualhelp/engine/index.html#//00010000037m000000>`_  
  dans le fichier geodatabase. Les dimensions de la grille sont déterminées par 
  l'origine et l'échelle. L'origin définie la localisation de points de grille de référence 
  dans l'espace. L'échelle est la réciproque de la résolution. Par conséquent, pour 
  obtenir nue grille avec une origine à 0 et une résolution de 0.001 sur tous 
  les axes, vous définieres toutes les origines à 0 et toutes les échelles à 1000.
* **XYTOLERANCE, ZTOLERANCE :** ces paramètres contrôlent la tolération 
  d'aimantations utilisée pour les fonctionnalités avancé d'ArcGIS comme les 
  règles de topologie et les réseaux. Ils n'affecteront pas les opérations d'OGR, 
  mais ils seront utilisé par ArcGIS. Les unités des paramètres sont les unités du 
  système de référence des coordonnées.
  
Exemples
=========

* Lire à partir d'un FileGDB et charger dans PostGIS : 
  ::
    
    ogr2ogr -overwrite -skipfailures -f "PostgreSQL" PG:"host=myhost user=myuser 
      dbname=mydb password=mypass" "C:\somefolder\BigFileGDB.gdb" "MyFeatureClass"

* Obtenir des infos détaillées du FileGDB :
  ::
    
    ogrinfo -al "C:\somefolder\MyGDB.gdb"

Notes de compilation
======================

Lisez les `exemple de compilation sous Windows de GDAL pour les plugins <http://trac.osgeo.org/gdal/wiki/BuildingOnWindows>`_. 
Vous trouverez une section similaire dans nmake.opt pour FileGDB.

Après cela, allez dans le répertoire *$gdal_source_root\ogr\ogrsf_frmts\filegdb* 
et exécutez :

::
    
    nmake /f makefile.vc plugin
    nmake /f makefile.vc plugin-install

Problèmes connus
================

* Les champs blob n'ont pas été implémenté
* FGDB coordinate snapping will cause geometries to be altered during writing. 
  Use the origin and scale layer creation options to control the snapping behavior.

Liens
======

* `Page des fichiers Géodatabade d'ESRI <http://resources.arcgis.com/fr/content/geodatabases/10.0/file-gdb-api>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/03/24 (trunk 23787)