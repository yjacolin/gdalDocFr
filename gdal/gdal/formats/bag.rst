.. _`gdal.gdal.formats.bag`:

===================================
BAG --- Bathymetry Attributed Grid
===================================

Ce pilote permet la gestion en lecture seule des données bathymétriques au format 
BAG. Les fichiers BAG sont en fait un profile d'un produit spécifique dans un 
fichier HDF5, mais un pilote personnalisé existe pour présenter les données dans 
une manière plus pratique que celle disponible via le pilote HDF5 générique.

Les fichiers BAG ont deux ou trois bandes d'images représentant les valeurs de 
l'élévation (bande 1), l'incertitude (bande 2) et l'élévation nominale (bande 3) 
pour chaque cellule dans une zone en grille raster.

La transformation géographique et le système de coordonnées sont extraits des 
métadonnées XML interne fournie par le jeu de données. Cependant, certain produits 
peuvent avoir des formats du système de données non gérés.

Le XML complet de métadonnées est disponible dans le domaine de métadonnées 
"xml:BAG".

Les valeurs Nodata, minimum et maximum pour chaque bande sont également fournies.

.. seealso::

* Implémenté dans *gdal/frmts/hdf5/bagdataset.cpp*.
* Le projet Open Navigation Surface <http://www.opennavsurf.org>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/09/04 (trunk 22975)