.. _`gdal.gdal.formats.jpegls`:

========
JPEGLS
========

.. versionadded:: 1.8.0

Ce pilote est une implémentation d'un lecteur/écriture de JPEG-LS basé sur la 
bibliothèque Open Source CharLS (Licence style BSD).
Au moment de la rédaction, la bibliothèque CharLS dans sa version 1.0 n'a pas de 
cible "``make install``". Par conséquence, l'intégration du pilote dans le système 
de compilation de GDAL est un peu rude. Sur Unix, vous devez éditer le fichier 
*GDALmake.opt* et éditer les lignes liées à CHARLS.

Le pilote peut lire et écrire des images sans perte ou proche du sans perte. Notez 
qu'il ne vise pas à traiter des images trop grandes (sauf si virtual memory est 
disponible), puisque l'ensemble de l'image doit être compressé/décompressé en 
une seule opération.

Options de création
====================

* **INTERLEAVE=PIXEL/LINE/BAND :** entrelacement des données en flux compressé. 
  BAND par défaut.
* **LOSS_FACTOR=error_threshold :** 0 (la valeur par défaut) signifie une compression 
  sans perte. N'importe quelle valeur plus haute sera la limite maximale pour 
  l'erreur.

.. seealso::

  * Implémenté dans *gdal/frmts/jpegls/jpeglsdataset.cpp*.
  * `Page principale de la bibliothèque CharLS <http://charls.codeplex.com/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 21192)