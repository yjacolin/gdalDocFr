.. _`gdal.gdal.formats.isis2`:

============================================================
ISIS2 -- Cube ISIS de l'astrogéologie de l'USGS (Version 2)
============================================================

ISIS2 est un format utilisé par le groupe Planetary Cartography de l'USGS pour 
stocker et distribuer des images planétaire. GDAL fournie un accès en lecture 
seule aux données images formaté en ISIS2.

Les fichiers ISIS2 ont souvent une extensions .cub, parfois avec un fichier .lbl 
(label) associé. Quand un fichier .lbl existe il doit être utilisé comme le nom 
du jeu de données plutôt que celui du fichier .cub.

En plus de la gestion pour la plupart des configurations d'images de ISIS2, ce 
pilote lit également les informations du système de coordonnées et de 
géoréférencement ainsi que d'autres métadonnées d'en-tête sélectionné.

L'implémentation de ce pilote a été financé par la *Geological Survey* des 
États-Unis.

ISIS2 fait partie de la famille des formats PDS et ISIS3.

Problèmes de création
======================

Pour le moment le pilote ISIS2 écrit un en-tête très minimal avec seulement les 
informations de structure de l'image. Aucun système de coordonnées, de géoréférencement 
ou d'autres métadonnées n'est capturé.

Options de création
*******************

* **LABELING_METHOD=ATTACHED/DETACHED :** Détermine si l'en-tête des étiquettes 
  doivent être dans le même fichier que l'image (ATTACHED par défaut) ou dans un 
  fichier séparé (DETACHED).
* **IMAGE_EXTENSION=extension :** définie l'extension utilisée pour les fichiers 
  images détachés, "cub" par défaut.  Utilisé seulement si LABELING_METHOD=DETACHED.

.. seealso::

* Implémenté dans *gdal/frmts/pds/isis2dataset.cpp*.
* :ref:`gdal.gdal.formats.pds`
* :ref:`gdal.gdal.formats.isis2`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/19 (trunk 21710)