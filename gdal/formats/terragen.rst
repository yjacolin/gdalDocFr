.. _`gdal.gdal.formats.terragen`:

====================================
Terragen --- Terragen™ Terrain File
====================================

Les fichiers Terragen terrain stockent des valeurs d'élévations sur 16 bites 
avec une grille d'espacement optionnelle (mais pas de positionnement). 
L'extension du fichier pour les heightfields de Terragen est "TER" ou "TERRAIN" 
(qui dans le cas précédent est le même que Leveller, mais le pilote ne 
reconnait que les fichiers Terragen). L'ID du pilote est "Terragen". Le jeu de 
données est basé sur des fichiers et possède seulement une bande d'élévation. 
Les élévations vides ne sont pas gérées. Les pixels sont considéré comme des 
points.

Lecture
=========

``dataset::GetProjectionRef()`` renvoie un système de coordonnées local en 
utilisant des mètres.

``band::GetUnitType()`` renvoie des mètres.

Les élévations sont en *Int16*. Vous devez utiliser ``band::GetScale()`` et 
``band::GetOffset()`` pour les convertir en mètres.

Écriture
=========

Utilisez l'appel *Create*. Définissez l'option *MINUSERPIXELVALUE* (de type 
*float*) pour l'élévation la plus basse de vos données élévation, et 
*MAXUSERPIXELVALUE* à la plus haute. L'unité doit correspondre à l'unité de 
l'élévation que vous donnerez à ``band::SetUnitType()``.

Appelez ``dataset::SetProjection()`` et ``dataset::SetGeoTransform()`` avec les 
détails du système de coordonnées. Autrement, le pilote n'encodera pas les 
élévations physique proprement. Les systèmes de coordonnées géographique (basé 
sur des degrés) seront  convertie en système local basé sur des mètres.

Pour garder la précision, les meilleures hauteur de base et d'échelle seront 
utilisé pour utiliser au mieux le domaine sur 16 bit.

Les élévations sont en *Float32*.

Roundtripping
==============

Les erreurs par trip tendent à quelques centimètres pour les élévations et 
jusqu'à un ou deux mètres pour l'étendue au sol si des systèmes de coordonnées 
basé sur les degrés sont écrit. Les gros MNT en degré implique des distorsions 
inévitable depuis que le pilote utilise seulement des mètres.

Historique
===========

* **v1.0 (Mar 26/06) :** Création ;
* **v1.1 (Apr 20/06) :** Ajout des corrections de la lecture de SIZE et de la 
  gestion de ``Create()`` ;
* **v1.2 (Jun 6/07) :** Amélioration de la détermination de l'échelle et de la 
  hauteur de base lors de l'écriture.

.. seealso::

  * Implémenté dans *gdal/frmts/terragen/terragendataset.cpp*.
  * Lisez le fichier `readme.txt <http://gdal.org/readme.txt>`_ pour l'installation 
    et la gestion des informations.
  * `Spécification des fichiers <http://www.planetside.co.uk/terragen/dev/tgterrain.html>`_ Terragen Terrain.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 22:10 (trunk 11619)