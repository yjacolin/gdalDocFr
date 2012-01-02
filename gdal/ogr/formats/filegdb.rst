.. _`gdal.ogr.formats.filegdb`:

Pilote de l'API FileGDB
========================

Aperçu
--------

Le pilote FileGDB fournie un accès en lecture et écriture vers les sources de 
données basé sur FileGDB (celui créé par ArcGIS 10 et supérieur).

Dépendances
------------

* SDK de l'API FileGDB
* OGR >= 1.9.0

Usage
--------

Utilisé comme n'importe quel pilote basé sur des fichiers - pointez juste vers le 
répertoire FileGDB (un répertoire qui se termine avec le suffixe ".gdb").

* Lire à partir d'un FileGDB et charger dans PostGIS : 
  ::
    
    ogr2ogr -overwrite -skipfailures -f "PostgreSQL" PG:"host=myhost user=myuser 
      dbname=mydb password=mypass" "C:\somefolder\BigFileGDB.gdb" "MyFeatureClass"

* Obtenir des infos détaillées du FileGDB :
  ::
    
    ogrinfo -al "C:\somefolder\MyGDB.gdb"

Notes de compilation
---------------------

Lisez les `exemple de compilation sous Windows de GDAL pour les plugins <http://trac.osgeo.org/gdal/wiki/BuildingOnWindows>`_. 
Vous trouverez une section similaire dans nmake.opt pour FileGDB.

Après cela, allez dans le répertoire *$gdal_source_root\ogr\ogrsf_frmts\filegdb* 
et exécutez :

::
    
    nmake /f makefile.vc plugin
    nmake /f makefile.vc plugin-install

Problèmes connus
-----------------

Les champs date et blob n'ont pas été implémenté. C'est probablement juste quelques 
lignes de code, mais le développeur n'a pas eut assez de temps.

Liens
-----

* `Page de l'API des fichiers de Geodatabase <http://resources.arcgis.com/fr/content/geodatabases/10.0/file-gdb-api>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/07/10 (trunk 22551)