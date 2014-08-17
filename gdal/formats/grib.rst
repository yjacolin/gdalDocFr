.. _`gdal.gdal.formats.grib`:

============================================================================
GRIB -- WMO General Regularly-distributed Information sous la forme Binaire
============================================================================

GDAL gère la lecture des données raster des formats GRIB1 et GRIB2, avec un 
embryon de gestion pour le système de coordonnées, le géoréférencement et les 
autres méta-données. Le format GRIB est communément utilisé pour la distribution 
d'information météorologique, et est diffusé par l'Organisation Météorologique 
Mondiale.

Le pilote GRIB de GDAL est basé sur une version modifiée de l'application degrib 
qui a été écrite par Arthur Taylor du NOAA NWS NDFD (MDL). L'application degrib 
(et le pilote GRIB de GDAL) est compilé avec la bibliothèque de décodage de grib 
g2clib écrit initialement par John Huddleston du NOAA NWS NCEP.

Il y a plusieurs schémas d'encodage pour les données raster au format GRIB. La 
plupart devrait être géré en incluant l'encodage PNG. Les fichiers GRIB encodés 
en JPEG2000 sont généralement géré si GDAL est également compilé avec la gestion 
du JPEG2000 par un des pilotes JPGE2000 de GDAL. La bibliothèque JasPer 
généralement fournie la meilleure gestion du jpeg2000 pour le pilote GRIB.

Les fichiers GRIB peuvent être représenté dans GDAL comme ayant plusieurs bandes, 
avec un ensemble de bande représentant une séquence temps. Les bandes GRIB sont 
représentées en Float64 (virgule flottante à double précision) sans regard de 
leur valeurs réelles. Les méta-données GRIB sont capturés par bande de 
méta-données et utilisé pour définir des descriptions de bandes, similaire à 
ceci :

::
    
    Description = 100000[Pa] ISBL="Isobaric surface"
        GRIB_UNIT=[gpm]
        GRIB_COMMENT=Geopotential height [gpm]
        GRIB_ELEMENT=HGT
        GRIB_SHORT_NAME=100000-ISBL
        GRIB_REF_TIME=  1201100400 sec UTC
        GRIB_VALID_TIME=  1201104000 sec UTC
        GRIB_FORECAST_SECONDS=3600 sec

Les fichiers GRIB2 peuvent également inclure un extrait du numéro de modèle de 
définition du produit (octet 8-9), et les valeurs du modèle de définition du 
produit (> à 10 octets) sous forme de métadonnées comme ceci :

::
    
    GRIB_PDS_PDTN=0
    GRIB_PDS_TEMPLATE_NUMBERS=3 5 2 0 105 0 0 0 1 0 0 0 1 100 0 0 1 134 160 255 0 0 0 0 0

Options de configuration
=========================

Ce paragraphe liste les options de configuration qui peuvent être définie pour modifier 
le comportement par défaut du pilote GRIB.

* **GRIB_NORMALIZE_UNITS :** (GDAL >= 1.9.0) Peut être définie à NO pour éviter gdal de normaliser à métric.

Problèmes connus
================

La bibliothèque que GDAL utilise pour lire les fichiers GRIB est connu pour ne pas 
être thread-safe vous devez donc éviter de lire et écrite plusieurs jeux de 
données GRIB au même moment à partir de thread différents.

.. seealso::

  * `Décodeur GRIB2 de "degrib" NOAA NWS NDFD <http://www.weather.gov/mdl/NDFD_GRIB2Decoder/>`_
  * `Bibliothèque de décodage de grib par g2clib NOAA NWS NCEP <http://www.nco.ncep.noaa.gov/pmb/codes/GRIB2/>`_
  * `Documents sur le format GRIB WMS <http://www.wmo.int/pages/prog/www/WMOCodes/GRIB.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (trunk 23235)
