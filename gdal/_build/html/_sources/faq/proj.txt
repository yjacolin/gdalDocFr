.. _`gdal.faq.proj`:

=========================================
FAQ Projection et système de coordonnées 
=========================================

Que sont les projections Well Known Text, et comment les utiliser ?
=====================================================================

*Well Known Texte* d'OpenGIS est un format textuel pour définir les systèmes de 
coordonnées. Il est assez librement basé sur le modèle de système de coordonnées 
de l'[[http:*www.epsg.org/|EPSG]]. Bien que GDAL lui-même envoie juste ces 
définitions comme des chaines textuels, il y a également une classe `OGRSpatialReference <http:*www.gdal.org/ogr/classOGRSpatialReference.html>`_ dans GDAL/OGR pour 
les manipuler et un lien vers `PROJ.4 <http:*proj.maptools.org/>`_ pour la 
transformation entre les systèmes de coordonnées. La classe *OGRSpatialReference*, 
et le lien avec PROJ.4 (mais pas PROJ.4 lui-même) sont liés dans la bibliothèque 
GDAL par défaut. Plus d'informations sur WKT et *OGRSpatialReference* peuvent être 
trouvé dans le `tutorial sur les projections dans OGR <http:*www.gdal.org/ogr/osr_tutorial.html>`_.

Puis je reprojeter des rasters avec GDAL?
============================================

Oui, vous pouvez utiliser le programme ''gdalwarp'' ou développer un programme 
qui utilise la classe `GDALWarpOperation <http://www.gdal.org/classGDALWarpOperation.html>`_ 
décrite dans le tutorial de l'`API Warp de GDAL <http://www.gdal.org/warptut.html>`_.

Pourquoi GDAL ne choisit pas automatiquement la transformation de datum ? 
===========================================================================

Il n'existe pas de chose comme un ensemble par défaut et précis de paramètres 
de transformation de datum pour un datum. OGR utilise (NADCON) par défaut, qui 
est le plus précis qui existe pour l'Amérique du Nord, mais dans le cas général 
(le monde) cela est très dur à déterminer et il n'y normalement pas de telle 
chose par défaut. La transformation qui doit être utilisée dépend de la zone 
couverte exacte, précision requise, etc. En d'autres mots, les utilisateurs 
doivent faire attention et faire leur boulot. Quelques liens : 
`FAQ de proj4 <http://proj.maptools.org/faq.html>`_, `Site <http://casoilresource.lawr.ucdavis.edu/drupal/node/259>`_, 
`Message sur la liste de diffusion <http://www.nabble.com/issue-warning-to-user-when-performing-datum-shift-%28OGR%2C-GDAL%29-t2029971.html>`_.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/10 21:31