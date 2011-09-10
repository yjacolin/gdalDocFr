.. _`gdal.gdal.formats.gif`:

===================================
GIF -- Graphics Interchange Format
===================================

GDAL gère la lecture et l'écriture des fichiers GIF normaux et interlacés. Les 
fichiers GIF apparaissent toujours comme ayant une bande de 8 bites de carte de 
couleur. Les fichiers GIF ne gèrent pas le géoréférencement.

Une image GIF avec une transparence aura cette entrée noté comme ayant une valeur 
alpha de 0.0 (transparent). Aussi, la valeur transparente sera renvoyé comme la 
valeur noData pour la bande.

Si un fichier world ESRI existe avec l'extension .gfw, .gifw ou .WLD, il sera 
lu et utilisé pour établir la géotransformation pour l'image.

À partir de GDAL 1.9.0, les métadonnées XMP peuvent être extraite à partir du 
fichier, et sera stocké comme XML brute dans le domaine de médatonnées xml:XMP.

Problème lors de la création
=============================

Les fichiers GIF peuvent seulement être créé comme une bande de 8 bit en 
utilisant le mécanisme « CreateCopy ». S'il est écrit à partir d'un fichier qui 
n'a pas de carte de couleur, une carte de couleur par défaut en nuance de gris 
est générée. Les fichiers GIF transparent ne sont pas gérés pour l'instant en 
création.

* **WORLDFILE=ON :** force la génération d'un fichier World d'ESRI associé (.wld).

Des fichiers interlacés (progressive) peuvent être générés en fournissant 
l'option *INTERLACING=ON* lors de la création. 

À partir de GDAL 1.7.0, la gestion du GIF interne de GDAL a été implémenté en se 
basant sur les source de la bibliothèque giflib 4.1.6 (écrite par Gershon Elbor, 
Eric Raymond et Toshio Kuratomi), générant donc des GIG compressé en LZW.

Ce pilote a été écrit grâce au financement de DM Solutions Group 
(http://www.dmsolutions.ca), et CIET International (http://www.ciet.org).

**Lisez également :**

* `Page principale de giflib <http://sourceforge.net/projects/giflib/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/07 (trunk 22678)