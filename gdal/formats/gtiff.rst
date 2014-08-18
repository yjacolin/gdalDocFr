.. _`gdal.gdal.formats.gtiff`:

================
Le format Gtiff
================

La plupart des formes de fichiers TIFF et GeoTIFF sont supportés par GDAL en 
lecture, et certaines variétés peuvent être écrite.
Lorsque GDAL est compilé avec la version interne de la librairie libtiff, ou 
avec une version de libtiff >= 4.0, GDAL gère également la lecture et l'écriture 
de fichiers BigTIFF (évolution du format TIFF pour gérer des fichiers de taille 
supérieure à 4 GO).

Les types de bandes en Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, 
CInt16, CInt32, CFloat32 et CFloat64 sont supportées en lecture et en écriture. 
Les images avec une palette retourneront des informations sur la palette 
associée à la bande. Les formats de compression listés ci-dessous devrait être 
également supportés en lecture.

De plus, les fichiers de un bite et certains formulations inhabituelles de 
fichier GeoTIFF, tels que les fichiers avec un modèle de couleur YCbCr, seront 
automatiquement transformé sous la forme RVBA (Rouge, Vert, Bleu, Alpha), et 
traité comme quatre bandes de huit bites.

Géo-référencement
==================

La plupart des projections devrait être supportées, avec le signalement que, 
dans le but de traduire un système de projection non commune et de coordonnées 
Géographique en OGC WKT, il est nécessaire d'avoir les fichiers csv EPSG 
disponible. Ils doivent être trouvés à l'endroit pointé par la variable 
d'environnement GEOTIFF_CSV.

Le géo-référencement à partir d'un GéoTIFF est supporté sous la forme d'un 
« point » et d'une taille de pixel, une matrice de transformation ou une liste 
de points d'amer.

Si aucune information de géo-référencement n'est disponible dans le fichier 
TIFF en lui-même, GDAL cherchera un fichier world d'ESRI avec l'extension .tfw, 
.tiffw ou .wld, ou également comme un fichier .tab de MapInfo (seul les points 
d'amer sont utilisé, les Coordsys seront ignorés).

GDAL peut lire et écrire le *RPCCoefficientTag* comme décrit dans l'extension 
proposée `RPCs in GeoTIFF <http://geotiff.maptools.org/rpc_prop.html>`_. La balise 
est écrite seulement pour les fichiers créés avec le profile par défaut 
GDALGeoTIFF. Pour les autres profiles, un fichier .RPB est créé. Dans le modèle 
de données de GDAL, les coefficients RPC sont stockés dans le domaine de 
métadonnée RPC. Pour plus de détails, voir la `RFC de géoréférencement RPC 
<http://trac.osgeo.org/gdal/wiki/rfc22_rpc>`_. Si des fichiers .RPB ou _RPC.TXT 
sont trouvés, ils seront utilisés pour lire les RPCs, même si la balise 
*RPCCoefficientTag* est définie.

.. _`gdal.gdal.formats.gtiff.internal_mask`:

Masques de transparence interne
=================================
.. versionadded:: 1.6.0

Les fichiers TIFF peuvent contenir des masques de transparence internes. Le 
pilote GeoTIFF reconnait un répertoire interne comme étant un masque de 
transparence lorsque le bite FILETYPE_MASK est positionné sur l'attribut 
TIFFTAG_SUBFILETYPE. Selon la spécification TIFF, de tels masques de 
transparence internes contiennent des données échantillonnées à 1 bite. Bien que 
la spécification TIFF autorise des résolutions plus grandes les masques de 
transparence, le pilote GeoTIFF ne gère que ceux qui ont la même dimension que 
l'image principale. Des masques de transparence internes sont également gérés.

.. versionadded:: 1.6.0 lorsque la variable d'environnement 
  *GDAL_TIFF_INTERNAL_MASK*  est positionnée à YES, et que le fichier GeoTIFF est 
  ouvert en mode mise à jour, la méthode *CreateMaskBand()* appelée sur un fichier 
  TIFF ou une de ses bandes créera un masque de transparence interne. Sinon, le 
  comportement par défaut des masques de transparence sera utilisé, c'est-à-dire 
  la création d'un fichier .msk, comme indiqué dans la `RFC 15 <http://rac.osgeo.org/gdal/wiki/rfc15_nodatabitmask>`_

.. versionadded:: 1.8.0 une bande de masque interne d'1-bit sont décompressé. Lors 
  de la relecture, pour réaliser la conversion entre la bande de masque et la 
  bande alpha plus facilement, les bandes de masque sont exposées à l'utilisateur 
  tout en étant promus en 8 bits (i.e. la valeur pour les pixels non masqués est 
  de 255) à moins que l'option de configuration *GDAL_TIFF_INTERNAL_MASK_TO_8BIT* 
  est définie à NO. Cela n'affecte pas la manière dont la bande de masque est écrite 
  (c'est toujours 1-bit).

.. _`gdal.gdal.formats.gtiff.apercues`:

Aperçus
===========

Le pilote GeoTIFF gère la lecture, la création et la mise à jour d'aperçus 
internes. Ceux-ci peuvent être créés sur des fichiers GeoTIFF ouverts en mode 
mise à jour (avec gdaladdo par exemple). Si le fichier GeoTIFF est ouvert en 
lecture seule, la création d'aperçus sera faite dans un fichier externe .ovr. 
Les aperçus sont mise à jour uniquement sur requête par appel à la méthode 
*BuildOverviews()*.

Si un fichier GeoTIFF possède un masque de transparence et que la variable 
d'environnement GDAL_TIFF_INTERNAL_MASK est positionnée à YES et que le fichier 
est ouvert en mode  mise à jour, *BuildOverviews()** créera automatiquement des 
aperçus pour le masque de transparence interne. Ces aperçus seront rafraichis 
par des appels ultérieurs à *BuildOverviews()*, même si *GDAL_TIFF_INTERNAL_MASK* 
n'est pas positionnée à YES.

.. versionadded:: 1.8.0 La taille du bloc (hauteur et largeur de la tuile) 
  utilisée pour les aperçues (interne ou externe) peut être définie en définissant 
  la variable d'environnement*GDAL_TIFF_OVR_BLOCKSIZE* à une puissance de deux 
  entre 64 et 4096. 128 est la valeur par défaut.

Métadonnées
============

GDAL peut faire face aux balises baseline  du TIFF comme métadonnées au niveau du 
jeu de données :

* TIFFTAG_DOCUMENTNAME
* TIFFTAG_IMAGEDESCRIPTION
* TIFFTAG_SOFTWARE
* TIFFTAG_DATETIME
* TIFFTAG_ARTIST
* TIFFTAG_HOSTCOMPUTER
* TIFFTAG_COPYRIGHT
* TIFFTAG_XRESOLUTION
* TIFFTAG_YRESOLUTION
* TIFFTAG_RESOLUTIONUNIT
* TIFFTAG_MINSAMPLEVALUE (lecture seule)
* TIFFTAG_MAXSAMPLEVALUE (lecture seule)

Le nom de l'item de métadonnées est l'un des noms ci-dessus  ("TIFFTAG_DOCUMENTNAME", ...).

Les autres items de métadonnées non standard peuvent être stockés dans un fichier 
TIFF créé avec le profile GDALGeoTIFF (par défaut, voir plus bas dans la 
section :ref:`gdal.gdal.formats.gtiff.issues`). Ces items de métadonnées sont 
groupés ensemble dans une chaîne XML stockés dans la balise ASCII non standard 
*TIFFTAG_GDAL_METADATA/* (code 42112). Quand le profile BASELINE ou GeoTIFF sont 
utilisé, ces items de métadonnées non standard sont stockés dans un fichier PAM 
.aux.xml.

La valeur de l'item de métadonnées *GDALMD_AREA_OR_POINT* ("AREA_OR_POINT") est 
stockée dans la clé GeoTIFF *RasterPixelIsPoint* pour les profiles *GDALGeoTIFF* 
ou *GeoTIFF*.

.. versionadded:: 1.90 les métadonnées XMP peuvent être extraites à partir du 
   fichier et seront stockées dans un contenu brute XML dans le domaine de 
   métadonnées xml:XMP.

.. versionadded:: 1.10 les métadonnées EXIF peuvent être extrait du fichier et 
   seront stockées dans le domaine métadonnées EXIF.

Valeur nodata
===============

GDAL stocke la valeur nodata de la bande dans la balise ASCII non standard 
*TIFFTAG_GDAL_NODATA* (code 42113) pour les fichiers créés avec le profile par 
défaut *GDALGeoTIFF*. Notez que toutes les bandes doivent avoir la même valeur 
nodata. Quand le profile BASELINE ou GeoTIFF sont utilisé, la valeur nodata est 
stockée dans le fichier PAM .aux.xml file.

.. _`gdal.gdal.formats.gtiff.issues`:

Problèmes de création
======================

Les fichiers GeoTIFF peuvent être créés avec n'importe quel type de bande 
définie dans GDAL, les types complexes inclus. Les fichiers créés peuvent avoir 
n'importe quel nombre de bandes. Les fichiers avec exactement trois bandes 
donneront une interprétation photométrique de RVB, les fichiers avec exactement 
quatre bandes donneront une interprétation photométrique de RVBA, tandis que 
toutes les autres combinaisons donneront une interprétation photométrique de 
MIN_IS_WHITE. Les fichiers avec des tables de pseudo-couleur, ou des points 
d'amer peuvent, pour l'instant, seulement être créés lors d'une création à 
partir d'un ensemble de données GDAL avec ces objets (*GDALDriver:CreateCopy()*).

.. note::
    Notez que le format GeoTIFF ne gère pas la description paramétrique des datums, 
    donc les paramètres *TOWGS84* dans les systèmes de coordonnées sont perdu 
    dans le format GeoTIFF.

Options de création
********************

* **TFW=YES :** Force la génération d'un fichier associé world d'ESRI (.tfw). 
  Lisez la section les fichiers world pour plus de détails.
* **INTERLEAVE=[BAND,PIXEL] :** Par défaut les fichiers TIFF avec des pixels 
  entrelacées (PLANARCONFIG_CONTIG dans la terminologie TIFF) sont créés. 
  Ceux-ci sont sensiblement moins efficace que les bandes séparées pour certaines 
  choses, mais certaines applications supporte seulement les fichiers TIFF avec 
  des pixels entrelacés.
* **TILED=YES :** Par défaut des fichiers TIFF « strip » sont créés (NdT : des 
  fichiers « nus », sans tuilage par exemple). Cette option peut être utilisé 
  pour forcer la création de fichiers TIFF tuilés.
* **BLOCKXSIZE=n :** définit la largeur de la tuile, par défaut à 256.
* **BLOCKYSIZE=n :** définit la hauteur de la tuile ou du « strip » [Set tile 
  or strip height]. La hauteur de la tuile est de 256 par défaut, la hauteur 
  du « strip » est par défaut à une valeur de 8K ou inférieure.
* **NBITS=n :** Crée un fichier avec moins de 8 bites par échantillon, en 
  passant une valeur de 1 à 7. Le type du pixel doit être l'octet (Byte). À 
  partir de 1.6.0, les valeurs de n=9...15 (type UInt16) et n=17...31 (type 
  UInt32) sont également accepté.
* **COMPRESS=[JPEG/LZW/PACKBITS/DEFLATE/CCITTRLE/CCITTFAX3/CCITTFAX4/NONE] :** 
  définit la compression à utiliser. JPEG doit seulement être utilisé avec des 
  données en octet (8 bit par canal). Mais à partir de GDAL 1.7.0 et en supposant 
  que GDAL a été compilé avec les bibliothèques internes libtiff et libjpeg, il 
  est possible de lire et écrite les fichiers TIFF avec des fichiers TIFF 
  compressé en JPEG 12 bit (vue comme des bandes UInt16 avec NBITS=12). Voir la 
  page wiki `"8 et 12 bit JPEG dans les TIFF" <http://trac.osgeo.org/gdal/wiki/TIFF12BitJPEG>`_ 
  pour plus de détails. La compression CCITT doit être uniquement utilisée avec 
  des données à 1 bite (NBITS=1). La valeur par défaut est aucune compression (NONE).
* **PREDICTOR=[1/2/3] :** définit la [predictory] pour la compression LZW ou 
  DEFLATE. La valeur par défaut est de 1 (pas de prédiction), 2 est la 
  prédiction par différence horizontale et 3 par point flottant. [Set the 
  predictor for LZW or DEFLATE compression. The default is 1 (no predictor), 
  2 is horizontal differencing and 3 is floating point prediction.]
* **SPARSE_OK=TRUE/FALSE :** (à partir de GDAL 1.6.0) est ce que les fichiers 
  nouvellement créés doivent ils être autorisés à être *sparsé* ? Les fichiers 
  *sparsés* ont 0 tuiles/strip de distance pour les blocs jamais écrit et sauver 
  de l'espace ; cependant, la plupart des paquets hors GDAL ne peuvent pas lire 
  de tels fichiers. *FALSE* par défaut.
* **JPEG_QUALITY=[1-100] :** définit la qualité JPEG lors de l'utilisation de 
  la compression JPEG. Une valeur de 100 est la meilleur qualité (faible 
  compression) et 1 est la moins bonne qualité (meilleure compression). Par 
  défaut la valeur est à 75.
* **ZLEVEL=[1-9]  :** définit le niveau de compression à utiliser avec la 
  compression DEFLATE. Une valeur de 9 correspond à la compression la plus 
  forte, 1 à la plus faible. La valeur par défaut est de 6.
* **PROFILE=[GDALGeoTIFF/GeoTIFF/BASELINE] :** contrôle quelles balises 
  inhabituelles sont émises par GDAL. 

  * Avec GDALGeoTIFF (la valeur par défaut) plusieurs balises GDAL 
    personnalisées peuvent être écrites. 
  * Avec GeoTIFF seulement des balises GeoTIFF seront ajoutés à celle 
    habituelles. 
  * Avec BASELINE aucune balises GDAL ou GeoTIFF sera écrites. BASELINE est 
    parfois utile lors de l'écriture de fichier qui seront lu par des 
    applications intolérante aux balises non reconnues.

* **PHOTOMETRIC=[MINISBLACK/MINISWHITE/RGB/CMYK/YCBCR/CIELAB/ICCLAB/ITULAB] :** 
  définit la balise d'interprétation photométrique. Par défaut la valeur est à 
  MINISBLACK, mais si l'image en entrée possède trois ou quatre bandes de type 
  Octet, alors RGB sera utilisé. Vous pouvez écraser la valeur par défaut en 
  utilisant cette option.
* **ALPHA=[YES/NON-PREMULTIPLIED/PREMULTIPLIED/UNSPECIFIED] :** Le premier 
  "extrasample" est noté comme étant alpha s'il existe 
  un extra samples. Cela est nécessaire si vous désirez produire un fichier 
  TIFF en nuance de gris avec une bande alpha (par exemple).
  Pour GDAL <1.10 seula la valeur YES est géré et il est interprété comme 
  *alpha PREMULTIPLIED* (ASSOCALPHA dans TIFF). À partir de GDAL 1.10, YES est 
  un alias pour *alpha NON-PREMULTIPLIED* et les autres valeurs peuvent être 
  utilisées.
* **BIGTIFF=YES/NO/IF_NEEDED/IF_SAFER :** Contrôle si le fichier créé est un 
  fichier BigTIFF ou un TIFF classique. 

  * *YES* force le format BigTIFF. 
  * *NO* force le format TIFF classique.
  * *IF_NEEDED* créera seulement BigTIFF si cela est clairement nécessaire (non 
    compressé, et des images plus grande que 4 Go).
  * *IF_SAFER* créera un BigTIFF si le fichier résultant *pourrait* excédé 4 Go. 

  BigTIFF est une variante du TIFF qui peut contenir plus de 4 Go de données (la 
  taille des TIFF classique est limité à cette valeur). L'option est disponible si 
  GDAL a été complié avec la bibliothèque libtiff 4.0 ou supérieure (ce qui est le 
  cas de la version interne de libtiff à partir de GDAL >= 1.5.0). *IF_NEEDED* par 
  défaut (*IF_NEEDED* et *IF_SAFER* sont disponible à partir de GDAL 1.6.0) 
 
  Lors de la création d'un nouveau GeoTIFF avec aucune compression, GDAL calcul en 
  avance la taille du fichier résultant. Si la taille calculée de ce fichier est 
  supérieur à 4 Go, GDAL décidera automatiquement un fichier BigTIFF. Cependant, 
  quand la compression est utilisée, il n'est pas possible de connaitre à l'avance 
  la taille du fichier, un fichier classique sera alors choisit. Dans ce cas, 
  l'utilisateur doit explicitement choisir la création d'un bigTIFF avec l'option 
  BIGTIFF=YES s'il a anticipé la taille finale du fichier. Si l'option BigTIFF n'a 
  pas été explicitement demandée ou supposée et que le fichier résultant est trop 
  gros pour le fichier classique TIFF, libtiff échouera avec un message d'erreur 
  comme "TIFFAppendToStrip:Maximum TIFF file size exceeded".

* **PIXELTYPE=[DEFAULT/SIGNEDBYTE] :** en définissant ce paramètre à SIGNEDBYTE, 
  un nouveau fichier d'octet peut être écrit en force comme octet signé.
* **COPY_SRC_OVERVIEWS=[YES/NO] :** (GDAL >= 1.8.0, CreateCopy() seulement) en 
  définissant ce paramètre à YES (NO par défaut), les aperçues potentiellement 
  existantes du jeu de données source seront copiées vers le jeu de données cible 
  sans retraitement. Si les aperçues de la bande de masque existe aussi, en 
  supposant que l'option de configuration*GDAL_TIFF_INTERNAL_MASK* est définie à 
  YES, elles seront aussi copiées. Notez que cette option de création n'aura 
  `aucun effet <http://trac.osgeo.org/gdal/ticket/3917>`_ si les options générales 
  (i.e. options qui ne sont pas des options de création) de gdal_translate sont 
  utilisées.

À propos de la compression d'images RVB au format JPEG
=======================================================

Lorsqu'on convertit une image RVB dans le format JPEG-dans-TIFF, utilisez 
PHOTOMETRIC=YCBCR peut rendre le fichier résultant typiquement de 2 à 3 fois 
plus petits que la valeur photométrique par défaut (RGB). Quand on utilise 
PHOTOMETRIC=YCBCR, l'option INTERLEAVE doit être laissée à sa valeur par défaut 
(PIXEL), sinon libtiff échouera lors de la compression des données.
Prenez note également que les dimensions des tuiles ou des "strips" doivent être 
un multiple de 8 pour PHOTOMETRIC=RGB ou 16 pour PHOTOMETRIC=YCBCR

Options de configuration
*************************

Ce paragraphe liste les options de configuration qui peuvent être définie pour 
modifier le comportement par défaut du pilote GTiff.


.. <!-- debug/autotest option : GTIFF_DONT_WRITE_BLOCKS -->
* **GTIFF_IGNORE_READ_ERRORS :** (GDAL >= 1.9.0) peut être définie à TRUE pour 
  éviter de renvoyer les erreurs libtiff vers les erreurs GDAL.
  Can help reading partially corrupted TIFF files
* **ESRI_XML_PAM :** peut être définie à TRUE pour forcer l'écriture des 
  métadonnées vers le PAM dans le domaine xml:ESRI.
* **JPEG_QUALITY_OVERVIEW :** entier entre 0 et 100. Valeur par défaut : 75. 
  Qualité des aperçues compressées en JPEG, soit en interne soit en externe.
* **GDAL_TIFF_INTERNAL_MASK :** Voir la section :ref:`gdal.gdal.formats.gtiff.internal_mask`. 
  Valeur par défaut : FALSE.
* **GDAL_TIFF_INTERNAL_MASK_TO_8BIT :** Voir la section 
  :ref:`gdal.gdal.formats.gtiff.internal_mask`. Valeur par défaut : TRUE
* **USE_RRD :** peut être définie à TRUE pour forcer les aperçues externes dans 
  le format RRD. Valeur par défaut : FALSE
* **TIFF_USE_OVR :** peut être définie à TRUE pour forcer les aperçues externes 
  dans le format GeoTIFF (.ovr). Valeur par défaut : FALSE
* **GTIFF_POINT_GEO_IGNORE :** peut être définie à TRUE pour revenir au 
  comportement de GDAL < 1.8.0 pour la manière dont les pixels sont interprétés 
  par rapport à la géotransformation. Voir 
  `RFC 33: GTiff - Fixing PixelIsPoint Interpretation <http://trac.osgeo.org/gdal/wiki/rfc33_gtiff_pixelispoint>`_
  pour plus de  détails. Valeur par défaut : FALSE.
* **GTIFF_REPORT_COMPD_CS :** (GDAL >= 1.9.0). peut être définie à TRUE pour 
  éviter de modifier la verticale du CS dans un composant CS. Valeur par défaut 
  : FALSE
* **GDAL_ENABLE_TIFF_SPLIT :** peut être définie à FALSE pour éviter que des 
  fichiers d'une seule bande soient présentée comme en ayant plusieurs. Valeur 
  par défaut : TRUE
..  <!-- debug option : <li>GDAL_TIFF_ENDIANNESS : Possible values : LITTLE, BIG, INVERTED, NATIVE. Default value : NATIVE -->
..  <!-- not sure it is wise to advertize this one. I doubt it works correctly if set to NO. CONVERT_YCBCR_TO_RGB -->
..  <!-- debug/autotest option : GTIFF_DELETE_ON_ERROR -->
* **GDAL_TIFF_OVR_BLOCKSIZE :** Voir la section :ref:`gdal.gdal.formats.gtiff.apercues`.
* **GTIFF_LINEAR_UNITS :** peut être définie en BROKEN pour lire les fichiers 
  GeoTIFF qui ont un easting/northing improprement définie en mètre lorsqu'ils 
  doivent être en unité linéaire du système de coordonnées. 
  (`Ticket #3901 <http://trac.osgeo.org/gdal/ticket/3901>`_).

.. seealso::

  * Page d'information sur GeoTIFF : http://www.remotesensing.org/geotiff/geotiff.html
  * Page libtiff : http://www.remotesensing.org/geotiff/geotiff.html
  * Détails du format de fichier BigTIFF : http://www.awaresystems.be/imaging/tiff/bigtiff.html

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (trunk 25411)
