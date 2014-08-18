.. _`gdal.gdal.formats.gta`:

============================
GTA - Generic Tagged Arrays
============================

.. versionadded:: 1.9.0 GDAL peut lire et écrire des fichiers de données GTA 
   via la bibliothèque libgta.

GTA est un format de fichier qui peut stocker n'importe quel sorte de données 
tabulaire multidimensionnel, permettant des manipulations génériques de tableau 
de données ainsi que la conversion vers et à partir d'autres formats de 
fichiers.

**Options de création :**

* **COMPRESS=method :** Définie la méthode de compression GTA : NONE (par 
  défaut) ou une parmi BZIP2, XZ, ZLIB, ZLIB1, ZLIB2, ZLIB3, ZLIB4, ZLIB5, 
  ZLIB6, ZLIB7, ZLIB8, ZLIB9.

.. seealso::

  * `Page principale de GTA <http://gta.nongnu.org/>`_


.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (Trunk r23475)

