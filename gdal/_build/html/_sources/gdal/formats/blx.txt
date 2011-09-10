.. _`gdal.gdal.formats.blx`:

=====================================
BLX -- Magellan BLX Topo File Format
=====================================

BLX est le format pour le stockage de données topographique dans les GPS 
Magellan. Ce pilote gère à la fois la lecture et l'écriture. De plus les 4 
niveaux d'aperçus inhérent au format BLX peut être utilisé avec le pilote.

Le format BLX est basé sur des tuiles pour le moment la taille des tuiles est 
fixée à une taille de 128x128. De plus les dimensions doivent être un multiple 
de la taille de la tuile.

Le type de données est fixé à Int6 et la valeur pour les valeurs non définie est 
définie à -32768. Dans le format BLX les valeurs non définies sont seulement 
gérées au niveau de la tuile. Pour les pixels non définie dans des tuiles non 
vides voyez les options **FILLUNDEF/FILLUNDEFVAL**.

Géoréférencement
=================

La projection BLX est fixée à WGS84 et le géoréférencement à partir des BLX est 
géré sous la forme de tiepoint et de taille de pixel.

Problèmes lors de la création
=============================

**Options de création  :**

* **ZSCALE=1 :** définie l'incrémentation de le quantisation désirée pour 
  l'accès en écriture. Une valeur plus importante résultera en une meilleure 
  compression et une moins bonne résolution verticale.
* **BIGENDIAN=YES :** si **BIGENDIAN** est définie, le fichier en sortie sera 
  au format XLB (big endian blx).
* **FILLUNDEF=YES :** si **FILLUNDEF** est définie à **yes** la valeur de 
  **FILLUNDEFVAL** sera utilisé à la place de -32768 pour les tuiles vides. 
  Ceci est nécessaire puisque le format BLX ne gère que les valeurs indéfinie 
  pour les tuiles complètes, pas pour les pixels individuels.
* **FILLUNDEFVAL=0 :** Voir FILLUNDEF 

.. yjacolin at free.fr, Yves Jacolin - 2009/03/27 20:13 (trunk 15554)