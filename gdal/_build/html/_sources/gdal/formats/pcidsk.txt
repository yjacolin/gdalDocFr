.. _`gdal.gdal.formats.pcidsk`:

=======================================
PCIDSK --- PCI Geomatics Database File
=======================================

Fichiers de base de données PCIDSK utilisé par les logiciels PCI EASI/PACE pour 
l'analyse d'image. Il est géré en lecture et écriture par GDAL. Tous les types 
de données de pixel, et d'organisation des donnés (pixel entrelacé, bande 
entrelacée, fichier entrelacé et tuile) doivent être gérés.

Pour l'instant, les segments LUT et PCT sont ignorés, mais les segments PCT 
doivent être traité comme associé avec les bandes. Les fichiers d'ensemble et 
les méta-données spécifique aux bandes doivent être correctement associés avec 
l'image ou les bandes.

Le géoréférencement est géré bien qu'il peut y avoir certaines limitations dans 
la gestion des *datums* et des ellipsoïdes. Les segments des points d'amer 
sont ignorés. les segments RPC seront renvoyés comme métadonnées RPC dans le style 
de GDAL 

Les aperçues internes d'images (pyramide) seront également lu correctement bien 
que les nouveaux aperçues demandés seront construit en externe comme un fichier 
.ovr.

Les segments vectoriels sont géré par le pilote OGR PCIDSK.

Options de création
====================

Notez que les fichiers PCIDSK ont toujours produit des pixels entrelacés, même 
si d'autres organisations sont géré en lecture.

* **INTERLEAVING=PIXEL/BAND/FILE/TILED :** définie l'entrelacement pour les données 
  des fichiers raster.
* **COMPRESSION=NONE/RLE/JPEG :** définie la compression à utiliser. Les valeurs 
  autre que NONE (celle par défaut) peut être seulement utilisé avec l'entrelacement TILED.
  Si JPEG est sélectionné il peut inclure une valeur de qualité comprise entre 1 
  et 100 - par exemple COMPRESSION=JPEG40.
* **TILESIZE=n :** quand INTERLEAVING est TILED, la taille des tuiles peut être 
  sélectionné avec ce paramètre - par défaut 127 pour 127x127.

Lisez également
================

* Implémenté dans *gdal/frmts/pcidsk/pcidskdataset2.cpp*.
* `SDK PCIDSK <http://home.gdal.org/projects/pcidsk/index.html>`_.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/15 (trunk 7688)