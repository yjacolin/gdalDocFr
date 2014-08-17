.. _`gdal.ogr.formats.sua`:

SUA - Tim Newport-Peace's Special Use Airspace Format
======================================================

(GDAL/OGR >= 1.8.0)

Ce pilote lit les fichiers décrivant le format .SUA des Special Use Airspaces dans 
le Tim Newport-Peace.

Airspace sont retournée comme features d'une couche unique, avec une géométrie de 
type Polygon et les champs suivants : TYPE, CLASS, TITLE, TOPS, BASE.

Les géométries Airspace faites d'arcs seront téssélées.

Voir également
--------------

* `Description du format .SUA <http://soaring.gahsys.com/TP/sua.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/04 (trunk )