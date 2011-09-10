.. _`gdal.gdal.gdal_fillnodata`:

================
gdal_fillnodata
================

**Usage :**
::
    
    gdal_nodatafill [-q] [-md max_distance] [-si smooth_iterations]
                [-o name=value] [-b band]
                srcfile [-nomask] [-mask filename] [-of format] [dstfile]

**Description :**

Le script ``gdal_nodatafill.py`` remplit les régions sélectionné (généralement 
des zones *nodata*) en interpolant à partir de pixels valides autour des bords 
de la zone.

Des détails supplémentaires sur l'algorithme sont disponibles sur la 
documentation de *GDALFillNodata()*.

* **-q :** le script se lance en mode silencieux. La barre de progression est 
  supprimée et les messages ne sont pas affichés.
* **-md max_distance :** la distance maximale (en pixels) que l'algorithme 
  recherchera pour les valeurs à interpoler.
* **-si smooth_iterations :** le nombre d'itérations de filtre d'atténuation 
  moyen 3x3 à lancer après l'interpolation pour amortir les artefacts. Par 
  défaut il n’y a aucune itération d'atténuation.
* **-o name=value :** définie un argument spécial à l'algorithme. Pour l'instant 
  non géré.
* **-b band :** la bande sur laquelle opérée, par défaut la première bande est 
  utilisée.
* **srcfile :** le fichier source raster utilisé pour identifier les pixels 
  cibles. Seule une bande est utilisée.
* **-nomask :** n'utilise pas le masque de validité par défaut pour la bande 
  en entrée (tel que *nodata* ou le masque alpha).
* **-mask filename :** utilise la première bande du fichier spécifié comme masque 
  de validité (zéro est invalide, autre que zéro est valide).
* **dstfile :** le nouveau fichier à créer avec les résultats interpolés. S'il 
  n'est pas fourni, la bande source sera mise à jour à la place.
* **-of format :** sélectionne le format de sortie. Par défaut GeoTIFF (GTIFF). 
  Utiliser le nom court du format.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/21 19:20 (http://gdal.org/gdal_fillnodata.html Page originale)
