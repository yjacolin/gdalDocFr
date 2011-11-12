.. _`gdal.gdal.gdal_translate`:

===============
gdal_translate
===============

Converti des données raster en différents formats.

**Usage :**
::
    
    gdal_translate [--help-general]
       [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
             CInt16/CInt32/CFloat32/CFloat64}] [-strict]
       [-of format] [-b band] [-mask band] [-expand {gray|rgb|rgba}]
       [-outsize xsize[%] ysize[%]]
       [-unscale] [-scale [src_min src_max [dst_min dst_max]]]
       [-srcwin xoff yoff xsize ysize] [-projwin ulx uly lrx lry]
       [-a_srs srs_def] [-a_ullr ulx uly lrx lry] [-a_nodata value]
       [-gcp pixel line easting northing [elevation]]*
       [-mo "META-TAG=VALUE"]* [-q] [-sds]
       [-co "NAME=VALUE"]*
       src_dataset dst_dataset

L'utilitaire ``gdal_translate`` peut être utilisé pour convertir des données 
raster en différents formats, et éventuellement réaliser des opérations comme 
re-échantillonner, réduire les pixels pendant le calcul.

* **-ot : type** Pour que la bande en sortie soit du type de données indiqué.
* **-strict :** N'oublie pas les pertes de données et les erreurs lors de la 
  transformation vers le format de sortie.
* **-of format :** Sélectionne le format de sortie. Celui par défaut est le 
  GéoTiff (GTiff). Utilisez les noms de formats courts. 
* **-b band :** Sélectionne une bande en entrée pour la sortie. Les bandes sont 
  numérotées à partir de 1. De multiples options ``-b`` peuvent être utilisées 
  pour sélectionner une série de bandes en entrée pour l'insertion dans le 
  fichier de sortie ou pour ordonner les bandes.
* **-mask *band* :** (GDAL >= 1.8.0) Sélectionne une bande *band* en entrée 
  pour créer une bande de masquage dans le jeu de données en sortie. Les bandes 
  sont numéroté à partir  de 1. *band* peut être définie à "none" pour éviter 
  de copier le masque global du jeu de données en entrée s'il existe. Autrement 
  il sera copié par défaut ("auto"), sauf si le masque est un canal alpha ou 
  s'il est explicitement utilisé pour une bande normale du jeu de données en  
  sortie ("-b mask"). *band* peut également être définie à "mask,1" (ou 
  seulement "mask") pour signifier la bande de masque de la première bande du 
  jeu de données en entrée.
* **-expand rgb|rgba:** (From GDAL 1.6.0) Présente un jeu de donné avec une 
  bande munie d'une table de couleur comme un fichier avec 3 (RVB) ou 4 
  (RVBA) bandes. Utile pour des pilotes comme JPEG, JPEG2000, MrSID, ECW qui ne 
  gèrent pas des rasters avec les tables de couleurs. La valeur 'gray' (à partir 
  de GDAL 1.7.0) permet d'étendre un jeu de données avec une table de couleur 
  qui contient seulement les niveaux de gris en un jeu de données de gris indéxé.
* **-outsize xsize[%] ysize[%] :** Définit la taille du fichier exporté. L'unité 
  est le pixel et ligne sauf si '%' est utilisé auquel cas il est une fraction 
  de la taille de l'image en entrée.
* **-scale [src_min src_max [dst_min dst_max]] :** Redimensionne la valeur du 
  pixel en entrée à partir du domaine *src_min* à *src_max* et du domaine 
  *dst_min* à *dst_max*. S'il est omis le domaine de sortie est de 0 à 255. S'il 
  est omis le domaine en entrée est automatiquement calculé à partir des données 
  sources.
* **-unscale :** Applique la méta-donnée d'échelle/d'offset pour les bandes à 
  convertir de valeurs ajustées à des valeurs non ajustées. Il est aussi souvent 
  nécessaire de redéfinir le type de données en sortie avec le paramètre **-ot**.
* **-srcwin xoff yoff xsize ysize :** Sélectionne une région à partir de l'image 
  source pour copie basée sur la location pixel/ligne.
* **-projwin ulx uly lrx lry :** Sélectionne une région à partir de l'image 
  source pour copie (comme *-srcwin*) mais avec les bords en coordonnées 
  géoréférencées.
* **-a_srs srs_def :** Écrase la projection du fichier de sortie. La paramètre 
  *srs_def* peut être de la forme de n'importe quel de ceux acceptés par 
  GDAL/ORG, WKT, PROJ4, EPSG:n ou un fichier contenant un WKT.
* **-a_ullr ulx uly lrx lry :** Assigne/écrase les bornes géoréférencées du 
  fichier géoréférencé. Cela définit les bornes géoréférencées au fichier de 
  sortie, en ignorant les conséquences.
* **-a_nodata value :** Assigne une valeur nodata définit aux bandes exportées. 
  À partir de GDAL 1.8.0, ce paramètre peut être définie à *none* pour éviter 
  de définir une valeur nodata dans le fichier en sortie si elle existe pour le 
  fichier source.
* **-mo "META-TAG=VALUE" :** Définir une clé et une valeur d'une méta-données 
  aux données en sortie si possible.
* **-co "NAME=VALUE" :** Définit une option créée pour le pilote du format de 
  sortie. Des options -co multiples peuvent être listées. Voyez la 
  documentation du format définit pour la création d'options pour chaque format.
* **-gcp pixel line easting northing elevation :** Ajoute un point d'amer 
  (GCP en anglais) indiqué aux données en sortie. Cette option peut être définie 
  plusieurs fois pour fournir un ensemble de points d'amer (GCP).
* **-q :** Supprime l'affichage du suivi de progression et autre affichage 
  d'informations.
* **-sds :** Copie tous les sous-ensembles de données de ce fichier en fichier 
  indépendant. Utilisé avec les formats HDF ou OGDI qui possèdent des 
  sous-ensembles de données.
* **src_dataset :** Le nom du fichier source. Il peut être soit un nom de 
  fichier, une URL d'une source de données ou un nom d'un sous jeu de données 
  pour les fichiers de plusieurs jeux de données.
* **dst_dataset :** Le nom du fichier de destination.


**Exemple :**
::
    
    gdal_translate -of GTiff -co "TILED=YES" utm.tif utm_tiled.tif

À partir de GDAL 1.8.0, pour créer un fichier TIFF avec une compression en JPEG 
avec un masque interne à partir un jeu de données RGBA :
::
    
    gdal_translate rgba.tif withmask.tif -b 1 -b 2 -b 3 -mask 4 -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR --config GDAL_TIFF_INTERNAL_MASK YES

À partir de GDAL 1.8.0, pour créer un jeu de données RGBA à partir d'un jeu de 
données RGB avec un masque :
::
    
    gdal_translate withmask.tif rgba.tif -b 1 -b 2 -b 3 -b mask


.. yjacolin at free.fr, Yves Jacolin - 2010/12/27 17:47 (http:*gdal.org/gdal_translate.html - Trunk 21320)

