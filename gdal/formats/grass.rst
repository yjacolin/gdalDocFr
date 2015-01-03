.. _`gdal.gdal.formats.grass`:

================
Le format GRASS
================

GDAL gère d'une manière optionnelle la lecture de cartes raster ou des groupes 
d'images de GRASS, mais pas l'écriture ou l'export. La gestion des couches 
rasters au format GRASS est déterminée lorsque la bibliothèque est configurée et 
nécessite que libgrass soit pré-installée (lisez les remarques ci-dessous).

Les rasters de GRASS peuvent être sélectionnés de différentes manières.

* Le chemin complet vers le fichier cellhd peut être définie. Ce n'est pas un 
  chemin relatif, ou du moins il doit contenir toutes les parties du chemin dans 
  la base de données GRASS avec la racine de la base de données incluse. 
  L'exemple suivant ouvre la cellule « proj_tm » dans le jeu de carte 
  « PERMANENT » de la région « proj_tm » dans la base de données GRASS placée 
  dans */u/data/grassdb*.

  Par exemple :
  ::
    
    gdalinfo /u/data/grassdb/proj_tm/PERMANENT/cellhd/proj_tm
    

* Le chemin complet vers le répertoire contenant les informations sur le groupe 
  d'images (ou le fichier REF à l'intérieur) peut être définie pour se référer à 
  l'ensemble du groupe comme un simple jeu de données. Les exemples suivants font 
  la même chose.

  Par exemple :
  ::
    
    gdalinfo /usr2/data/grassdb/imagery/raw/group/testmff/REF
    gdalinfo /usr2/data/grassdb/imagery/raw/group/testmff

* S'il y a un fichier de configuration .grassrc5, .grassrc6 (GRASS 6) .grass7/rc 
  (GRASS 7) correcte dans le répertoire home de l'utilisateur, alors les cartes 
  rasters ou les groupes d'images peuvent être ouverts juste avec le nom de la 
  cellule. Cela fonctionne seulement pour les cartes raster ou les groupes 
  d'images dans la région en cours et le jeu de données comme définie dans le 
  fichier de configuration.

Les fonctionnalités suivantes sont gérées par le lien GDAL/GRASS :

* Jusqu'à 256 entrée dans la carte de couleur des cellules sont lues (0-255).
* Les cellules à entier compressé et non compressé, point flottant et double 
  précision sont toutes supportées. Les cellules d'entier sont classées avec une 
  bande de type « Byte » si le format 1-byte est utilisé. Autrement les cellules 
  d'entiers sont traités comme Uint32 (représente un entier 32-bit non signé).
* Les informations de géo-référencement sont proprement lu à partir de GRASS.
* Un essaie est réalisé pour traduire les systèmes de coordonnées, mais 
  certaines conversions peuvent échouées, en particulier la prise en charge des 
  datums et des unités.
 
Remarque sur les variations du pilote
=====================================

Pour GRASS 5.7, Radim Blazek a déplacé le pilote pour utiliser la bibliothèque 
partagée de GRASS directement au lieu d'utiliser libgrass. Pour l'instant (GDAL 
1.2.2 et suivant) les deux versions du pilote sont disponibles et peut être 
configuré en utilisant l'option « --with-libgrass » pour la manière avec libgrass 
ou « --with-grass=<dir> » pour la nouvelle version de la bibliothèque GRASS 5.7. 
La version du pilote GRASS 5.7 ne gère pas pour l'instant l'accès au système de 
coordonnées, bien qu'il soit possible que cela soit corrigé.

.. seealso::

  * `Page officielle de GRASS GIS <http://grass.osgeo.org/>`_
  * `page libgrass <http://home.gdal.org/projects/grass/>`_



.. yjacolin at free.fr, Yves Jacolin - 2013/08/14 (trunk 26321)