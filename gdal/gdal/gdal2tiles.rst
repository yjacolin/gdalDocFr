.. _`gdal.gdal.gdal2tiles`:

gdal2tiles.py
==============

Génère un répertoire avec des tuiles TMS, un KML et des visualisateurs web simples.

Usage
------

::
    
    gdal2tiles.py [-p profile] [-r resampling] [-s srs] [-z zoom]
                [-e] [-a nodata] [-v] [-h] [-k] [-n] [-u url]
                [-w webviewer] [-title "Title"] [-c copyright]
                [-g googlekey] [-b bingkey] input_file [output_dir]

Description
------------

La commande génère un répertoire avec de petites tuiles et métadonnées, suivant 
la spécification du Service de Tuilage de carte de l'OSGeo. Des pages web 
simples avec des visualiseurs basés sur Google Map et OpenLayers sont générés 
également - tout le monde peut confortablement explorer vos cartes en ligne et 
vous n'avez pas besoin d'installer ou de configurer un logiciel spécial (comme 
Mapserver) et la carte s'affiche très rapidement dans le navigateur web. Vous 
avez seulement besoin de télécharger votre répertoire généré dans un serveur web.

``GDAL2Tiles`` créé également les métadonnées nécessaires pour Google Earth 
(*SuperOverlay* KML), dans le cas où la carte fournie utilise une projection 
*EPSG:4326*.

Les fichiers world et les références spatiales incluses sont utilisés durant la 
génération des tuiles, mais vous pouvez publier également une image sans le 
géoréférencement.


* **-p PROFILE, --profile=PROFILE :** Profile de coupe des tuiles (mercator, geodetic, 
  raster) - 'mercator' par défaut (compatible avec Google Maps). 
* **-r RESAMPLING, --resampling=RESAMPLING :** Méthode de reéchantillonage (average, near, 
  bilinear, cubic, cubicspline, lanczos, antialias) - 'average' par défaut.
* **-s SRS, --s_srs=SRS :** Le système de référence spatial utilisé pour la source 
  de données en entrée.
* **-z ZOOM, --zoom=ZOOM :** Niveaux de zoom à générer (format : '2-5' ou '10'). 
* **-e, --resume :** Mode résume. Génère seulement les fichiers manquants.
* **-a NODATA, --srcnodata=NODATA :** Valeur de transparence NODATA à assigner 
  aux données en entrée.
* **-v, --verbose :**  génère une sortie verbeuse lors de la génération des tuiles. 
* **-h, --help :** Affiche un message d'aide et quitte. 
* **--version :** Affiche le numéro de version du programme et quitte. 

**Options KML (Google Earth) :**

Options pour les métadonnées SuperOverlay de Google Earth

* **-k, --force-kml :** génère les fichiers KML pour Google Earth - par défaut pour 
  le profile 'geodetic' et 'raster' en EPSG:4326. Pour des sources de données dans 
  des projections différentes, utilisez le avec précaution !
* **-n, --no-kml :** Évite la génération de fichier KML pour EPSG:4326. 
* **-u URL, --url=URL :** Adresse URL où les tuiles générées seront publiées.

**Options du visualiseur Web :**

Options pour les visualiseurs HTML générés a la Google Maps.

* **-w WEBVIEWER, --webviewer=WEBVIEWER :**
    Web viewer to generate (all,google,openlayers,none) - default 'all'. 
* **-t TITLE, --title=TITLE :** Titre de la carte. 
* **-c COPYRIGHT, --copyright=COPYRIGHT :** Copyright de la carte. 
* **-g GOOGLEKEY, --googlekey=GOOGLEKEY :** Clé de l'API de Google Map, voir 
  http://code.google.com/apis/maps/signup.html. 
* **-b BINGKEY, --bingkey=BINGKEY :** Clé de l'API Bing Maps, voir https://www.bingmapsportal.com/

.. warning::
    gdal2tiles.py est un script Python qui nécessite la compilation avec la 
    liaison python de nouvelle génération.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/gdal2tiles.html Trunk r25410)
