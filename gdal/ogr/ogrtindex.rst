.. _`gdal.ogr.ogrtindex`:

ogrtindex
==========

Créer un index de tuile.

Usage
-------

::
    
    ogrtindex [-lnum n]... [-lname name]... [-f output_format]
          [-write_absolute_path] [-skip_different_projection]
                 output_dataset src_dataset...

Le programme ``ogrtindex`` peut être utilisé pour créer des index de tuiles - 
un fichier contenant une liste d'identification d'un groupe d'autre fichiers en 
fonction de leurs étendues spatiales. Cela a d'abord pour but d'être utilisé 
avec `MapServer <http://mapserver.org>`_ pour l'accès aux tuiles en 
utilisant le type de connexion ogr.

* **-lnum n :** ajoute le numéro de couche 'n' de chaque fichier source dans 
  l'index des tuiles.
* **-lname nom :** ajoute la couche nommé 'nom' de chaque fichier source dans 
  l'index des tuiles.
* **-f output_format :** sélectionne un nom de format en sortie. Créer un 
  shapefile par défaut.
* **-tileindex field_name :** le nom à utiliser pour le nom du jeu de données. 
  *LOCATION* par défaut.
* **-write_absolute_path :** les noms de fichiers sont écrit avec des chemins 
  absolus.
* **-skip_different_projection :** seulement les couches avec le même 
  référentiel de projection que des couches déjà inséré dans l'index des tuiles 
  seront inséré.

Si aucun arguments *-lnum* ou *-lname* sont données, il est supposé que toutes 
les couches dans les jeux de données sources doivent être ajoutées à l'index de 
tuile comme enregistrement indépendant.

Si l'index de tuile existe déjà, les enregistrements seront ajouté, autrement 
l'index sera crée.

C'est un des défauts de l'actuel programme ``ogrtindex`` qui ne cherche pas à 
copier la définition du système de coordonnées de la source de données vers 
l'index de tuiles (comme il est attendue par `MapServer <http://mapserver.org>`_ 
quand *PROJECTION AUTO* est utilisé).

Cet exemple créera un shapefile (tindex.shp) contenant un index de tuiles des 
couches *BL2000_LINK* dans tous les fichiers NTF dans le répertoire de travail :
::
    
    % ogrtindex tindex.shp wrk/*.NTF

.. yjacolin at free.fr, Yves Jacolin 2010/12/30 14:48 (http:*www.gdal.org/ogrtindex.html Trunk 21366)
