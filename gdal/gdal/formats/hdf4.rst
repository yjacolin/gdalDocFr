.. _`gdal.gdal.formats.hdf4`:

HDF4 --- Hierarchical Data Format Version 4 (HDF4)
====================================================

Il y a deux formats HDF (4.x et les versions antérieures) et HFD5. Ces formats 
sont complètement différents et incompatible. Ce pilote a été destiné uniquement 
pour l'importation des formats de fichier HDF4. Le Système d'Observation de la 
Terre (EOS,  Earth Observing System) de la NASA maintient ses propres 
modifications HDF appelé HDF-EOS. Ces modifications convient pour les données de 
capteur distant et est pleinement compatible avec  la base du HDF. Ce pilote 
peut importer  des fichiers HDF4-EOS. Pour l'instant EOS utilise HDF4-EOS pour 
le stockage des données (satellites télémétrique de type 'Terra' et 'Aqua'). 
Dans le futur ils passeront au format HDF5-EOS, qui sera utilisé pour le 
satellite télémétrique de type 'Aura'.

Gestion des Images Multiples (Sous-ensemble de données)
--------------------------------------------------------

Le Format de Données Hiérarchique (HDF) est un conteneur pour différents 
sous-ensemble de données. Pour les données stockant des sous-ensemble de Données 
Scientifique (SDS, Scientific Datasets) est utilisé le plus souvent. SDS est un 
tableau multi-dimensionnel  remplit de données. Un fichier HDF peut contenir 
différents tableaux SDS. Ceux-ci peuvent se différencier par la taille, le 
nombre de dimensions et peuvent représenter des données de région différentes.

Si le fichier contient seulement un SDS qui apparaît être une image, il peut 
accessible normalement, mais s'il contient des images multiples, il peut être 
nécessaire d'importer le fichier via une procédure en deux étapes. La première 
est d'obtenir un rapport des composantes images (tableaux SDS) du fichier avec 
``gdalinfo``, puis d'importer les images désirées avec ``gdal_translate``. La 
commande ``gdalinfo`` liste tous les sous-ensembles de données 
multi-dimensionnelles à partir du fichier HDF en entrée. Le nom des images 
individuelles (sous-ensemble de données) sont assignés à l'objet méta-données 
**SUBDATASET_n_NAME**. La description de chaque image est trouvé dans l'objet 
méta-données **SUBDATASET_n_DESC**. Pour les images HDF4, le nom du sous-ensemble 
de données sera formaté comme suit :
::
    
    //HDF4_SDS:subdataset_type:file_name:subdataset_index//

où ``subdataset_type`` montre des noms prédéfinis pour quelques sous-ensemble 
de données HDF bien connus,  ``file_name`` est le nom du fichier en entrée et 
``subdataset_index`` est l'index de l'image à utiliser (pour utilisation interne 
dans GDAL).

Pour la seconde étape, vous devez fournir ce nom à ``gdalinfo`` ou 
``gdal_translate`` pour la lecture des données.
Par exemple, nous voulons lire des données à partir du sous-ensemble de données 
MODIS Level 1B :
::
    
    $ gdalinfo GSUB1.A2001124.0855.003.200219309451.hdf
    Driver: HDF4/Hierarchical Data Format Release 4
    Size is 512, 512
    Coordinate System is `'
    Metadata:
        HDFEOSVersion=HDFEOS_V2.7
        Number of Scans=204
        Number of Day mode scans=204
        Number of Night mode scans=0
        Incomplete Scans=0
    ...beaucoup de méta-données sautées ...
    Subdatasets:
        SUBDATASET_1_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:0
        SUBDATASET_1_DESC=[408x271] Latitude (32-bit floating-point)
        SUBDATASET_2_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:1
        SUBDATASET_2_DESC=[408x271] Longitude (32-bit floating-point)
        SUBDATASET_3_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:2
        SUBDATASET_3_DESC=[12x2040x1354] EV_1KM_RefSB (16-bit unsigned integer)
        SUBDATASET_4_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:3
        SUBDATASET_4_DESC=[12x2040x1354] EV_1KM_RefSB_Uncert_Indexes (8-bit unsigned integer)
        SUBDATASET_5_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:4
        SUBDATASET_5_DESC=[408x271] Height (16-bit integer)
        SUBDATASET_6_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:5
        SUBDATASET_6_DESC=[408x271] SensorZenith (16-bit integer)
        SUBDATASET_7_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:6
        SUBDATASET_7_DESC=[408x271] SensorAzimuth (16-bit integer)
        SUBDATASET_8_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:7
        SUBDATASET_8_DESC=[408x271] Range (16-bit unsigned integer)
        SUBDATASET_9_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:8
        SUBDATASET_9_DESC=[408x271] SolarZenith (16-bit integer)
        SUBDATASET_10_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:9
        SUBDATASET_10_DESC=[408x271] SolarAzimuth (16-bit integer)
        SUBDATASET_11_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:10
        SUBDATASET_11_DESC=[408x271] gflags (8-bit unsigned integer)
        SUBDATASET_12_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:12
        SUBDATASET_12_DESC=[16x10] Noise in Thermal Detectors (8-bit unsigned integer)
        SUBDATASET_13_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:13
        SUBDATASET_13_DESC=[16x10] Change in relative responses of thermal detectors (8-bit unsigned integer)
        SUBDATASET_14_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:14
        SUBDATASET_14_DESC=[204x16x10] DC Restore Change for Thermal Bands (8-bit integer)
        SUBDATASET_15_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:15
        SUBDATASET_15_DESC=[204x2x40] DC Restore Change for Reflective 250m Bands (8-bit integer)
        SUBDATASET_16_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:16
        SUBDATASET_16_DESC=[204x5x20] DC Restore Change for Reflective 500m Bands (8-bit integer)
        SUBDATASET_17_NAME=HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:17
        SUBDATASET_17_DESC=[204x15x10] DC Restore Change for Reflective 1km Bands (8-bit integer)
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0,  512.0)
    Upper Right (  512.0,    0.0)
    Lower Right (  512.0,  512.0)
    Center      (  256.0,  256.0)

Maintenant sélectionnons un sous-ensemble de données, décrit comme 
[12x2040x1354] EV_1KM_RefSB (16-bit unsigned integer) :
::
    
    $ gdalinfo HDF4_SDS:MODIS_L1B:GSUB1.A2001124.0855.003.200219309451.hdf:2
    Driver: HDF4Image/HDF4 Internal Dataset
    Size is 1354, 2040
    Coordinate System is `'
    Metadata:
        long_name=Earth View 1KM Reflective Solar Bands Scaled Integers
    ...méta-données sautées ...
    Corner Coordinates:
    Upper Left  (    0.0,    0.0)
    Lower Left  (    0.0, 2040.0)
    Upper Right ( 1354.0,    0.0)
    Lower Right ( 1354.0, 2040.0)
    Center      (  677.0, 1020.0)
    Band 1 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 2 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 3 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 4 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 5 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 6 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 7 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 8 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 9 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 10 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 11 Block=1354x2040 Type=UInt16, ColorInterp=Undefined
    Band 12 Block=1354x2040 Type=UInt16, ColorInterp=Undefined

Ou vous pouvez utiliser ``gdal_translate`` pour lire les bandes de l'image à 
partir de ce sous-ensemble de données.
Notez que vous devez fournir exactement le contenu de la ligne marqué 
**SUBDATASET_n_NAME** à GDAL, en incluant le préfixe ``HDF4_SDS:``.

Ce pilote a seulement pour but d'importer des sous-ensembles de capteur distant 
et géospatiale sous forme d'image raster. Si vous voulez explorer toutes les 
données contenu dans un fichier HDF vous devez utiliser un autre outil (vous 
pouvez trouver des informations sur différents outils HDF en utilisant les 
liens à la fin de cette section).

Géo-référencement
------------------

Il n'y a pas de manière universelle pour stocker le géo-référencement dans les 
fichiers HDF. Cependant, certains types de produits ont des mécanismes pour 
sauvegarder le géo-référencement, et certains sont gérés par GDAL. Pour 
l'instant, sont supportés (subdataset_type est indiqué entre parenthèses) :

* fichiers HDF4 créés par GDAL (**GDAL_HDF4**) 
* ASTER Level 1A (**ASTER_L1A**) 
* ASTER Level 1B (**ASTER_L1B**) 
* ASTER Level 2 (**ASTER_L2**) 
* ASTER DEM (**AST14DEM**) 
* MODIS Level 1B Earth View products (**MODIS_L1B**) 
* MODIS Level 3 products (**MODIS_L3**) 
* SeaWiFS Level 3 Standard Mapped Image Products (**SEAWIFS_L3**) 

Par défaut le pilote hdf4 lit seulement les points d'amer à partir de toutes les 
10 lignes et colonne à partir du jeu de données EOS_SWATH. Vous pouvez changer 
ce comportement en définissant la variable d'environnement *GEOL_AS_GCPS* à 
PARTIAL (défaut), NONE, ou FULL.

Problèmes de création
---------------------

Ce pilote support la création des ensembles de données Scientifique HDF4. Vous 
pouvez créer un ensemble de données 2D (un pour chaque bande en entrée) ou un 
simple ensemble de données 3D ou la 3ème dimension représente le numéro de la 
bande. Toutes les méta-données et les descriptions des bandes des ensembles de 
données en entrée sont stockés comme des attributs HDF4. Les informations de 
projection (s'ils existent) et les coefficients de transformation affine sont 
aussi stockés sous forme d'attributs. Les fichiers créés par GDAL ont un 
attribut spécial :
::
    
    "Signature=Created with GDAL (http://www.remotesensing.org/gdal/)"

et sont automatiquement reconnus lors de la lecture, ainsi les informations de 
projections et la matrice de transformation sont restaurés.

**Options de création :**

* **RANK=n :** créé un SDS à n-dimension. Pour l'instant seul les ensembles de 
  données 2D et 3D sont gérés. Par défaut un ensemble de données à 3 dimensions 
  sera créée.

Méta-données
--------------

Tous les attributs HDF4 sont traduit en transparence comme des méta-données 
GDAL. Dans les fichiers HDF, les  attributs peuvent être assigné à l'ensemble 
du fichier autant qu'à des sous-ensemble de données particuliers. 

Compilation du pilote
----------------------

Ce pilote a été compilé au plus haut de la bibliothèque NCSA HDF, vous avez donc 
besoin de compiler GDAL avec le support HDF4. Vous pouvez chercher un binaire 
pré-compilé pour votre distribution ou télécharger le code source ou les 
binaires de la page de NCSA HDF (voyez les liens ci-dessous).

Noter que la bibliothèque NCS HDF a été compilé avec de nombreux paramètres par 
défaut dans le fichier *hlimits.h*. Par exemple, *hlimits.h* définie le nombre 
maximal de fichiers ouverts :
::
    
    #   define MAX_FILE   32

Si vous avez besoin d'ouvrir plus de fichier HDF4 simultanément, vous devez 
changer cette valeur et recompiler la bibliothèque HDF4 (et relier GDAL si vous 
utilisez des bibliothèques HDF statiques).

Voir aussi
----------

* Implémenté comme *gdal/frmts/hdf4/hdf4dataset.cpp* et *gdal/frmts/hdf4/hdf4imagedataset.cpp*.
* `Group HDF <http://www.hdfgroup.org/>`_
* Sources de donnée aux formats HDF4 et HDF4-EOS : 

  * `Earth Observing System Data Gateway <http://edcimswww.cr.usgs.gov/pub/imswelcome/>`_

* Documentation de produits individuels, géré par ce pilote :

  * `Geo-Referencing ASTER L1B Data <http://edcdaac.usgs.gov/aster/ASTER_GeoRef_FINAL.pdf>`_
  * `ASTER Standard Data Product Specifications Document <http://asterweb.jpl.nasa.gov/documents/ASTERHigherLevelUserGuideVer2May01.pdf>`_
  * `MODIS Level 1B Product Information and Status <http://www.mcst.ssai.biz/mcstweb/L1B/product.html>`_
  * `MODIS Ocean User's Guide <http://modis-ocean.gsfc.nasa.gov/userguide.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/098 (trunk 22813)