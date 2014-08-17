.. _`gdal.ogr.formats.filegdb`:

=================================================
Pilote des fichiers Geodatabase d'ESRI (FileGDB)
=================================================

Le pilote FileGDB fournie un accès en lecture et écriture vers les fichiers 
géodatabase (répertoire .gdb) créés par ArcGIS 10 et supérieur.

Dépendances
============

* `SDK de l'API FileGDB <http://resources.arcgis.com/content/geodatabases/10.0/file-gdb-api>`_

.. versionadded:: OGR >= 1.9.0

Chargement d'entités par lot
=============================

.. versionadded:: OGR >= 1.9.2

L'option de configuration FGDB_BULK_LOAD peut être définie à YES pour accélerer 
l'insertion d'entité (ou parfois pour résoudre des problèmes lors de l'insertion 
un lot d'entités - voir `Ticket #4420 <http://trac.osgeo.org/gdal/ticket/4420>`_). 
L'effet de cette option de configuration est d'écrire un blocage d'écriture et une 
désactivation temporaire des indexes. Ceux-ci sont restorés lorsque le jeu de données 
est fermé ou quand une opération de lecture est réalisée.

Gestion de SQL 
===============

.. versionadded:: OGR >= 1.10

Les requêtes SQL sont lancé par le moteur SQL de l'API du SDK FileGDB. Ceci est 
valable pour les requêtes de type non-SELECT. Cependant, dû à la gestion 
imprécise/partielle pour les requêtes SELECT dans les versions actuelles de 
l'API du SDK FileGDB SDK API (v1.2), les requêtes SELECT seront lancé par 
défaut par le moteur SQL d'OGR. Cela peut être changé en spécifiant l'option 
*-dialect FileGDB* à ogrinfo ou ogr2ogr.

Requêtes SQL spéciales
=========================

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
* **XYTOLERANCE, ZTOLERANCE :** ces paramètres contrôlent la tolération 
  d'aimantations utilisée pour les fonctionnalités avancé d'ArcGIS comme les 
  règles de topologie et les réseaux. Ils n'affecteront pas les opérations d'OGR, 
  mais ils seront utilisé par ArcGIS. Les unités des paramètres sont les unités du 
  système de référence des coordonnées.
  Les valeurs par défaut d'ArcMap 10.0 et OGR pour XYTOLERANCE sont 0.001m (ou équivalent) 
  pour les systèmes de coordonnées projetés, et 0.000000008983153° pour les systèmes 
  de coordonnées géographique.
* **XORIGIN, YORIGIN, ZORIGIN, XYSCALE, ZSCALE :** ces paramètres contrôlent la 
  `grille de précision des coordonnées <http://help.arcgis.com/en/sdk/10.0/java_ao_adf/conceptualhelp/engine/index.html#//00010000037m000000>`_  
  dans le fichier geodatabase. Les dimensions de la grille sont déterminées par 
  l'origine et l'échelle. L'origin définie la localisation de points de grille de référence 
  dans l'espace. L'échelle est la réciproque de la résolution. Par conséquent, pour 
  obtenir nue grille avec une origine à 0 et une résolution de 0.001 sur tous 
  les axes, vous définieres toutes les origines à 0 et toutes les échelles à 1000.

   .. important::
     Le domaine définie par ``(xmin=XORIGIN, ymin=YORIGIN, xmax=(XORIGIN + 9E+15 / XYSCALE), ymax=(YORIGIN + 9E+15 / XYSCALE))`` 
     nécessite d'englober chaque valeur de coordonnées possible pour la classe 
     d'entité. Si des entités sont ajoutées avec des coordonnées qui sont en dehors 
     du domaine, des erreurs apparaitront dans ArcGIS avec l'index spatial, la 
     sélection des entités et l'export des données.
    
    Valeurs par défaut d'ArcMap 10.0 et OGR :
    
    * pour les systèmes de coordonnées géographiques : XORIGIN=-400, 
      YORIGIN=-400, XYSCALE=1000000000
    * pour les systèmes de coordonnées projetées : XYSCALE=10000 pour une valeur 
      par défaut de XYTOLERANCE de 0.001m. XORIGIN et YORIGIN changent en 
      fonction du système de coordonnées, mais une valeur par défaut d'OGR de 
      -2147483647 est conforme avec celle par défaut de XYSCALE pour tous les 
      systèmes de coordonnées.

* **XML_DEFINITION** : quand cette option est définie, sa valeur sera utilisé comme 
   définition XML pour créer une nouvelle table. Le noeud racine d'une telle définition 
   XML doit être l'élément <esri:DataElement> conforme à FileGDBAPI.xsd
  
  .. versionadded:: gdal >= 1.10
  
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

* `Page des fichiers Géodatabade d'ESRI <http://resources.arcgis.com/content/geodatabases/10.0/file-gdb-api>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/03/24 (trunk 25229)