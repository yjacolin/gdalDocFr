.. _`gdal.gdal.formats.isis3`:

ISIS3 -- USGS Astrogeology ISIS Cube (Version 3)
==================================================

ISIS3 est un format utilisé par le groupe Planetary Cartography de l'USGS pour 
stocker et distribuer des images planétaire. GDAL fournie un accès en lecture 
seule aux données images formaté en ISIS3.

Les fichiers ISIS3 ont souvent une extensions .cub, parfois avec un fichier .lbl 
(label) associé. Quand un fichier .lbl existe il doit être utilisé comme le nom 
du jeu de données plutôt que celui du fichier .cub.

En plus de la gestion pour la plupart des configurations d'images de ISIS3, ce 
pilote lit également les informations du système de coordonnées et de 
géoréférencement ainsi que d'autres métadonnées d'en-tête sélectionné.

L'implémentation de ce pilote a été financé par la *Geological Survey* des 
États-Unis.

ISIS3 fait partie de la famille des formats PDS et ISIS2.

Voir également
---------------

* Implémenté dans *gdal/frmts/pds/isis2dataset.cpp*.
* :ref:`gdal.gdal.formats.pds`
* :ref:`gdal.gdal.formats.isis2`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/18 (trunk 21710)