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
lorsqu'il s'agit de grandes images.

Le pilote WEBP ne gère que 3 bandes (RGB) d'images.

Le pilote WEBP peut être utilisé comme format interne utilisé par le pilote 
:ref:`gdal.gdal.formats.rasterlite`.

Options de création
====================

* **QUALITY=n** par défaut l'option *quality* est définie à 75, mais cette option 
  peut être utilisé pour sélectionner d'autres valeurs. Les valeurs doivent être 
  comprises entre 1 et 100. Les valeurs faibles résultent en un plus grand taux 
  de compression, mais une moins bonne qualité d'image.

.. seealso::

* `Home page WebP <http://code.google.com/intl/fr/speed/webp/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/19 (trunk 22043)