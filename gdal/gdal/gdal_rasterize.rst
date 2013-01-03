.. _`gdal.gdal.gdal_rasterize`:

gdal_rasterize
===============

Rastérise un vecteur polygone dans un raster.

**Usage :**
::
    
    Usage: gdal_rasterize [-b band]* [-i] [-at]
       [-burn value]* | [-a attribute_name] [-3d]
       [-l layername]* [-where expression] [-sql select_statement]
       [-of format] [-a_srs srs_def] [-co "NAME=VALUE"]*
       [-a_nodata value] [-init value]*
       [-te xmin ymin xmax ymax] [-tr xres yres] [-tap] [-ts width height]
       [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
             CInt16/CInt32/CFloat32/CFloat64}] [-q]
       <src_datasource> <dst_filename>

Ce programme transforme des géométries vectorielles (points, lignes et 
polygones) dans des bande(s) raster d'une image raster. Les fichiers vecteurs 
sont lus à partir des formats vectoriels gérés par OGR.

.. note:: Les données vecteur doivent être dans le même système de coordonnées 
   que les données raster ; la reprojection à la volée n'est pas possible.

Depuis GDAL 1.8.0, le fichier cible de GDAL peut être créé par 
``gdal_rasterize``. Une des options *-tr* ou *-ts* doit être utilisé dans ce cas.

* **-b band :** la bande dans laquelle placer les valeurs. Plusieurs arguments 
  *-b* peuvent être utilisés pour transformer une liste de bandes. Par défaut, 
  seule la bande 1 est transformée.
* **-i :** inverse la rastérisation. Imposer la valeur de la brulure fixée ou 
  la valeur de la brulure associée avec le premier objet dans toute l'image en 
  dehors du polygone fournie.
* **-at :** active l'option de rasterisation ALL_TOUCHED afin que tous les 
  pixels touchés par des lignes ou des polygones seront mis à jour et pas 
  seulement ceux sur le chemin de la ligne ou dont le point centrale est dans 
  le polygone. les règles de rendu normal sont désactivé par défaut.
* **-burn value :** une valeur fixe à créer dans la bande pour tous les objets. 
  Une liste d'options -burn peut être fournit, un par bande à écrire.
* **-a attribute_name :** définit un champ d'attribut à utiliser sur l'objet 
  comme valeur finale. Cette valeur sera utilisée dans toutes les bandes en sortie.
* **-3d :** indique que la valeur finale doit être extraite à partir de la 
  valeur « Z » de l'objet (pas encore implémenté). Ces valeurs sont ajustées 
  par la valeur de rasterisation donnée par les options "-burn value" ou "-a 
  attribute_name" si ceux-ci ont été fournie. Pour l'instant seuls les points 
  et les lignes sont dessinés en 3D.
* **-l layername :** la ou les couche(s) de la source de données qui sera 
  utilisée pour les objets en entrées. Peut être définie plusieurs fois, mais 
  au moins une couche ou une option *-sql* doit être définie.
* **-where expression :** une requête SQL de style WHERE optionnel doit être 
  appliqué pour sélectionner les objets à rastériser à partir d'une ou plusieurs 
  couche(s).
* **-sql select_statement :**  requête SQL à utilisée sur la source de données 
  pour produire une couche virtuelle d'objets à rastériser.
* **-of format :** (GDAL >= 1.8.0) sélectionne le format en sortie. GeoTIFF 
  (GTiff) par défaut. Utilisez le nom de format court.
* **-a_nodata value :** (GDAL >= 1.8.0) assigne une valeur *nodata* définie aux 
  bandes en sortie.
* **-init value :** (GDAL >= 1.8.0) Pré-initialise les bandes d'image en sortie 
  avec ces valeurs. Cependant, elles ne sont pas noté comme valeur *nodata* dans 
  le fichier en sortie. Si seulement une valeur est données, la même valeur est 
  utilisée pour toutes les bandes.
* **-a_srs srs_def :** (GDAL >= 1.8.0) écrase la projection des fichiers en 
  sortie. Si non spécifié, la projection du fichier vecteur en entrée sera 
  utilisée si elle est disponible. Si les projections sont incompatible entre 
  les fichiers en entrée et en sorties, aucune tentative de reprojection ne sera 
  effectuée. La valeur de *srs_def* peut être n'importe quelle valeur sous la 
  forme gérée par GDAL/OGR, WKT complet, PROJ.4, EPSG:n ou un fichier contenant 
  le WKT.
* **-co "NAME=VALUE" :** (GDAL >= 1.8.0) passe une option de création au pilote 
  du format de sortie. De multiples options *-co* peuvent être listées. Voyez la 
  documentation spécifique du format pour les options de création légales pour 
  chaque format.
* **-te xmin ymin xmax ymax :** (GDAL >= 1.8.0) définie les étendues 
  géoréférencées. Les valeurs doivent être exprimées en unité du 
  géoréférencement. Si aucun n'est définie, l'étendue du fichier en sortie 
  sera l'étendue des couches vecteurs.
* **-tr xres yres :** (GDAL >= 1.8.0) définie la résolution cible. Les valeurs 
  doivent être exprimées en unité de géoréférencement. Les deux valeurs doivent 
  être positives.
* **-tap :** (GDAL >= 1.8.0) (*target aligned pixels*) aligne les coordonnées 
  de l'étendue du fichier en sortie aux valeurs de l'option *-tr*, tel que 
  l'étendue aligné inclue l'étendue minimale.
* **-ts width height :** (GDAL >= 1.8.0) définie la taille du fichier en sortie 
  en pixels et lignes. Notez que l'option *-ts* ne peut pas être utilisé avec 
  l'option *-tr*.
* **-ot type :** (GDAL >= 1.8.0) pour que les bandes en sortie soient du type 
  de données indiqué. Float64 par défaut.
* **-q :** (GDAL >= 1.8.0) supprime la barre de progression et autre affichage 
  d'information.
* **src_datasource :** n'importe quelle source de données supportée par OGR en 
  lecture.
* **dst_filename :** le fichier de sortie supporté par GDAL. Doit supporter le 
  mode d'accès de mise à jour. Avant la version 1.8.0 de GDAL, 
  ``gdal_rasterize`` ne pouvait pas créer de nouveau fichier de sortie.

**Exemples :**

La commande suivante rastérisera tous les polygones à partir de mask.shp en un 
fichier RGB TIFF work.tif avec la couleur rouge (RGB = 255,0,0) :

::
    
    gdal_rasterize -b 1 -b 2 -b 3 -burn 255 -burn 0 -burn 0 -l mask mask.shp work.tif
  
La commande suivante rastérisera tout les bâtiments « class A » dans le fichier 
d'élévation en sortie, en prenant l'élévation à partir de l'attribut ROOF_H :

::
    
    gdal_rasterize -a ROOF_H -where 'class="A"' -l footprints footprints.shp city_dem.tif

.. yves at georezo.net, Yves Jacolin - 2013/01/01 (http://gdal.org/gdal_rasterize.html Trunk r25410)
