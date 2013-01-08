.. _`gdal.gdal.formats.netcdf`:

==================================
NetCDF : Network Common Data Form
==================================

Ce format est géré en lecture et écriture. NetCDF est une interface pour 
l'accès au données orienté 'tableau' et est utilisé pour représenter des données 
scientifique.

Les méta-données des valeurs rempli ou la compatibilité arrière des valeurs 
manquantes sont préservés comme valeur NODATA lorsque cela est disponible.

.. note:: Implémenté dans *gdal/frmts/netcdf/netcdfdataset.cpp*.

Multiple Image Handling (sous-jeu de données)
===============================================

Nework Command Data Form est un conteneur pour plusieurs tableaux différents la 
plupart du temps utilisé pour stocker des jeux de données scientifiques. Un 
fichier netCDF peut contenir plusieurs jeux de données. Ils peuvent différer par 
la taille, le nombre de dimensions et peuvent représenter des données pour 
différentes régions.

Si le fichier contient seulement un tableau netCDF et que celle-ci est une image, 
elle peut être accédé directement mais si le fichier contient de multiples 
images il peut être nécessaire d'importer le fichier via un processus en deux 
étapes.

La première étape est d'obtenir un rapport des images qui composent le jeu de 
données dans le fichier en utilisant ``gdalinfo``, puis d'importer les images 
désirées en utilisant ``gdal_translate``. La commande ``gdalinfo`` liste tous 
les sous-jeu de données  multidimensionnel à partir du fichier netCDF d'entrée.

Le nom des images individuelles sont assigné à l'entrée de méta-données 
*SUBDATASET_n_NAME*. La description pour chaque image se trouve dans l'entrée 
de méta-données *SUBDATASET_n_DESC*. Pour netCDF les images suivront ce format 
: *NETCDF:filename:variable_name*

où *filename* esy le nom du fichier en entrée, et *variable_name* est le jeu de 
données sélectionné dans le fichier.

Pour la seconde étape vous fournissez ce nom pour ``gdalinfo`` pour obtenir les 
informations sur le jeu de données ou ``gdal_translate`` pour lire le jeu de 
données.

Par exemple, nous voulons lire les données d'un fichier NetCDF :

::
    
    $ gdalinfo sst.nc
    Driver: netCDF/Network Common Data Format
    Size is 512, 512
    Coordinate System is `'
    Metadata:
        NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment
        NC_GLOBAL#institution=IPSL (Institut Pierre Simon Laplace, Paris, France)
        NC_GLOBAL#source=IPSL-CM4_v1 (2003) : atmosphere : LMDZ (IPSL-CM4_IPCC, 96x71x19) ; ocean ORCA2 (ipsl_cm4_v1_8, 2x2L31); sea ice LIM (ipsl_cm4_v
        NC_GLOBAL#contact=Sebastien Denvil, sebastien.denvil@ipsl.jussieu.fr
        NC_GLOBAL#project_id=IPCC Fourth Assessment
        NC_GLOBAL#table_id=Table O1 (13 November 2004)
        NC_GLOBAL#experiment_id=SRES A2 experiment
        NC_GLOBAL#realization=1
        NC_GLOBAL#cmor_version=9.600000e-01
        NC_GLOBAL#Conventions=CF-1.0
        NC_GLOBAL#history=YYYY/MM/JJ: data generated; YYYY/MM/JJ+1 data transformed  At 16:37:23 on 01/11/2005, CMOR rewrote data to comply with CF standards and IPCC Fourth Assessment requirements
        NC_GLOBAL#references=Dufresne et al, Journal of Climate, 2015, vol XX, p 136
        NC_GLOBAL#comment=Test drive
    Subdatasets:
        SUBDATASET_1_NAME=NETCDF:"sst.nc":lon_bnds
        SUBDATASET_1_DESC=[180x2] lon_bnds (64-bit floating-point)
        SUBDATASET_2_NAME=NETCDF:"sst.nc":lat_bnds
        SUBDATASET_2_DESC=[170x2] lat_bnds (64-bit floating-point)
        SUBDATASET_3_NAME=NETCDF:"sst.nc":time_bnds
        SUBDATASET_3_DESC=[24x2] time_bnds (64-bit floating-point)
        SUBDATASET_4_NAME=NETCDF:"sst.nc":tos
        SUBDATASET_4_DESC=[24x170x180] sea_surface_temperature (32-bit floating-point)Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0,  512.0)
    Upper Right (  512.0,    0.0)
    Lower Right (  512.0,  512.0)
    Center      (  256.0,  256.0)


Ces fichiers NetCDF contiennent 4 jeux de données, *lon_bnds*, *lat_bnds*, *tim_bnds* et *tos*. Maintenant sélectionnez le sous-jeu de données, décrit comme :

::
    
    NETCDF:"sst.nc":tos
    
    [24x17x180] sea_surface_temperature (32-bit floating-point)

et obtenez l'information sur le nombre de bande qu'il y a à dans cette variable.

::
    
    $ gdalinfo NETCDF:"sst.nc":tos
    Driver: netCDF/Network Common Data Format
    Size is 180, 170
    Coordinate System is `'
    Origin = (1.000000,-79.500000)
    Pixel Size = (1.98888889,0.99411765)
    Metadata:
        NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment
        NC_GLOBAL#institution=IPSL (Institut Pierre Simon Laplace, Paris, France)
        
    .... D'autres métadonnées
    
        time#standard_name=time
        time#long_name=time
        time#units=days since 2001-1-1
        time#axis=T
        time#calendar=360_day
        time#bounds=time_bnds
        time#original_units=seconds since 2001-1-1
    Corner Coordinates:
    Upper Left  (   1.0000000, -79.5000000)
    Lower Left  (   1.0000000,  89.5000000)
    Upper Right (     359.000,     -79.500)
    Lower Right (     359.000,      89.500)
    Center      ( 180.0000000,   5.0000000)
        Band 1 Block=180x1 Type=Float32, ColorInterp=Undefined
        NoData Value=1e+20
        Metadata:
            NETCDF_VARNAME=tos
            NETCDF_DIMENSION_time=15
            NETCDF_time_units=days since 2001-1-1
    Band 2 Block=180x1 Type=Float32, ColorInterp=Undefined
        NoData Value=1e+20
        Metadata:
            NETCDF_VARNAME=tos
            NETCDF_DIMENSION_time=45
            NETCDF_time_units=days since 2001-1-1
    
    .... D'autres bandes
    
    Band 22 Block=180x1 Type=Float32, ColorInterp=Undefined
        NoData Value=1e+20
        Metadata:
            NETCDF_VARNAME=tos
            NETCDF_DIMENSION_time=645
            NETCDF_time_units=days since 2001-1-1
    Band 23 Block=180x1 Type=Float32, ColorInterp=Undefined
        NoData Value=1e+20
        Metadata:
            NETCDF_VARNAME=tos
            NETCDF_DIMENSION_time=675
            NETCDF_time_units=days since 2001-1-1
    Band 24 Block=180x1 Type=Float32, ColorInterp=Undefined
        NoData Value=1e+20
        Metadata:
            NETCDF_VARNAME=tos
            NETCDF_DIMENSION_time=705
            NETCDF_time_units=days since 2001-1-1


``gdalinfo`` affiche le nombre de bandes dans un sous-jeu de données. Il y a 
des méta-données attachées à chaque bande. Dans cet exemple, les méta-données 
indique que chaque bande corresponde à un tableau de température mensuelle de 
la surface de la mer à partir de janvier 2001. Il y a 24 mois de données dans 
ce sous-jeu de données. Vosu pouvez utiliser ``gdal_translate`` pour lire le 
sous-jeu de données.

Notez que vous devez fournir exactement le contenu de la ligne noté 
*SUBDATASET_n_NAME* à GDAL, incluant le préfixe *NETCDF:*.

Le préfixe *NETCDF:* doit être en premier. Il déclenche le pilote netCDF du 
sous-jeu de données. Ce pilote a pour objectif seulement pour importer de 
capteurs distant et des jeux de données géospatiales sous la forme d'image 
raster. Si vous voulez explorer toutes les données contenues dans le fichier 
NetCDF vous devez utiliser un autre outil.

Dimension
==========

Le pilote NetCDF suppose que les données suivent la convention CF-1 d'UNIDATA. 
Les dimensions dans les fichiers NetCDF utilisent les règles suivantes : 
(Z,Y,X). S'il y a plus de 3 dimensions, le pilote les fusionnera en bandes. Par 
exemple si vous avez un tableau à 4 dimensions de type (P, T, Y, X). Le pilote 
multipliera les 2 dernières dimensions (P*T). Le pilote affichera les bandes 
dans l'ordre suivant. Il incrémentera d'abord T puis P. Les méta-données seront 
affichées sur chaque bande avec ses valeurs T et P correspondantes.

Géoréférencement
=================

Il n'y a pas de manière universelle de stocker le géoréférencement dans les 
fichiers netCDF. Le pilote tente d'abord de suivre la convention CF-1 à partir 
d'UNIDATA en cherchant la méta-données nommé "*grid_mapping*". Si 
"*grid_mapping*" n'est pas présent, le pilote tentera de trouver un tableau de 
grille lat/lon pour définir le tableau de géoréférencement. Le pilote NetCDF 
vérifie que le tableau lat/lon est espacé équitablement.

Si ces deux méthodes échouent, le pilote NetCDF tentera de lire les méta-données 
suivantes directement et définira un géoéréférencement.

* spatial_ref (Well Known Text) 
* GeoTransform (GeoTransform array) 

ou,

* *Northernmost_Northing*
* *Southernmost_Northing*
* *Easternmost_Easting*
* *Westernmost_Easting*

Problèmes de créations
=======================

Ce pilote gère la création de fichier netCDF en suivant la convention CF-1. Vous 
pouvez créer des ensembles de jeux de données 2D. Chaque tableau de variable est 
nommé Band1, Band2, ... BandN.

Chaque bande possédera des métadonnées liée en donnant une courte description 
de la donnée qu'elel contient.

Méta-données GDAL pour NetCDF
==============================

Tous les attributs de netCDF sont traduits de manière transparente vers les 
méta-données GDAL.

La traduction suit les règles suivantes :

* Les méta-données de NetCDF global ont une balise préfixé *NC_GLOBAL*.
* Les méta-données du jeu de données ont leur noms de variable préfixés.
* Chaque préfixe est suivie du signe #.
* L'attribut NetCDF suit la forme : *name=value*.

Exemple :

::
    
    $ gdalinfo NETCDF:"sst.nc":tos
    Driver: netCDF/Network Common Data Format
    Size is 180, 170
    Coordinate System is `'
    Origin = (1.000000,-79.500000)
    Pixel Size = (1.98888889,0.99411765)
    Metadata:

Les attributs globaux de NetCDF :
::
    
    NC_GLOBAL#title=IPSL  model output prepared for IPCC Fourth Assessment SRES A2 experiment

Les attributs des variables pour : tos, lon, lat et time

::
    
    tos#standard_name=sea_surface_temperature
    tos#long_name=Sea Surface Temperature
    tos#units=K
    tos#cell_methods=time: mean (interval: 30 minutes)
    tos#_FillValue=1.000000e+20
    tos#missing_value=1.000000e+20
    tos#original_name=sosstsst
    tos#original_units=degC
    tos#history= At   16:37:23 on 01/11/2005: CMOR altered the data in the following ways: added 2.73150E+02 to yield output units;  Cyclical dimension was output starting at a different lon;
    lon#standard_name=longitude
    lon#long_name=longitude
    lon#units=degrees_east
    lon#axis=X
    lon#bounds=lon_bnds
    lon#original_units=degrees_east
    lat#standard_name=latitude
    lat#long_name=latitude
    lat#units=degrees_north
    lat#axis=Y
    lat#bounds=lat_bnds
    lat#original_units=degrees_north
    time#standard_name=time
    time#long_name=time
    time#units=days since 2001-1-1
    time#axis=T
    time#calendar=360_day
    time#bounds=time_bnds
    time#original_units=seconds since 2001-1-1

Améliorations du pilote
========================

.. versionadded:: 1.9.0

Le pilote a reçu des modifications significatif dans GDAL 1.9.0, voyez le 
fichier NEWS et `Amélioration NetCDF <http://trac.osgeo.org/gdal/wiki/NetCDF_Improvements>`_.

Changements importants
***********************

* ajout de la gestion pour les types de fichiers NC2, NC4 et NC4C pour la 
  lecture et l'écriture et HDF4 pour la lecture. voir `Format de fichier NetCDF <http://www.unidata.ucar.edu/software/netcdf/docs/netcdf/File-Format.html#File-Format>`_ pour les détails.

  * *NC :* Format classique NetCDF : Le format original binaire.
  * *NC2 :* Format offset 64-bit : gestion des variables plus grandes
  * *NC4 :* Format NetCDF-4: Utilise HDF5
  * *NC4C :* Format du model NetCDF-4 : HDF5 avec des limitations NetCDF
  * *HDF4 :* Format SD HDF4

* Improved support for CF-1.5 projected and geographic SRS reading and writing
* Improvements to metadata (global and variable) handling
* Added simple progress indicator
* Added support for DEFLATE compression (reading and writing) and szip (reading) - requires NetCDF-4 support
* Added support for valid_range/valid_min/valid_max
* Proper handling of signed/unsigned byte data
* Added support for Create() function - enables to use netcdf directly with gdalwarp

Options de création
********************

* **FORMAT=[NC/NC2/NC4/NC4C] :** Set the netcdf file format to use, NC is the 
  default. NC2 is normally supported by recent netcdf installations, but NC4 
  and NC4C are available if netcdf was compiled with NetCDF-4 (and HDF5) support.
* **COMPRESS=[NONE/DEFLATE] :** Set the compression to use.  DEFLATE is only 
  available if netcdf has been compiled with NetCDF-4 support. NC4C format is the 
  default if DEFLATE compression is used.
* **ZLEVEL=[1-9] :**  Set the level of compression when using DEFLATE compression. 
  A value of 9 is best, and 1 is least compression. The default is 1, which offers 
  the best time/compression ratio.
* **WRITE_BOTTOMUP=[NO/YES] :**  Set the y-axis order for export, overriding the 
  order detected by the driver. NetCDF files are usually assumed "bottom-up", 
  contrary to GDAL's model which is "north up". This normally does not create a 
  problem in the y-axis order, unless there is no y axis geo-referencing. Files 
  without geo-referencing information will be exported in the netcdf default 
  "bottom-up" order, and the contrary for files with geo-referencing. For import 
  see Configuration Option GDAL_NETCDF_BOTTOMUP below.
* **WRITE_GDAL_TAGS=[YES/NO] :** Define if GDAL tags used for georeferencing 
  (spatial_ref and GeoTransform) should be exported, in addition to CF tags. Not 
  all information is stored in the CF tags (such as named datums and EPSG codes), 
  therefore the driver exports these variables by default.  In import the CF 
  "grid_mapping" variable takes precedence and the GDAL tags are used if they 
  do not conflict with CF metadata.
* **WRITE_LONLAT=[YES/NO/IF_NEEDED] :** Define if CF lon/lat variables are 
  written to file. Default is YES for geographic SRS and NO for projected SRS. 
  This is normally not necessary for projected SRS as GDAL and many 
  applications use the X/Y dimension variables and CF projection information. 
  Use of IF_NEEDED option creates lon/lat variables if the projection is not 
  part of the CF-1.5 standard.
* **TYPE_LONLAT=[float/double] :** Set the variable type to use for lon/lat 
  variables. Default is double for geographic SRS and float for projected SRS. 
  If lon/lat variables are written for a projected SRS, the file is considerably 
  large (each variables uses X*Y space), therefore TYPE_LONLAT=float and 
  COMPRESS=DEFLATE are advisable in order to save space.
* **PIXELTYPE=[DEFAULT/SIGNEDBYTE] :** En définissant ceci à SIGNEDBYTE, un 
  nouveau fichier Byte peut être forcé à être créé. 


Options de configuration
*************************

* **GDAL_NETCDF_BOTTOMUP=[YES/NO] :** Définie l'ordre de l'axe y pour l'import, 
  écrasant l'ordre détecté par le pilote. Cette option n'est habituellement pas 
  nécessaire à moins qu'un jeu de données spécifique cause un problème (qui doit 
  être reporté dans le trac de GDAL).


Compilation du pilote
=======================

Ce pilote est compilé avec la bibliothèque netCDF d'UNIDATA.

Vous devez télécharger ou compiler la bibliothèque netCDF avant de configurer 
GDAL avec la gestion de netCDF.

Lisez le `Wiki GDAL sur NetCDF <http://trac.osgeo.org/gdal/wiki/NetCDF>`_ pour 
les instructions de compilation et les informations en regard de HDF4, NetCDF-4 
et HDF5.

.. seealso::

* `convention NetCDF CF-1.5 <http://cf-pcmdi.llnl.gov/documents/cf-conventions/1.5/cf-conventions.html>`_
* `Bibliothèque NetCDF compilé <http://www.unidata.ucar.edu/downloads/netcdf/index.jsp>`_
* `Documentation NetCDF <http://www.unidata.ucar.edu/software/netcdf/docs/>`_


.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/frmt_netcdf.html trunk 23644)
