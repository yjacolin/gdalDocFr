.. _`gdal.gdal.gdalinfo`:

gdalinfo
=========

Listes des informations sur le jeu de données raster.

**Usage :**
::
    
    gdalinfo [--help-general] [-mm] [-stats] [-hist] [-nogcp] [-nomd]
         [-norat] [-noct] [-nofl] [-checksum] [-proj4] [-mdd domain]* 
         [-sd subdataset] datasetname

Le programme gdalinfo liste diverses informations sur les jeux de données 
raster supportés par GDAL.

* **-mm :** Force le calcul des valeurs min/max réelles pour chaque bande dans 
  le jeu de données.
* **-stats :** Lit et affiche des statistiques de l'image. Force le calcul si 
  aucune n'est présente dans l'image.
* **-approx_stats :** Lit et affiche les statistiques de l'image. Force leur
  calcul is aucune statistique n'est stockée dans l'image. Cependant, elles 
  peuvent être calculées en se basant sur des aperçus ou un sous jeu de données
  de toutes les tuiles. Utile si vous êtes pressé et ne désirez pas avoir des 
  statistiques précises.
* **-hist :** Renvoie des informations sur l'histogramme pour toutes les bandes.
* **-nogcp :** Supprime  l'affichage de la liste des points d'amer. Il peut être 
  utile pour certains jeux de données avec un grand nombre de points d'amer 
  (GCP) tel que L1B AVHRR ou HDF4 MODIS qui en contiennent des centaines.
* **-nomd :** Supprime l'affichage des méta-données. Certains jeux de données 
  peuvent contenir beaucoup de méta-données. 
* **-nrat :** Supprime l'affichage de la table d'attribut du raster.
* **-noct :** Supprime l'impression des tables de couleurs.
* **-checksum :** Force le calcul d'un checksum pour chaque bande du jeu de 
  données.
* **-mdd domain :** Affiche les méta-données pour le domaine défini.
* **-nofl :** (GDAL >= 1.9.0) Affiche seulement le premier fichier de la liste 
  des fichiers.
* **-sd *subdataset* :** (GDAL >= 1.9.0) Si le jeu de données en entrée contient 
  plusieurs sous jeu de données, lit et affiche un sous jeu de données avec un 
  numéro définie (à partir de 1). Ceci est une alternative à l'utiliastion d'un 
  nom complet de sous jeu de données.
* **-proj4 :** (GDAL >= 1.9.0) Affiche une chaîne PROJ.4 correspondant au système 
  de coordonnées du fichier. 

Le programme ''gdalinfo'' affichera les données suivantes (si elles sont 
connues) :

* Le pilote du format utilisé pour lire le fichier.
* La taille du raster (en pixels et en lignes). 
* Le système de coordonnées du fichier (au format OGC WKT). 
* La géotransformation associée avec le fichier (les coefficients de rotation 
  ne sont généralement pas affichés).
* Les coordonnées des bornes dans le système géoréférencé et si possible basé 
  sur lat/long sur la géotransformation entière (mais pas les points d'amer 
  ou GCP). 
* Les points d'amer (GCP en anglais).
* Les méta-données des gros fichiers (incluant les sous-jeux de données). 
* Les types de données des bandes.
* Les interprétations de couleurs des bandes.
* La taille des blocs des bandes. 
* Les descriptions des bandes.
* Les valeurs min/max des bandes (connues en interne et calculables).
* Le checksum des bandes (si le calcul est demandé).
* La valeur NODATA des bandes. 
* Les résolutions des aperçus des bandes disponibles. 
* Le type d'unité des bandes (c'est à dire "mètres" ou "pied" pour les bandes 
  d'élévation).
* Les tables de pseudo-couleurs des bandes.


**Exemple :**
::
    
    gdalinfo ~/openev/utm.tif 
    Driver: GTiff/GeoTIFF
    Size is 512, 512
    Coordinate System is:
    PROJCS["NAD27 / UTM zone 11N",
        GEOGCS["NAD27",
            DATUM["North_American_Datum_1927",
                SPHEROID["Clarke 1866",6378206.4,294.978698213901]],
            PRIMEM["Greenwich",0],
            UNIT["degree",0.0174532925199433]],
        PROJECTION["Transverse_Mercator"],
        PARAMETER["latitude_of_origin",0],
        PARAMETER["central_meridian",-117],
        PARAMETER["scale_factor",0.9996],
        PARAMETER["false_easting",500000],
        PARAMETER["false_northing",0],
        UNIT["metre",1]]
    Origin = (440720.000000,3751320.000000)
    Pixel Size = (60.000000,-60.000000)
    Corner Coordinates:
    Upper Left  (  440720.000, 3751320.000) (117d38'28.21"W, 33d54'8.47"N)
    Lower Left  (  440720.000, 3720600.000) (117d38'20.79"W, 33d37'31.04"N)
    Upper Right (  471440.000, 3751320.000) (117d18'32.07"W, 33d54'13.08"N)
    Lower Right (  471440.000, 3720600.000) (117d18'28.50"W, 33d37'35.61"N)
    Center      (  456080.000, 3735960.000) (117d28'27.39"W, 33d45'52.46"N)
    Band 1 Block=512x16 Type=Byte, ColorInterp=Gray

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/gdalinfo.html - Trunk 25410)
