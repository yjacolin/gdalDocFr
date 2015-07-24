.. _`gdal.python.intro`:

Introduction
=============


Installation
-------------

Il existe plusieurs possibilités pour installer des extensions Python. Celles 
proposées ici sont indépendantes du système et permettent une certaine 
indépendances avec celui-ci.

Pour Windows installez `Python pour Windows <http://sourceforge.net/projects/pywin32/>`_

Système
*********

::
    
    $ sudo easy_install GDAL

Ou (mais lié à un système Debian ou Ubuntu) :
::
    
    $ sudo apt-get install python-gdal

Environnement virtuel
**********************

Installez les paquetages libgdal, exemple pour Ubuntu/Debian :
::
    
    $ sudo apt-get install libgdal libdal1-dev

Installez l'environnement virtuel :
::
    
    $ sudo easy_install virtualenv
    $ virtualenv --no-site-packages env

L'option ``--no-site-packages`` permet de ne pas mélanger le répertoire site-package 
du système de celui de l'environnement virtuel.

Puis activez (ie entrez dans l'environnement virtuel) :
::
    
    $ source bin/activate

La console change :
::
    
    (env)yves@helios:~/Documents/Geomatique/OSGeo/Projects/gdal/env$

Vous pouvez maintenant installer les extensions nécessaire :
::
    
    (env)$ cd env
    (env)$ gdal-config --version
    (env)$ bin/easy_install GDAL

Un problème ? Notez la version de GDAL (1.8.0 pour mon cas) puis essayer cette 
deuxième méthode :
::
    
    (env)$ pip install --no-install "GDAL>=1.7"

Vous obtenez encore :
::
    
        Could not run gdal-config!!!!
        Successfully downloaded GDAL

Puis lancer ces commandes :
::
    
    (env)$ rm -f build/gdal/setup.cfg
    (env)$ cd build/gdal
    (env)$ python setup.py build_ext --gdal-config=gdal-config \
        --library-dirs=/usr/lib \
        --libraries=gdal1.8.0 \
        --include-dirs=/usr/include/gdal \
    install

Testez l'installation :
::
    
    (env)$ bin/python

Puis :
::
    
    >>> from osgeo import gdal

Pour en sortir :
::
    
    (env)$ deactivate

API
----

Utilisation de Doxygen pour générer l'API : http://softlibre.free.fr/gdal/osgeo.ogr.html

::
    
    $ pydoc -w ogr
    
    $ epidoc ou sphinx

Utiliser la bibliothèque Python
---------------------------------

Si les étapes précédentes ont été réussi vous devez avoir la possibilité d'utiliser 
la bibliothèque GDAL-OGR en Python et avoir l'API au format HTML.

La classe GDAL
***************

Pour utiliser GDAL :
::
    
    >>> try:
    ...     from osgeo import gdal
    ... except ImportError:
    ...     import gdal

Explication : le bind Python de GDAL a évolué et a été incorporé dans une extension 
plus large nommé *osgeo*. La méthode ci-dessus permet d'être indépendante des 
versions de GDAL. Ainsi si la première partie (après le ``try:``) échoue la deuxième 
partie est lancé.

GDAL propose plusieurs classes d'objet nécessaire à la manipulation de raster : 
les classes *band*, *DataSet*, *Driver*, *RasterAttributeTable* et *ColorTable*.

La procédure pour manipuler des données raster est celle-ci :

* chargement des drivers et activation de celui qui est nécessaire (utilisation de la classe Driver) ;
* chargement du jeu de données via l'objet driver créé (la méthode Open() renvoie un objet DataSet) ;
* chargement de la bande nécessaire (la méthode GetRasterBand() renvoie un objet Band) ;
* transformation des données en Array pour manipulation des données ;
* transformation de l'array en données raster ;
* sauvegarde du raster
* destruction des objets utilisés : dataset, bande, driver, etc.

La classe OGR
***************

Les classes OGR ont évoluées depuis quelques versions. Elles font désormais 
partie de la classe *osgeo*. Pour garder une compatibilité avec les anciennes 
versions il est conseillé d'importer la classe *osgeo* et de le placer dans une 
méthode *try: except:* : 

Pour importer les classes OGR :

::
    
    >>> try:
    ...     from osgeo import ogr
    ...     from osgeo import osr
    ... except ImportError:
    ...     import ogr
    ...     import osr

La classe *osr* permet la gestion des systèmes de projection alors que la classe 
*ogr* permet de lire les fichiers vectoriels.
