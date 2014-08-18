.. _`gdal.gdal.formats.xyz`:

=========================
XYZ -- ASCII Gridded XYZ
=========================

.. versionadded:: 1.8.0

GDAL gère la lecture et l'écritue de jeux de données raster XYZ **quadrillées** 
ASCII (ie. les XYZ non quadrillé, XYZ LIDAR, etc. doivent être ouvert par d'autres 
moyens. Voir la documentation de la commande :ref:`gdal.gdal.gdal_grid`).

Ces jeux de données sont des fichiers ASCII avec (au moins) 3 colonnes, chaque 
lignes contenant les coordonnées X et Y du centre de la cellule et sa valeur.

L'espace entre chaque cellule doit être constante et aucune valeur manquante n'est 
gérée. Les cellules avec les mêmes coordonnées doivent être placées sur des 
lignes consécutives. Pour une même valeur de coordonnées Y, les lignes dans le 
jeu de données doit être organisé en augmentant les valeurs de X. La valeur des 
coordonnées Y peut augmenter ou diminuer cependant. Les séparateurs de colonnes 
gérés sont l'espace, les virgules, le point-virgule et les tabulations.

Le pilote tente de détecter une ligne d'en-tête et cherchera les noms 'x', 'lon' 
ou 'east' pour détecter l'index de la colonne X, 'y', 'lat' ou 'north' pour la 
colonne Y et 'z', 'alt' ou 'height' pour la colonne Z.  Si aucun en-tête n'est 
présent ou une des colonnes ne peuvent être identifié dans l'en-tête, les colonnes 
X, Y et Z (dans cet ordre) sont supposé d'être les trois premières colonnes de 
chaque ligne.

L'ouverture d'un gros jeu de données peut être lente puisque le pilote doit scanner 
l'ensemble du fichier pour déterminer la taille du jeu de donnes et la résolution 
spatiale. Le pilote auto-détectera le type de données parmi Byte, Int16, Int32 ou 
Float32.

Options de création
=====================

* **COLUMN_SEPARATOR=a_value :** où a_value est une chaîne utilisée pour séparer 
  la valeur des colonnes X,Y et Z. Par défaut à un espace
* **ADD_HEADER_LINE=YES/NO :** si une ligne d'en-tête doit être écrite (le 
  contenu est X <col_sep> Y <col_sep> Z). NO par défaut

.. seealso::

  * Documentation de la commande :ref:`gdal.gdal.gdal_grid`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/29 (trunk 19921)