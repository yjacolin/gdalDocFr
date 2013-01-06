.. fichier dans le répertoire "raw"

.. _`gdal.gdal.formats.mff2`:

===========================
MFF2 -- Vexcel MFF2 Image
===========================

GDAL gère le format de fichier raster Image MFF2 en lecture, mise à jour et 
création. Le format MFF2 (Multi-File Format 2) a été définie pour s'ajuster 
dans les bases de données Vexcel Hierarchical Key-Value (HKV), qui peut stocker 
des données binaires ainsi que des paramètres ASCII. Ce format est d'abord 
utilisé en interne dans le système de traitement Vexcel Insar.

Pour sélectionner un jeu de données MFF2, sélectionnez le répertoire contenant 
les fichiers *attrib*, et *image_data* du jeu de données.

Pour l'instant seulement la latitude/longitude et la projection UTM sont gérés 
(georef.projection.name = ll ou georef.projection.name = utm), par 
transformation affine calculée à partir des points d'amer en lat/long. Pour 
n'importe quelle action, si les points d'amer sont disponibles dans un fichier 
de géoreférencement , ceux-ci sont renvoyés avec le jeu de données.
Les fichiers nouvellement crées (avec un type de MFF2) sont toujours des raster 
brutes sans information de géoréférencement. pour la lecture et la création, 
tous les types de données (réel, entier, et complexe avec une profondeur en bit 
de 8, 16, 32) devraient être gérés.

.. warning::
    Lors de la création d'un nouveau fichier MFF2, assurez-vous de définir la 
    projection avant de définir la transformation spatiale (cela est nécessaire 
    parce que la transformation spatiales est stockée en interne sous forme de 
    5 points d'amer au sol en latitude/longitude et la projection est nécessaire 
    à la conversion).


.. note:: implémenté dans gdal/frmts/raw/hkvdataset.cpp.

Détails du format
==================

Structure générale du MFF2
***************************

Un « fichier » MFF2 est en réalité un ensemble de fichiers stockés dans un 
répertoire contenant un fichier d'en-tête ASCII nommé « attrib » et des données 
d'image binaire nommé « image_data ».En option, il peut y avoir un fichier 
« georef » ASCII contenant des informations de projection et de 
géoréférencement, et un fichier « image_data_ovr » (pour les données image 
binaire « image_data ») contenant les aperçus tuilés de l'image au format TIFF. 
Les fichiers ASCII sont arrangés sous forme de pairs clé=valeur. Les pairs 
autorisées pour chaque fichier sont décrites ci-dessous.

Le fichier "attrib"
********************

Au minimum, le fichier « attrib » doit contenir l'étendue de l'image, la taille 
en pixel en octets, l'encodage des pixels et le type des données, et l'ordre 
des octets. Par exemple :

::
    
    extent.cols    = 800
    extent.rows    = 1040
    pixel.size     = 32
    pixel.encoding = { unsigned twos_complement *ieee_754 }
    pixel.field    = { *real complex }
    pixel.order    = { lsbf *msbf }
    version        = 1.1

définie une image de 1040 lignes et 800 pixels pour l'étendue. Les pixels sont 
des entiers de 32 bits dont l'ordre est « l'octet le plus significatif en 
premier » (msbf), encodé selon la spécification ieee_754. Dans un MFF2, 
lorsqu'une valeur appartient à un certain sous-ensemble (par exemple pixel.order 
doit être soit lsbf ou msbf) toutes les options sont affichées entre crochets, 
et celui approprié pour le fichier en cours est indiqué par une « * ».

Le fichier peut aussi contenir  les lignes suivantes indiquant le nombre de 
canaux de données, et comment ils sont entrelacés à l'intérieur du fichier de 
données binaire.

::
    
    channel.enumeration = 1
    channel.interleave = { *pixel tile sequential }

Le fichier "image_data"
***********************

Le fichier « image_data » est constitué de données binaire brute avec une 
étendue, l'encodage du pixel, et le nombre de canaux comme indiqué dans le 
fichier « attrib ».

Le fichier "georef"
*******************

Le fichier « georef » est utilisé pour décrire des informations de géocodage et 
de projection pour les données binaires. Par exemple,

::
    
    top_left.latitude            = 32.93333333333334
    top_left.longitude           = 130.0
    top_right.latitude           = 32.93333333333334
    top_right.longitude          = 130.5
    bottom_left.latitude         = 32.50000000000001
    bottom_left.longitude        = 130.0
    bottom_right.latitude        = 32.50000000000001
    bottom_right.longitude       = 130.5
    centre.latitude              = 32.71666666666668
    centre.longitude             = 130.25
    projection.origin_longitude  = 0
    projection.name              = ll
    spheroid.name                = wgs-84*

décrit un image projetée en latitude/longitude (ll) orthogonale, avec les 
latitudes et longitudes basé sur l'ellipsoïde wgs-84.
Depuis la version 1.1 de MFF2, top_left renvoie au coin en haut à gauche du 
pixel en haut à gauche. top_right renvoie au coin en haut à droite du pixel en 
haut à droite. bottom_left renvoie au coin en bas à gauche du pixel en bas à 
gauche. bottom_right renvoie au coin en bas à droite du pixel en bas à droite. 
centre renvoie au centre des quatre coins définie plus haut (le centre de l'image).

Mathématiquement, pour une image Npix par Nline, les coins et le centre sous 
forme de coordonnées (pixel,line) pour la version 1.1 de MFF2 sont :
::
    
    top_left: (0,0)
    top_right: (Npix,0)
    bottom_left: (0,Nline)
    bottom_right: (Npix,Nline)
    centre: (Npix/2.0,Nline/2.0)

Ces calculs sont réalisé en virgule flottante (c'est à dire que les coordonnées 
du centre peuvent prendre des valeurs non entières).

Remarquez que les coins sont toujours exprimé en latitude/longitude, même pour 
les images projetées.

Projection gérées
******************

image projetée latitude/longitude Orthogonal -ll, avec les latitudes parallèles 
aux lignes et les longitudes parallèles aux colonnes. Paramètres : nom du 
sphéroïde, projection, longitude d'origine (longitude à l'origine des coordonnées 
de la projection). Si non définie, la valeur est par défaut la longitude central 
de l'image en sortie basée sur ces limites de projection.

Image projeté en Universal Transverse Mercator – utm. Paramètres : nom du 
sphéroïde, projection origine de la projection (méridien central pour la 
projection utm). Le méridien centrale doit être le méridien au centre de la zone 
UTM, par exemple 3 degré, 9 degré,  12 degré, etc. Si cela n'est pas définie ou 
définie à un méridien central UTM valide, le lecteur doit annuler la valeur au 
méridien central valide le plus proche basé sur la longitude centrale de l'image 
en sortie. La latitude à l'origine, de la projection UTM est toujours de 0 degré.

Ellipsoïdes reconnus
*********************

Le format MFF2 associe les noms suivants avec les paramètres du rayon à 
l'équateur et le coefficient à l'aplatissement de l'ellipsoïde :

::
    
    airy-18304:            6377563.396      299.3249646
    modified-airy4:        6377340.189      299.3249646
    australian-national4:  6378160          298.25
    bessel-1841-namibia4:  6377483.865      299.1528128
    bessel-18414:          6377397.155      299.1528128
    clarke-18584:          6378294.0        294.297
    clarke-18664:          6378206.4        294.9786982
    clarke-18804:          6378249.145      293.465
    everest-india-18304:   6377276.345      300.8017
    everest-sabah-sarawak4:6377298.556      300.8017
    everest-india-19564:   6377301.243      300.8017
    everest-malaysia-19694:6377295.664      300.8017
    everest-malay-sing4:   6377304.063      300.8017
    everest-pakistan4:     6377309.613      300.8017
    modified-fisher-19604: 6378155          298.3
    helmert-19064:         6378200          298.3
    hough-19604:           6378270          297
    hughes4:               6378273.0        298.279
    indonesian-1974:       6378160          298.247
    international-1924:    6378388          297
    iugc-67:               6378160.0        298.254
    iugc-75:               6378140.0        298.25298
    krassovsky-1940:       6378245          298.3
    kaula:                 6378165.0        292.308
    grs-80:                6378137          298.257222101
    south-american-1969:   6378160          298.25
    wgs-72:                6378135          298.26
    wgs-84:                6378137          298.257223563
    ev-wgs-84:             6378137          298.252841
    ev-bessel:             6377397          299.1976073


Explication des champs
***********************

* **channel.enumeration :**  (optionnelle seulement nécessaire pour les 
  multibandes) Nombre de canaux dedonnées (par exemple 3 pour rgb)
* **channel.interleave = { \*pixel tile sequential } :** (optionnelle seulement 
  nécessaire pour les multibandes)
  Pour des données multibandes, indique comment les canaux sont entrelacés. \*pixel 
  indique des les données sont stockés en valeur de rouge, vert, bleu, rouge, vert, 
  bleu etc. par opposition à (ligne de valeurs rouge) (ligne de valeur de vert) 
  (ligne de valeur de bleu) ou (canal complet de rouge) (canal complet de vert) 
  (canal complet de bleu)
* **extent.cols :** nombre de colonne de données.
* **extent.rows :** nombre de ligne de données.
* **pixel.encoding = { *unsigned twos-complement ieee-754 } :** combiné avec 
  pixel.size et pixel.field pour donner le type de données :
  
  ::
    
    (encoding, field, size)- type
    (unsigned, real, 8)- unsigned byte data
    (unsigned, real, 16)- unsigned int 16 data
    (unsigned, real, 32)- unsigned int 32 data
    (twos-complement, real, 16)- signed int 16 data
    (twos-complement, real, 32)- signed int 32 data
    (twos-complement, complex, 64)- complex signed int 32 data
    (ieee-754, real, 32)- real 32 bit floating point data
    (ieee-754, real, 64)- real 64 bit floating point data
    (ieee-754, complex, 64)- complex 32 bit floating point data
    (ieee-754, complex, 128)- complex 64 bit floating point data

* **pixel.size :** taille d'un pixel d'un canal (bits).
* **pixel.field = { \*real complex } :** si la données est réelle ou complexe.
* **pixel.order = { \*lsbf msbf } :** ordonnancement des bytes des données 
  (least ou most significant byte first).
* **version :** (seulement dans les versions récentes – si non présent, une 
  version plus vielle est présumé) Version de mff2.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/16 22:19 (trunk 8933)