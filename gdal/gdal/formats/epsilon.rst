.. _`gdal.gdal.formats.epsilon`:

Epsilon - images compressé par ondelette
=========================================

À partir de GDAL 1.7.0, GDAL peut lire et écrire des images compressé par 
ondelette  via la bibliothèque Epsilon.

À partir de GDAL 1.9.0, epsilon 0.9.1 est nécessaire.

Le pilote repose sur la bibliothèque Open Source EPSILON (double licence LGPL/GPL 
v3). Dans son état actuel, le pilote sera seulement capable de lire les images 
avec une tuilage interne régulier.

Le pilote EPSILON gère seulement les images d'1 bande (nuance de gris) et de 3 
bandes (RVB).

Cela est censé être principalement utilisé par le pilote :ref:`gdal.gdal.formats.rasterlite`.

Options de création
--------------------

* **TARGET** réduction cible de la taille comme pourcentage de l'original (0-100). 
  96 par défaut.
* **FILTER**. voir la documentation EPSILON ou ``gdalinfo --format EPSILON`` pour 
  une liste complète des ID des filtres. 'daub97lift' par défaut.
* **BLOCKXSIZE=n :** définie la largeur des tuiles, 256 par défaut. Puissance de 
  deux entre 32 et 1024
* **BLOCKYSIZE>=n :** définie la hauteur des tuiles, 256 par défaut. Puissance de 
  deux entre 32 et 1024.
* **MODE=[NORMAL/OTLPF] :** OTLPF est une sorte de hack pour réduire les artefacts 
  des contours quand l'image est découpée en plusieurs tuiles. Dû à des contraintes 
  mathématiques cette méthode peut être être appliquée seulement aux filtres 
  biorthogonaux. OTLPF par défaut.
* **RGB_RESAMPLE=[YES/NO] :** si le buffer RVB doit être re-échantillonné en 
  4:2:0. YES par défaut.

**Voir également :**

* `Page principale d'EPSILON <http://sourceforge.net/projects/epsilon-project>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/05 (trunk 22363)