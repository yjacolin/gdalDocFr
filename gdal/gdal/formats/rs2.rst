.. _`gdal.gdal.formats.rs2`:

RS2 -- RadarSat 2 XML Product
==============================

Ce pilote lira certain produits polarimétrique XML de RadarSat 2. En particulier, 
les produits complexes, et les produits détecté de magnitude de 16 bits.

Les produits XML de RadarSat 2 sont distribués avec un fichier primaire en XML 
appelé *product.xml* et un ensemble de fichiers de données de support XML avec 
l'imagerie réelle stockée dans des fichiers TIFF. Le pilote RS2 sera utilisé si 
le fichier *product.xml* ou le répertoire le contenant est sélectionné, et il 
peut traiter toutes les imageries sous la forme d'un jeu de données consistant.

Les produits complexes utilisent des fichiers TIFF « 32 bites typé void » qui ne 
sont pas lisible d'une manière compréhensible normalement. Le pilote RS2 prend 
soin de convertir cela en un format Cint16 interne utile.

Le pilote RS2 lit également les points de géolocation à partir du fichier 
*product.xml* et les représentent comme des points d'amer sur le jeu de données.

Il est très probable que le format International de RadarSat sera distribué avec 
d'autres sortes de jeux de données dans de ce format : cependant, pour l'instant 
ce pilote gère spécifiquement les produits polarimétriques RadarSat 2. Tous les 
autres seront ignorés, ou résultat en plusieurs erreurs *runtime*. Il est espéré 
que ce pilote peut être généralisé avec d'autres échantillons du produit en 
fonction de leur disponibilité.

**Lisez également :**

* RadarSat document RN-RP-51-27.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 21:33 (trunk 15536)