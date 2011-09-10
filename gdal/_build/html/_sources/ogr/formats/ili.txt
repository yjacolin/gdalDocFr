.. _`gdal.ogr.formats.ili`:

=========
INTERLIS
=========

OGR gère le format INTERLIS en lecture et écriture.

`INTERLIS <http://www.interlis.ch/>`_ est un standard qui a été spécialement 
créé dans le but de répondre aux besoins de modélisation et l'intégration de 
données spatiales dans des systèmes d'information géographique future et 
contemporain. La version actuelle est INTERLIS version 2. INTERLIS version 1 
reste un standard suisse. Avec l'utilisation de données spatiales documenté et 
unifié et des possibilités d'échanges flexible les avantages suivantes apparaissent :

* la documentation standardisé ;
* l'échange de données compatible ;
* l'intégration complète des données spatiales par exemple à partir de 
  différents fournisseur de données ;
* Test de qualité ;
* le stockage des données à long terme ;
* la sécurité du *contrat-preuve* et la disponibilité du logiciel.

Modèle
=======

Les données sont lues et écrites dans des fichiers de transfert qui ont des 
formats différent dans INTERLIS 1 (.itf) et INTERLIS 2 (.xml). Pour utiliser le 
modèle INTERLIS (.ili) un interpréteur Java est nécessaire à l'exécution, et le 
fichier ili2c.jar (inclus dans le 
`compilateur pour INTERLIS 2 <http://interlis.ch/interlis2/download23_e.php#outils>`_ 
doit être dans le path. Le fichier modèle peut être ajouté au fichier de 
transfert séparé par une virgule.

Quelques transformations possible avec :ref:`gdal.ogr.ogr2ogr`.

* Interlis 1 -> Shape :
  ::
    
    ogr2ogr -f "ESRI Shapefile" shpdir ili-bsp.itf,ili-bsp.ili

* Interlis 2 -> Shape :
  ::
    
    ogr2ogr -f "ESRI Shapefile" shpdir RoadsExdm2ien.xml,RoadsExdm2ben.ili,RoadsExdm2ien.ili

  ou sans model :
  ::
    
    ogr2ogr -f "ESRI Shapefile" shpdir RoadsExdm2ien.xml

* Shape -> Interlis 1 :
  ::
    
    ogr2ogr -f "Interlis 1" ili-bsp.itf Bodenbedeckung__BoFlaechen_Form.shp

* Shape -> Interlis 2 :
  ::
    
    ogr2ogr -f "Interlis 2" LandCover.xml,RoadsExdm2ben.ili RoadsExdm2ben_10.Roads.LandCover.shp

* Import incrémental de Interlis 1 vers PostGIS :
  ::
    
    ogr2ogr -f PostgreSQL PG:dbname=warmerda av_fixpunkte_ohne_LFPNachfuehrung.itf,av.ili -lco OVERWRITE=yes
    ogr2ogr -f PostgreSQL PG:dbname=warmerda av_fixpunkte_mit_LFPNachfuehrung.itf,av.ili -append

Interpolation d'arc
====================

Les géométries d'arc d'INTERLIS sont converties en polygone.

L'angle d'interpolation peut être changé avec la variable d'environnement *ARC_DEGREES* (Par défaut : 1 degré).

Autres remarques
=================

* Plus d'information : http://gis.hsr.ch/wiki/OGR (en allemand)
* Le développement du pilote ONTERLIS d'OGR a été financé par 
  `Swiss Federal Administration <http://www.kogis.ch/>`_, 
  `Canton Solothurn <http://www.so.ch/de/pub/departemente/bjd/gis.htm>`_ et 
  `Canton Thurgovia <http://www.geoinformation.tg.ch/>`_.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/02 (trunk 21673)