.. _`gdal.gdal.formats.pds`:

=====================================
PDS -- Système de données planétaire
=====================================

PDS est un format utilisé d'abord par la NASA pour stocker et distribuer des 
données images planétaire, lunaire et solaire. GDAL fournie un accès en lecture 
seul aux données d'imagerie formaté en PDS.

Les fichiers PDS ont souvent l'extension .img, parfois avec un fichier .lbl (label) 
associé. Quand un fichier .lbl file existe il doit être utilisé comme nom de jeu 
de données plutôt que celui du fichier .img.

En plus de la gestion de la plupart des configuration d'image PDS, ce pilote lit 
également les informations du système de coordonnées et de géoréférencement ainsi 
que d'autres métadonnées d'en-tête.

L'implémentation de ce pilote a été financé par la Surveillance Géologique des 
États-Unis.

En raison des ambiguïtés dans la spécification du PDS, le géoréférencement de 
certains produits est subtilement ou grossièrement incorrect. Il y a des variables 
de configuration qui peuvent être définies pour ces produits afin de corriger 
l'interprétation du géoréférencement. Certains détails sont disponibles dans le
`ticket #3940 <http://trac.osgeo.org/gdal/ticket/3940>`_.

PDS fait partie de la famille des formats incluant ISIS2 et ISIS3.

.. seealso::

  * Implémentéd dans *gdal/frmts/pds/pdsdataset.cpp*.
  * `Système de données planétaire de la NASA <http://pds.nasa.gov/>`_
  * :ref:`gdal.gdal.formats.isis2`
  * :ref:`gdal.gdal.formats.isis3`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/17 (trunk 22516)