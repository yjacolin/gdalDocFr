.. _`gdal.gdal.formats.jp2openjpeg`:

==================================================================
JP2OpenJPEG --- pilote JPEG2000 basé sur la bibliothèque OpenJPEG
==================================================================

.. versionadded::

Ce pilote est une implémentation d'un lecteur/écriture  de JPEG2000 basé sur la 
bibliothèque OpenJPEG **v2**.

Pour GDAL 1.10 ou supérieure, utilisez openjpeg 2.0.

Pour GDAL 1.9.x ou inférieure, utilisez la branche v2 à partir du dépôt 
Subversion : http://openjpeg.googlecode.com/svn/branches/v2 (avant la révision 
2230 lorsqu'elle a été supprimée). 

Le pilote utilise l'API VSI Virtual File, il peut donc lire les fichiers NITF 
compressés en JPEG2000.

.. versionadded:: 1.9.0 les métadonnées XMP peuvent être extraites des fichiers 
  JPEG2000, et seront stockées comme contenu brute XML dans le domaine de métadonnées 
  xml:XMP.

À partir de GDAL 1.10, le pilote gère l'écriture des informations de géoréférencment 
comme boites GeoJP2 ou GMLJP2.

Options de création
====================

* **CODEC=JP2/J2K :** JP2 ajoutera des boîtes JP2 autour des données codestream. 
  La valeur est déterminé automatiquement à partir de l'extension du fichier. Si 
  c'est ni JP2 ou J2K, le codec J2K sera utilisé.
* **GMLJP2=YES/NO :** (à partir de GDAL 1.10) Indique si une boîte GML conforme 
  au GML de l'OGC dans les spécification JPEG2000 doit être incluse dans le 
  fichier. YES par défaut.
* **GeoJP2=YES/NO :** (à partir de GDAL 1.10) Indique si une boîte UUID/GeoTIFF
  conforme aux spécification GeoJP2 (GeoTIFF dans JPEG2000) doit être inclus 
  dans le fichier. YES par défaut.
* **QUALITY :** pourcentage entre 0 et 100. Une valeur de 50 signifie que le fichier 
  sera de moité de taille en comparaison aux données non compressées, 33 signifie 
  1/3, etc.. 25 par défaut.
* **REVERSIBLE=YES/NO :** YES signifie compression sans perte. No par défaut.
* **RESOLUTIONS :** Nombre de niveaux de résolution. Entre 1 et 7. 6 par défaut.
* **BLOCKXSIZE :** largeur de la tuile . 1024 par défaut.
* **BLOCKYSIZE :** hauteur de la tuile. 1024 par défaut.
* **PROGRESSION :** ordre de progression : LRCP, RLCP, RPCL, PCRL ou CPRL. LRCP par défaut.
* **SOP=YES/NO :** YES signifie générer des segments marqueur SOP. No par défaut.
* **EPH=YES/NO :** YES signifie générer des segments marqueur EPH. No par défaut.
* **YCBCR420=YES/NO :** (GDAL >= 1.11) YES si RVB doit être reéchantilloné en 
  YCbCr 4:2:0. Défauts à *NO*.
* **YCC=YES/NO :** (GDAL >= 2.0) YES si l' espace de couleur RVB doit être 
  transformé en YCC. Défauts à *YES*.

Compression sans perte
************************

La compression sans perte peut être réalisée si **toutes** les options de 
création suivantes sont définies :

* QUALITY=100
* REVERSIBLE=YES
* YCBCR420=NO (ce qui est la valeur par défaut)

.. seealso::

  * Implémenté dans *gdal/frmts/openjpeg/openjpegdataset.cpp*.
  * `Page official du JPEG-2000 <http://www.jpeg.org/JPEG2000.html>`_
  * `La page de la bibliothèque OpenJPEG <http://code.google.com/p/openjpeg/>`_

Autres pilotes JPEG2000 pour GDAL :

* :ref:`gdal.gdal.formats.jpeg2000` (open source)
* :ref:`gdal.gdal.formats.jp2ecw` (propriétaire)
* :ref:`gdal.gdal.formats.jp2mrsid` (propriétaire)
* :ref:`gdal.gdal.formats.jp2kak` (propriétaire)

.. yjacolin at free.fr, Yves Jacolin - 2014/09/03 (trunk 27631)