.. _`gdal.gdal.formats.ers`:

ERS -- ERMapper .ERS
=====================

GDAL gère la lecture et l'écriture de fichiers raster avec des fichiers 
d'en-têtes .ers avec certaines limitations. Le format ascii .ers est utilisé 
par ERMapper pour étiqueter les fichiers de données brutes ainsi que fournir 
des méta-données étendues et un géoréférencement pour certains autres fichiers. 
Le format .ERS et ses variantes sont également utilisés pour contenir les 
descriptions d'algorithmes d'ERMapper mais ceux-ci ne sont pas gérés par GDAL.

**Voir également :**

* Implémenté dans *gdal/frmts/ers/ersdataset.cpp*.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/27 20:12 (trunk 14382)