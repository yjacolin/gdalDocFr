.. _`gdal.gdal.gdaltransform`:

gdaltransform
===============

Reprojete des coordonnées

**Usage :**
::
    
    gdaltransform [--help-general]
        [-i] [-s_srs srs_def] [-t_srs srs_def] [-to "NAME=VALUE"]
        [-order n] [-tps] [-rpc] [-geoloc]
        [-gcp pixel line easting northing [elevation]]*
        [srcfile [dstfile]]

Description
------------

La commande ''gdaltransform'' reprojete une liste de coordonnées vers n'importe 
quelle projection gérée, incluant les transformations basées sur les points 
d'amer (GCP).

* **-s_srs srs def :** définition de la référence spatiale de la source. Le 
  système de coordonnées qui peut être envoyé est n'importe lequel géré par 
  l'appel *OGRSpatialReference.SetFromUserInput()*, ce qui inclut EPSG PCS et 
  points d'amer (c'est-à-dire EPSG:4296), les déclarations PROJ.4 (comme 
  ci-dessus), ou le nom d'un fichier .prj contenant un format Well Known Text.
* **-t_srs srs_def :** définition de la référence spatiale de la cible. Le 
  système de coordonnées qui peut être envoyé est n'importe lequel géré par 
  l'appel *OGRSpatialReference.SetFromUserInput()*, ce qui inclut EPSG PCS et 
  points d'amer (c'est-à-dire EPSG:4296), les déclarations PROJ.4 (comme 
  ci-dessus), ou le nom d'un fichier .prj contenant un format Well Known Text.
* **-to NAME=VALUE :** définie une option de transformation disponible à envoyer 
  à *GDALCreateGenImgProjTransformer2()*. 
* **-order n :** ordre de la fonction polynomiale utilisé pour le découpage 
  (1 à 3). Par défaut la valeur est basée sur le nombre de points d'amer 
  disponible.
* **-tps :** force l'utilisation d'une transformation par interpolation 
  (thin plate spline) basée sur les points d'amer disponibles.
* **-rpc :** force l'utilisation des RPCs. 
* **-geoloc :** force l'utilisation des tableaux de géolocation.
* **-i :** transformation inverse : de la destination vers la source.
* **-gcp pixel line easting northing [elevation] :** fourni un point d'amer à 
  utiliser pour la transformation (généralement ou plus sont requis).
* **srcfile :** fichier avec la définition de la projection source ou les points 
  d'amer. S'il n'est pas donné, la projection source est lu à partir de la 
  ligne de commande *-s_srs* ou les paramètres *-gcp*.
* **dstfile :** fichier avec la définition de la projection de destination.

Les coordonnées sont lues par pair (ou triplet) de nombre par ligne de l'entrée 
standard, transformée, et écrite vers la sortie standard de la même manière. 
Toutes les transformations offertes par ''gdalwarp'' sont prises en charge, 
incluant celles basées sur les points d'amer.

Notez que l'entrée et la sortie doivent toujours êtrer sous forme décimale. Il n'y 
pas de gestion actuellement pour l'entrée et la sortie en DMS.

Si un fichier image en entré est fournie, input est en coordonnées pixel/ligne 
sur cette image. Si un fichier sorti est fourni, l'output est en coordonnées 
pixel/ligne sur cette image.

Exemple de reprojection
------------------------

Simple reprojection d'un système de coordonnées projeté à un autre :

::
    
    gdaltransform -s_srs EPSG:28992 -t_srs EPSG:31370
    177502 311865

Produit la sortie suivante en mètre dans la projection "Belge 1972 / Belgian 
Lambert 72" :

::
    
    244510.77404604 166154.532871342 -1046.79270555763

Exemple d'image RPC
--------------------

La commande suivante demande une transformation basée sur des RPC en utilisant 
le modèle RPC associé avec le fichier nommé. Parce que l'option *-i* (inverse) est 
utilisée, la transformation part des coordonnées géoréférencées (WGS84) en 
sortie vers des coordonnées d'images.

::
    
    gdaltransform -i -rpc 06OCT20025052-P2AS-005553965230_01_P001.TIF
    125.67206 39.85307 50                    

produit cette sortie mesurée en pixel et lignes d'une image :

::
    
    3499.49282422381 2910.83892848414 50

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 ([http://gdal.org/gdaltransform.html r25410)
