.. _`gdal.ogr.formats.openair`:

==============================================
OpenAir - OpenAir Special Use Airspace Format
==============================================

(GDAL/OGR >= 1.8.0)

Ce pilote lit les fichiers décrivant les *Special Use Airspaces* au format 
OpenAir.

Airspace sont retournés sous forme de features d'une couche unique appelée 
'airspaces', avec une géométrie de type polygone et les champs suivants : 
CLASS, NAME, FLOOR, CEILING.

Les géométries Airspace composées d'arcs seront tessélées. Les informations de 
style lorsqu'elles sont présentes sont renvoyées au niveau de la feature.

Une couche supplémentaire appelée 'labels' contiendra une feature pour chaque 
label (élément AT). Il peut y avoir de multiple enregistrement AT pour un segment 
airspace AT. Les champs sont les mêmes que ceux de la couche 'airspaces'.

Voir également
===============

* `Description du format OpenAir <http://www.winpilot.com/UsersGuide/UserAirspace.asp>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/02 (trunk 20003)