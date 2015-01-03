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

Le pilote recherche "opengis.net/gml" et une des chaînes de séparation listées 
dans l'option NAS_INDICATOR (dont la valeur par défaut est 
"NAS-Operationen.xsd;NAS-Operationen_optional.xsd;AAA-Fachschema.xsd") pour 
déterminer si l'entrée est un fichier NAS et ignore tous les fichiers qui ne 
correspondent pas.

Voir également
--------------

* `PostNAS <http://trac.wheregroup.com/PostNAS>`_
* `norGIS ALKIS-Import <http://www.norbit.de/68/>`_

.. yjacolin at free.fr, Yves Jacolin - 2014/12/11 (trunk 28131)