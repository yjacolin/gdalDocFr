.. _`gdal.ogr.formats.ao`:

==================
ArcObjects d'ESRI
==================

Aperçu
=======

Le pilote ArcObjects d'OGR fournit un accès en lecture seule vers les sources de 
données ArcObjects. Puisqu'il utilise le SDK d'ESRI, il est nécessaire d'avoir 
une licence ESRI pour fonctionner. Néanmoins, cela signifie également que le 
pilote a une complète abstraction d'ESRI. Parmi ces derniers, vous avez :

* GeoDatabases :

  * GeoDatabase Personnelle (.mdb)
  * fichier GeoDatabase (.gdb)
  * GeoDatabase Entreprise (.sde).

* Shapefiles d'ESRI

Bien que cela n'ait pas été étendue pour faire cela encore (il n'y a pas eut de 
besoin), il peut potentiellement géré également les abstractions GeoDatabase 
suivantes.

* Les classes d'entités d'annotation et de dimension
* Classes de relations
* Réseaux (GN et ND)
* Topologies
* Terrains
* Représentations
* Parcel Fabrics

Vous pouvez essayer ceux-ci et ils devraient fonctionner - mais n'ont pas été 
testés. Notez que les abstractions au-dessus ne peuvent pas être gérés avec 
l'API FileGeoDatabase ouverte.


Dépendances
=============

* Une licence ArcView ou ArcEngine (ou supérieur) - est nécessaire pour que cela 
  fonctionne.
* Les bibliothèques ESRI installées. Cela est typiquement le cas si vous avez 
  installé ArcEngine, ArcGIS Desktop ou Server - Nécessaire pour compiler. Notez 
  que ce code devrait également compiler en utilisant le SDK \*nix ArcEngine, 
  cependant le développeur n'a pas accès à ce SDK et n'a donc pas pu l'essayer.

Usage
=====

Préfixé la source de données avec "AO:" 

* Lire un fichier GDB et charger les données dans PostGIS :
  ::
    
    ogr2ogr -overwrite -skipfailures -f "PostgreSQL" PG:"host=myhost user=myuser 
    dbname=mydb password=mypass" AO:"C:\somefolder\BigFileGDB.gdb" "MyFeatureClass"

* Obtenir des informations détaillées d'une GéoDatabase Personnelle :
  ::
    
    ogrinfo -al AO:"C:\somefolder\PersonalGDB.mdb"

* Obtenir des informations détaillées de la GéoDatabase Enterprise (.sde contient 
  une version cible auquel se connecter) : 
  ::
    
    ogrinfo -al AO:"C:\somefolder\MySDEConnection.sde"

Notes de compilation
=====================

Lisez :ref:`gdal.install`. Vous trouverez une section similaire dans *nmake.opt* 
pour ArcObjects.

Après cela, allez dans le répertoire *$gdal_source_root\ogr\ogrsf_frmts\arcobjects* 
et exécutez :


::
    
    nmake /f makefile.vc plugin
    nmake /f makefile.vc plugin-install

Problèmes connus
=================

Les champs *date* et *blob* n'ont pas été implémentés. C'est probablement juste 
quelques lignes de code, mais le développeur n'a pas eut assez de temps.

.. yjacolin at free.fr, Yves Jacolin - 2011/06/30 (trunk 21273)