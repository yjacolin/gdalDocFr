.. _`gdal.gdal.gdalmove`:

gdalmove.py
============

Transforme le géoréférencement d'un fichier raster en place

**Usage :**

::
	
	gdalmove.py [-s_srs <srs_defn>] -t_srs <srs_defn>
		        [-et <max_pixel_err>] target_file

Description
************

Le script *gdalmove.py* transforme les limites d'un fichier raster d'un système 
de coordonnées en un autre, met à jour le système de coordonées et le 
géorégérencement du fichier. Cela est réalisé sans modifier les valeurs des pixels. 
C'est sensiblement similaire à l'utilisation de *gdalwarp* pour transformer une 
image mais en évitant le re-échantillonage afin de ne pas altérer l'image. C'est 
généralement possible pour des transformations qui sont linéaire dans la zone du 
fichier.

Si aucune valeur de seuil d'erreur (*-et*) n'est fournie alors le fichier n'est 
pas réellement mis à our mais les erreurs qui ne seraient pas nettoyer seraient 
retournées. Si *-et* est fournie alors le fichier est seulement modifié si 
l'erreur apparente introduite est inférieure à seuil indiqué (en pixels).

Pour le moment le géoréférencement transformé est calculé en partant des coins 
haut gauche, haut droit, bas ghauche du géoréférencement. Une réduction de 
l'erreur d'ensemble pourrait être réalisée en utilisant la méthode des moindres 
carrés avec au moins les 4 coins.

* **-s_srs srs_defn :** Écrase le système de coordoonées du fichier avec la 
  définition du système de coordonnées indiquée. Optionnel. Si non fournie le 
  système de coordonnées source est lu à partir du fichier source.
* **-t_srs srs_defn :** Définie le système de coordonnées cible. Ce système de 
  coordonnées sera écrit dans le fichier après la mise à jour.
* **-et max_pixel_err :** Le seuil d'erreur (en pixels) au delà duquel le fichier 
  ne sera pas mis à jour. S'il n'est pas fourni aucune mise à jour ne sera 
  appliquée au fichier mais les erreurs seront retournées.
* **target_file :**  Le fichier sur lequel opérer. Pour le mettre à jour, celui-ci
  doit être un format qui gère les mises à jour des informations de SRS et de 
  géoréférencement.


.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/gdalmove.html Trunk r25410)
