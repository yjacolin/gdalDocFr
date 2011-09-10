.. _`gdal.gdal.formats.r`:

=========================
R -- R Object Data Store
=========================

Le format de fichier des objets R est pris en charge pour un accès en écriture, 
et un accès limité en lecture par GDAL. Ce format est le format natif que R 
utilise pour les objets sauvegardés avec la commande *save* et chargés commande 
*load*. GDAL gère l'écriture un jeu de données comme objet de tableau dans ce 
format, et supporte la lecture des fichiers avec les rasters simples 
essentiellement dans la même organisation. Il ne lira pas la plupart des 
fichiers objet R.

Pour le moment il n'y a pas de gestion de lecture et d'écriture d'informations 
géoréférencement.

Options de création
====================

* **ASCII=YES/NO :** produit un fichier formaté en ASCII, au lieu du binaire, si 
  définie à YES. NO par défaut.
* **COMPRESS=YES/NO :** Produit un fichier compressé si YES, autrement un fichier 
  non compressé. YES par défaut.

Voir également
===============

* `Project R <http://www.r-project.org/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/19 (trunk 17835)