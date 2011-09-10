.. _`gdal.gdal.gdalbuildvrt`:

=============
gdalbuildvrt
=============

Construit un VRT à partir d'une liste de jeu de données.

Usage
======

::
    
    gdalbuildvrt [-tileindex field_name] [-resolution {highest|lowest|average|user}]
             [-tr xres yres] [-tap] [-separate] [-allow_projection_difference] [-q]
             [-te xmin ymin xmax ymax] [-addalpha] [-hidenodata]
             [-srcnodata "value [value...]"] [-vrtnodata "value [value...]"]
             [-input_file_list my_liste.txt] [-overwrite] output.vrt [gdalfile]*


Description
=============

Ce programme construit un fichier VRT (Jeu de données virtuel) qui est une 
mosaïque d'une liste de jeux de données de GDAL en entrée. La liste des jeux de 
données de GDAL en entrée peut être définie à la fin de la ligne de commande, 
ou placer dans un fichier texte (un nom de fichier par ligne) pour les listes 
importantes, ou cela peut être un index de tuile de MapServer (voir l'utilitaire 
:ref:`gdal.gdal.gdaltindex` ). Dans ce dernier cas, toutes les entrées dans l'index de 
tuile seront ajoutées au VRT.

Avec l'option *-separate*, chaque fichiers est placé dans une bande séparée et 
empilée dans les bandes VRT. Autrement, les fichiers sont considéré comme des 
tuiles d'une mosaïque plus importante et le fichier VRT a autant de bande que 
ceux des fichiers en entrée.

Si un jeu de données de GDAL est réalisé à partir de plusieurs sous jeu de 
données et ne possède aucune bande raster, tous les sous jeux de données seront 
ajoutés au fichier VRT plutôt que le jeu de données lui-même.

``gdalbuildvrt`` réalise quelques vérifications pour s'assurer que tous les 
fichiers qui seront mis dans le VRT ont des caractéristiques similaires : nombre 
de bandes, projection, interprétation de couleur... Sinon, les fichiers qui ne 
correspondent pas aux caractéristiques communes seront ignorés.

S'il y a un certain taux de recouvrement, ente les fichiers, l'ordre de 
superposition peut dépendre de l'ordre où ils sont insérés dans le fichier VRT, 
mais vous ne devez pas compter sur ce comportement.

Cette commande est en partie différente de la commande ``gdal_vrtmerge.py`` et 
est compilé par défaut à partir de GDAL 1.6.1.

* **-tileindex :** utilise la valeur définie comme champ d'index de tuile, au 
  lieu de la valeur par défaut, 'location'.
* **-resolution {highest|lowest|average|user} :** Si la résolution de tous les 
  fichiers en entrée n'est pas la même, l'option ``-resolution`` permet à 
  l'utilisateur de contrôler la manière dont la résolution en sortie sera 
  calculée. ``average`` est celle par défaut. 'highest' prendra les plus petites 
  valeurs de la dimension des pixels au sein du jeu de raster. 'lowest' prendra 
  les plus grandes valeurs de la dimension des pixels au sein du jeu de raster. 
  'average' calculera une moyenne des dimensions des pixels au sein du jeu de 
  rasters. 'user' est nouveau dans GDAL 1.7.0 et doit être utilisé en 
  combinaison avec l'option *-tr* pour définir une résolution cible.
* **-tr xres yres :** (à partir de GDAL 1.7.0) définie la résolution cible. 
  Les valeurs doivent être exprimées en unité géorérérencée. Les deux valeurs 
  doivent être positives. Définir ces valeurs est bien sur incompatible avec les 
  valeurs *highest|lowest|average* de l'option *-resolution*.
* **-tap :** (GDAL >= 1.8.0) (*target aligned pixels*) aligne les coordonnées de 
  l'étendue du fichier en sortie avec les valeurs de l'option *-tr*, de telle 
  sorte que l'étendue alignée inclus l'étendue minimale.
* **-te xmin ymin xmax ymax  :** (à partir de GDAL 1.7.0) définie les étendues 
  géoréférencées d'un fichier vrt. Les valeurs doivent être exprimées en unité 
  du géoréférencement. Si celle-ci n'est pas définie, l'étendue du VRT est la 
  boîte minimale du jeu des rasters sources.
* **-addalpha :** (à partir de GDAL 1.7.0) ajoute une bande de masque alpha au 
  VRT quand le raster source en possède une. Utile principalement pour les 
  sources RGB (ou les sources en niveau de gris). La bande alpha est rempli à 
  la volée avec la valeur 0 dans les zones sans raster source, et la valeur 255 
  dans les zones avec un raster source. Cela permet à un visualiseur RGBA 
  d'afficher les zones sans rasters source en transparence et les zones avec 
  des rasters sources en opaque. Cette option n'est pas compatible avec 
  l'option *-separate*.
* **-hidenodata :** (à partir de GDAL 1.7.0) même si les bandes contiennent des 
  valeurs *nodata*, cette option permet au bande VRT de ne pas renvoyer la 
  valeur *NoData*. Cela est utile lorsque vous désirez contrôler la couleur 
  d'arrière plan du jeu de données. En l'utilisant en parallèle avec l'option 
  *-addalpha*, vous pouvez préparer un jeu de données qui ne renvoie pas la valeur 
  *nodata* mais est transparent dans la zone qui contient aucune donnée.
* **-srcnodata value [value...] :** (à partir de GDAL 1.7.0) définie les 
  valeurs *nodata* au niveau de la bande en entrée (différentes valeurs peuvent 
  être fournies pour chaque bande). Si plus d'une valeur est fournie toutes les 
  valeurs doivent être entre guillemet pour les réunir ensemble comme argument 
  unique. Si l'option n'est pas définie, les définitions *nodata* intrinsèques 
  sur le premier jeu de donnée seron utilisé (s'ils existent). La valeur définie 
  par cette option est écrit dans l'élément *NODATA* de chaque élément 
  *ComplexSource*. Utilisez une valeur à *None* pour ignorer les définitions 
  *nodata* intrinsèques des jeux de données sources.
* **-vrtnodata value [value...] :** (à partir de GDAL 1.7.0) définie les valeurs 
  *nodata* au niveau de la bande vrt (différentes valeurs peuvent être fournies 
  pour chaque bande). Si plus d'une valeur est fournie toutes les valeurs doivent 
  être entre guillemet pour les réunir ensemble comme argument unique. Si 
  l'option n'est pas définie, les définitions *nodata* intrinsèques sur le 
  premier jeu de donnée seron utilisé (s'ils existent). La valeur définie par 
  cette option est écrit dans l'élément *NoDataValue* de chaque élément 
  *VRTRasterBand*. Utilisez une valeur à *None* pour ignorer les définitions 
  *nodata* intrinsèques des jeux de données sources.
* **-separate :** (à partir de GDAL 1.7.0) place chaque fichier en entré dans 
  une bande séparée et empilée. Dans ce cas, seule la première bande de chaque 
  jeu de données sera placé dans une nouvelle bande. Contrairement au mode par 
  défaut, il ne nécessite pas que toutes les bandes aient le même type de 
  données.
* **-allow_projection_difference :** (à partir de GDAL 1.7.0) quand cette option 
  est définie, la commande acceptera de réaliser un VRT même si les jeux de 
  données en entrée n'ont pas la même projection. Note : cela ne signifie pas 
  qu'ils seront reprojeté. Leurs projections seront simplement ignoré.
* **-input_file_list :** pour définir un fichier texte avec un nom de fichier à 
  chaque ligne.
* **-q :** (à partir de GDAL 1.7.0) pour désactiver la barre de progression dans 
  la console.
* **-overwrite :** écrase le VRT s'il existe déjà.

Exemple
========

::
    
    gdalbuildvrt doq_index.vrt doq/*.tif
    gdalbuildvrt -input_file_list my_liste.txt doq_index.vrt
    gdalbuildvrt -separate rgb.vrt red.tif green.tif blue.tif
    gdalbuildvrt -hidenodata -vrtnodata "0 0 255" doq_index.vrt doq/*.tif


.. yjacolin at free.fr, Yves Jacolin - 2010/12/28 15:12 (http://gdal.org/gdalbuildvrt.html Trunk 21324)
