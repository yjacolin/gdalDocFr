.. _`gdal.gdal.formats.grass`:

Le format GRASS
================

GDAL gère d'une manière optionnelle la lecture de couches raster au format 
GRASS existantes (cells et groupes d'images), mais pas l'écriture et l'export. 
La gestion des couches rasters au format GRASS est déterminée lorsque la 
bibliothèque est configurée, et nécessite que libgrass soit pré-installée (lisez 
les remarques ci-dessous).

Sélection des rasters de GRASS
-------------------------------

Les rasters de GRASS peuvent être sélectionnés de différentes manières.

Chemin complet vers le fichier cellhd
***************************************

Le chemin complet vers le fichier cellhd pour la cellule peut être définie. Ce 
n'est pas un chemin relatif, ou du moins il doit contenir toutes les parties du 
chemin dans la base de données avec la racine de la base de données incluse. 
L'exemple suivant ouvre la cellule « proj_tm » dans le jeu de carte « PERMANENT 
» de la région « proj_tm » dans la base de données GRASS placée dans 
*/u/data/grassdb*.

Par exemple :
::
    
    % gdalinfo /u/data/grassdb/proj_tm/PERMANENT/cellhd/proj_tm

Chemin complet vers le répertoire
**********************************

Le chemin complet vers le répertoire contenant les informations sur le groupe 
d'image (ou le fichier REF à l'intérieure) peut être définie pour se référer à 
l'ensemble du groupe comme un simple jeu de données. Les exemples suivants font 
la même chose.

Par exemple :
::
    
    % gdalinfo /usr2/data/grassdb/imagery/raw/group/testmff/REF
    % gdalinfo /usr2/data/grassdb/imagery/raw/group/testmff

Fichier de configuration
*************************

S'il y a un fichier de configuration .grassrc5 correcte dans le répertoire home 
de l'utilisateur, alors les cellules et les groupes d'images peuvent être 
ouverte juste avec le nom de la cellule. Cela fonctionne seulement pour les 
cellules ou les images dans la région en court et le jeu de données comme 
définie dans le fichier .grassrc5.

Fonctionnalités gérées
----------------------

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

**Voyez également :**

* `Page officielle de GRASS GIS <http://grass.itc.it/>`_
* `page libgrass <http://home.gdal.org/projects/grass/>`_

**Remarques sur les variations des pilotes :**

Pour GRASS 5.7, Radim Blazek a déplacé le pilote pour utiliser la bibliothèque 
partagée de GRASS directement au lieu d'utiliser libgrass. Pour l'instant (GDAL 
1.2.2 et suivant) les deux versions du pilote sont disponibles et peut être 
configuré en utilisant l'option « --with-libgrass » pour la manière avec libgrass 
ou « --with-grass=<dir> » pour la nouvelle version de la bibliothèque GRASS 5.7. 
La version du pilote GRASS 5.7 ne gère pas pour l'instant l'accès au système de 
coordonnées, bien qu'il soit possible que cela soit corrigé.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/22 19:51 (trunk 9815)