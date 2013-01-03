.. _`gdal.gdal.gdaltindex`:

gdaltindex
===========

Construit un index de tuile de raster dans un shapefile.

**Usage :**
::
    
    gdaltindex [-tileindex field_name] [-write_absolute_path] \
      [-skip_different_projection] [-t_srs target_srs] index_file [gdal_file]*

Ce programme construit un shapefile avec un enregistrement pour chaque fichier 
raster en entré, un attribut contenant le nom du fichier, et un objet polygone 
entourant le raster. Ce fichier est utilisable dans `MapServer <http://mapserver.org/>`_ 
comme une mosaïque de raster (tileindex).

* Le shapefile (index_file) sera créé s'il n'existe pas, autrement il sera 
  ajouté à celui existant.
* Le champ d'indexation des tuiles par défaut est 'location'.
* Les noms des fichiers raster seront inclus dans le fichier exactement comme 
  ils sont dénommés dans la ligne de commande à moins que l'option 
  *-write_absolute_path* ne soit utilisée.
* Si *-skip_different_projection* est définie, seuls les fichiers avec le 
  même fichier de référence de projection que ceux dans le tileindex seront insérés.
* Si **-t_srs** est utilisé, les géométries du fichier en entrée seront reprojeté 
  vers le système de référence de coordonnées désiré.
  Notez qu'utiliser cette option génère des fichiers qui ne sont pas compatible avec 
  MapServer.
* Des polygones rectangulaires simples sont générés dans le même système de 
  coordonnées que les rasters ou dans le système de référence cible si l'option 
  *-t_srs* est utilisée.

**Exemple :**
::
    
    gdaltindex doq_index.shp doq.tif

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01  (Trunk 25410)
