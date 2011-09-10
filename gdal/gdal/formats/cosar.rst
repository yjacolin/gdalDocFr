.. _`gdal.gdal.formats.cosar`:

==============================================
COSAR -- TerraSAR-X Complex SAR Data Product
==============================================

Ce pilote fournit la possibilité de lire les données complexes TerraSAR-X. Bien 
que la plupart des utilisateurs reçoivent les données au format GeoTIFF 
(représentant la radiation détectée réfléchit à partir des cibles, les produits 
ScanSAR seront distribué au format COSAR.

Pour l'essentiel, COSAR est une matrice binaire annotée, avec chaque échantillon 
contenu sous 4 bytes (16 bytes réel, 16 bytes imaginaire) stocké avec le byte 
le plus significatif en premier (Big Endian). Dans un conteneur COSAR il y a un 
ou plusieurs "bursts" qui représentent des bursts ScanSAR individuel. Notez que 
si un produit Stripmap ou Spotlight est contenu dans un conteneur COSAR il est 
stocké dans un seul burst.

La gestion des données ScanSAR est en cours de dévéloppement, dû à la difficulté 
de s'adapter aux identifiant des "bursts" ScanSAR dans le modèle GDAL.

Voir également :

* DLR Document TX-GS-DD-3307 "Level 1b Product Format Specification."

.. yjacolin at free.fr, Yves Jacolin - 2009/02/22 19:30 (Trunk 13797)