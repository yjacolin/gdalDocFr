.. _`gdal.gdal.formats.bmp`:

BMP --- Microsoft Windows Device Independent Bitmap
====================================================

Bitmaps Indépendant des Périphériques de MS Windows gérés par le noyau de 
Windows et le plus souvent utilisé pour stocker les images de décoration du 
système. Dû à la nature du format BMP il y a plusieurs restrictions et ne il 
peut pas être utilisé pour le stockage d'image générale. En particulier, vous 
pouvez seulement créer des images monochrome sur 1 bit, pseudo-couleur sur 8 
bits et RVB de 24 bits. Même si des images en nuance de gris doivent être sauvé 
sous la forme pseudo-couleur.

Ce pilote gère la lecture de presque n'importe quel type de fichiers BMP et peut 
en écrire un qui devrait être géré sur n'importe quel système Windows. Seulement 
des fichiers simple- ou tri-bandes peut être sauvé dans un fichier BMP. Les 
valeurs en entrée seront re-échantillonnées en 8 bits.

Si un fichier worl ESRI exist avec l'extension .bpw, .bmpw ou .wld, il sera lu 
et utilisé pour établir la géotransformation pour l'image.

**Options de création :**

* **WORLDFILE=YES :** force la génération d'un fichier world d'ESRI associé 
  (avec l'extension .wld). 

**Lisez également :**

* Implémenté dans *gdal/frmts/bmp/bmpdataset.cpp*.
* **Référence Bitmap MSDN :** http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/bitmaps_9qg5.asp

.. yjacolin at free.fr, Yves Jacolin - 2009/02/15 19:54 (trunk 13801)