.. _`gdal.gdal.gdal_proximity`:

================
gdal_proximity
================

produit une carte raster de proximité.

Usage
=====
::
    
    gdal_proximity.py srcfile dstfile [-srcband n] [-dstband n] 
                  [-of format] [-co name=value]*
                  [-ot Byte/Int16/Int32/Float32/etc]
                  [-values n,n,n] [-distunits PIXEL/GEO]
                  [-maxdist n] [-nodata n] [-fixed-buf-val n]

Description
============

Le script ``gdal_proximty.py`` génère une carter raster de proximité indiquant 
la distance  du centre de chaque pixel au centre du pixel le plus proche 
identifié comme le pixel cible. Les pixels cibles sont ceux du raster source 
pour lequel la valeur du pixel du raster est dans l'ensemble des valeurs des 
pixels cibles.

* **srcfile :** le fichier raster source pour identifier les pixels cibles.
* **dstfile :** le fichier raster de destination dans laquelle la carte de 
  proximité sera écrite.
* **-srcband n :** identifie la bande dans le fichier source à utiliser (1 par 
  défaut).
* **-srcband n :** identifie la bande dans le fichier de destination à utiliser 
  (1 par défaut).
* **-of format :** sélectionne le format de sortie. GeoTIFF par défaut (GTiff). 
  Utilisez le nom du format court.
* **-co "NAME=VALUE" :** envoie une option de création au pilote du format de 
  sortie. De multiplies options *-co* peuvent être listé. Lisez la documentation 
  spécifique du format pour les options légales de création pour chaque format.
* **-ot datatype :** force le type spécifique de la bande d'images en sortie. 
  Utilisez les noms de type (c'est-à-dire Byte, Int16...)
* **-values n,n,n :** une liste de valeurs de pixel cible dans l'image source à 
  considérer comme des pixels cibles. Si elle n'est pas définie, tous les pixels 
  différents de zéro seront considérés comme des pixels cibles.
* **-distunits PIXEL/GEO :** indique si les distances générées doivent être en 
  pixel ou en coordonnées géoéréférencées (PIXEL par défaut).
* **-maxdist n :** la distance maximale à générer. Tous les pixels au-delà de 
  cette distance se verront assignés soit la valeur *nodata* soit 65535. La 
  distance est interprétée en pixel à moins que le paramètre *-distunits GEO* 
  ne soit définie.
* **-nodata n :** définie nue valeur *nodata* à utiliser pour le raster de 
  proximité de destination.
* **-fixed-buf-val n :** définie une valeur à appliquer à tous les pixels qui 
  sont à *-maxdist* des pixels cibles (pixels cibles inclut) à la place d'une 
  valeur de distance.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/18 22:10 (http://gdal.org/gdal_proximity.html Page originale)
