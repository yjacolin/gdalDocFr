.. _`gdal.ogr.presentation`:

Présentation d'OGR
===================

La bibliothèque OGR Simple Features est une bibliothèque (et outils en ligne de 
commande) `open source <http://www.opensource.org/>`_ en C++ fournissant un accès 
en lecture (et parfois en écriture) d'une grande variété de formats de fichiers 
vecteur incluant les fichiers ESRI Shapefiles, S-57, SDTS, PostGIS, Oracle 
Spatial, et les formats Mapinfo mid/mif et TAB.

OGR fait partie de la bibliothèque :ref:`gdal.gdal.presentation`.

Ressource
----------

* :ref:`gdal.ogr.formats.index` : ESRI Shapefile, ESRI ArcSDE, MapInfo (tab et 
  mid/mif), GML, KML, PostGIS, Oracle Spatial, ...
* Programme OGR : ogrinfo, ogr2ogr, ogrtindex
* :ref:`gdal.ogr.sql`

Download
---------

Exécutable prêt à être utilisé
*******************************

Le meilleur moyen pour obtenir les commandes OGR prêtes à l'emploi est de 
télécharger le dernier kit `FWTools <http://fwtools.maptools.org/>`_ pour votre 
plateforme. Bien qu'importante, ceci inclus les compilations des commande OGR 
avec plusieurs composants optionnels. Une fois téléchargé suivez les instructions 
incluses pour configurer vos chemins et autres variables d'environnement 
correctement puis vous pourrez utiliser les différentes commandes OGR à partir 
de la ligne de commande. Le kit inclus également `OpenEv <http://openev.sf.net/>`_, 
un visualiseur qui affichera les fichiers vecteurs gérés par OGR.

Source
********

Le code source de ce projet est disponible en OpenSource sous licence type X 
Consortium. La bibliothèque OGR est pour le moment un sous-composant faiblement 
couplé de la bibliothèque GDAL. Vous obtenez tout GDAL pour le prix d'OGR. Voyez 
la page de `téléchargement <http://www.gdal.org/download.html>`_ de GDAL et de 
`compilation <http://www.gdal.org/gdal_building.html>`_ pour les détails pour 
obtenir les source et les compiler.

Rapport de Bug
---------------

Les bugs de GDAL/OGR peuvent être `remontés <http://trac.osgvisualiser sur le webeo.org/gdal/>`_ et 
`listé <http://trac.osgeo.org/gdal/report/1?sort=ticket&asc=0>`_ en utilisant TRAC.

Listes de diffusion
--------------------

Une liste de faible volume `gdal-announce <http://lists.osgeo.org/mailman/listinfo/gdal-announce>`_ 
où vous pouvez vous inscrire vous permet de recevoir des informations sur le 
projet GDAL/OGR.

La liste gdal-dev@lists.osgeo.org peut être utilisé pour les discussions 
sur le développement et les problèmes d'utilisation lié à OGR et aux technologies 
associées. L'inscription peut être réalisé et les archives 
`visualiser sur le web <http://lists.osgeo.org/mailman/listinfo/gdal-dev/>`_.

.. yjacolin at free.fr, Yves Jacolin - 2010/12/30 14:05 (http://gdal.org/ogr/ Trunk 17937)