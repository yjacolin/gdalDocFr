.. _`gdal.gdal.formats.webp`:

============
WEBP - WEBP
============

À partir de GDAL 1.9.0, GDAL peut lire et écrire des images WebP via la bibliothèque 
WebP.

WebP est un nouveau format d'image qui fournit une compression sans perte pour 
les images photographiques. Un fichier WebP consiste de données image VP8 et 
d'un conteneur basé sur RIFF.

Le pilote repose sur la bibliothèque Open Source WebP (licence BSD). La 
bibliothèque WebP (du moins dans sa version 0.1) ne propose que la compression et 
la décompression des images complètes, La RAM peut donc  être une limitation
lorsqu'il s'agit de grandes images (qui sont limitées à 16383x16383 pixels).

Le pilote WEBP gère 3 bandes (RGB) d'images. Il gère également 4 bandes (RVBA) 
à partir de GDAL 1.10 et libwebp 0.1.4.

Le pilote WEBP peut être utilisé comme format interne utilisé par le pilote 
:ref:`gdal.gdal.formats.rasterlite`.

.. versionadded:: 1.10 Les métadonnées XMP peuvent être extraites du fichier 
   et seront stockées comme contenu brute XML dans le domaine de métadonnées 
   xml:XMP.

Options de création
====================

* **QUALITY=n :** par défaut l'option *quality* est définie à 75, mais cette option 
  peut être utilisé pour sélectionner d'autres valeurs. Les valeurs doivent être 
  comprises entre 1 et 100. Les valeurs faibles résultent en un plus grand taux 
  de compression, mais une moins bonne qualité d'image.
* **LOSSLESS=True/False (GDAL >= 1.10.0 et libwebp >= 0.1.4) :** Par défaut une 
  compression avec perte est utilisé. Si définie à *True* une compression sans 
  perte sera utilisée.

.. seealso::

  * `Home page WebP <https://developers.google.com/speed/webp/>`_

.. yjacolin at free.fr, Yves Jacolin - 2014/03/08 (trunk 27021)
