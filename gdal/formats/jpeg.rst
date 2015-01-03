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

.. versionadded:: 1.10.1, le pilote prend en charge le bitmask où les bites sont 
   ordonées avec le bit le plus signifiquant en premier (tandis que la convention 
   usuel est le moins signifiquant en premier). Le pilote tentera de détecter 
   automatiquement cette situation, mais les heuristiques peuvent échouer. Dans 
   ce cas là, vous pouvez définir l'option de configuration *JPEG_MASK_BIT_ORDER* 
   à *MSB*. Le bitmask peut également être complètement ignoré en spécifiant 
   *JPEG_READ_MASK* à *NO*.

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

.. versionadded:: 1.9.0 les métadonnées XMP peuvent être extraite des fichiers, 
  et seront stockées comme contenu brute XML dans le domaine de métadonnées 
  xml:XMP.

.. versionadded:: 2.0, les vignettes EXIF inclus (avec compression JPEG) peuvent 
   être utilisé comme aperçues et générées par GDAL.

Métadonnes de profile de couleur
================================

.. versionadded:: 1.11, GDAL prend en charge les métadonnées de profile de couleur 
   suivant dans le domaine *COLOR_PROFILE* :

* SOURCE_ICC_PROFILE (profile ICC encodé en Base64 inclus dans le fichier.)

Notez que cette propriété de métadonnées peut seulement être utilisé sur les données 
pixels brutes. Si une conversion automatique versr RVB a été réalisée, l'information 
de profile de couleur ne peut pas être utilisé.

Cet élément de métadonnées peut être utilisé comme options de création.

Gestion des erreurs
====================

Lors du décodage, la bibliothèque libjpeg a une certaine résilience lors d'erreurs 
dans le flux de données JPEG et essayera de les récupérer autant que possible. 
À partir de GDAL 1.11.2, ces erreurs seront rapportés comme alertes GDAL, mais 
peuvent optionnellement être considérés comme de véritables erreurs en 
définissant l'option de configuration *GDAL_ERROR_ON_LIBJPEG_WARNING* à *TRUE*.

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
* **INTERNAL_MASK=YES/NO :** Par défaut, si nécessaire, un masque interne dans 
  l'approche "masque compressé en zlib ajouté au fichier" est écrit pour 
  identifier les pixels qui ne sont pas des données valides. À partir de GDAL 
  1.10, cela peut être désactivé en définissant cette option à *NO*.
* **ARITHMETIC=YES/NO :** (À partir de GDAL 1.10) Pour activer l'encodage 
  arithmétique. Pas activé dans toutes les compilations de libjpeg à cause 
  de potentielles restrictions légales.
* **BLOCK=1...16 :** (À partir de  GDAL 1.10 and libjpeg 8c) Taille des blocs 
  DCT. Toutes les valeurs de 1 à 16 sont possible. 8 par défaut (format ligne 
  de base). Une valeur autre que 8 produira des fichiers incompatible avec 
  les versions inférieures à 8c de libjpeg.
* **COLOR_TRANSFORM=RGB or RGB1 :** (À partir de GDAL 1.10 et libjpeg 9). 
  Définie à RGB1 pour les RVB sans perte. Note : cela produira des fichiers 
  incompatible avec les versions inférieures à 9 de libjpeg.
* **SOURCE_ICC_PROFILE=value :** (à partir de GDAL 1.11). Profile ICC encodé en 
  Base64.
* **COMMENT=string :** (à partir de GDAL 2.0). Chaîne à inclure dans un marqueur 
  de commentaire JPEG. Lors de la lecture, de telles chaînes sont exposées dans 
  l'élément COMMENT de métadonnées.
* **EXIF_THUMBNAIL=YES/NO :** (à partir de GDAL 2.0). Pour générer une vignette 
  (aperçu) EXIF, lui-même compressé en JPEG. Défaut à NO. Si activé, la 
  dimension maximale de la vignette sera de 128, si ni *THUMBNAIL_WIDTH* ou 
  *THUMBNAIL_HEIGHT* ne sont définie.
* **THUMBNAIL_WIDTH=n :** (à partir de GDAL 2.0). Largeur de la vignette. Seulement 
  pris en considération si *EXIF_THUMBNAIL=YES*.
* **THUMBNAIL_HEIGHT=n :** (à partir de GDAL 2.0). Hauteur de la vignette. Seulement 
  pris en considération si *EXIF_THUMBNAIL=YES*.

.. seealso::

  * Indépendant JPEG Group : http://www.ijg.org/
  * `libjpeg-turbo <http://sourceforge.net/projects/libjpeg-turbo/>`_
  * :ref:`gdal.gdal.formats.gtiff`

.. yjacolin at free.fr, Yves Jacolin - 2014/12/30 (trunk 28270)