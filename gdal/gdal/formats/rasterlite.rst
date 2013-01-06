.. _`gdal.gdal.formats.rasterlite`:

==================================
Rasterlite - Rasters in SQLite DB
==================================

À partir de GDAL 1.7.0, le pilote Rasterlite permet la lecture et la création de 
bases de données Rasterlite.

Ces bases de données peuvent être produites par les utilitaires de la distribution 
`rasterlite <http://www.gaia-gis.it/spatialite>`_, tel que rasterlite_load, 
rasterlite_pyramids, ....

Le pilote gère la lecture d'images en nuances de gris, en palette et RVB sous 
forme de tuiles GIF, PNG, TIFF ou JPEG.

Le pilote gère également la lecture des aperçues/pyramides, le système de 
référence spatiale et l'étendue spatiale.

Les tuiles compressé en onde ne sont pas gérées par défaut par GDAL, sauf si le 
pilote :ref:`gdal.gdal.formats.epsilon` a été compilé.

GDAL/OGR doit être compilé avec la gestion du pilote SQLite. Pour la gestion de 
la lecture, la liaison avec la bibliothèque spatialite n'est pas nécessaire, mais 
une bibliothèque sqlite3 suffisamment récente est nécessaire pour lire les bases 
de données rasterlite. La bibliothèque rasterlite n'est pas requises non plus. Pour 
la gestion de l'écriture d'une nouvelle table, la liaison avec la bibliothèque 
*est* nécessaire

Bien que la documentation de Rasterlite ne mentionne que le GIF, PNG, TIFF, JPEG 
et WAVELET (pilote EPSILON) comme formats de compression pour les tuiles, le 
pilote gère la lecture et l'écriture des tuiles internes dans n'importe quel 
format pris en charge par GDAL. De plus, le pilote Rasterlite permet aussi la 
lecture et l'écriture autant de bandes et autant de types de bandes que géré par 
le pilote pour les tuiles internes.


Syntaxe de la chaîne de connexion en mode lecture
==================================================

Syntaxe : ``'rasterlitedb_name' or 'RASTERLITE:rasterlitedb_name[,table=raster_table_prefix][,minx=minx_val,miny=miny_val,maxx=maxx_val,maxy=maxy_val][,level=level_number]``

où :

* *rasterlitedb_name* est le nom du fichier de la base de données rasterlite.
* *raster_table_prefix* est le préfixe de la table raster à ouvrir. Pour chaque 
  raster, Il y a deux tables SQLite correspondantes, suffixé avec _rasters et 
  _metadata
* *minx_val,miny_val,maxx_val,maxy_val* définie une étendue personnalisée (exprimée 
  en unité du système de coordonnées) pour le raster qui peut être différent de 
  l'étendue par défaut.
* *level_number* est le niveau de pyramide/Aperçue à ouvrir, 0 étant la base de 
  la pyramide.

Problèmes  de création
=======================

Le pilote peut créer une nouvelle base de données si nécessaire, créer une 
nouvelle table raster si nécessaire et copier un jeu de données source dans la 
table raster définie.

Si les données existent déjà dans la table raster, les nouvelles données seront 
ajoutées. Vous pouvez utiliser les options de création *WIPE=YES* pour effacer 
les données existantes.

Le pilote ne gère pas la mise à jour d'un bloc dans une table existante. Il peut 
seulement ajouter de nouvelles données.

Syntaxe pour le nom du jeu de données en sortie : ``'RASTERLITE:rasterlitedb_name,table=raster_table_prefix' or 'rasterlitedb_name'``

Il est possible de définir seulement le nom de la base de données comme de la forme 
plus haut, mais seulement si la base de données n'existe pas déjà. Dans ce cas le 
nom de la table raster sera la base du nom de la base de données elle-même.

Options de création
*******************

* **WIPE (=NO by default):** définie à YES pour supprimer toutes les données pré-
  existantes dans la table définie
* **TILED (=YES by default) :** définie à NO si le jeu de données source doit 
  être écrit comme une tuile unique dans la table raster
* **BLOCKXSIZE=n:** définie la largeur de la tuile. 256 par défaut.
* **BLOCKYSIZE=n:** définie la hauteur de la tuile. 256 par défaut.
* **DRIVER=[GTiff/GIF/PNG/JPEG/EPSILON/...] :** nom du pilote GDAL à utiliser pour 
  stocker les tuiles. GTiff par défaut.
* **COMPRESS=[LZW/JPEG/DEFLATE/...] :** (pilote GTiff) nom de la méthode de compression
* **PHOTOMETRIC=[RGB/YCbCr/...] :** (pilote GTiff) interprétation photométrique
* **QUALITY :** (pilote GTiff compressé JPEG, JPEG et WEBP) qualité JPEG/WEBP 
  1-100. 75 par défaut.
* **TARGET :** (pilote EPSILON) réduction de la taille cible comme pourcentage de 
  l'original (0-100). 96 par  défaut.
* **FILTER :** (pilote EPSILON) identifiant du filtre. 'daub97lift' par défaut.

Aperçues
=========

Le pilote gère la construction (si le jeu de données est ouvert en mode update) 
et la lecture des aperçues internes.

Si aucun aperçue interne n'est détecté, le pilote tentera d'utiliser des aperçues 
externes (fichiers .ovr).

Exemples
=========

* Accéder à une BdD rasterlite avec une table raster unique :
  ::
    
    $ gdalinfo rasterlitedb.sqlite -noct

  En sortie :
  
  ::
    

    Driver: Rasterlite/Rasterlite
    Files: rasterlitedb.sqlite
    Size is 7200, 7200
    Coordinate System is:
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]
    Origin = (-5.000000000000000,55.000000000000000)
    Pixel Size = (0.002083333333333,-0.002083333333333)
    Metadata:
    TILE_FORMAT=GIF
    Image Structure Metadata:
    INTERLEAVE=PIXEL
    Corner Coordinates:
    Upper Left  (  -5.0000000,  55.0000000) (  5d 0'0.00"W, 55d 0'0.00"N)
    Lower Left  (  -5.0000000,  40.0000000) (  5d 0'0.00"W, 40d 0'0.00"N)
    Upper Right (  10.0000000,  55.0000000) ( 10d 0'0.00"E, 55d 0'0.00"N)
    Lower Right (  10.0000000,  40.0000000) ( 10d 0'0.00"E, 40d 0'0.00"N)
    Center      (   2.5000000,  47.5000000) (  2d30'0.00"E, 47d30'0.00"N)
    Band 1 Block=480x480 Type=Byte, ColorInterp=Palette
    Color Table (RGB with 256 entries)

* Lister une BdD de table multi-raster :

  ::
    
    $ gdalinfo multirasterdb.sqlite

  En sortie :
  
  ::
    
    Driver: Rasterlite/Rasterlite
    Files:
    Size is 512, 512
    Coordinate System is `'
    Subdatasets:
        SUBDATASET_1_NAME=RASTERLITE:multirasterdb.sqlite,table=raster1
        SUBDATASET_1_DESC=RASTERLITE:multirasterdb.sqlite,table=raster1
        SUBDATASET_2_NAME=RASTERLITE:multirasterdb.sqlite,table=raster2
        SUBDATASET_2_DESC=RASTERLITE:multirasterdb.sqlite,table=raster2
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0,  512.0)
    Upper Right (  512.0,    0.0)
    Lower Right (  512.0,  512.0)
    Center      (  256.0,  256.0)

* Accéder à une table raster dans une BdD de table multi-raster :

  ::
    
    $ gdalinfo RASTERLITE:multirasterdb.sqlite,table=raster1

* Créer une nouvelle BdD rasterlite avec des données encodées en tuiles JPEG :

  ::
    
    $ gdal_translate -of Rasterlite source.tif RASTERLITE:my_db.sqlite,table=source -co DRIVER=JPEG

* Créer des aperçues internes :

  ::
    
    $ gdaladdo RASTERLITE:my_db.sqlite,table=source 2 4 8 16

* Nettoyer des aperçues internes :

  ::
    
    $ gdaladdo -clean RASTERLITE:my_db.sqlite,table=source

* Créer des aperçues externe dans un fichier .ovr :

  ::
    
    $ gdaladdo -ro RASTERLITE:my_db.sqlite,table=source 2 4 8 16


.. seealso::

* `Page principale sur Spatialite et Rasterlite <http://www.gaia-gis.it/spatialite>`_
* `Manuel sur Rasterlite <http://www.gaia-gis.it/spatialite/rasterlite-man.pdf>`_
* `Howto sur Rasterlite <http://www.gaia-gis.it/spatialite/rasterlite-how-to.pdf>`_
* `Base de données échantillon <http://www.gaia-gis.it/spatialite/resources.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/21 (trunk )