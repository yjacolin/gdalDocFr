.. _`gdal.python.raster.intro`:


Raster
=======

Lire un fichier Raster
-------------------------

Les drivers
**************

Vous devez charger les drivers pour les utiliser. Pour charger les drivers en 
une fois (pour lire un raster seulement, pas pour écrire), utiliser :
::
    
    gdal.AllRegister()

Puis créez votre objet driver :
::

    driver = gdal.GetDriverByName('SRTMHGT')

enfin enregistrez le :
::
    
    driver.Register()

Lire un fichier raster
**********************

Vous pouvez maintenant lire un fichier raster sous forme de jeu de données 
(dataset) :
::
    
    file = '~/Local/Data/Raster/N43E004.hgt'
    ds = gdal.Open(file, gdal.GA_ReadOnly)

La méthode Open() prend deux paramètres : le chemin du fichier et la méthode de 
lecture. Vous avez deux constantes possibles pour la méthode de lecture :

::
    
    GA_ReadOnly = 0
    GA_Update = 1

Si python vous renvoie un message d'erreur sur la constante *GA_ReadOnly*, vous 
pouvez la remplacer par sa valeur (0 donc).

Lorsque le jeu de données est chargé on test si son ouverture ne pose pas de 
problème :
::
    
    if ds is None:
        print 'impossible d ouvrir '+file
        sys.exit(1)

Voici quelques méthodes définies pour récupérer de l'information sur vos données :
::
    
    ds.GetProjection() # obtenir la projection

En plus des méthodes définie dans l'API il existe trois propriétés :
::
    
    ds.RasterXSize
    ds.RasterYSize
    ds.RasterCount

Bande
*******

Pour travailler sur les pixels, nous devons obtenir la bande :
::
    
    band = ds.GetRasterBand(1)

Puis récupérons les données dans un tableau :
::
    
    data = band.ReadAsArray(xOffset, yOffset, 1, 1)

1,1 est la taille de la cellule que nous voulons récupérer.

xOffset et yOffset sont obtenu en calculant la distance en pixel entre le bord 
en haut à gauche et le point pour chaque axes (ordonnés et abscisses). Nous 
connaissons les coordonnées du point haut gauche, la taille d'une cellule en 
pixel. Nous avons donc :
::
    
    xOffset (en pixel) = (originX - X) (en coordonnées)
    1 pixel            = pixelWidth (en coordonnées)
    ------------------------------------------------------
    xOffset = (originX - X) (en coordonnées) / pixelWidth

Même chose pour les ordonnées !

Si notre data set est la couche N43E004.hgt (format SRTM), gdalinfo nous donne ceci :
::
    
    $ gdalinfo N43E004.hgt
    Driver: SRTMHGT/SRTMHGT File Format                    
    Files: N43E004.hgt
    Size is 1201, 1201
    Coordinate System is:
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            TOWGS84[0,0,0,0,0,0,0],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
        AXIS["Lat",NORTH],
        AXIS["Long",EAST],
        AUTHORITY["EPSG","4326"]]
    Origin = (3.999583333333333,44.000416666666666)
    Pixel Size = (0.000833333333333,-0.000833333333333)
    Corner Coordinates:
    Upper Left  (   3.9995833,  44.0004167) (  3d59'58.50"E, 44d 0'1.50"N)
    Lower Left  (   3.9995833,  42.9995833) (  3d59'58.50"E, 42d59'58.50"N)
    Upper Right (   5.0004167,  44.0004167) (  5d 0'1.50"E, 44d 0'1.50"N)
    Lower Right (   5.0004167,  42.9995833) (  5d 0'1.50"E, 42d59'58.50"N)
    Center      (   4.5000000,  43.5000000) (  4d30'0.00"E, 43d30'0.00"N)
    Band 1 Block=1201x1 Type=Int16, ColorInterp=Undefined
    NoData Value=-32768
    Unit Type: m

En python faîtes :
::
    
    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]

Si nous cherchons la valeur de la coordonnées (43.2, 4.2) :
::
    
    xOffset = int((4.2 - originX) / pixelWidth)
    yOffset = int((43.2 - originY) / pixelHeight)

Si vous avez un offset négatif, il est fort probable que vous ayez choisit un point en dehors de la zone de couverture du raster. Nous pouvons relancer la commande suivante :
::
    
    data = band.ReadAsArray(xOffset, yOffset, 1, 1)

Les données (cad la variable data) est un tableau en 2 dimensions de la taille qui a été définie plus haut (1,1). Pour récupérer une valeur du tableau :
::
    
    value = data[0,0]

Comment récupérer tous le raster dans le tableau à deux dimensions ? En définissant les offset à 0 et en donnant la largeur et la hauteur du raster dans la taille de la cellule à récupérer.

Le tableau de valeur est un tableau de colonne, les deux valeurs sont bien des colonnes et des lignes et non des coordonnées. De plus la première ligne et la première colonne commencent à 0 !

.. note::
    **Quelques conseils :**

    Ne lisez pas un pixel à chaque fois mais récupérer les tous en une fois, puis traiter les. Ne lisez qu'un pixel à la fois si vous êtes sur d'en avoir besoin que d'un ou deux ! Malheureusement pour de gros jeux de données, cela peut poser problème ;) La solution est d'utiliser la taille des blocs ou de lire une ligne et de faire le traitement voulu, puis traiter la ligne suivante.
    Ne traitez pas un pixel à la fois, mais utiliser les fonctions built-in de Python, notamment le module Numpy ou Numeric.

Écrire un fichier Raster
-------------------------
