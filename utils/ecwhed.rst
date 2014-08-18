.. _`gdal.utils.ecwhed`:

ecwhed
========

Éditeur et visualiser d'en-tête ECW

Synopsis
---------

Usage :
::

    ecwhed [--help]
       [--version]
       [-a_ullr ulx uly lrx lry]
       [-co "DATUM=VALUE"]
       [-co "PROJ=VALUE"]
       file

Description
------------

La commande ``ecwhed`` est un visualiseur et éditeur pour les en-têtes des fichiers 
ECW. Le programme peut changer les datums, la projection et les coordonnées des 
coins sans décompresser et recompresser l'image.

 * **-a_ullr ulx uly lrx lry :** assigne/écrase les limites de géoréférencement 
   du fichier en sortie. Cela assigne les limites de géoréférencement au fichier 
   en sortie, ignorant celle dérivée du fichier source.

 * **-co "DATUM=VALUE" :** assigne/écrase un datum

 * **-co "PROJ=VALUE" :** assigne/écrase la projection 

Exemples
---------

Par exemple, les informations de géoréférencement contenu dans un fichier ECW 
peuvent être affichées avec la commande suivante :
::

    ecwhed FRA-0100.ecw

    Datum = NTF
    Projection = LM2FRANC
    Origin = (223000.000000, 2152500.000000)
    Pixel Size = (100.000000, -100.000000)
    Corner Coordinates:
    Upper Left = (223000.000000, 2152500.000000)
    Upper Right = (547500.000000, 2152500.000000)
    Lower Left = (223000.000000, 1690000.000000)
    Lower Right = (547500.000000, 1690000.000000)

Par exemple, un fichier ECW peut être géoréférencé avec la commande suivante :

::
    
    ecwhed -co "DATUM=NTF" -co "PROJ=LM2FRANC" -a_ullr 970000 1860000 980000 1850000 map.ecw

Téléchargement
---------------

Le code source est disponible ici : `ecwhed-0.1.tar.gz <http://jrepetto.free.fr/ecwhed/ecwhed-0.1.tar.gz>`_. 
Diffusé sous lince GPL version 2. Pour la compiler, vous avez besoin du SDK ECW 
d'ErMapper, qui peut être téléchargé à partir du `site web d'ErMapper <http://www.ermapper.com/>`_.

Source : http://jrepetto.free.fr/ecwhed/

.. Dernière révision : 02/07/2008
