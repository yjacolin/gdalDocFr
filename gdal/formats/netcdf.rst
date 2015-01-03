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
données dans le fichier en utilisant :ref:`gdal.gdal.gdalinfo`, puis d'importer les images 
désirées en utilisant :ref:`gdal.gdal.gdal_translate`. La commande :ref:`gdal.gdal.gdalinfo` liste tous 
les sous-jeu de données  multidimensionnel à partir du fichier netCDF d'entrée.

Le nom des images individuelles sont assigné à l'entrée de méta-données 
*SUBDATASET_n_NAME*. La description pour chaque image se trouve dans l'entrée 
de méta-données *SUBDATASET_n_DESC*. Pour netCDF les images suivront ce format 
: *NETCDF:filename:variable_name*

où *filename* esy le nom du fichier en entrée, et *variable_name* est le jeu de 
données sélectionné dans le fichier.

Pour la seconde étape vous fournissez ce nom pour :ref:`gdal.gdal.gdalinfo` pour obtenir les 
informations sur le jeu de données ou :ref:`gdal.gdal.gdal_translate` pour lire le jeu de 
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


:ref:`gdal.gdal.gdalinfo` affiche le nombre de bandes dans un sous-jeu de données. Il y a 
des méta-données attachées à chaque bande. Dans cet exemple, les méta-données 
indique que chaque bande corresponde à un tableau de température mensuelle de 
la surface de la mer à partir de janvier 2001. Il y a 24 mois de données dans 
ce sous-jeu de données. Vous pouvez utiliser :ref:`gdal.gdal.gdal_translate` pour lire le 
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

* Gestion améliorée pour CF-1.5 pour les projections projectées et geographiques en lecture et écriture.
* Amélioration de la prise en charge des métadonnées (global et variable).
* Ajout d'un indicateur de progression simple 
* Ajout de la gestion de la compression DEFLATE (en lecture et écriture) et szip (en lecture) - nécessite la gestion de NetCDF-4.
* Ajout de la gestion pour les paramètres valid_range/valid_min/valid_max
* Prise en charge correct des données bytes signés/non signés.
* Ajout de la gestion pour la fonction *Create()* - permet d'utiliser netcdf directement avec :ref:`gdal.gdal.gdalwarp`
* Ajout de la gestion des variables de coordonnées à deux dimension CF (voir 
  `Conventions CF <http://cfconventions.org/1.6.html#idp5559280>`_) via des 
  tableaux GDAL GEOLOCATION (voir `RFC 4: Geolocation Arrays <https://trac.osgeo.org/gdal/wiki/rfc4_geolocate>`_)
  (GDAL >= 1.10)

Options de création
********************

* **FORMAT=[NC/NC2/NC4/NC4C] :** Définie le format de fichier netcdf à utiliser,
  NC est celui par défaut. NC2 n'est normalement géré par les installations 
  récentes de netcdf, mais NC4 et NC4C sont disponible si netcdf a été 
  compilé avec la gestion de NetCDF-4 (et HDF5).
* **COMPRESS=[NONE/DEFLATE] :** Définie la compression à utiliser  DEFLATE est 
  disponible seulement si netcdf a été compilé avec la gestion de NetCDF-4. 
  Le format NC4C est celui par défaut si la compression DEFLATE est utilisée.
* **ZLEVEL=[1-9] :** Définie le niveau de compression lors de l'utilisation de 
  DEFLATE. Une valeur de 9 est le plus haut, et 1 est la plus basse. 1 est la 
  valeur par défaut, qui offre le meilleur taux de compression/temps.
* **WRITE_BOTTOMUP=[NO/YES] :** Définie l'ordre de l'axe y pour l'export, 
  écrasant l'ordre détecté par le pilote. Les fichiers NetCDF sont habituellement 
  supposé "bottom-up", contrairement au model de GDAL qui est "north-up". Cela 
  ne créé pas de problème dans l'ordre de l'axe y à moins qu'il n'y ait pas 
  de géoréférencement de l'axe y. Les fichiers sans informations géo-référencement 
  seront exportés dans l'ordre "bottom-up" par défaut du NetCDF et le contraire 
  pour les fichiers avec géo-référencement. Pour l'import voir le paramètre 
  *GDAL_NETCDF_BOTTOMUP* dans la section :ref:`gdal.gdal.formats.netcdf.co` 
  ci-dessous.
* **WRITE_GDAL_TAGS=[YES/NO] :** Définie si les balises GDAL utilisées pour le 
  géo-référencement (spatial_ref et GeoTransform) doivent être exportées, en 
  plus des balises CF. Toutes les informations sont stockées dans la balise CF 
  (tels que les datums nommés et les codes EPSG), Par conséquent le pilote 
  exporte ces varaibles par défaut. En import les variables CF "grid_mapping" 
  prend la précédence et les balises GDAL sont utilisées si elles ne rentrent 
  pas en conflit avec les métadonnées CF.
* **WRITE_LONLAT=[YES/NO/IF_NEEDED] :** Définie si les variables lon/lat CF sont 
  écrites dans le fichier. YES par défaut pour les SRS géographiques et NO pour 
  les SRS projetés. Ce n'est normalement pas nécessaire pour les SRS projetés 
  puisque GDAL et beaucoup d'applications utilises les variables de dimensions 
  X/Y et les informations de projection CF. L'utilisation de l'option *IF_NEEDED* 
  créé des varaibles lon/lat si la projection ne fait pas partie du standard 
  CF-1.5.
* **TYPE_LONLAT=[float/double] :** Définie le type de variable à utiliser pour 
  les variables lon/lat. *Double* par défaut pour les SRS géographique et 
  *float* pour les SRS projetés. Si les variables lon/lat sont écrit pour un 
  SRS projeté, le fichier est considérablement large (chaque variable utilise 
  X*Y espaces); par conséquent *TYPE_LONLAT=float* et *COMPRESS=DEFLATE* sont 
  conseillés pour sauver de l'espace.
* **PIXELTYPE=[DEFAULT/SIGNEDBYTE] :** En définissant ceci à SIGNEDBYTE, un 
  nouveau fichier Byte peut être forcé à être créé. 

.. _`gdal.gdal.formats.netcdf.co`:

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


.. yjacolin at free.fr, Yves Jacolin - 2014/05/29 (http://gdal.org/frmt_netcdf.html trunk 27422)
