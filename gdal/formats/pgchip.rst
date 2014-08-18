.. _`gdal.gdal.formats.pgchip`:

==========================================================
PGCHIP - Le pilote GDAL de Postgis pour les données raster
==========================================================

.. warning::
    **Ce pilote est en cours de développement !**


Objectifs
==========

Le but du pilote PGCHIP est de fournir une interface entre 
`GDAL <http://gdal.org>`_ et Postgis. GDAL est une bibliothèque de traduction 
pour les formats de données géospatiaux et `Postgis <http://www.postgis.org>`_ 
une extension spatiale pour `PostgreSQL <http://www.postgresql.org>`_, un système 
de gestion de base de données open source relationnel. Ce projet n'est pas une 
interface OGR à PostGIS, si vous recherchez cela (code orienté vecteur), vous 
pouvez regarder le :ref:`gdal.ogr.formats.postgresql`. 	

Comment PostGIS gère les rasters ?
===================================

Il ne les gère pas. Cependant, un type spécial nommé CHIP existe dans les 
sources de PostGIS. Quelques fonctions sont également disponible pour manipuler 
des données qui pourraient être stockées dans un objet CHIP.
		

Pourquoi ne pas utliser GDAL pour développer une extension complète de données raster au sein de PostGIS ?
============================================================================================================

GDAL fournie une très bonne interface pour l'implémentation de pilote. Son 
design permet un développement rapide et facile de nouveaux wrapper pour les 
formats raster. De plus, les programmes en ligne de commande sont très 
intéressantes pour tester le nouveau pilote et pour convertir des fichiers 
raster dans le type de données CHIP de PostGIS. Ajouter la gestion du raster 
dans PostGIS impliquerait de modifier ses sources pour optimiser la structure 
et les fonction du type CHIP. Cependant, il serait certainement intéressant de 
s'impliquer dans le développement de PostGIS pour déplacer certaines fonctions 
du pilotes PGCHIP dans le moteur de base de données. Par ce moyen, nous gardons 
les deux projets parfaitement indépendant.

Restrictions importantes du pilote
===================================

* Le pilote PGCHIP est en cours de développement ce qui signifie qu'il n'a pas 
  été entièrement testé et aucune version stable n'est téléchargeable.
* Le pilote gère seulement les types *GDT_Byte* et *GDT_UInt16* et gère 1 ou 4 
  bandes (GREY_SCALE, PALETTE et RGBA)
* Le nom de la colonne pour le type CHIP n'est pas encore modifiable et est 
  définie à "raster" par défaut.
* Dans le but de définir la base de données à laquelle vous voulez vous 
  connecter, vous devez définir la chaîne de connection. Les différents 
  paramètres de connection (host,port,dbname) doivent être délimités avec un 
  caractère "#". Le nom de la couche PostGIS doit apparaître à la fin de la 
  chaîne après un argument "%layer=". Exemple :

::
    
    $ gdalinfo PG:host=192.168.1.1#dbname=mydb%layer=myRasterTable

Comment j'installe le pilote PGCHIP ?
======================================

**Nécessité :**

* Assurez vous d'avoir une installation complète à partir des sources 
  PostgreSQL/Postgis claire ;
* Vous devez aussi avoir Proj4 installé et configuré dans PostGIS pour que le 
  pilote fonctionne.

**Notes d'installation :**

- Allez dans le répertoire *frmts* dans l'arborescence des sources de GDAL.
- Décompressez l'archive *pgchip* dans le répertoire *frmts*.
- Éditez GNUMakefile poru définir le chemin include de Postgis.
- Ajoutez les déclaration de points d'entrées d'enregistrement :

  - Ouvrez *gdal/gcore/gdal_frmts.h*
  - Ajoutez "void CPL_DLL GDALRegister_PGCHIP(void);" entre the CPL_C_START et CPL_C_END tags

- Ajoutez un appel à la fonction d'entregistrement dans *frmts/gdalallregister.c*. Dans la fonction *GDALAllRegister()* ajoutez les lignes suivantes :

::
    
    #ifdef FRMT_pgchip
        GDALRegister_PGCHIP();
    #endif

- Ajoutez le nom du format court à la macro *GDAL_FORMATS* dans *GDALmake.opt.in* (et dans *GDALmake.opt*) :

  - Localisez y la variable *GDAL_FORMATS* et ajoutez "pgchip" (en minuscule) à la liste des formats ;

- Ajouter une entrée spécifique au format à la macro EXTRAFLAGS dans *frmts/makefile.vc* ;
- Recompiler votre bibliothèque GDAL :

  - ``make clean``
  - ``./configure``
  - ``make``
  - ``make install``

Comment puis je tester le pilote ?
====================================

Vous pouvez choisir de compiler votre propre application en utilisant 
l'`API <http://gdal.maptools.org/gdal_tutorial.html>`_ ou utiliser les 
:ref:`gdal.gdal.presentation`. Quelques exemples :
::
    
    $ gdaltranslate -of pgchip /DATA/myRaster.png PG:host=192.168.1.1#dbname=mydb%layer=myRasterTable

Cette ligne de commande créera une table nommée *myRasterTable* et y copiera 
les données raster. Vous pouvez vouloir exporter le nouvel raster inséré dans 
un autre format :
::
    
    $ gdaltranslate -of bmp  PG:host=192.168.1.1#dbname=mydb%layer=myRasterTable /DATA/myRaster.bmp

TODO List
===========

* Tester la compatibilité du pilote avec différents formats raster ;
* Modifier la chaîne de connection pour faire face avec le nom de la colonne raster ;
* Améliorer le nombre de couleur des options d'interprétations ;
* Augmenter le nombre de types de données et de matrice de géotransformation gérés ;
* Améliorer la conversion du SRID ;
* Test du makefile.vc (Visual C) ;
* ... 	
		

Téléchargement
===============

`pgchip-1.1.tar.gz <http://simon.benjamin.free.fr/pgchip/download.php>`_
		

Information sur l'auteur et rapport de bug
===========================================

  simon (dot) benjamin (at) free (dot) fr


.. yjacolin at free.fr, Yves Jacolin - 2009/03/27 20:21