.. _`gdal.gdal.gdalwarp`:

gdalwarp 
=========

Utilitaire de déformation et de re-projection d'image simple. 


**Usage :**
::
    
    gdalwarp [--help-general] [--formats]
        [-s_srs srs_def] [-t_srs srs_def] [-to "NAME=VALUE"]
        [-order n] [-tps] [-rpc] [-geoloc] [-et err_threshold]
        [-te xmin ymin xmax ymax] [-tr xres yres] [-ts width height]
        [-wo "NAME=VALUE"] [-ot Byte/Int16/...] [-wt Byte/Int16]
        [-srcnodata "value [value...]"] [-dstnodata "value [value...]"] -dstalpha
        [-r resampling_method] [-wm memory_in_mb] [-multi] [-q]
        [-of format] [-co "NAME=VALUE"]*
        srcfile* dstfile

La commande ``gdalwarp`` est une commande de déformation et de re-projection 
d'image. Le programme peut re-projeter dans n'importe quelles projections 
supportées, et appliquer les points d'amer stockés avec l'image si l'image est 
« brute » avec les informations de contrôle.

* **-s_srs srs def :** Définition de la référence spatiale de la source. Le 
  système de coordonnées qui peut être utilisé sont ceux supportés par l'appel 
  de OGR Spatial *Reference.SetFromUserInput()*, ce qui inclut les déclarations 
  EPSG, GCS (c'est-à-dire EPSG:4296), PROJ.4 (comme ci-dessus), ou le nom d'un 
  fichier .prf contenant un texte « well known ».
* **-t_srs srs_def :** Définition de la référence spatiale de la cible. Le 
  système de coordonnées qui peut être utilisé sont ceux supportés par l'appel 
  de OGR Spatial *Reference.SetFromUserInput()*, ce qui inclut les déclarations 
  EPSG, GCS (c'est-à-dire EPSG:4296), PROJ.4 (comme ci-dessus), ou le nom d'un 
  fichier .prf contenant un texte « well known ».
* **-to NAME=VALUE :** définie une option de transformation disponible pour être 
  envoyé à la méthode *DALCreateGenImgProjTransformer2()*.
* **-order n :** ordre de l'équation polynomiale utilisé pour déformer  (1 à 3). 
  La valeur par défaut pour choisir un ordre polynomial se base sur le nombre 
  de points d'amer.
* **-tps :** active l'utilisation de la transformation de type « thin plate 
  spline » basé sur les points d'amer disponible. 
* **-rpc :** force l'utilisation des RPC.
* **-geoloc :** force l'utilisation des tableaux Geolocation.
* **-et err_threshold :** seuil d'erreur pour l'approximation de la 
  transformation (en pixel – par défaut à 0,125).
* **-te xmin ymin xmax ymax :** définie l'étendue géoréférencée du fichier à 
  créer en sortie.
* **-tr xres yres :** définie la résolution du fichier en sortie (en unité 
  du géoréférencement cible).
* **-ts width height :** définie la taille du fichier en sortie en pixels et 
  lignes. si *width* ou *height* est définie à 0, les autres dimensions seront 
  supposées à partir de la résolution calculée. Notez que ``-ts`` ne peut pas 
  être utilisé avec ``-tr``.
* **-wo "NAME=VALUE" :** définie une option de déformation. La doc de 
  *GDALWarpOptions::papszWarpOptions* montre toutes les options. Multiple 
  options **-wo** peuvent être listé.
* **-ot type :** pour définir le type des bandes en sortie.
* **-wt type :** type de donnée des pixels de travail. Les types de données des 
  pixels dans l'image source et les buffers des images de destinations.
* **-r :** Méthode de rééchantillonnage à utiliser. Les méthodes disponibles sont :

    * *near* : interpolation du plus proche voisin (par défaut, l'interpolation 
      la plus rapide, mais de moins bonne qualité).
    * *bilinear* : interpolation bilinéaire.
    * *cubic* : interpolation cubique.
    * *cubicspline* : interpolation cubique spline (algorithme le plus lent).
    * *lanczos* : interpolation *Lanczos windowed sinc*.

* **-srcnodata value [value...] :** définie les valeurs de masques nodata pour 
  les bandes en entrées (différentes valeurs peuvent être indiquées pour chaque 
  bande). Si plus d'une valeur est indiquée, toutes les valeurs devront être 
  entourées de guillemets pour être considérées comme un seul argument. Les 
  valeurs masquées ne seront pas utilisées pour l'interpolation. Utilisez une 
  valeur ``None`` pour ignorer les définitions de nodata intrinsèque du jeu de 
  données sources.
* **-dstnodata value [value...] :** définie les valeurs de masques nodata pour 
  les bandes en sortie (différentes valeurs peuvent être indiquées pour chaque 
  bande). Si plus d'une valeur est indiquée toutes les valeurs devront être 
  entourées de guillemets pour être considérées comme un seul argument. Les 
  nouveaux fichiers seront initialisés avec cette valeur et si possible la 
  valeur nodata sera enregistrée dans le fichier en sortie.
* **-dstalpha :** Créé une bande alpha en sortie pour identifier les pixels 
  nodata (non définie/transparent).
* **-wm memory_in_mb :** définie la quantité de mémoire (en mégaoctets) que 
  l'API de déformation est autorisée à utiliser pour la mise en cache.
* **-multi :** utilise une implémentation multithread pour la déformation. De 
  multiples threads seront utilisés pour calculer les morceaux de l'image et 
  exécuter des opérations d'entrée/sortie simultanément.
* **-q :** mode silencieux.
* **-of format :** sélectionne le format de sortie. Par défaut, GéoTIFF (Gtiff). 
  Utilisez le format de nom court.
* **-co "NAME=VALUE" :** passe une option de création au pilote du format en 
  sortie. De multiples options ``-co`` peuvent être listées. Lisez la 
  documentation spécifique du format pour les options de création légales pour 
  chaque format.
* **-cutline datasource :** active l'utilisation d'une ligne de découpage flou à 
  partir du nom de la source de données OGR.
* **-cl layername :** sélectionne la couche nommée à partir du jeu de données de 
  lignes de découpage.
* **-cwhere expression :** restreint des objets des lignes de découpage désirées 
  basé sur une requête attributaire.
* **-csql query :** sélectionne les objets des lignes de découpage en utilisant 
  une requête SQL au lieu de se baser sur une couche avec l'option ``-cl``.
* **-cblend distance :** définie une distance floue à utiliser pour flouter les 
  lignes de découpage (en pixels).
* **srcfile :** le nom du fichier source.
* **dstfile :** le nom du fichier de destination.

Le mosaïquage dans un fichier en sortie qui existe déjà est supporté si le 
fichier existe déjà. L'étendue spatiale d'un fichier existant ne sera pas 
modifiée pour s'accommoder aux nouvelles données, vous pouvez donc l'enlever 
dans ce cas.

Des lignes de découpage polygonales peuvent être utilisées pour restreindre la 
zone du fichier de destination qui peut être mis à jour, incluant leur mélange. 
Les éléments des lignes de découpage doivent être présents dans les unités 
géographiques des fichiers de destination.

**Exemple :**

Par exemple, une scène spot de 8 bits stocké dans un fichier GéoTIFF avec les 
points d'amer aux coins en lat/long peuvent être déformé en une projection UTM 
avec la commande suivante :
::
    
    gdalwarp -t_srs '+proj=utm +zone=11 +datum=WGS84' raw_spot.tif utm11.tif

Par exemple, le second canal d'une image RASTER stocké au format HDF avec les 
points d'amer des coins en lat/long peut être déformé en une projection UTM 
avec la commande suivante :
::
    
    gdalwarp HDF4_SDS:ASTER_L1B:"pg-PR1B0000-2002031402_100_001":2 \
       pg-PR1B0000-2002031402_100_001_2.tif

.. yjacolin at free.fr, Yves Jacolin - 2009/02/15 19:30* (http://gdal.org/gdalwarp.html Trunk 21324)
