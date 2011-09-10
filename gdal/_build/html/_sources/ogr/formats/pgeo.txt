.. _`gdal.ogr.formats.pgeo`:

==========================
ESRI Personal GeoDatabase
==========================

OGR gère en option la lecture de fichier .mdb des Géodatabases Personnelles via 
ODBC. Les Géodatabases Personnelles sont une base de données Microsoft Access(r) 
avec un ensemble de tables définies par ESRI pour prendre en compte les 
méta-données de la géodatabase, et avec des géométries pour les objets contenu 
dans une colonne BLOB dans un format personnalisé (essentiellement des fragments 
de géométries de Shapefile). Ces pilotes accèdent aux géodatabases personnelles 
via ODBC, mais ne dépend d'aucuns middleware d'ESRI.

Les Géodatabases Personnelles sont accédées en passant le nom du fichier .mdb 
pour être accédé comme source de données. Sous Windows, aucun DSN d'ODBC n'est 
nécessaire. Sous Linux, il y a un problème avec des connexions sans DSN dû à une 
implémentation incomplète ou bugguée de cette fonctionnalité dans le paquet MDB 
Tools. Il est donc nécessaire de configurer un Data Source Name (DSN) si le 
pilote `MDB Tools <http://mdbtools.sourceforge.net>`_ est utilisé (vérifiez les 
instructions ci-dessous).

Dans le but de faciliter la compatibilité avec différentes configurations, l'option 
de configuration PGEO_DRIVER_TEMPLATE a été ajouté pour fournir une façon pour 
définir par programmation le DSN avec le nom du fichier comme argument. Dans le 
cas où le nom du pilote est connu, cela permet la construction de DSN basé sur 
cette information d'une manière identique à celle par défaut (utilisé pour 
Windows access pour le pilote Microsoft Access).

OGR traite toutes les tables de géométrie comme des couches. La plupart des 
géométries devraient être gérée, données 3D incluses. Les informations de 
mesure seront ignorées. Les informations du système de coordonnées devraient 
être proprement associées aux couches.

Pour l'instant, le pilote de Géodatabase Personnelle d'OGR ne se sert pas des 
index spatiaux pour accélérer les requêtes spatiales, bien que cela puisse être 
ajouté dans le futur.

Par défaut, les commandes SQL sont envoyées directement au moteur de base de 
données MDB. Il est également possible de demander au pilote de prendre en charge 
les commandes SQL avec le moteur :ref:`gdal.ogr.sql`, en définissant la chaine 
*OGRSQL* à la méthode *ExecuteSQL()*, comme nom du dialecte SQL.

Comment utiliser le pilote PGeo avec unixODBC et MDB Tools
===========================================================

À partir de GDAL/OGR 1.9.0, le pilote :ref:`gdal.ogr.formats.mdb` est une autre 
façon de lire les fichiers .mdb géodatabase personnelle d'ESRI sans nécessité 
unixODBC et les outils MDB.

Cet article donne les explications étape par étape pour utiliser OGR avec le 
paquet unixODBC et pour accéder aux Géodatabases Personnelles avec le pilote 
PGeo.

Pré-requis
-----------

- Installez `unixODBC <http://www.unixodbc.org/>`_ >= 2.2.11
- Installez `MDB Tools`_ >= 0.6. La version 
  0.5.99 a également été testée par le développeur (pré-version 0.6).

(sur Ubuntu 8.04 : ``sudo apt-get install unixodbc libmdbodbc``)

Configuration
--------------

Il y a deux fichiers de configuration pour unixODBC :

* *odbcinst.ini* - ce fichier contient la définition des pilotes ODBC 
  disponibles à tous les utilisateurs ; ce fichier peut être trouvé dans le 
  répertoire */etc* ou la localisation donnée par */--sysconfdir* SI 
  VOUS COMPILEZ ``unixODBC`` vous-même.
* *odbc.ini* - ce fichier contient la définition des sources de données ODBC 
  (entré DSN) disponibles à tous les utilisateurs.
* *~/.odbc.ini* - le fichier privé où les utilisateurs peuvent placer leurs 
  propres sources de données ODBC.

Le format des fichiers de configuration est très simple :

::
    
    [section_name]
    entry1 = value
    entry2 = value

Pour plus de détails, référez-vous au `manuel d'unixODBC <http://www.unixodbc.org/doc/>`_.

1. Configuration du pilote ODBC
********************************

D'abord , vous devez configurer le pilote ODBC pour accéder aux bases de données 
Microsoft Access(r) avec MDB Tools. Ajoutez la définition suivante à votre 
fichier *odbcinst.ini*.

::
    
    [Microsoft Access Driver (*.mdb)]
    Description = MDB Tools ODBC drivers
    Driver     = /usr/lib/libmdbodbc.so.0
    Setup      =
    FileUsage  = 1
    CPTimeout  =
    CPReuse    =

* *[Microsoft Access Driver (*.mdb)]* - souvenez-vous d'utiliser "Microsoft 
  Access Driver (*.mdb)" comme nom de la section parce que le pilote PGeo créé 
  la chaine de connections ODBC pour les Géodatabases Personnelles en utilisant 
  la chaine "DRIVER=Microsoft Access Driver (*.mdb);".
* *Description* - courte description de cette définition du pilote.
* *Driver* - chemin complet de pilote ODBC pour MDB Tools.

2. Configuration de la source de données ODBC
***********************************************

Dans cette section, on utilise 'sample.mdb' comme nom de la géodatabase 
personnelle, remplacez la avec le nom de votre propre base de données.

Créez un fichier *.odbc.ini* dans votre répertoire *HOME* :

::
    
    $ touch ~/.odbc.ini

Placez-y la définition de la source de données ODBC suivante dans ce fichier :
::
    
    [sample_pgeo]
    Description = Sample PGeo Database
    Driver      = Microsoft Access Driver (*.mdb)
    Database    = /home/mloskot/data/sample.mdb
    Host        = localhost
    Port        = 1360
    User        = mloskot
    Password    =
    Trace       = Yes
    TraceFile   = /home/mloskot/odbc.log


Explication étape par étape d'une entrée DSN :

* *[sample_pgeo]* - c'est le nom de la source de données ODBC (DSN). Vous vous 
  référez à votre Géodatabase personnelle en utilisant ce nom. Vous pouvez 
  utiliser votre propre nom ici.
* *Description* - courte description de l'entrée DSN.
* *Driver* - nom complet du pilote défini à l'étape 1, au-dessus.
* *Database* - chemin complet vers le fichier *.mdb* de votre Géodatabase 
  Personnelle.
* entré *Host*, *Port*, *User* et *Password* ne sont pas utilisé par le pilote 
  MDB Tools.

Tester le pilote PGeo avec ogrinfo
-----------------------------------

Maintenant vous pouvez tester l'accès à une source de données PGeo avec ``ogrinfo``.

D'abord, vérifiez que vous avez le pilote PGeo compilé dans OGR :

::
    
    $ ogrinfo --formats
    Supported Formats:
        ESRI Shapefile
        ...
        PGeo
        ...

Maintenant vous pouvez accéder à votre Géodatabase personnelle. Comme source de 
données utilisez *PGeo:<DSN>* où *<DSN>* est un nom d'une entré DSN que vous 
avez placé dans votre fichier *.odbc.ini*.

::
    
    ogrinfo PGeo:sample_pgeo
    INFO: Open of `PGeo:sample_pgeo'
    using driver `PGeo' successful.
    1. ...

Après avoir lancé la commande ci-dessous, vous devez obtenir la liste des 
couches stockée dans votre géodatabase.

Maintenant, vous pouvez réaliser une requête pour détailler une couche particulière :
::
    
    ogrinfo PGeo:sample_pgeo <layer name>
    INFO: Open of `PGeo:sample_pgeo'
    using driver `PGeo' successful.
    
    Layer name: ...

Ressources
============

* `À propos des geodatabase d'ESRI <http://www.esri.com/software/arcgis/geodatabase/index.html>`_
* `[mdbtools-dev] les connexions sans DSN non géré ? <http://sourceforge.net/mailarchive/forum.php?thread_id=10463538&forum_id=5183>`_

Voir également
===============

* :ref:`gdal.ogr.formats.mdb`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 21551)
