.. _`gdal.gdal.gdal_sieve`:

gdal_sieve
===========

Supprime les petits polygones raster.

Usage
-------

::
    
    gdal_sieve [-q] [-st threshold] [-4] [-8] [-o name=value]
           srcfile [-nomask] [-mask filename] [-of format] [dstfile]

Description
------------

Le script ``gdal_sieve.py`` enlève les polygones raster plus petits que la 
taille du seuil définie (en pixels) et les remplace avec la valeur du pixel du 
polygone du plus proche voisin. Le résultat peut être écrit dans la bande raster 
existante ou copié dans un nouveau fichier.

Des détails supplémentaires sur l'algorithme sont disponibles dans la 
documentation ``GDALSieveFilter()``.

* **-q :** le script se lance en mode silencieux. La barre de progression est 
  supprimée et les messages ne sont pas affichés.
* **-st threshold :** définie le seuil de la taille en pixel. Seuls les 
  polygones raster plus petits que cette taille seront supprimés.
* **-o name=value :** définie un argument spécial à l'algorithme. Pour l'instant 
  non géré.
* **-4 :** 4 connectivités doivent être utilisées lors de la détermination des 
  polygones. C'est-à-dire que les diagonales des pixels ne sont pas considérées 
  comme connectées. C'est la valeur par défaut
* **-8 :** 8 connectivités doivent être utilisées lors de la détermination des 
  polygones. C'est-à-dire que les diagonales des pixels sont considérées comme 
  directement connectées.
* **srcfile :** le fichier raster source utilisé pour identifié les pixels 
  cibles. Seule la première bande est utilisée.
* **-nomask :** n'utilise pas le masque de validité par défaut pour la bande 
  en entrée (tel que nodata ou les masques alpha).
* **-mask filename :** utilise la première bande du fichier définie comme 
  masque de validité (zéro est invalide, autre que zéro est valide).
* **dstfile :** le nouveau fichier à créer avec les résultats filtrés. S'il 
  n'est pas fourni, la bande source sera mise à jour à la place.
* **-of format :** sélectionne le format de sortie. GeoTIFF par défaut (GTiff). 
  Utilisez le nom de format court.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/19 19:57 (http://gdal.org/gdal_sieve.html Page originale)
