.. _`gdal.gdal.formats.ilwis`:

ILWIS -- Raster Map
=====================

Ce pilote implémente la lecture et l'écriture des cartes raster ILWIS et les 
listes des cartes. Sélectionnez les fichiers raster avec les extensions *.mpr* 
(pour les cartes raster) ou *.mpl* (pour les listes de cartes).

Fonctionnalités :
------------------
 
* Gère les types de données de pixel en octet, Int16, Int32 et Float64.
* Gère les listes de carte avec les ensembles de cartes raster ILWIS associés.
* Lit et écrit le géoréférencement (.grf). Gestion des transformations de 
  géoréférencement est limitée seulement au GeoRefCorner orienté Nord. Si 
  possible, la transformation affine est calculée à partir des coordonnées des 
  coins.
* Lit et écrit les fichiers de coordonnées (.csy). La gestion est limitée au : 
  type de projection de la projection et au type Lat/Lon qui sont définis dans 
  le fichier .csy, le reste des types de projection pré-définie est ignoré.

Limitations :
-------------
 
* Les listes de cartes avec le stockage des cartes raster internes (tels que 
  ceux produits par Import General Raster) ne sont pas gérées.
* Les fichiers de domaine ILWIS (.dom) et de représentation (.rpr) sont 
  actuellement ignorés.

Note : Implémenté dans *gdal/frmts/ilwis*.

**Voir également :**

* `http://www.itc.nl/ilwis/default.asp <http://www.itc.nl/ilwis/default.asp>`_.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 13616)