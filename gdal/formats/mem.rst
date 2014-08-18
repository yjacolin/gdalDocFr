.. _`gdal.gdal.formats.mem`:

=========================
MEM -- In Memory Raster
=========================

GDAL gère la possibilité de prendre en charge des rasters dans un format 
temporaire en mémoire. Cela est d'abord utile pour les jeux de données 
temporaires dans les scripts ou en interne dans des applications. Il n'est 
généralement d'aucune utilité à l'utilisateur final.
Les jeux de données en mémoire doivent gérer la plupart des espèces 
d'informations auxiliaires dont les méta-données, les systèmes de coordonnées, 
le géoréférencement, les points d'amer, l'interprétation des couleurs, les 
tables de couleur et tous les types de données des pixel.

Format des noms des jeux de données
====================================

Il est possible d'ouvrir un tableau existant en mémoire. Pour cela, construire 
un nom de jeux de données de la forme suivante :

::
    
    MEM:::option=value[,option=value...]

Par exemple :
::
    
    MEM:::DATAPOINTER=342343408,PIXELS=100,LINES=100,BANDS=3,DATATYPE=Byte,
       PIXELOFFSET=3,LINEOFFSET=300,BANDOFFSET=1


* ``DATAPOINTER`` : pointeur vers le premier pixel de la première bande 
  représentée par un entier long. Note : cela peut ne pas fonctionner sur les 
  plate-formes où un entier long est en 32 bites et un pointeur est en 64 bites. 
  (obligatoire) 
* ``PIXELS`` : largeur d'un raster en pixel (obligatoire)
* ``LINES``: hauteur d'un raster en ligne (obligatoire)
* ``BANDS`` : nombre de bande, défaut à 1 (optionnel)
* ``DATATYPE`` : nom du type de données, comme retourné par 
  ``GDALGetDataTypeName()`` (par exemple Byte, Int16), Byte par défaut. 
  (optionnel)
* ``PIXELOFFSET`` : distance en bytes entre le début d'un pixel et le suivant 
  sur la même ligne scannée. (optionnel)
* ``LINEOFFSET`` : distance en bytes entre le début d'une ligne scannée et la 
  suivante (optionnel)
* ``BANDOFFSET`` : distance en bytes entre le début d'une bande de données et 
  la suivante.

Options de création
=====================

* Il n'y a aucune options de création de gérées.
* Le format MEM  est un des seuls qui gère la méthode ``AddBand()``. La méthode 
  ``AddBand()`` gère les options DATAPOINTER, PIXELOFFSET et LINEOFFSET pour 
  faire référence à un tableau existant en mémoire.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 21:12 (trunk 10860)