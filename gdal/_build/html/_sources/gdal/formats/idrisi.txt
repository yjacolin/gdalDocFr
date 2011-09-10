.. _`gdal.gdal.formats.idrisi`:

=============================
RST --- Idrisi Raster Format
=============================

Ce format est typiquement un format brute. Il y a juste une bande par fichier, 
sauf dans les types de données RGB24 où les bandes rouges, vertes et bleues sont 
stockées entrelacées par pixel dans l'ordre Bleu, Vert et Rouge. Les autres 
types de données sont des entiers non signés sur 8 bits avec des valeurs de 0 à 
255 ou des entiers signés sous 16 bits avec des valeurs de -32.768 à 32.767 ou 
des points à précisions flottantes de 32 bits. La description du fichier est 
stockée dans un fichier texte d'accompagnement, avec une extension RDC.

Le fichier RDC de description de l'image n'inclut pas de table de couleur, ou 
d'informations détaillées sur le géoréférencement. La table de couleurs présente 
peut être obtenu par un autre fichier d'accompagnement en utilisant le même nom 
que le fichier RST et l'extension SMP.

Pour l'identification des référencements géographiques, le fichier RDC contient 
des informations qui renvoient vers un fichier qui détient les détails des 
références géographiques. Ces fichiers utilisent l'extension REF et résident 
dans le même répertoire que l'image RST ou plus probablement dans les 
répertoires d'installation d'Idrisi.

Par conséquent la présence ou l'absence du logiciel Idrisi dans le système 
d'exploitation déterminera la manière dont ce pilote fonctionnera. En définissant 
la variable d'environnement IDRISIDIR pour pointer vers le répertoire 
d'installation principale d'Idrisi cela permettra à GDAL de trouver plus 
d'informations plus détaillées sur les références géographiques et les 
projections dans les fichiers REF.

Notez que le pilote RST reconnaît les conventions de nom utilisés dans Idrisi 
pour les références géographique UTM et Plate carré (State Plane), il n'a donc 
pas besoin d'accéder aux fichiers REF. C'est le cas pour le fichier RDC qui 
définie « utm-30n » et « spc87ma1 » dans le champ « ref. system ». Notez que 
l'export vers le format RST de n'importe quel système de référence géographique 
générera une suggestion pour le contenu du fichier REF dans la section 
commentaire du fihcier RDC.

* « .rst » le fichier image brute
* « .rdc » le fichier descriptif
* « .smp » le fichier de la table de couleur
* « .ref » le fichier de référence géographiques

**Voir également :**

* Implémenté dans *gdal/frmts/idrisi/idrisiraster.cpp*. 
* www.idrisi.com


.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 20:34 (trunk 13513)