.. _`gdal.gdal.formats.rmf`:

=============================
RMF --- Raster Matrix Format
=============================

RMF est un format simple raster tuilé utilisé dans les SIG "Integration" et 
"Panorama". Le format lui-même a très peu de possibilité.

Il y a deux types de RMF appelé MTW et RSW. MTW gère les données entières 16 
bites et les points flottant 32/64 bites dans un seul canal et a pour objectif 
de stocké les données MNT. RSW est un raster avec un objectif plus général, il 
gère un canal simple avec une carte de couleur ou trois canaux d'image RVB. Seul 
les données 8 bits peuvent être rangé dans un RSW. Un géoréférencement simple 
peut être fournit pour les deux types d'image.

Méta-données
===============

* **ELEVATION_MINIMUM :** valeur d'élévation minimum (seulement MTW).
* **ELEVATION_MAXIMUM :** valeur d'élévation maximum (seulement MTW).
* **ELEVATION_UNITS :** nom de l'unité pour les valeurs raster (seulement 
  MTW). Peut être "m" (mètres), "cm" (centimètres), "dm" (décimètres), "mm" 
  (millimètres).
* **ELEVATION_TYPE :** peut être soit (élévation absolue) soit 1 (élévation 
  totale). Seulement MTW.

Options création
=================

* **MTW=ON :** force la génération de matrice MTW (RSW sera crée par défaut).
* **BLOCKXSIZE=n :** définie la largeur de la tuile, par défaut, définie à 256.
* **BLOCKYSIZE=n :** définie la hauteur de la tuile, par défaut, définie à 256.

**Lisez également :**

* Implémenté dans *gdal/frmts/rmf/rmfdataset.cpp*.
* Page principale de "Panorama" GIS : http://www.gisinfo.ru/index_en.htm

.. yjacolin at free.fr, Yves Jacolin -2009/03/09 21:46 (trunk 15709)