.. _`gdal.gdal.formats.leveller`:

=========================================
Leveller --- Daylon Leveller Heightfield
=========================================

(http://www.lizardtech.com/)

Leveller heightfields stocke des valeurs d'élévation sur 32 bit. Les formats 
versions 4 à 7 sont géré avec différents canevas (voir ci-dessous). L'extension 
du fichier pour Leveller heightfields est « TER » (qui est le même que celui de 
Terragen, mais le pilote ne reconnais que les fichiers Leveller).

Les bloques sont organisé sous forme de ligne scannée à haut pixel (lignes) avec 
la première ligne scannée en haut (nord) du bord du DEM, et les pixels adjacents 
sur chaque ligne augmentant de la gauche vers la droite (ouest vers l'est).

Le type de bande est toujours Float32, même avec les formats versions 4 et 5 
utilise physiquement des points fixes de 16.16. Le pilote les convertit en point 
flottant.

Lecture
=========

``dataset::GetProjectionRef()`` renverra seulement un système de coordonnée pour 
les fichiers de versions 4 à 6.

``dataset::GetGeoTransform()`` renverra une simple transformation mondiale avec 
une origine centrée pour les formats 4 à 6. Pour la version 7, il renvoie une 
transformation mondiale réelle sauf pour les rotations. La transformation de 
l'identité n'est pas considéré comme une condition d'erreur ; Les documents de 
Leveller les utilisent souvent.

``band::GetUnitType()`` rapportera les unités de mesure utilisé par le fichier 
au lieu de convertir les types inhabituels en mètre. Une liste de type d'unité 
se trouve dans le module *levellerdataset.cpp*.

``band::GetScale()`` et ``band::GetOffset()`` renverra la transformation 
physique vers celle logique (c'est à dire brute vers celle du monde réelle) 
pour les données d'élévation.

Écriture
===========

L'appel ``dataset::Create()`` est géré, mais pour les fichiers de version 7 
seulement.

``band::SetUnitType()`` peut être définie à n'importe quel type d'unité listé 
dans le module levellerdataset.cpp.

``dataset::SetGeoTransform()`` ne doit pas inclure les données de rotation.

De même que le pilote Terragen, l'option ``MINUSERPIXELVALUE`` doit être 
définie. Cela laisse le pilote cartographier correctement les élévations 
logiques (le monde réel) vers les élévations physiques.
 
Les informations d'en-tête sont écrit lors du premier appel à *band::IWriteBlock*.

Historique
===========

* v1.2 (Jul 17/07) : ajout de la version 7 et gestion de *Create*.
* v1.1 (Oct 20/05) : correction des erreurs dans coordsys et dans « elev 
  scaling » errors.

.. seealso::

* Implémenté dans gdal/frmts/leveller/levellerdataset.cpp.
* Le SDK de Leveller, qui documente le format Leveller : 
  http://www.daylongraphics.com/products/leveller/dev/index.htm


.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 21:10 (trunk 11800)