.. _`gdal.ogr.formats.sdts`:

======
SDTS
======

Les jeux de données SDTS TVP (profile vectoriel topologique *Topological Vector 
Profile*) et *Point Profile* sont gérés en lecture. Chaque module attribut 
primaire, noeud (point), ligne et polygone sont créé comme une couche distincte.

Pour sélectionner un transfert SDTS, le nom du fichier catalogue doit être 
utilisé. Par exemple *TR01CATD.DDF* où les quatre  premiers caractères sont ce 
qui typiquement varie.

Les informations des systèmes de coordonnées de SDTS sont proprement gérées pour 
la plupart des systèmes de coordonnées définie dans SDTS.

Il n'y a pas de gestion de création ou de mise à jour dans le pilote SDTS.

Notez que dans les jeux de données TVP la géométrie polygonal est formée à partir 
de la géométrie dans les modules lignes. Les attributs des modules d'attribut 
primaire doivent être proprement attachés à leur objet noeud, ligne ou polygone 
attaché, mais peuvent être accédé séparément de leur propre couche.

Ce pilote ne gère pas les jeux de données SDTS raster (DEM).

Voir également
==============

* `Bibliothèque d'abstraction de SDTS <http://home.gdal.org/projects/sdts/index.html>`_ : 
  la bibliothèque de base utilisé pour implémenter le pilote.
* http://mcmcweb.er.usgs.gov/sdts : Page web sur principale SDTS de l'USGS.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/25 22:17 (trunk 9815)