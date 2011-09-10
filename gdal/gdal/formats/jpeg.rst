.. _`gdal.gdal.formats.jpeg`:

=============================
JPEG -- JPEG JFIF File Format
=============================

Le format JPEG JFIF est géré en lecture et écriture batch, mais ne met pas à 
jour. Les fichiers JPEG sont représentés comme des jeux de données d'une bande 
(nuance de gris) ou de trois bandes (RVB) avec des bandes de valeurs en byte.

Le pilote convertira automatiquement les images dont l'espace de couleur est 
YCbCr, CMYK ou YCbCrK vers RVB à moins que l'option *GDAL_JPEG_TO_RGB* est 
définie à *NO* (*YES* par défaut). Lorsque la traduction de l'espace de 
couleur vers RVB est réalisée, l'espace de couleur source est indiquée dans les 
méta-données *SOURCE_COLOR_SPACE* du domaine *IMAGE_STRUCTURE*.

Il n'y a actuellement aucune gestion pour les informations de géo-référencement 
ou des méta-données pour les fichiers JPEG. Mais si un fichier world ESRI existe 
avec l'extension .jgw, .jpgw/.jpegw ou .wld comme suffixes, il sera lu et 
utilisé pour établir la géo-transformation pour l'image. S'il est disponible un 
fichier MapInfo .tab sera également utilisé pour le géoréférencement. Les 
aperçues peuvent être construit pour les fichiers JPEG dans un fichier .ovr 
externe.

Le pilote gère également l'approche "ajout au fichier du masque compressé zlib" 
utilisé par quelques fournisseurs de données pour ajouter un masque pour 
identifier les pixels qui ne sont pas des données valides. Voir 
`RFC 15 <http://trac.osgeo.org/gdal/wiki/rfc15_nodatabitmask>`_ pour plus de détails.

Le pilote JPEG de GDAL est compilé en utilisant la bibliothèque jpeg du *Groupe 
JPEG indépendant*. Notez également que le pilote GeoTIFF gère les TIFF tuilés 
avec des tuiles compressées en JPEG.

Pour lire et écrire des images JPEG avec des échantillons de 12 bits, vous pouvez 
compiler GDAL avec la bibliothèque libjpeg interne (basé sur IJG libjpeg-6b, avec 
des modifications supplémentaires pour la gestion de l'échantillon 12-bit), ou 
passer explicitement *--with-jpeg12=yes* au script configure lors de la compilation 
externe de libjpeg. Voir la page wiki 
`"8 and 12 bit JPEG in TIFF" <http://trac.osgeo.org/gdal/wiki/TIFF12BitJPEG>`_ 
pour plus de détails.

Il est également possible d'utiliser le pilote JPEG avec libjpeg-turbo, une 
version de libjpeg, compatible API et ABI avec IJG libjpeg-6b, qui utilise les 
instructions MMX, SSE et SSE2 SIMD pour accélérer la compression/décompression 
du JPEG baseline.

À partir de GDAL 1.9.0, les métadonnées XMP peuvent être extraite des fichiers, 
et seront stockées comme contenu brute XML dans le domaine de métadonnées 
xml:XMP.

Options de création
====================

Les fichiers JPEG sont crée en utilisant le code du pilote « JPEG ». Seules les 
types de bande en byte sont gérés, et seulement les configurations 1 et 3 bandes 
(RGB). La création des fichiers JPEG est implémentée par la méthode batch 
(CreateCopy). Les espaces de couleurs YCbCr, CMYK ou YCbCrK ne sont pas gérés 
en création. Si le jeu de données source possède un masque nodata, il sera 
ajouté comme un masque compressé en zlib au fichier JPEG :

* **WORLDFILE=YES :** Force la génération d'un fichier world ESRI associé 
  (avec l'extension .wld). 
* **QUALITY=n :** Par défaut l'option qualité est défini à 75, mais cette 
  option peut être utilisée pour définir une autre valeur. La valeur doit être 
  compris entre 10 et 100. De faibles valeurs entraînent une plus grand taux de 
  compression, mais une qualité d'image moins bonne. Les valeurs au-dessus de 95 
  ne sont pas significativement de meilleur qualité mais peuvent être 
  substantiellement plus importante.
* **PROGRESSIVE=ON :** Active la génération de jpeg progressif. Dans certain 
  cas cela affichera une image d'une résolution réduite dans un visualiseur tel 
  que Netscape et Internet Explorer, avant que le fichier entier ne soit 
  téléchargé. Cependant, certaines applications ne peuvent  pas lire les jpeg 
  progressive du tout. GDAL peut lire les jpeg progressifs, mais n'utilise pas 
  l'avantage de leur nature progressive.

Voir également
---------------

* Indépendant JPEG Group : http://www.ijg.org/
* `libjpeg-turbo <http://sourceforge.net/projects/libjpeg-turbo/>`_
* :ref:`gdal.gdal.formats.gtiff`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08(trunk 22678)