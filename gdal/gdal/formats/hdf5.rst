.. _`gdal.gdal.formats.hdf5`:

HDF5 --- Hierarchical Data Format Release 5 (HDF5)
===================================================

Ce pilote a pour objectif d'importer le format de fichiers HDF5. Cette 
modification est disponible pour l'utilisation de données de capteur distant et 
complètement compatible avec le format HDF5 sous jascent. Ce pilote peut importer 
les fichiers HDF5-EOS. Actuellement EOS utilise HDF5 pour le stockage de données 
(télémétrie à partir des satellites 'Aura'). Dans le future ils passeront au 
format HDF5 qui sera utilisé pour la télémétrie à partir des satellites 'Aura' .

Gestion des images multiples (Sous jeux de données)
----------------------------------------------------

Hierarchical Data Format est un conteneur pour plusieurs jeux de données 
différents. Pour le stockage des données. HDF contient des tableaux 
multidimensionnels remplit par des données. Un fichier HDF peut contenir 
plusieurs tableaux. Ceux-ci peuvent être différent en taille et dimensions.

La première étape est d'avoir un rapport des images composants (tableau) dans 
le fichier en utilisant ``gdalinfo`` puis d'importer les images désirées en 
utilisant ``gdal_translate``. La commande ``gdalinfo`` liste tous les sous jeux 
de données multidimensionnels à partir du fichier HDF en entrée. Le nom des 
images individuelles (sous jeux de données) sont assignés à l'objet de 
méta-données *SUBDATASET_n_NAME*. La description pour chaque image est trouvée 
dans l'objet méta-données *SUBDATASET_n_DESC*. Pour les images HDF5 les noms 
du sous jeu de données sera formaté comme cela :
::
    
    HDF5:file_name:subdataset

où :

* **file_name** est le nom du fichier d'entrée ;
* **subdataset** est le nom du jeu de données du tableau à utiliser (pour 
  utilisation interne dans GDAL).

À la deuxième étape vous devez fournir ce nom pour ``gdalinfo`` ou 
``gdal_translate`` pour une lecture réelle des données.

Par exemple, nous voulons lire des données à partir du jeu de données OMI/Aura 
Ozone (O3) :

::
    
    $ gdalinfo OMI-Aura_L2-OMTO3_2005m0326t2307-o03709_v002-2005m0428t201311.he5
    Driver: HDF5/Hierarchical Data Format Release 5
    Size is 512, 512
    Coordinate System is `'

    Subdatasets:
        SUBDATASET_1_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/APrioriLayerO3
        SUBDATASET_1_DESC=[1496x60x11] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/APrioriLayerO3 (32-bit floating-point)
        SUBDATASET_2_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/AlgorithmFlags
        SUBDATASET_2_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/AlgorithmFlags (8-bit unsigned character)
        SUBDATASET_3_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudFraction
        SUBDATASET_3_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudFraction (32-bit floating-point)
        SUBDATASET_4_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudTopPressure
        SUBDATASET_4_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/CloudTopPressure (32-bit floating-point)
        SUBDATASET_5_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ColumnAmountO3
        SUBDATASET_5_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ColumnAmountO3 (32-bit floating-point)
        SUBDATASET_6_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/LayerEfficiency
        SUBDATASET_6_DESC=[1496x60x11] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/LayerEfficiency (32-bit floating-point)
        SUBDATASET_7_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/NValue
        SUBDATASET_7_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/NValue (32-bit floating-point)
        SUBDATASET_8_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/O3BelowCloud
        SUBDATASET_8_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/O3BelowCloud (32-bit floating-point)
        SUBDATASET_9_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/QualityFlags
        SUBDATASET_9_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/QualityFlags (16-bit unsigned integer)
        SUBDATASET_10_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity331
        SUBDATASET_10_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity331 (32-bit floating-point)
        SUBDATASET_11_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity360
        SUBDATASET_11_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Reflectivity360 (32-bit floating-point)
        SUBDATASET_12_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Residual
        SUBDATASET_12_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Residual (32-bit floating-point)
        SUBDATASET_13_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep1
        SUBDATASET_13_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep1 (32-bit floating-point)
        SUBDATASET_14_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep2
        SUBDATASET_14_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/ResidualStep2 (32-bit floating-point)
        SUBDATASET_15_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/SO2index
        SUBDATASET_15_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/SO2index (32-bit floating-point)
        SUBDATASET_16_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Sensitivity
        SUBDATASET_16_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/Sensitivity (32-bit floating-point)
        SUBDATASET_17_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepOneO3
        SUBDATASET_17_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepOneO3 (32-bit floating-point)
        SUBDATASET_18_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepTwoO3
        SUBDATASET_18_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/StepTwoO3 (32-bit floating-point)
        SUBDATASET_19_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/TerrainPressure
        SUBDATASET_19_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/TerrainPressure (32-bit floating-point)
        SUBDATASET_20_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/UVAerosolIndex
        SUBDATASET_20_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/UVAerosolIndex (32-bit floating-point)
        SUBDATASET_21_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dR
        SUBDATASET_21_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dR (32-bit floating-point)
        SUBDATASET_22_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dT
        SUBDATASET_22_DESC=[1496x60x12] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Data_Fields/dN_dT (32-bit floating-point)
        SUBDATASET_23_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/GroundPixelQualityFlags
        SUBDATASET_23_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/GroundPixelQualityFlags (16-bit unsigned integer)
        SUBDATASET_24_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Latitude
        SUBDATASET_24_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Latitude (32-bit floating-point)
        SUBDATASET_25_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Longitude
        SUBDATASET_25_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/Longitude (32-bit floating-point)
        SUBDATASET_26_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/RelativeAzimuthAngle
        SUBDATASET_26_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/RelativeAzimuthAngle (32-bit floating-point)
        SUBDATASET_27_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarAzimuthAngle
        SUBDATASET_27_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarAzimuthAngle (32-bit floating-point)
        SUBDATASET_28_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarZenithAngle
        SUBDATASET_28_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/SolarZenithAngle (32-bit floating-point)
        SUBDATASET_29_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/TerrainHeight
        SUBDATASET_29_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/TerrainHeight (16-bit integer)
        SUBDATASET_30_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingAzimuthAngle
        SUBDATASET_30_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingAzimuthAngle (32-bit floating-point)
        SUBDATASET_31_NAME=HDF5:"OMI-Aura_L2-OMTO3_2005m0113t0224-o02648_v002-2005m0625t035355.he5"://HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingZenithAngle
        SUBDATASET_31_DESC=[1496x60] //HDFEOS/SWATHS/OMI_Column_Amount_O3/Geolocation_Fields/ViewingZenithAngle (32-bit floating-point)
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0,  512.0)
    Upper Right (  512.0,    0.0)
    Lower Right (  512.0,  512.0)
    Center      (  256.0,  256.0)

Maintenant sélectionnons un des sous jeu de données, décrit comme [1645x60] 
CloudFraction (32-bit floating-point) :

::
    
    $ gdalinfo HDF5:"OMI-Aura_L2-OMTO3_2005m0326t2307-o03709_v002-2005m0428t201311.he5":CloudFraction 
    Driver: HDF5Image/HDF5 Dataset
    Size is 60, 1645
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
    GCP Projection = GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AXIS["Lat",NORTH],AXIS["Long",EAST],AUTHORITY["EPSG","4326"]]
    GCP[  0]: Id=, Info=
            (0.5,0.5) -> (261.575,-84.3495,0)
    GCP[  1]: Id=, Info=
            (2.5,0.5) -> (240.826,-85.9928,0)
    GCP[  2]: Id=, Info=
            (4.5,0.5) -> (216.754,-86.5932,0)
    GCP[  3]: Id=, Info=
            (6.5,0.5) -> (195.5,-86.5541,0)
    GCP[  4]: Id=, Info=
            (8.5,0.5) -> (180.265,-86.2009,0)
    GCP[  5]: Id=, Info=
            (10.5,0.5) -> (170.011,-85.7315,0)
    GCP[  6]: Id=, Info=
            (12.5,0.5) -> (162.987,-85.2337,0)


... 3 000 points d'amer sont lu à partir du fichier si le tableau de Latitude et Longitude sont présent :
::
    
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0, 1645.0)
    Upper Right (   60.0,    0.0)
    Lower Right (   60.0, 1645.0)
    Center      (   30.0,  822.5)
    Band 1 Block=60x1 Type=Float32, ColorInterp=Undefined
    Open GDAL Datasets:
        1 N DriverIsNULL 512x512x0


vous pouvez utiliser ``gdal_translate`` pour la lecture des bandes d'images à 
partir de ce jeu de données.

Notez que vous devez fournir le contenu exact de la ligne noté 
**SUBDATASET_n_NAME** à GDAL, incluant le préfixe *HDF5:*.

Ce pilote a seulement pour objectif d'importer des jeux de données géospatiaux 
et de capteur distant sous la forme d'images raster (tableaux 2D ou 3D). Si vous 
voulez explorer toutes les données dans un fichier HDF vous devez utiliser un 
autre outil (vous pouvez trouver plus d'informations sur les différents outils 
HDF en utilisant les liens en bas de cette page).

Géoréferencement
-----------------

Il n'y a pas de moyen universel de stockage du géoréférencement dans les 
fichiers HDF. Cependant, certains types de produits ont des mécanismes pour la 
sauvegarde du géoréférencement, et certains sont gérés par GDAL. Actuellement 
ceux gérés sont (subdataset_type affiché entre parenthèses):

* HDF5 OMI/Aura Ozone (O3) Total Column 1-Orbit L2 Swath 13x24km (Level-2 OMTO3) 

Méta-données
------------

Aucune méta-données n'est lues pour l'instant à partir des fichiers HDF5.

Compilation du pilote
---------------------

Ce pilote est compilé au dessus de la bibliothèque HDF5 NCSA, vous avez donc 
besoin de télécharger la bibliothèque HDF5-1.6.4 ou plus récent. Vous avez aussi 
besoin des bibliothèques zlib 1.2 et szlib 2.0. Pour les utilisateurs Windows 
assurez vous d'avoir définie les attributs d'écriture (spécialement si vous 
utilisez cygwin) et que les DLL peuvent être localisé par votre variable 
d'environnement PATH. Vous pouvez aussi télécharger le code source de la page 
HDF NCSA (voir lien ci-dessous).

Voir également
--------------

* Implementé dans *gdal/frmts/hdf5/hdf5dataset.cpp and gdal/frmts/hdf5/hdf5imagedataset.cpp*.
* `Page de téléchargement de NCSA HDF5 <http://hdf.ncsa.uiuc.edu/HDF5/release/obtain5.html>`_ 
  sur le site `National Center for Supercomputing Applications <http://www.ncsa.uiuc.edu/>`_
* `HDFView est un outil de visualisation pour la navigation et l'édition de fichiers NCSA HDF4 et HDF5 <http://hdf.ncsa.uiuc.edu/hdf-java-html/hdfview/>`_.
* Documentation pour les produits individuels, géré par ce pilote :
  - `Aura OMI Total Ozone Data Product-OMTO3 <http:*disc.gsfc.nasa.gov/Aura/OMI/omto3.shtml>`_ 

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 17235)