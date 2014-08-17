.. _`gdal.gdal.formats.ingr`:

==================================
INGR --- Intergraph Raster Format
==================================

Le format est géré en lecture et écriture.

Le format de fichier Raster d'Intergraph était le format de fichier natif 
utilisé par les applications logicielles d'Intergraphe pour stocker les données 
raster. Il se manifeste dans plusieurs formats de données internes.


Lecture des fichiers INGR
============================

Ceci sont les formats de données que le pilote INGR gère en lecture :

* 2 - Entier en Byte
* 3 - Word Integer
* 4 - 32 bit entiers
* 5 - Point à virgule flottante 32 bit
* 6 - Point à virgule flottante 64 bit
* 9 - Run Length Encoded
* 10 - Run Length Encoded Color
* 24 - CCITT Group 4
* 27 - RVB adaptif
* 28 - 24 bit non compressé
* 29 - Nuance de gris adaptif
* 30 - JPEG GRIS
* 31 - JPEG RVB
* 32 - JPEG CYMK
* 65 - Tuilé
* 67 - Ton continu

Le format "65 - Tuilé" n'est pas un format ; c'est juste une indication que le 
fichier est tuilé. Dans ce cas l'en-tête des tuiles contient le véritable code 
de format des données qui peut être n'importe quel code cité au-dessus. Le 
pilote INGR peut lire les instances tuilés et non tuilés de n'importe quels 
formats de données gérés.

Écrire des fichiers INGR
==========================

Ceci est la liste des formats que le pilote INGR gère en écriture :

* 2 - Byte Integer
* 3 - Word Integers
* 4 - Integers 32Bit
* 5 - Floating Point 32Bit
* 6 - Floating Point 64Bit

Notez que l'écriture dans ce format n'est pas encouragé !

Extension de fichier
=====================

Ce qui suit est une partie de la liste des extensions de fichier INGR :

+------+--------------------------------------------------------------------------------+
+ .cot + données 8-bit nuance de couleur ou table de couleur                            +
+------+--------------------------------------------------------------------------------+
+ .ctc + 8-bit nuance de couleur utilisant une compression PackBits-type (pas commun)   +
+------+--------------------------------------------------------------------------------+
+ .rgb + 24-bit couleur et nuance de gris (non compressé et compression PackBits-type)  +
+------+--------------------------------------------------------------------------------+
+ .ctb + données 8-bit table de couleur (non compressé ou encodé en run-length)         +
+------+--------------------------------------------------------------------------------+
+ .grd + données 8, 16 et 32 bit élévation                                              +
+------+--------------------------------------------------------------------------------+
+ .crl + données 8 ou 16 bit, run-length compressé nuance de gris ou table de couleur   +
+------+--------------------------------------------------------------------------------+
+ .tpe + données 8 ou 16 bit, run-length compressé nuance de gris ou table de couleur   +
+------+--------------------------------------------------------------------------------+
+ .lsr + données 8 ou 16 bit, run-length compressé nuance de gris ou table de couleur   +
+------+--------------------------------------------------------------------------------+
+ .rle + données 1-bit run-length compressé (16-bit runs)                               +
+------+--------------------------------------------------------------------------------+
+ .cit + données CCITT G3 ou G4 1-bit                                                   +
+------+--------------------------------------------------------------------------------+
+ .g3  + données CCITT G3 1-bit                                                         +
+------+--------------------------------------------------------------------------------+
+ .g4  + données CCITT G4 1-bit                                                         +
+------+--------------------------------------------------------------------------------+
+ .tg4 + données CCITT G4 1-bit (tuilé)                                                 +
+------+--------------------------------------------------------------------------------+
+ .cmp + JPEG nuance de gris, RGB, ou CMYK                                              +
+------+--------------------------------------------------------------------------------+
+ .jpg + JPEG nuance de gris, RGB, ou CMYK                                              +
+------+--------------------------------------------------------------------------------+

*Source* : http://www.oreilly.com/www/centers/gff/formats/ingr/index.htm

Le pilote INGR ne nécessite pas une extension de fichier spécifique dans le but 
d'identifier ou de créer un fichier INGR.


Géoréférencement
==================

Le pilote INGR ne gère pas la lecture ou l'écriture d'information géoréférencée. 
La raison est qu'il n'y a pas de manières universelle de stocker le 
géoréférencement dans les fichiers INGR. Il est possible d'avoir des données 
géoréférencées stocké dans un fichier .dgn d'accompagnement ou dans le stockage 
des données spécifiques à l'application dans le fichier lui même.

.. seealso::

Pour plus d'information :

* Implémenté dans *gdal/frmts/ingr/intergraphraster.cpp*.
* www.intergraph.com
* http://www.oreilly.com/www/centers/gff/formats/ingr/index.htm
* Fichier des spécifications : ftp://ftp.intergraph.com/pub/bbs/scan/note/rffrgps.zip/

.. yjacolin at free.fr, Yves Jacolin - 2008/04/05 18:09 (trunk 12129)