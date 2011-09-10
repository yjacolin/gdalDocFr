.. _`gdal.faq.gdal`:

===============
F.A.Q. Raster
===============

Pourquoi gdalwarp ou gdal_merge n'écrit pas la plupart des formats ?
=======================================================================

GDAL gère beaucoup de formats raster en lecture, mais beaucoup moins de formats 
en écriture. Parmi ceux gérés en écriture la plupart ne sont gérés seulement en 
mode *create copy*. Essentiellement cela signifie qu'ils doivent être écrits 
séquentiellement à partir d'une copie en entrée fournie de l'image à écrire. 
Les programmes tels que ``gdal_merge.py`` ou ``gdalwarp`` qui écrit des morceaux 
d'image non séquentiellement ne peuvent pas écrire facilement vers ces formats 
écrit séquentiellement. D'une manière générale les formats qui sont compressés, 
tel que PNG, JPEG et GIF sont à écriture séquentielle. Aussi certains formats 
nécessitent que des informations telles que le système de coordonnées, et la 
table de couleur soient connues au moment de la création et donc ceux-ci sont 
aussi des formats à écriture séquentielle.

Quand vous rencontrez ce problème il est généralement pas une bonne idée 
d'écrite d'abord le résultat au format GeoTIFF puis de traduire vers le format 
cible.

Pour déterminer quels formats gèrent quelles possibilités, utilisez l'option 
*--formats* avec à peu près toutes les commandes GDAL. Chaque pilote inclura 
soit r (lecture seule), rx (lecture et écriture séquentielle) ou rw+ (lecture, 
écriture séquentielle ou aléatoire).

Comment améliorer les performances de gdalwarp ?
================================================

Brièvement : utilisez la mémoire déformée et configurez le paramètre *cachemax*. 
Par exemple ``gdalwarp --config GDAL_CACHEMAX 500 -wm 500`` utilise 500MB de RAM 
pour lire/écrire le cache, et 500 MB de RAM pour les buffers de travail pendant 
la déformation.

Pour plus de détails, lisez `UserDocs/GdalWarp <http://trac.osgeo.org/gdal/wiki/UserDocs/GdalWarp>`_.

Comment convertir un raster en une couche de polygones ?
=========================================================

TBD

Comment puis je créer un raster blanc basé sur l'étendue de fichiers vecteurs pour utiliser avec gdal_rasterize ?
==================================================================================================================

Aujourd'hui la commande ``gdal_rasterize`` ne peut pas créer de raster blanc 
basé sur une source de données vecteur bien que cette fonctionnalité ait été 
considérée ([[http://trac.osgeo.org/gdal/ticket/1599|Ticket #1599]]). Jusqu'à 
ce que cette fonctionnalité soit ajouté, vous devrez trouver un moyen de générer 
un raster qui correspond à l'étendue de votre couche vectorielle. Vous pouvez 
alors utiliser ce raster blanc à partir de votre couche vectorielle.

Une approche est d'utiliser ``gdal_translate`` pour découper et aplanir un 
fichier raster existant qui couvre votre zone d'intérêt. Lisez cet 
`exemple de syntaxe <http://lists.osgeo.org/pipermail/gdal-dev/2008-February/016061.html>`_.

Une autre approche est d'utiliser un des langages de GDAL pour créer un raster 
blanc à partir de rien. La part la plus difficile est la compréhension de la 
syntaxe de *GeoTransform*. Cet extrait en Python montre comment lire un 
shapefile et sortir un tiff qui correspond à l'étendue du shapefile.

.. note ::
    Vous devez modifier la variable *px* basée sur la résolution désirée et la 
    dimension du raster.

::
    
    #!/usr/bin/env python

    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr
    import numpy

    shp = 'test.shp'
    tiff = 'test.tif'
    px = .001
    tiff_width = 7850
    tiff_height = 3500

    # Import vector shapefile
    vector = ogr.GetDriverByName('ESRI Shapefile')
    src_ds = vector.Open(shp)
    src_lyr = src_ds.GetLayerByIndex(index=0)
    src_extent = src_lyr.GetExtent()

    # Create new raster layer with 4 bands
    raster = gdal.GetDriverByName('GTiff')
    dst_ds = raster.Create( tiff, tiff_width, tiff_height, 4, gdal.GDT_Byte)

    # Create raster GeoTransform based on upper left corner and pixel resolution
    raster_transform = [src_extent[0], px, 0.0, src_extent[3], 0.0, -px]
    dst_ds.SetGeoTransform( raster_transform )

    # Get projection of shapefile and assigned to raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(src_lyr.GetSpatialRef().__str__())
    dst_ds.SetProjection( srs.ExportToWkt() )

    # Create blank raster with fully opaque alpha band
    zeros = numpy.zeros( (tiff_height, tiff_width), numpy.uint8 )
    dst_ds.GetRasterBand(1).WriteArray( zeros )
    dst_ds.GetRasterBand(2).WriteArray( zeros )
    dst_ds.GetRasterBand(3).WriteArray( zeros )
    opaque = numpy.ones((tiff_height,tiff_width), numpy.uint8 )*255
    dst_ds.GetRasterBand(4).WriteArray( opaque )


===== Puis je utiliser gdal_rasterize pour générer des polygones "non solides " ? =====

Lisez la page `How gdal_rasterize works <htttp://lists.maptools.org/pipermail/gdal-dev/2006-June/009294.html>`_
 dans les archives de gdal-dev.

Comme Chris Barker le suggère, les possibilités de rastérisation deGDAL sont 
assez limitées d'un point de vue du style du rendu. D'autres outils peuvent être 
plus appropriés si vous voulez faire quelque chose de plus sophistiqué que 
rastériser des polygones dans une seule couleur.

Exemples d'autres outils : `Quantum GIS <http://www.osgeo.org/qgis/>`_, 
`GRASS <http://www.osgeo.org/grass/>`_, `MapServer <http://www.osgeo.org/mapserver/>`_, 
`GMT <http://gmt.soest.hawaii.edu/>`_, `SAGA GIS <http://www.saga-gis.uni-goettingen.de/>`_.

Cependant, si votre raster gère la transparence dans la bande alpha (RGBA), 
alors vous pouvez utiliser ``gdal_rasterize`` pour "brûler" complètement les 
zones transparentes dans votre image avec :

::
    
    $ gdal_rasterize -b 4 -burn 0 -where your_field=some_value -l your_layer your_vector_file.shp your_raster

Comment utiliser gdal_translate pour extraire une sous partie d'un raster ?
============================================================================

``Gdal_translate`` a été désigné pour convertir à partir et vers divers formats 
raster, mais il peut aussi réaliser des opérations de géotraitement utile durant 
la conversion.

Si vous désirez extraire une sous partie d'un raster vous pouvez utiliser les 
options *-srcwin* ou *-projwin*. Dans la terminologie GDAL, ce sont des 
opérations de "subsetting" qui permet de sélectionner une sous fenêtre 
"subwindows" pour copier à partir d'un jeu de données sources dans un jeu de 
données de destination.

Voici un exemple de l'utilisation de ``gdal_translate`` sur une orthophographie 
NAIP au format sid pour sélectionner une petite zone qui montre l'île Blakely, 
WA :

::
    
    $ gdal_translate -projwin 510286 5385025 518708 5373405 ortho_1-1_1n_s_wa055_2006_1.sid naip_ortho_blakely_island.tif

Cet exemple utilise l'option *-projwin* qui accepte les coordonnées des limites 
dans les coordonnés projetées plutôt qu'en pixel (*-srcwin*). *-projwin* de 
``Gdal_translate`` nécessite les coordonnées X et Y du coin en haut à gauche, 
les coordonnées X et Y du coin le plus à droite. L'image NAIP dans cet exemple 
est en NAD 83 Utm 10, pour obtenir les coordonnées des limites j'ai simplement 
chargé l'inde shapfile qui est fournie avec l'image NAIP dans Quantum GIS et lu 
les coordonnées sur l'écran pour former mon étendue.

.. note::
    Aujourdh'ui le découpage d'un raster en utilisant une étendue vectorielle 
    polygonale n'est pas gérée, mais est en discussion (lisez http://trac.osgeo.org/gdal/ticket/1599). 
    Cependant, il est assez facile d'obtenir l'étendue d'un shapefile donné et 
    de convertir ses coordonnées dans la forme utilisable par ``gdal_translate`` 
    sans lire manuellement l'étendue dans une autre application comme QGIS. 

Disons que vous avez un shapefile nommé *clipping_mask.shp* utiliser ``ogrinfo`` pour obtenir l'étendue :

  * notez que l'utilisation d'une pipe (|) et de la commande ``grep`` est 
    optionnelle (*| grep Extent*), mais une manière habile de limiter 
    l'information renvoyée par ``ogrinfo`` pour obtenir juste ce dont vous avez 
    besoin :

::
    
    $ ogrinfo clipping_mask.shp -so -al | grep Extent
    # which gives the extent as xMin,yMin, xMax, yMax:
    Extent: (268596, 5362330) - (278396, 5376592)
    # which is (xMin,yMin) - (xMax,yMax)

Puis copier et coller ce texte pour créer votre commande de découpe avec ``gdal_translate`` :

::
    
    # -projwin's ulx uly lrx lry is equivalent to xMin, yMax, xMax, yMin so just switch the Y coordinates
    # For the above Extent that would turn into:
    $ gdal_translate -projwin 268596 5376592 278396 5362330 src_dataset dst_dataset


Comment retrouver la liste des formats supportés par ma version de GDAL ?
===========================================================================

Utilisez la commande :
::
    
    gdalinfo --formats

Celle-ci vous renvoie :
::
    
    $ gdalinfo --formats
    Supported Formats:
        GRASS (ro): GRASS Database Rasters (5.7+)
        VRT (rw+): Virtual Raster
        GTiff (rw+): GeoTIFF
        NITF (rw+): National Imagery Transmission Format
        HFA (rw+): Erdas Imagine Images (.img)
        SAR_CEOS (ro): CEOS SAR Image
        CEOS (ro): CEOS Image
        ELAS (rw+): ELAS
        AIG (ro): Arc/Info Binary Grid
        AAIGrid (rw): Arc/Info ASCII Grid
        SDTS (ro): SDTS Raster
        OGDI (ro): OGDI Bridge
        DTED (rw): DTED Elevation Raster
        PNG (rw): Portable Network Graphics
        JPEG (rw): JPEG JFIF
        MEM (rw+): In Memory Raster
        JDEM (ro): Japanese DEM (.mem)
        GIF (rw): Graphics Interchange Format (.gif)
        ESAT (ro): Envisat Image Format
        FITS (rw+): Flexible Image Transport System
        BSB (ro): Maptech BSB Nautical Charts
        XPM (rw): X11 PixMap Format
        BMP (rw+): MS Windows Device Independent Bitmap
        AirSAR (ro): AirSAR Polarimetric Image
        RS2 (ro): RadarSat 2 XML Product
        PCIDSK (rw+): PCIDSK Database File
        PCRaster (rw): PCRaster Raster File
        ILWIS (rw+): ILWIS Raster Map
        SGI (ro): SGI Image File Format 1.0
        Leveller (ro): Leveller heightfield
        GMT (rw): GMT NetCDF Grid Format
        netCDF (rw): Network Common Data Format
        PNM (rw+): Portable Pixmap Format (netpbm)
        DOQ1 (ro): USGS DOQ (Old Style)
        DOQ2 (ro): USGS DOQ (New Style)
        ENVI (rw+): ENVI .hdr Labelled
        EHdr (rw+): ESRI .hdr Labelled
        PAux (rw+): PCI .aux Labelled
        MFF (rw+): Vexcel MFF Raster
        MFF2 (rw+): Vexcel MFF2 (HKV) Raster
        FujiBAS (ro): Fuji BAS Scanner Image
        GSC (ro): GSC Geogrid
        FAST (ro): EOSAT FAST Format
        BT (rw+): VTP .bt (Binary Terrain) 1.3 Format
        LAN (ro): Erdas .LAN/.GIS
        CPG (ro): Convair PolGASP
        IDA (rw+): Image Data and Analysis
        NDF (ro): NLAPS Data Format
        DIPEx (ro): DIPEx
        ISIS2 (ro): USGS Astrogeology ISIS cube (Version 2)
        PDS (ro): NASA Planetary Data System
        JPEG2000 (rw): JPEG-2000 part 1 (ISO/IEC 15444-1)
        ECW (rw): ERMapper Compressed Wavelets
        JP2ECW (rw+): ERMapper JPEG2000
        L1B (ro): NOAA Polar Orbiter Level 1b Data Set
        FIT (rw): FIT Image
        RMF (rw+): Raster Matrix Format
        WCS (ro): OGC Web Coverage Service
        RST (rw+): Idrisi Raster A.1
        RIK (ro): Swedish Grid RIK (.rik)
        USGSDEM (rw): USGS Optional ASCII DEM (and CDED)
        GXF (ro): GeoSoft Grid Exchange Format


.. yjacolin at free.fr, Yves Jacolin - 2009/03/10 21:27
