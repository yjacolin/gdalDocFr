.. _`gdal.gdal.formats.ers`:

=====================
ERS -- ERMapper .ERS
=====================

GDAL gère la lecture et l'écriture de fichiers raster avec des fichiers 
d'en-têtes .ers avec certaines limitations. Le format ascii .ers est utilisé 
par ERMapper pour étiqueter les fichiers de données brutes ainsi que fournir 
des méta-données étendues et un géoréférencement pour certains autres fichiers. 
Le format .ERS et ses variantes sont également utilisés pour contenir les 
descriptions d'algorithmes d'ERMapper mais ceux-ci ne sont pas gérés par GDAL.

.. versionadded:: 1.9.0 les valeurs PROJ, DATUM et UNITS trouvées dans l'en-tête 
   ERS sont reportées dans le domaine méta-données ERS.

Problèmes de création
======================

**Options de création :**

* **PIXELTYPE=value :** en définissant cela à SIGNEDBYTE, un nouveau fichier Byte peut être forcé comme byte signé
* **PROJ=name :** (GDAL >= 1.9.0) Nom de la chaîne de projection ERS à utiliser. Example commun sont NUTM11 ou GEODETIC. 
  Si définie, cela écrasera la valeur calculée par SetProjection() ou SetGCPs().
* **DATUM=name :** (GDAL >= 1.9.0) Nom de la chaîne de datum de ERS à utiliser.
  Des exemples typiques sont WGS84 ou NAD83. Si définie, cela écrasera la valeur calculée par SetProjection() ou SetGCPs().
* **UNITS=name :** (GDAL >= 1.9.0) Nom des unités de projection ERS à utilisere :
  METERS (par défaut) ou FEET (pied US). Si définie, cela écrasera la valeur calculée par SetProjection() ou SetGCPs().

.. seealso::

* Implémenté dans *gdal/frmts/ers/ersdataset.cpp*.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (trunk 23028)

