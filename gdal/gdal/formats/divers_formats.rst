.. _`gdal.gdal.formats.divers_formats`:
i
===============
Formats divers
===============

.. _`gdal.gdal.formats.divers_formats.aaigrid`:

AAIGrid -- Arc/Info ASCII Grid
================================

Géré pour l'accès en lecture et écriture, incluant la lecture d'une 
transformation affine de géoréférencement et certaines projections. Ce format 
est le format ASCII d'échange pour Arc/Info Grid, et prennent la forme d'un 
fichier ASCII, plus parfois un fichier .prj associé. Il est normalement produit 
par la commande ``ASCIIGRID`` d'Arc/Info.

La gestion des projections (lu si un fichier \*.prj est disponible) est assez 
limitée. Des exemples additionnels de fichier .prj peuvent être envoyé au 
mainteneur,  warmerdam@pobox.com.

La valeur ``NODATA`` pour la lecture de la grille est également préservée 
lorsqu'elle est disponible.

Par défault, le type de données renvoyé pour les jeux de données AAIGRID par GDAL 
est auto-détecté, et définie à Float32 pour les grilles avec des valeurs de point 
en virgule flottante ou sinon en Int32. Cela est réalisé par l'analyse du format 
des valeurs NODATA et les premiers 1000 ko de données de la grille. À partir de 
GDAL 1.8.0, vous pouvez explicitement définir le type de données en définissant 
l'option de configuration *AAIGRID_DATATYPE* (les valeurs Int32, Float32 et 
Float64 sont actuellement gérés)

Si les pixels écrits ne sont pas carrés (la largeur et la hauteur du pixel dans 
l'unité géoréférencé diffèrent) alors les paramètres DX et DY seront affichés à 
la place de CELLSIZE. De tel fichier peuvent être utilisé dans Golden Surfer, 
mais pas dans la plupart des programmes de lecture de grille ASCII. Pour forcer 
la taille du pixel X à utiliser comme ``CELLSIZE`` utilisez l'option de création 
``FORCE_CELLSIZE=YES`` ou re-échantillonné l'entrée pour avoir des pixels carrés.

Lors de l'écriture de valeurs en virgules flottantes, le pilote utilise le motif 
de format *"%6.20g* par défaut. Vous pouvez lire le `manuel de référence <http://en.wikipedia.org/wiki/Printf>`_ 
pour printf pour avoir une idée du comportement exact de ceci ;-). vous 
pouvez aussi spécifier le nombre de décimal avec l'option de création 
``DECIMAL_PRECISION``. par exemple ``DECIMAL_PRECISION=3`` renverra des nombres 
avec trois décimales.

Le pilote AIG est également disponible pour le format de grille binaire d'Arc/Info.

.. note:: Implémenté dans gdal/frmts/aaigrid/aaigriddataset.cpp.

.. _`gdal.gdal.formats.divers_formats.ace2`:

ACE2 -- ACE2
=============

(à partir de GDAL >= 1.9.0)

C'est un pilote de commodité afin de lire les MNT d'ACE2 . Ces fichiers 
contiennent des données binaires brutes. Le géoréférencement est entièrement 
déterminé par le nom du fichier. Qualité, source et confiance des couches sont 
de type Int16, alors que les données d'altitude sont retournées comme Float32.

`Aperçu du produit ACE2 <http://tethys.eaprs.cse.dmu.ac.uk/ACE2/shared/overview>`_

.. note:: Implémenté dans *gdal/frmts/raw/ace2dataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.adrgarc`:

ADRG/ARC Digitized Raster Graphics (.gen/.thf)
===============================================

Géré par GDAL en lecture. La création est possible mais doit être considérée 
comme expérimentale et une manière de tester l'accès en lecture (bien que les 
fichiers créés par le pilote peut être lu avec succès par d'autres logiciels).

Un jeu de données EADGR est composé de plusieurs fichiers. Le fichier reconnu 
par GDAL est le Fichier d'Information Général (.GEN). GDAL a besoin également du 
fichier image (.IMG) dans lequel se trouve les données.

Le fichier d'En-tête de Transmission (.THF) peut également être utilisé comme 
une entrée à GDAL. Si le THF référence plus d'une image, GDAL renverra la 
composition des images comme sous jeu de données. Si le THF référence une seule 
image seulement, GDAL l'ouvrira directement.

Les aperçues, légendes et insets ne sont pas utilisé. Les zones Polaires (ARC 
Zone 9 et 18) ne sont pas gérées (dû au manque de données tests).

C'est une alternative à l'utilisation de `OGDI Bridge <http://www.gdal.org/frmt_ogdi.html>`_ 
pour les jeux de données ADRG.

Voyez également : Les `spécification ADRG <http://earth-info.nga.mil/publications/specs/printed/89007/89007_ADRG.pdf>`_ (MIL-A-89007)

.. _`gdal.gdal.formats.divers_formats.aig`:

AIG -- Arc/Info Binary Grid
============================

Géré par GDAL pour l'accès en lecture. Ce format est le format binaire 
interne pour les grilles Arc/Info, et prend la forme de répertoire de niveau de 
couverture (NdT, si vous trouvez mieux ...) dans une base de données Arc/Info. 
Pour ouvrir la couverture sélectionnez le répertoire de la couverture, ou un 
fichier .adf (tel que hdr.adf) à l'intérieure. Si le répertoire ne contient pas 
de fichier(s) avec un nom comme *w001001.adf* alors ce n'est pas une couverture 
de grille.

La gestion inclut la lecture d'une transformation affine du géoréférencement, 
certaines projections et une table de couleur (.clr) si disponible.

Ce pilote a été développé sur la base d'un *reverse-engineering* du format. Lisez 
la description du format pour plus de détails : 
http://home.gdal.org/projects/aigrid/index.html.

La gestion des projections (lu si un fichier prj.adf est disponible) est assez 
limité. Des exemples additionnels de fichier .prj peuvent être envoyé au 
mainteneur,  warmerdam@pobox.com.

.. note:: Implémenté dans gdal/frmts/aigrid/aigdataset.cpp.


.. _`gdal.gdal.formats.divers_formats.bsb`:

Format BSB -- Maptech/NOAA BSB Nautical Chart
==============================================

Le format BSB Nautical Chart est géré en accès en lecture, incluant la lecture 
de la table de couleur et les points de références (comme les points d'amer). 
Notez que les fichiers .BSB ne peuvent pas être sélectionné directement. À la 
place sélectionnez les fichiers .KAP. Les versions 1.1, 2.0 et 3.0 ont été 
testées avec succès.

Ce pilote doit également géré le format GEO/NOS tel que fournit par Softchart. 
Ces fichiers normalement ont l'extension .nos avec des fichiers .geo associés 
contenant le géoréférencement ... Les fichiers .geo sont pour l'instant ignoré.
Ce pilote est basé sur le travail de Mike Higgins. Lisez les fichiers 
frmts/bsb/bsb_read.c pour les détails sur les brevets affectant le format BSB.

À partir de GDAL 1.6.0, il est possible de sélectionner une palette de couleur 
alternative via l'option de configuration ``BSB_PALETTE``. La valeur par défaut 
est *RGB*. Voici d'autres valeurs qui peuvent être utilisées : *DAY*, *DSK*, 
*NGT*, *NGR*, *GRY*, *PRC*, *PRG* ...

.. note:: Implémenté dans gdal/frmts/bsb/bsbdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.bt`:

Format BT -- VTP .bt Binary Terrain
====================================

Le format .BT est utilisé pour les donnés d'élévation dans le logiciel VTP. Le 
pilote inclut la gestion pour la lecture et l'écriture du format .bt 1.3 
incluant la gestion des types de données des pixels en Int16, Int32 et Float32.
Le pilote ne gère pas la lecture et l'écriture des fichiers compressés (.bt.gz) 
même si cela est géré par le logiciel VTP. S'il vous plaît, décompressez les 
fichiers avant d'utiliser GDAL avec "gzip -d file.bt.gz".

Les projections dans les fichiers .prj externes sont lu et écrit, et la gestion 
pour la plupart des systèmes de coordonnées définie en interne est également 
disponible.

L'accès des images en lecture et écriture avec le pilote .bt de GDAL est 
terriblement lent à cause de l'inefficacité de la stratégie d'accès aux colonnes 
de données. Cela pourrait être corrigé, mais demanderait un effort important.

.. note:: Implémenté dans gdal/frmts/raw/btdataset.cpp.

Lisez également : Le format de fichier BT est défini sur le site Web de VTP : 
http://www.vterrain.org/Implementation/Formats/BT.html.

.. _`gdal.gdal.formats.divers_formats.ceos`:

CEOS -- CEOS Image
===================

C'est un simple lecteur pour les fichiers images ceaos. Pour l'utiliser, 
sélectionné le fichier d'imagerie principale. Ce pilote lit seulement les 
données images, et ne récupère pas les méta-données ou le géoréférencement.

Ce pilot est connu pour fonctionner avec les données CEOS produites par Spot 
Image, mais présente des problèmes avec plusieurs autres sources de données. En 
particulier, il ne fonctionnera qu'avec les données non signées sous 8 bits.

Voyez le pilote séparé SAR_CEOS (page 75, E.XXXV.29) pour accéder aux produits 
de données SAR CEOS.

.. note:: Implémenté dans gdal/frmts/ceos/ceosdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.dods`:

DODS/OPeNDAP – lecture des rasters à partir de serveurs DODS/OPeNDAP
=====================================================================

Gestion pour l'accès en lecture des serveurs DODS/OPeNDAP. Envoie l'URL 
DODS/OPeNDAP au pilote tel que vous l'aurez accéder pour un fichier local. L'URL 
définit le serveur distant, le jeu de données et les rasters dans le jeu de 
données. De plus, vous devez dire au pilote quelles dimensions doivent être 
interprétées comme bandes distinctes ainsi que laquelle correspond à la latitude 
et la longitude. Lisez le fichier README.DODS pour de plus amples informations.

.. _`gdal.gdal.formats.divers_formats.doq1`:

DOQ1 -- Première génération USGS DOQ
=====================================

Gestion de l'accès en lecture, incluant la lecture d'une transformation du 
géoréférencement affine, et la capture de la projection. Ce format est le vieux 
format, non étiqueté DOQ (Digital Ortho Quad) de l'USGS.

.. note:: Implémenté dans gdal/frmts/raw/doq1dataset.cpp.

.. _`gdal.gdal.formats.divers_formats.doq2`:

DOQ2 – Nouveau USGS DOQ étiqueté
==================================

Gestion pour l'accès en lecture, incluant la lecture  d'une transformation du 
géoréférencement affine, et la capture de la projection et la lecture des autres 
champs auxiliaires comme métadonnées. Ce pilote est le nouveau format, étiqueté 
DOQ (Digital Ortho Quad) de l'USGS.

Ce pilote a été développé par Derrick J Brashear.

.. note:: Implémenté dans gdal/frmts/raw/doq2dataset.cpp.

Lisez également : les standards DOQ de l'USGS sur 
http://rockyweb.cr.usgs.gov/nmpstds/doqstds.html

.. _`gdal.gdal.formats.divers_formats.e00grid`:

E00GRID -- Arc/Info Export E00 GRID
====================================

(GDAL >= 1.9.0)

GDAL gère la lecture des raster/MNT exporté comme grilles E00.

Le pilote a été testé avec des jeux de données tels que ceux disponibles sur 
`ftp://msdis.missouri.edu/pub/dem/24k/county/ <ftp://msdis.missouri.edu/pub/dem/24k/county/>`_

.. note:: Implémenté dans *gdal/frmts/e00grid/e00griddataset.cpp*.


.. _`gdal.gdal.formats.divers_formats.ehdr`:

EHdr -- ESRI .hdr Labelled
===========================

GDAL gère la lecture et l'écriture du format d'étiquette .hdr d'ESRI, souvent 
appelé format BIL d'ESRI. Les types de données raster d'entier en 8, 16 et 32 
bits sont gérés ainsi que les virgules flottantes en 32 bites. Les systèmes de 
coordonnées (à partir d'un fichier .prj) et le géoréférencement sont gérés. Les 
options non reconnues dans le fichier .hdr sont ignorées. Pour ouvrir un jeu de 
données, sélectionnez le fichier avec le fichier image (souvent avec l'extension 
.bil). Si présent, le fichier des tableaux de couleurs .clr sont lu mais pas 
écrit.

Ce pilote ne fait pas toujours la différenciation entre les données en virgules 
flottantes et en entier. L'extension GDAL au format .hdr pour les différencier 
est d'ajouter un champ nommé *PIXELTYPE* avec des valeurs parmi *FLOAT*, 
*SIGNEDINT* ou *UNSIGNEDINT*. En combinaison avec le champ *NBITS* il est 
possible de décrire toutes les variations des types de pixel.
 
Par exemple :

::
    
    ncols 1375
    nrows 649
    cellsize 0.050401
    xllcorner -130.128639
    yllcorner 20.166799
    nodata_value 9999.000000
    nbits 32
    pixeltype float
    byteorder msbfirst

Ce pilote peut être suffisant pour lire les données GTOPO30.

.. note:: Implémenté dans *gdal/frmts/raw/ehdrdataset.cpp*.

Lisez également : 

* ESRI whitepaper : Formats d'image étendue pour ArcView GIS 3.1 et 3.2 (BIL, 
  voir p. 5) : http://downloads.esri.com/support/whitepapers/other\_/eximgav.pdf
* GTOPO30 - Global Topographic Data : http://edcdaac.usgs.gov/gtopo30/gtopo30.html
* Documentation sur GTOPO30 : http://edcdaac.usgs.gov/gtopo30/README.html
* :ref:`gdal.gdal.formats.divers_formats.srtmhgt`


.. _`gdal.gdal.formats.divers_formats.envi`:

ENVI - ENVI .hdr Labelled Raster
================================

GDAL gère certaines variations de fichiers raster brute avec un fichier.hdr de 
styles ENVI associés décrivant le format. Pour sélectionner un fichier raster 
ENVI existant sélectionnez le fichier binaire contenant la donnée (par opposition 
aux fichier .hdr), et GDAL trouvera le fichier .hdr en remplaçant l'extension du 
jeu de données par .hdr.

GDAL devrait gérer la lecture des formats  bil, bip et bsq interlacée, et la 
plupart des types de pixel sont gérés, incluant les entiers sur 8 bit non signés, 
16 et 32 bits signés et non signés, les virgules flottantes sur 32 et 64 bits et 
les virgules flottantes complexes sur 32 et 64 bits. Il y a une gestion limitée pour la 
reconnaissance du mot-clé map_info avec le système de coordonnées et le 
géoréférencement. En particulier, UTM et  State Plane devraient fonctionner.

Options de création :

* ``INTERLEAVE=BSQ/BIP/BIL`` : force la génération d'un type définie 
  d'interlacement. BSQ === band sequental (par défaut), BIP === data 
  interleaved by pixel, BIL === data interleaved by line.
* ``SUFFIX=REPLACE/ADD`` : force l'ajout du suffixe ".hdr" au fichier fournit, 
  par exemple, si l'utilisateur sélectionne le nom "file.bin" pour le nom en 
  sortie du jeu de données, le fichier d'en-tête "file.bin.hdr" sera crée. Par 
  défaut le suffixe du fichier d'en-tête remplace le suffixe du fichier binaire, 
  par exemple pour  "file.bin" le fichier d'en-tête nommé "file.hdr" sera créé. 

.. note:: Implémenté dans *gdal/frmts/raw/envidataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.envisat`:

Envisat -- Envisat Image Product
==================================

GDAL gère le format du produit Envisat en accès en lecture. Tous les types 
d'échantillon sont gérés. Les fichiers avec deux jeux de données de mesures 
correspondantes (MDS) sont représentés comme ayant deux bandes. Pour l'instant 
tous les produits ASAR de niveau 1 et supérieur et quelques produits MERIS et 
AATSR sont gérés.

Les points de contrôles des jeux de données GEOLOCATION GRID ADS sont lus si 
elles sont disponibles, généralement en donnant une bonne couverture du jeu de 
données. Les points d'amer sont en WGS84.

Virtuellement toutes les paires clés/valeurs du MPH et SPH (en-têtes Primaire et 
Secondaire) sont copiées comme des métas-données de niveau du jeu de données.

Les paramètres ASAR et MERIS contenue dans les enregistrements ADS et GADS (sauf 
ceux de la géolocalisation) peuvent être récupérés sous forme de pair de clé/valeur 
en utilisant le domaine de métadonnées "RECORDS".

.. note:: Implémenté dans *gdal/frmts/envisat/envisatdataset.cpp*.

**Lisez également :** Envisat Data Products à l'ESA : http://envisat.esa.int/dataproducts/

.. _`gdal.gdal.formats.divers_formats.fits`:

FITS -- Flexible Image Transport System
========================================

FITS est un format utilisé principalement par les astronomes, mais c'est un 
format relativement simple qui gère les types d'images arbitraires et les images 
multispectrales et donc a trouvé son utilisation dans GDAL. La gestion de FITS 
est implémentée par la bibliothèque SFITSIO standard 
(http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html) que vous devez 
avoir sur votre système dans le but d'activer la gestion FITS. À la fois la 
lecture et l'écriture de fichiers FITS sont gérées. À ce moment, aucune gestion 
pour un système de géoréférencement n'est développée, mais la gestion du WCS 
(World Coordinate System) est possible dans le futur.

Les mots-clés d'en-tête non standard qui sont présents dans le fichier FITS 
seront copiés vers les méta-données du jeu de données quand le fichier est 
ouvert, pour l'accès par les méthodes de GDAL. De même, les mots-clés non 
standard que l'utilisateur définit dans les méta-données du jeu de données seront 
écrits dans le fichier FITS quand la prise en charge de GDAL sera fermée.

Remarque à ceux qui sont familiers avec la bibliothèque ``CFITSIO`` : la 
regraduation automatique des valeurs des données, déclenchée par la présence des 
mots-clés d'en-tête ``BSCALE`` et ``BZERO`` dans un fichier FITS, est désactivée 
dans GDAL. Ces mots-clés d'en-tête sont accessible et peuvent être mise à jour 
par les méta-données du jeu de données, de la même manière que les autres 
mots-clés d'en-tête, mais ils n'affectent pas la lecture/l'écriture des valeurs 
des données à partir de/vers le fichier.

.. note:: Implémenté dans *gdal/frmts/fits/fitsdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.grssgrd`:

GRASSASCIIGrid -- GRASS ASCII Grid
===================================

(GDAL >= 1.9.0)

Gère la lecture du format grille ASCII de GRASS (similaire à la commande 
ASCIIGRID d'Arc/Info).

Part défaut, le type des données renvoyé pour les jeux de données grilles ASCII 
de GRASS par GDAL est autodétecté, et définie à Float32 pour les grilles avec des 
valeurs en virgules flottantes ou sinon Int32. Cela est réalisé par l'analyse du 
format des valeurs nulles et les premiers 100 ko de onnées de la grille. Vous 
pouvez aussi explicitement définir le type de données en définissant l'option de 
configuration *GRASSASCIIGRID_DATATYPE* (les valeurs Int32, Float32 et Float64 
sont géré pour l'instant).

.. note:: Implémenté dans *gdal/frmts/aaigrid/aaigriddataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.gsag`:

GSAG -- Golden Software ASCII Grid File Format
===============================================

C'est la version basé sur l'ASCII (lisible par un être humain) d'un des formats 
raster utilisé par les produits de Golden Software (tels que ceux de la série 
Surfer). Ce format est géré à la fois en lecture et en écriture (création, 
suppression et copie incluse). Pour l'instant les formats associés pour la 
couleur, les méta-données, et les formes ne sont pas gérés.

.. note:: *Implémenté dans gdal/frmts/gsg/gsagdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.gsbg`:

GSBG -- Golden Software Binary Grid File Format
===============================================

C'est la version binaire (non lisible par un être humain) d'un des formats 
raster utilisés par les produits de Golden Software (tels que ceux de la série 
Surfer). Comme pour la version ASCII, ce format est géré à la fois en lecture 
et en écriture (création, suppression et copie inclus). Pour l'instant les 
formats associés pour la couleur, les méta-données, et les formes ne sont pas 
gérés.

.. note:: *Implémenté dans gdal/frmts/gsg/gsbgdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.gs7bg`:

GS7BG -- Golden Software Surfer 7 Binary Grid File Format
==========================================================

C'est la version binaire (non lisible par un être humain) d'un des formats 
raster utilisés par les produits de Golden Software (tels que ceux de la série 
Surfer). Ce format diffère du format GSBG (connu également comme le format 
grille binaire de Surfer 6), il est plus compliqué et moins flexible. Ce format 
est géré en lecture seule.

.. note:: Implémenté dans *gdal/frmts/gsg/gs7bgdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.gxf`:

GXF -- Grid eXchange File
=========================

C'est un format d'échange de raster diffusé par Geosoft, et en fait un standard 
dans le champ de la gravité/magnétique. Le format est géré en lecture et 
écriture et inclus la gestion des informations de géo-référencement et de 
projections.

Par défaut, le type de données renvoyé pour les jeux de données GXF par GDAL est 
Float32. À partir de GDAL 1.8.0, vous pouvez définir le type de données en 
définissant l'option de configuration *GXF_DATATYPE* (Float64 géré pour le moment)

Détails sur le code géré, et le format peuvent être trouvé sur la page GXF-3 
http://home.gdal.org/projects/gxf/index.html

.. note:: Implémenté dans *gdal/frmts/gxf/gxfdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.ida`:

IDA -- Analyse et affichage d'image
===================================

GDAL gère la lecture et l'écriture des images IDA avec quelques limitations. Les 
images IDA sont les images du format de WinDisp 4. Les fichiers ont toujours 
une bande de données 8 bits. Les fichiers IDA ont souvent l'extension .img bien 
que cela n'est pas requis.

Les informations de projection et de géoréférencement est lu bien que certaines 
projections (c'est à dire Météosat et Hammer-Aitoff) ne sont pas gérés. Lors de 
l'écriture des fichiers IDA la projection doit avoir un false easting et false 
northing de zéro. Les systèmes de coordonnées gérés dans les fichiers IDA sont 
Géographique, Lambert Conformal Conic, Lambert Azimuth Equal Area, Albers 
Equal-Area Conic et Goodes Homolosine.

Les fichiers IDA contiennent typiquement des valeurs échantillonnées en 8 bits via 
une pente et un décalage. Ceux-ci sont retournés comme les valeurs de pente et 
de décalage de la bande et ils doivent être utilisés si la donnée doit être 
re-échantillonée vers les valeurs brutes originales pour analyse. 

.. note:: Implémenté dans *gdal/frmts/raw/idadataset.cpp*. 

**Lisez également :** WinDisp : http://www.fao.org/giews/english/windisp/windisp.htm

.. _`gdal.gdal.formats.divers_formats.jdem`:

JDEM -- Japanese DEM (.mem)
===========================

GDAL inclut la gestion de la lecture pour les fichiers DEM Japonais, ayant 
normalement l'extension .mem. Ces fichiers sont un produit de la Japanese 
Geographic Survey Institute.

Ces fichiers sont représentés par une bande d'entiers flottants de 32bit avec 
des données d'élévation. Le géoréférencement des fichiers est retourné ainsi 
que le système de coordonnées (toujours en Lat/Lon sur le datum de Tokyo).
Il n'y a pas de gestion de la mise à jour ou de la création pour ce format.

.. note:: Implémenté dans *gdal/frmts/jdem/jdemdataset.cpp*.

**Lisez également :** Le site Web de Geographic Survey Institute (GSI) : 
http://www.gsi.go.jp/ENGLISH/

.. _`gdal.gdal.formats.divers_formats.lan`:

LAN -- Erdas 7.x .LAN et .GIS
==============================

GDAL gère la lecture des fichiers raster Erdas 7.x .LAN et GIS. Pour l'instant 
les types de données des pixels de 4 bits, 8 bits et 16 bits sont gérés pour la 
lecture et de 8 et 16 bits pour l'écriture.

GDAL lit l'étendue des cartes (geotransform) à partir des fichiers LAN/GIS, et 
tente de lire les informations du système de coordonnées. Cependant, ce format 
de fichier n'inclut pas complètement les informations du système de coordonnées, 
donc pour les systèmes de coordonnées UTM et state plane  une définition de 
LOCAL_CS est renvoyé avec des unités linéaires valides, mais aucune autres 
informations significatives.

Les fichiers .TRL, .PRO et world sont ignorés pour le moment.

.. note:: Implémenté dans *gdal/frmts/raw/landataset.cpp*

Le développement de ce pilote a été financé par Kevin Flanders de PeopleGIS 
(http://www.peoplegis.com/).

.. _`gdal.gdal.formats.divers_formats.mff`:

MFF -- Vexcel MFF Raster
=========================

GDAL inclut la gestion de la lecture, la mise à jour et la création du format 
raster MFF de Vexcel. Les jeux de données MFF consistent en un fichier d'en-tête 
(typiquement avec l'extension .hdr) et un ensemble de fichiers donnés avec des 
extensions comme .x00. .b00 etc. Pour ouvrir un jeu de donné sélectionnez le 
fichier .hdr.

La lecture des points d'amer Lat/Lon (TOP_LEFT_CORNER, ...) est gérée, mais il 
n'y a pas de gestion pour la lecture des informations de projections ou de 
transformation affine.

Les mots-clé non reconnus du fichier .hdr sont préservés comme méta-données.

Tous les types de données avec un équivalents GDAL sont gérés, incluant les 
précisions des types de données entiers, réels et complexes en 8, 16, 32 et 64 
bites. De plus, les fichiers organisés en tuile (comme produit par le Vexcel SAR 
Processor – APP) sont gérés en lecture.

En création (avec un code de format de MFF) un fichier raster simple et non 
géoréférencé est créé.

Les fichiers MFF ne sont pas normalement portables entre les systèmes avec 
différents ordres d'octets. Cependant, GDAL utilise le nouveau mot-clé BYTE_ORDER 
qui peut prendre la valeur de LSB (Integer -- little endian), et MSB (Motorola 
-- big endian).  Cela peut être manuellement ajouté au fichier .hdr si nécessaire.

.. note:: Implémenté dans gdal/frmts/raw/mffdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.ndf`:

NDF -- NLAPS Data Format
========================

GDAL a une gestion limitée des fichiers de Format de Données NLAPS. C'est un 
format d'abord   utilisé par le Centre de Données Eros pour la distribution des 
données Landsat. Les jeux de données NDF contiennent un fichier d'en-tête 
(souvent avec une extension .Hl) et un ou plus de fichiers de données brutes 
associées (souvent .I1, .I2, ...). Pour ouvrir un jeu de données sélectionner 
le fichier d'en-tête, souvent avec l'extension.H1, .H2 ou .HD.

Le pilote NDF gère seulement les données 8 bises. La seule projection gérée est 
UTM. La version 1 de NDF (NDF_VERSION=0.00)  et la version 2 de NDF sont toutes 
deux gérées.

.. note:: Implémenté dans gdal/frmts/raw/ndfdataset.cpp.

**Lisez également :** Les spécifications du format de Données NLAPS sur la page 
http://landsat.usgs.gov/documents/NLAPSII.pdf

.. _`gdal.gdal.formats.divers_formats.gmt`:

GMT -- GMT Compatible netCDF
============================

GDAL a une gestion limitée pour la lecture et l'écriture des fichies grid de 
netCDF. Les fichiers netCDF qui ne sont pas reconnus comme grilles (il manque 
des variables appelées dimension et z) seront ignorés silencieusement par ce 
pilote. Ce pilote a d'abord l'objectif de fournir un mécanisme pour l'échange 
de grille avec le paquet GMT (http://gmt.soest.hawaii.edu/). Le pilote netCDF 
doit être utilisé pour des jeux de données betCDF plus générales.

L'information des unités dans le fichier sera ignoré, mais les informations 
x_range, et y_range seront lut pour obtenir les éténdus de géoréférencement du 
raster. Tous les types de données netCDF doivent être gérés en lecture. Les 
fichiers nouvellement crées (avec un type de GMT) auront toujours comme unité le 
mètre pour x, y et z mais les valeurs de x_range, y_range et z_range  doivent 
être correct. Remarquez que netCDF n'ont pas de type de données non signé en 
byte, les rasters 8 bites devront être  généralement convertis en Int16 pour 
l'exporter vers GMT.

La gestion de netCDF dans GDAL est optionnelle et n'est pas compilée par défaut.

.. note:: Implémenté dans gdal/frmts/netcdf/gmtdataset.cpp.

**Lisez également :** Unidata NetCDF Page : http://www.unidata.ucar.edu/packages/netcdf/


.. _`gdal.gdal.formats.divers_formats.paux`:

PAux -- PCI .aux Labelled Raw Format
=====================================

GDAL inclut un développement partiel des fichiers rasters brutes étiquetées .aux 
pour la lecture, l'écriture et la création. Pour ouvrir un fichier étiquetté 
PCI, sélectionné le fichier de données brutes lui-même. le fichier .aux (qui 
doit avoir un nom identique) sera utilisé automatiquement.

Le type de format pour la création de nouveaux fichiers est PAux. Tous les types 
de données (8U, 16U, 16S, et 32R) sont gérés. Pour l'instant, le 
géo-référencement, les projections et les autres méta-données sont ignorés.

Options de création
********************

* **INTERLEAVE=PIXEL/LINE/BAND :** établit l'entrelacement de la sortie, BAND 
  par défaut.

.. note:: Implémenté dans gdal/frmts/raw/pauxdataset.cpp.

Voyez également : `Description du format .aux de PCI <http://www.pcigeomatics.com/cgi-bin/pcihlp/GDB|Supported+File+Formats|Raw+Binary+Image+Format+(RAW)|Raw+.aux+Format>`_

.. _`gdal.gdal.formats.divers_formats.pcraster`:

PCRaster raster file format
============================

GDAL inclut la gestion de la lecture et l'écriture de fichiers raster PCRaster. 
PCRaster est un système de modélisation dynamique pour des modèles de simulation 
distribués. Les principales applications de PCRaster se trouvent dans la 
modélisation environnementale : géographie, hydrologie, écologie pour en nommer 
quelques-uns. Des exemples incluent des modèles d'écoulement des eaux de pluie, 
modèles de compétition de la végétation et des modèles de stabilité des pentes.

Le pilote lit tous les types de cartes PCIRaster : booléens, nominales, 
ordinales, scalaire, directionnel et ldd. La même représentation de la cellule 
utilisée pour stocker les valeurs dans le fichier est utilisée pour stocker les 
valeurs en mémoire.

Le pilote détecte si la source du raster GDAL est un fichier PCRaster. Quand un 
tel raster est écrit dans un fichier de l'échelle de valeur du raster originel 
sera utilisé. Le pilote écrit **toujours** les valeurs en utilisant des 
représentations de la cellule UINT1, INT4 or REAL4, en fonction de l'échelle de 
valeurs :

+--------------------+--------------------------------+
+ Échelle de valeurs +  Représentation de la cellule  +
+--------------------+------------------------------==+
+ VS_BOOLEAN         +  CR_UINT1                      +
+--------------------+--------------------------------+
+ VS_NOMINAL         +  CR_INT4                       +
+--------------------+--------------------------------+
+ VS_ORDINAL         + CR_INT4                        +
+--------------------+--------------------------------+
+ VS_SCALAR          + CR_REAL4                       +
+--------------------+--------------------------------+
+ VS_DIRECTION       + CR_REAL4                       +
+--------------------+--------------------------------+
+ VS_LDD             + CR_UINT1                       +
+--------------------+--------------------------------+

Pour les rasters d'autres sources qu'un fichier PCRaster une échelle de valeurs 
et une représentation de la cellule sont déterminées en fonction des règles 
suivantes :

+---------------------+---------------------------+--------------------------------------+
+  Type de la source  +  Échelle de valeur cible  +  Représentation cible de la cellule  +
+---------------------+---------------------------+--------------------------------------+
+ GDT_Byte            +  VS_BOOLEAN               + CR_UINT1                             +
+---------------------+---------------------------+--------------------------------------+
+ GDT_Int32           +  VS_NOMINAL               + CR_INT4                              +
+---------------------+---------------------------+--------------------------------------+
+ GDT_Float32         +  VS_SCALAR                + CR_REAL4                             + 
+---------------------+---------------------------+--------------------------------------+
+ GDT_Float64         +  VS_SCALAR                + CR_REAL4                             +
+---------------------+---------------------------+--------------------------------------+

Le pilote peut convertir les valeurs d'une représentation de cellule gérée à un 
autre. Il ne peut pas convertir vers des représentations de cellule non gérée. 
Par exemple, il n'est pas possible d'écrire un fichier raster PCIRaster à partir 
de valeurs qui sont utilisées comme CR_INT2 (GDT_Int16). 

Bien que l'extension de fichier raster PCRaster soit de facto *.map*, le logiciel 
PCRaster ne nécessite pas une extension de fichier standard.

.. note:: Implémenté dans gdal/frmts/pcraster/pcrasterdataset.cpp.

**Lisez également :** PCRaster website at Utrecht University et PCRaster 
Environmental Software company website. 


.. _`gdal.gdal.formats.divers_formats.png`:

PNG -- Portable Network Graphics
=================================

GDAL inclut une gestion de la lecture et de la création des fichiers .png. Les 
fichiers en nuance de gris, pseudo-couleur, avec une palette, RVB et RVBA sont 
gérés ainsi que les précisions de 8 et 16 bits par échantillon.

Les fichiers PNG sont linéairement compressés, la lectuer aléatoire de gros 
fichier PNG peut être inefficace (résultat de plusieurs redémarrages de la 
décompression  à partir du début du fichier).

Les textes importants sont traduits en méta-données, typiquement avec des lignes 
multiples par objet. Les :ref:`gdal.gdal.formats.divers_formats.wld` avec les 
extensions .pgw, .pngw ou .wld seront lu. Les valeurs de transparence simple 
dans les fichiers en nuance de gris seront reconnues comme des valeurs *nodata* 
dans GDAL. Les index de transparence dans les images avec palette sont préservés 
quand la table de couleur est lu.

Les fichiers PNG peuvent être crée avec un type de PNG, en utilisant la méthode 
``CreateCopy()``, nécessitant un prototype que l'on peut lire. L'écriture inclus 
la gestion pour divers types d'images, et préservera les valeurs nodata/transparence. 
Les fichiers de géoréférencement .wld sont écrit si l'option WORLDFILE est 
définie. Tous les types de pixels autres que 16 bite non signés seront écrit 
sous huit bites.

À partir de GDAL 1.9.0, les métadonnées XMP peuvent être extraites du fichier, 
et seront stockés comme contenu brute XML dans le domaine de métadonnées xml:XMP.

**Options de création :**

* **WORLDFILE=YES :** force la génération d'un fichier world ESRI associé (avec 
  l'extension .wld). Lisez la section fichier World WLD -- ESRI World File, pour 
  plus de détails. 
* **ZLEVEL=n :** définie la quantité de temps à utiliser pour la compression. La 
  valeur par défaut est 6. Une valeur de 1 est rapide mais ne compresse pas, et 
  une valeur de 9 est lent mais compresse beaucoup mieux.

.. note:: Implémenté dans gdal/frmts/png/pngdataset.cpp.

La gestion de PNG a été développée sur la base de la bibliothèque de référence 
libpng. Plus d'information est disponible sur http://www.libpng.org/pub/png.

.. _`gdal.gdal.formats.divers_formats.pnm`:

PNM -- Netpbm (.pgm, .ppm)
==========================

GDAL inclut la gestion en lecture, et création des fichiers compatibles .pgm 
(nuance de gris), et .ppm (couleur RVB) avec l'outil Netpbm. Seul le format 
binaire (brute) est géré.

Les fichiers Netpbm peuvent être créés avec le type PNM.

**Options de création :**

* ``MAXVAL=n`` : force le paramétrage de la valeur maximale de la couleur à n 
  dans le fichier PNM en sortie. Cela peut être utile si vous planifiez 
  l'utilisation du fichier en sortie avec des logiciels qui ne sont pas libéraux 
  à cette valeur.

.. note:: Implémenté dans gdal/frmts/raw/pnmdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.rpftoc`:

Raster Product Format/RPF (a.toc)
=================================

C'est un lecteur (et seulement en lecture) de produits RPF, comme CADRG ou CIB 
qui utilise un fichier de contenu - *A.TOC* - à partir d'un échange RPF, et 
l'expose comme jeu de données virtuel dont la couverture est l'ensemble des cadres 
contenu dans la table de contenu.

Le pilote rapportera un sous jeu de données différents pour chaque sous jeu de 
données trouvé dans le fichier *A.TOC*.

Résultat d'une commande ``gdalinfo`` sur un fichier *A.TOC*.

::
    
    Subdatasets:
        SUBDATASET_1_NAME=NITF_TOC_ENTRY:CADRG_GNC_5M_1_1:GNCJNCN/rpf/a.toc
        SUBDATASET_1_DESC=CADRG:GNC:Global Navigation Chart:5M:1:1
    [...]
        SUBDATASET_5_NAME=NITF_TOC_ENTRY:CADRG_GNC_5M_7_5:GNCJNCN/rpf/a.toc
        SUBDATASET_5_DESC=CADRG:GNC:Global Navigation Chart:5M:7:5
        SUBDATASET_6_NAME=NITF_TOC_ENTRY:CADRG_JNC_2M_1_6:GNCJNCN/rpf/a.toc
        SUBDATASET_6_DESC=CADRG:JNC:Jet Navigation Chart:2M:1:6
    [...]
        SUBDATASET_13_NAME=NITF_TOC_ENTRY:CADRG_JNC_2M_8_13:GNCJNCN/rpf/a.toc
        SUBDATASET_13_DESC=CADRG:JNC:Jet Navigation Chart:2M:8:13

Dans certaines situations, les tuiles NITF (voir :ref:`gdal.gdal.formats.nitf`) 
dans le sous-jeu de données ne 
partagent pas la même palette. Le pilote RPFTOC fera du mieux qu'il peut pour 
recartographier les palettes à la palette rapportée par ``gdalinfo`` (qui est 
la palette de la première tuile du sous jeu de données). Dans les situations où 
il ne donnerait pas de bon résultat, vous pouvez tenter de définir la variable 
d'environnement ``RPFTOC_FORCE_RGBA`` à ``TRUE`` avant l'ouverture du sous-jeu 
de données. Cela entraînera l'exposition du sous-jeu de données RVBA par le 
pilote au lieu d'un jeu avec une palette.

Il est possible de construire les aperçus externes pour un sous jeu de données. 
L'aperçu pour le premier sous-jeu de données sera nommé *A.TOC.1.ovr* par 
exemple, pour le second jeu de données il sera nommé *A.TOC.2.ovr*, etc. Notez 
que vous devrez rouvrir le sous-jeu de données avec la même définition de 
``RPFTOC_FORCE_RGBA`` que celui que vous avez utilisé lors de la création. 
N'utilisez pas une méthode autre que le ré-échantillonnage de NEAREST lors de 
la construction des aperçus sur un sous-jeu de données avec palette 
(RPFTOC_FORCE_RGBA non définie).

Une commande ``gdalinfo`` sur un de ces sous jeu de données retournera les 
différentes méta-données NITF ainsi que la liste des tuiles NITF du sous-jeu de 
données.

Voir également :

* Pont OGDI : le pilote RPFTOC propose des fonctionnalités équivalentes (sans les 
  dépendances externes) au pilote RPF de la bibliothèque OGDI.
* `MIL-PRF-89038 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28080000+-+99999%29/MIL-PRF-89038_25371/>`_ : spécifications de RPF, CADRG, CIB

.. note:: Implémenté dans gdal/frmts/nitf/rpftocdataset.cpp

.. _`gdal.gdal.formats.divers_formats.sar_ceos`:

SAR_CEOS -- CEOS SAR Image
===========================

C'est un lecteur en lecture seul pour les fichiers images CEOS SAR. Pour 
l'utiliser, sélectionner le fichier image principal.
Ce pilote fonctionne avec la plupart des produits de données Radarsat et ERS, 
incluant les produits complexes ; cependant, il est improbable qu'il fonctionne 
pour les produits autres que Radar CEOS.
Le pilote CEOS plus simple est souvent approprié pour ceux-ci 
(http://www.remotesensing.org/gdal/frmt_various.html#CEOS). Le pilote tentera de 
lire 15 points d'amer lat/long en échantillonnant l'information de la 
superstructure de CEOS par ligne. Il capture également divers méta-données à 
partir de divers fichiers d'en-tête, incluant :

::
    
    CEOS_LOGICAL_VOLUME_ID=EERS-1-SAR-MLD  
    CEOS_PROCESSING_FACILITY=APP         
    CEOS_PROCESSING_AGENCY=CCRS    
    CEOS_PROCESSING_COUNTRY=CANADA      
    CEOS_SOFTWARE_ID=APP 1.62    
    CEOS_ACQUISITION_TIME=19911029162818919               
    CEOS_SENSOR_CLOCK_ANGLE=  90.000
    CEOS_ELLIPSOID=IUGG_75         
    CEOS_SEMI_MAJOR=    6378.1400000
    CEOS_SEMI_MINOR=    6356.7550000

Le pilote SAR_CEOS inclut également certaines gestions pour les données 
polarimétriques SIR-C et PALSAR. Le format SIR-C contient un image sous forme de 
matrice de dispersion compressée, décrit ici 
http://southport.jpl.nasa.gov/software/dcomp/dcomp.html. GDAL décompresse la 
donnée au moment de la lecture. Le format PALSAR contient des bandes qui 
correspondent presque exactement aux éléments d'une matrice de covariance 
d'Hermitian de 3x3- Lisez le document ERSDAC-VX-CEOS-004A.pdf sur 
http://www.ersdac.or.jp/palsar/palsar_E.html pour une description complète 
(stockage des pixels est décrit à la page 193). GDAL convertit celles-ci en 
bandes de matrices de covariance de point flottant complexe au fur et à mesure 
qu'ils sont lus. La convention utilisée pour représenter la matrice de covariance 
en terme d'éléments de matrice de dispersion HH, HV (=VH) et VV est indiquée 
ci-dessous. Notez que les éléments non diagonaux de la matrice sont des valeurs 
complexes, tandis que les valeurs diagonales sont des réels (bien que représenté 
par des bandes complexes).

* Band 1 : Covariance_11 (Float32) = HH*conj(HH) 
* Band 2 : Covariance_12 (CFloat32) = sqrt(2)*HH*conj(HV) 
* Band 3 : Covariance_13 (CFloat32) = HH*conj(VV) 
* Band 4 : Covariance_22 (Float32) = 2*HV*conj(HV) 
* Band 5 : Covariance_23 (CFloat32) = sqrt(2)*HV*conj(VV) 
* Band 6 : Covariance_33 (Float32) = VV*conj(VV) 

L'identité des bandes est également reflétée dans les métas-données. 

.. note:: Implémenté dans gdal/frmts/ceos2/sar_ceosdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.ctg`:

CTG -- USGS LULC Composite Theme Grid
=======================================

(GDAL >= 1.9.0)

Ce pilote peut lire les grilles *Land Use and Land Cover* (LULC) de l'USGS encodées 
au format *Character Composite Theme Grid* (CTG). Chaque fichier est renvoyé comme 
un jeu de données à 6 bandes de type Int32. La signification de chaque bande est 
celui-ci :

1. Code d'utilisation et de couvertures des sols (*Land Use and Land Cover Code*) ;
2. Code des unités politiques (*Political units Code*) ;
3. Code des subdivisions de recensement du comté et de tracts SMSA (*Census county subdivisions and SMSA tracts Code*) ;
4. Codes des unités hydrologiques (*Hydrologic units Code*) ;
5. Code des propriétaires du sol Fédéral (*Federal land ownership Code*) ;
6. Code de propriété du sol de l'état (*State land ownership Code*) ;

Ces fichiers sont typiquement nommés grid_cell.gz, grid_cell1.gz ou grid_cell2.gz 
sur le site USGS.

* `Land Use and Land Cover Digital Data (Data Users Guide 4) <http://edc2.usgs.gov/geodata/LULC/LULCDataUsersGuide.pdf>`_ 
  - version PDF de l'USGS
* `Land Use and Land Cover Digital Data (Data Users Guide 4) <http://www.vterrain.org/Culture/LULC/Data_Users_Guide_4.html>`_ 
  - version HTML convertie par Ben Discoe ;
* `Données LULC de l'USGS à 250K et 100K <http://edcftp.cr.usgs.gov/pub/data/LULC>`_

.. note:: Implémenté dans *gdal/frmts/ctg/ctgdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.dimap`:

DIMAP -- Spot DIMAP
===================

C'est un pilote en lecture seul pour les images décrites Spot DIMAP. Pour 
l'utiliser, sélectionnez le fichier METADATA.DIM dans le répertoire du produit, 
ou le répertoire même du produit.

L'image est un fichier image distinct, souvent un fichier TIFF, mais le jeu de 
données DIMAP prend en charge l'accès à ce fichier, et attache la géolocation 
et d'autres méta-données au jeu de données à partir du fichier XML de 
méta-données.

À partir de GDAL 1.6.0, le contenu des noeuds "Spectral_Band_Info" est renvoyé 
comme méta-données au niveau de la bande raster. Notez que le contenu de 
*Spectral_Band_Info* de la première bande est encore renvoyé comme méta-données 
du jeu de données, mais cela doit être considéré comme un moyen déprécié 
d'obtenir cette information.

.. note:: implémenté dans gdal/frmts/dimap/dimapdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.saga`:

SDAT -- SAGA GIS Binary Grid File Format
=========================================

(à partir de GDAL 1.7.0)

Le pilote gère la lecture et l'écriture (dont la création, la suppression et la 
copie) de grille binaire de SAGA GIS. Les jeux de données grille binaire de SAGA 
sont faite de fichier d'en-tête ASCII (.SGRD) et de données binaires (.SDAT) avec 
un nom de fichier commun. Le fichier .SDAT doit être sélectionné pour accéder au 
jeu de données.

Le pilote gère la lecture des types de données de SAGA suivantes 
(entre parenthèse les types GDAL correspondantes) : BIT (GDT_Byte), BYTE_UNSIGNED 
(GDT_Byte), BYTE (GDT_Byte), SHORTINT_UNSIGNED (GDT_UInt16), SHORTINT (GDT_Int16), 
INTEGER_UNSIGNED (GDT_UInt32), INTEGER (GDT_Int32), FLOAT (GDT_Float32) et DOUBLE 
(GDT_Float64).

Le pilote gère l'écriture des types de données SAGA suivantes : BYTE_UNSIGNED 
(GDT_Byte), SHORTINT_UNSIGNED (GDT_UInt16), SHORTINT (GDT_Int16), INTEGER_UNSIGNED 
(GDT_UInt32), INTEGER (GDT_Int32), FLOAT (GDT_Float32) et DOUBLE (GDT_Float64).

Pour le moment le pilote ne gère pas le zFactors autre que 1 et la lecture des 
grilles SAGA qui ont été écrite TOPTOBOTTOM.

.. note:: Implémenté dans *gdal/frmts/saga/sagadataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.sdts`:

SDTS -- USGS SDTS DEM
======================

GDAL inclut la gestion de la lecture des DEM formatés en USGS SDTS. Les fichiers 
DEM de l'USGS sont toujours renvoyé avec un type de données entier de 16 bite 
non signé, ou un flottant de 32 bit. Les informations de géoréférencement et de 
projection sont aussi renvoyées.

Les jeux de données SDTS consistent en un certain nombre de fichiers. Chaque 
DEM doit avoir un fichier avec un nom comme XXXCATD.DDF. Celui-ci doit être 
sélectionné pour ouvrir le jeu de données.

Les unités d'élévation d'un DEM peuvent être les mestres ou les pieds. La méthode 
GetType() sur un bande tentera de retourner si les unités sont des peis (« ft ») 
ou des mètres (« m »). 

.. note:: implémenté dans gdal/frmts/sdts/sdtsdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.sgi`:

SGI - SGI Image Format
=======================

Le pilote SGI gère pour l'instant la lecture et l'écriture des fichiers images 
SIG.

Le pilote gère aujourd'hui les images à 1, 2, 3 et 4 bandes. Il gère les images 
de « 8 bites par canal de valeur » et les images à la fois non compressées et 
run-length encoded (RLE) en lecture, mais les fichiers créés ont toujours une 
compression RLE.

Le pilote SGI de GDAL était basé sur le code de lecture d'image SGI de Paul 
Bourke.

**Lisez également :**

* Code de lecture des images SGIS de Paul Bourke : http://astronomy.swin.edu.au/~pbourke/dataformats/sgirgb/
* Document sur le format des fichiers images SGI : ftp://ftp.sgi.com/graphics/SGIIMAGESPEC

.. note:: Implémenté dans gdal/frmts/sgi/sgidataset.cpp.

.. _`gdal.gdal.formats.divers_formats.snodas`:

SNODAS -- Snow Data Assimilation System
========================================

(À partir de GDAL >= 1.9.0)

C'est un pilote commodité pour lire les données Snow Data Assimilation System. 
Ces fichiers contiennent des données binaires brutes en Int16. Le fichier à 
fournir à GDAL est le fichier.Hdr.

`Produits de données Snow Data Assimilation System (SNODAS) à NSIDC <http://nsidc.org/data/docs/noaa/g02158_snodas_snow_cover_model/index.html>`_

.. note:: Implémenté dans *gdal/frmts/raw/snodasdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.gen`:

Standard Product Format (ASRP/USRP) (.gen)
===========================================

(à partir de GDAL 1.7.0)

Les produits ASRP et USRP (comme définie par la DGIWG) sont des variations sur 
des formats de produits standards plus comment et sont gérés en lecture par 
GDAL. Les jeux de données ASRP et USRP sont fait de plusieurs fichiers - 
typiquement de fichiers .GEN, .IMG, .SOU et .QAL avec un nom de fichier commun. 
Le fichier .GEN doit être sélectionné pour accéder au jeu de données.

Les produits ASRP (dans un système de coordonnées géographiques) et USRP (dans 
un système de coordonnées UTM/UPS) sont des images à une seule bande avec une 
palette et un géoéréferencement.

.. note:: Implémenté dans  *gdal/frmts/adrg/srpdataset.cpp*

.. _`gdal.gdal.formats.divers_formats.srtmhgt`:

SRTMHGT - SRTM HGT Format
==========================

Le pilote SRTM HGT gère aujourd'hui la lecture des fichiers SRTM-3 et SRTM-1 V2 
(HGT).

Le pilote gère la création des nouveaux fichiers, mais les données en entrée 
doivent être exactement formatées en cell SRTM-3 ou SRTM-1. C'est-à-dire que 
la taille, et les limites doivent être appropriées pour une cellule.

**Lisez également :**

* `SRTM documentation <http://dds.cr.usgs.gov/srtm/version2_1/Documentation>`_
* `SRTM FAQ 1 <http://www2.jpl.nasa.gov/srtm/faq.html>`_
* `SRTM FAQ 2 <http://dds.cr.usgs.gov/srtm/version2_1/>`_

.. note:: Implémenté dans gdal/frmts/srtmhgt/srtmhgtdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.ecrgtoc`:

ECRG Table Of Contents (TOC.xml)
=================================

(À partir de GDAL 1.9.0)

C'est un lecteur en lecture seule pour les produits ECRG (Enhanced Compressed 
Raster Graphic), qui utilise le fichier de table de contenu, TOC.xml, et l'expose 
comme jeu de données virtuel dont la couverture est l'ensemble de cadre ACRG 
contenu dans la table de contenu.

Le pilote renverra un sous jeu de données différent pour chaque sous jeu de 
données trouvés dans le fichier TOC.xml.

Résultat de la commande ``gdalinfo`` sur un fichier TOC.xml :

::
    
    Subdatasets:
    SUBDATASET_1_NAME=ECRG_TOC_ENTRY:ECRG:FalconView:ECRG_Sample/EPF/TOC.xml
    SUBDATASET_1_DESC=ECRG:FalconView

Voir également
***************

* :ref:`gdal.gdal.formats.nitf` : format des cadres ECRG ;
* `MIL-PRF-32283 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28030000+-+79999%29/MIL-PRF-32283_26022/">`_ : spécification des produits ECRG.

.. note:: Implémenté dans *gdal/frmts/nitf/ecrgtocdataset.cpp*.

.. _`gdal.gdal.formats.divers_formats.eir`:

EIR -- Erdas Imagine Raw
=========================

GDAL gère le format Erdas Imagine Raw pour l'accès en lecture incluant les 
entiers non signés 1, 2, 4, 8, 16 et 32 bit, les entiers signés 16 et 32 bit et 
les virgules flottantes complexes 32 et 64 bits. Le géoréférencement est géré.

Pour ouvrir un jeu de données, sélectionner le fichier avec les informations 
d'en-tête. Le pilote trouve le fichier image à partir des informations 
d'en-tête. Les documents Erdas appelle le fichier en-tête du fichier brut et il 
peut avoir l'extension .raw bien que le fichier image qui contient les données 
brutes réels peuvent avoir l'extension .bl.

**Note :** Implémenté dans *gdal/frmts/raw/eirdataset.cpp*

.. _`gdal.gdal.formats.divers_formats.wld`:

WLD -- ESRI World File
=======================

Un fichier world file est un fichier texte ASCII consistant à 6 valeurs séparées 
par des nouvelles lignes. Le format est :

::
    
    pixel X size
    rotation about the Y axis (usually 0.0)
    rotation about the X axis (usually 0.0)
    negative pixel Y size
    X coordinate of upper left pixel center
    Y coordinate of upper left pixel center

Par exemple : 

::
    
    60.0000000000
    0.0000000000
    0.0000000000
    -60.0000000000
    440750.0000000000
    3751290.0000000000

Vous pouvez construire ce fichier simplement en utilisant votre éditeur de 
texte favori.

Les fichiers world file habituellement ont un suffixe .wld, ou parfois .tfw, 
tifw, .jgw ou d'autres suffixes en fonction du fichier image avec lequel il est 
fournit.

.. _`gdal.gdal.formats.divers_formats.xpm`:

XPM - X11 Pixmap
=================

GDAL inclut la gestion pour la lecture et l'écriture des fichiers image XPM 
(Format Pixmap X11). Ceux-ci sont des images à une bande de cartes de couleur 
d'abord utilisé à de simples but graphiques dans les applications X11. Il a été 
incorporé dans GDAL d'abord pour faciliter la traduction des images GDAL en une 
forme utilisable avec le toolkit GTK.

La gestion du XPM ne gère pas le géoréférencement (non disponible à partir des 
fichiers XPM) ni ne gère les fichiers XPM avec plus d'un caractère par pixel. 
Les nouveaux fichiers XPM doivent avoir une carte de couleur ou être en nuance 
de gris, et les tables de couleurs seront réduites à 70 couleurs automatiquement.

.. note:: Implémenté dans gdal/frmts/xpm/xpmdataset.cpp.

.. _`gdal.gdal.formats.divers_formats.hdr`:

GenBin - Binaire Générique (étiqueté .hdr)
==========================================

Ce pilote gère la lecture des fichiers "Binaire Générique" étiquetés avec un 
fichier .hdr mais distinct du format plus commun d'ESRI étiqueté .hdr  (pilote 
EHdr). L'origine de ce format n'est pas très claire. Les fichiers .hdr gérés par 
ce pilote ressemble à cela :

::
    
    {{{
    BANDS:      1
    ROWS:    6542
    COLS:    9340
    ...
    }}}

Les types de données U8, U16, S16, F32, F64, et U1 (bit)  des pixels sont gérés. 
Le géoréférencement et les informations du système de coordonnées devraient être 
gérés lorsqu'ils sont fournis.

.. note:: Implémenté dans *gdal/frmts/raw/genbindataset.cpp*

.. _`gdal.gdal.formats.divers_formats.gff`:

GFF - Sandia National Laboratories GSAT File Format
====================================================

Le pilote GDAL en lecture seul a été pensé pour fournir un accès aux données 
traitées à partir des différents capteurs expérimentaux des Laboratoires 
Nationale de Sandia. Le format est essentiellement un en-tête de longueur 
arbitraire contenant la configuration des instruments et les paramètres de 
performances en fonction d'une matrice binaire de données complexes de 16 ou 32 
bits ou de bytes réels.

Le format GFF a été implémenté sur la base du code Matlab fourni par Sandia pour 
lire les données. Le pilote gère tous les types de données (complexe sur 16 ou 
32 bits, bytes réels) théoriquement, cependant dû à un manque de données seules 
les données complexes sur 32 bits ont été testées.

Sandia fournit des données échantillon à http://sandia.gov/RADAR/sar-data.html.

L'extension pour les formats GFF est .gff.

.. note:: Implémenté dans gdal/frmts/gff/gff_dataset.cpp.

.. _`gdal.gdal.formats.divers_formats.zmap`:

ZMap -- ZMap Plus Grid
======================

(à partir de GDAL >= 1.9.0)

Géré pour l'accès en lecture et la création.

Ce format est un format d'échange ASCII pour les données en grille dans un format 
en ligne ASCII pour le transport et le stockage. Il est communément utilisé dans 
les applications dans la champs d'Exploration Pétrolière et Gazière.

Par défaut, les fichiers sont interprétés et écrit en fonction de la convention 
PIXEL_IS_AREA. Si vous définissez l'option de configuration *ZMAP_PIXEL_IS_POINT* 
à TRUE, la convention *PIXEL_IS_POINT* sera suivie pour interpréter/écrire le 
fichier (les valeurs géoréférencées dans l'en-tête du fichier seront alors 
considérées comme les coordonnées du centre des pixels). Notez que dans ce cas, 
GDAL renverra l'étendue avec sa convention usuelle PIXEL_IS_AREA (les coordonnées 
du coin haut à gauche comme reporté par GDAL sera une moitié de pixel en haut et 
à gauche des valeurs qui apparaît dans le fichier).

Spécification informelle donnée dans le `thread de la liste de diffusion GDAL-dev 
<http://lists.osgeo.org/pipermail/gdal-dev/2011-June/029173.html>`_

.. note:: Implémenté dans *gdal/frmts/zmap/zmapdataset.cpp*.

.. yjacolin at free.fr, Yves Jacolin - 2011/09/04 (trunk 22861)
