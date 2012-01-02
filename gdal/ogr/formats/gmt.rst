.. _`gdal.ogr.formats.gmt`:

GMT ASCII Vectors (.gmt)
=========================

OGR gère la lecture et l'écriture  au format vecteur ASCII de GMT. C'est le 
format utilisé par le paquet *Generic Mapping Tools* (GMT), et inclus les 
ajouts récents au format pour prendre en charge les types de géométries, et les 
attributs. Pour l'instant les fichiers GMT sont seulement géré s'ils ont 
l'extension ".gmt". Les anciens (simples) fichiers GMT sont traité soit comme 
des fichiers points soit des fichiers lignes selon si une ligne de ">" est 
rencontré avant le premier vertex. Les nouveau styles de fichiers ont une 
variété d'information auxiliaire incluant le type de la géométrie, les étendues 
des couches, le système de coordonnées et les déclarations des champs 
attributaires en commentaire dans l'en-tête, et pour chaque objet géométrique 
peut avoir des attributs.

Problème de création
---------------------

Le pilote gère la création de nouveau fichiers GMLT et l'ajout d'objet 
géométriques additionnel à des fichiers existant, mais la mise à jour d'objet 
géométrique existant n'est pas géré. Chaque couche est créer comme un fichier 
.gmt séparé.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 21:19 (trunk 11029)