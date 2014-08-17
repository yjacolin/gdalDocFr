.. _`gdal.ogr.formats.nas`:

NAS - ALKIS
============

Le lecteur NAS lit le format NAS/ALKIS utilisé pour les données cadastrales en 
Allemagne.
Le format est un profile GML avec des objets GML3 complexe qui ne peuvent pas 
être lu facilement avec le pilote GML générique d'OGR.

Le pilote dépend de la compilation de GDAL/OGR avec la bibliothèque XML Xerces.

Ce pilote a été implémenté dans le contexte du projet PostNAS qui a plus 
d'information sur son utilisation.

Voir également
--------------

* `PostNAS <http://trac.wheregroup.com/PostNAS>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/02 (trunk 20162)