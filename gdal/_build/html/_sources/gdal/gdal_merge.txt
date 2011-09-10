.. _`gdal.gdal.gdal_merge`:

==============
gdal_merge.py
==============

Mosaïquage d'un ensemble d'images

**Usage :**
::
    
    gdal_merge.py [-o out_filename] [-of out_format] [-co NAME=VALUE]*
                [-ps pixelsize_x pixelsize_y] [-tap] [-separate] [-v] [-pct]
                [-ul_lr ulx uly lrx lry] [-n nodata_value] [-init "value [value...]"]
                [-ot datatype] [-createonly] input_files

Cette commande mosaïquera automatiquement un ensemble d'images. Toutes les 
images devront être dans le même système de coordonnées et avoir un nombre 
assorti de bandes, mais elles peuvent se superposer et avoir des résolutions 
différentes. Dans les zones de superposition, la dernière image sera copiée par 
dessus les premières.

* **-o out_filename :**  nom du fichier en sortie, qui sera créé s'il n'existe 
  pas (*out.tif* par défaut).
* **-of format :** format de sortie, GéoTIFF par défaut (GTiff). 
* **-co NAME=VALUE :** option de création pour le fichier de sortie. Des options 
  multiples peuvent être définies.
* **-ot datatype :** force un type défini pour la sortie des bandes d'images. 
  Utilisez les noms des types (c'est-à-dire Byte, Int16...).
* **-ps pixelsize_x pixelsize_y :** taille du pixel à utiliser pour le fichier 
  en sortie. S'il n'est pas défini, la résolution du premier fichier sera utilisée.
* **-tap :** (GDAL >= 1.8.0) (*target aligned pixels*) aligne les coordonnées 
  de l'étendue du fichier en sortie aux valeurs de l'option *-tr* de telle sorte 
  que l'étendue alignée inclue l'étendue minimale.
* **-ul_lr ulx uly lrx lry :** l'étendu du fichier de sortie. S'il n'est pas 
  défini, la somme de toutes les étendues sera utilisée. 
* **-v :** génère une sortie bavarde des opérations de mosaïcage lorsqu'elles 
  sont réalisées.
* **-separate :**  chaque fichier en entrée dans une bande empilée séparée.
* **-pct :** récupérer la table pseudo-couleur à partir du premier fichier image 
  en entrée, et l'utiliser pour la sortie. Fusionner les images en pseudo-couleurs 
  de cette façon assume que tous les fichiers en entrée ont la même table de 
  couleur.
* **-n nodata_value :** ignore les pixels des fichiers qui sont fusionnés égaux 
  à cette valeur du pixel.
* **-init value(s) :** pré-initialise la bande du fichier en sortie avec ces 
  valeurs. Cependant, elle n'est pas notée comme valeur *nodata* dans le fichier 
  en sortie. Si une seule est données, la même valeur sera utilisé dans toutes 
  les bandes.
* **-createonly :** le fichier en sortie est créé (et éventuellement 
  pré-initialisé) mais aucune image en entrée n'est copié dans celui-ci.

.. warning::
    *rbg2pct.py* est un script Python, et ne fonctionnera seulement si GDAL a 
    été compilé avec le support de Python.

Exemple
========

Créer une image avec les pixels dans toutes les bandes initialisés à 255.
::
    
    % gdal_merge.py -init 255 -o out.tif in1.tif in2.tif

Créer une image RVB qui affiche en bleu les pixels sans données. Les deux 
premières bandes seront initialisé à 0 et la troisième le sera à 255.
::
    
    % gdal_merge.py -init "0 0 255" -o out.tif in1.tif in2.tif


.. yves at georezo.net, Yves Jacolin - 2010/12/29 15:02 (http://gdal.org/gdal_merge.html Trunk r21324)
