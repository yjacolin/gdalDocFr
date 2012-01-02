.. _`gdal.ogr.formats.svg`:

SVG - Scalable Vector Graphics
===============================

(OGR >= 1.9.0)

OGR gère la lecture du format SVG (si GDAL a été compilé avec la gestion de la 
bibliothèque *expat*).

Pour le moment, il lit uniquement les fichiers SVG qui sont renvoyé par le Serveur 
Vecteur en Flux de Cloudmade.

Toutes les coordonnées sont relative au SRS Pseudo-mercator (EPSG:3857).

Le pilote renverra 3 couches :

* points
* lines
* polygons

Voir également
---------------

* `Page SVG du W3C <http://www.w3.org/TR/SVG/>`_
* `Documentation du vecteur de Cloudmade <http://developers.cloudmade.com/wiki/vector-stream-server/Documentation>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/04 (trunk )