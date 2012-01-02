.. _`gdal.gdal.gdal_polygonize`:

gdal_polygonize
=================

Produit une couche polygonale à partir d'un raster.

Usage
-----

::
    
    gdal_polygonize [-o name=value] [-nomask] [-mask filename] raster_file [-b band]
                [-q] [-f ogr_format] out_file [layer] [fieldname]

Description
------------

Cette commande créée des polygones vectoriels pour toutes les zones connectés 
d'un pixel dans un raster partageant une valeur commune. Chaque polygone est 
créé avec un attribut indiquant la valeur du pixel de ce polygone. Un masque de 
raster peut aussi être fourni pour déterminer quels pixels sont éligibles pour 
le traitement.

La commande créera le jeu de données vectoriel en sortie si celui-ci n'existe 
pas, par défaut dans le format GML.

Elle est basée sur la fonction ``GDALPolygonize()`` qui possède des détails 
supplémentaires sur l'algorithme.

* **-nomask :** n'utilise pas le masque de validité par défaut pour la bande 
  en entrée (tel que nodata, ou les masques alpha).
* **-mask filename :** utilise la première bande du fichier définie comme masque 
  valide (zéro est invalide, non zéro est valide).
* **raster_file :** le fichier raster source à partir duquel les polygones sont 
  dérivés.
* **-b band :** la bande de *raster_file* à partir de laquelle construire les 
  polygones.
* **-f ogr_format :** sélectionne le format de sortie du fichier à créer. GML 
  par défaut.
* **out_file :** le fichier vecteur de destination dans lequel les polygones 
  seront écrits.
* **layer :** le nom de la couche à créer pour contenir les polygones.
* **fieldname :** le nom du champ à créer ("DN" par défaut).
* **-o name=value :** définie un argument spécial à l'algorithme. Pour l'instant 
  aucun n'est géré.
* **-q :** le script fonctionne en mode silencieux. La barre de progression est 
  supprimée et les messages du traitement ne sont pas affichés. 

.. yjacolin at free.fr, Yves Jacolin - 2009/02/19 19:38 (http://gdal.org/gdal_polygonize.html Page originale)
