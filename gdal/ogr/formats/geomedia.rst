.. _`gdal.ogr.formats.geomedia`:

Base de données MDB de Geomedia
================================

GDAL/OGR >= 1.9.0

OGR gère en option la lecture des fichiers .mdp de Geomedia via ODBC. Geomedia 
est une base de données Microsoft Access avec un ensemble de tables définies par 
Intergraph pour prendre en charge les métadonnées de la géodatabase, et des 
géométries pour la gestion des features dans une colonne BLOB dans un format 
particulier. Ce pilote accède à la base de données via ODBC mais ne dépend d'aucune 
couche middleware d'Intergraph.

Les fichiers .mdb de Geomedia sont accéder en passant le nom du fichier .mdb que 
l'on veut lire comme source de données. Sur Windows, aucun DSN ODBC n'est requis.
Sous linux, il y a des problèmes avec les connexions sans DSN dû à une 
implémentation de cette fonctionnalité buguée ou incomplète dans 
l'`outils MDB <http://mdbtools.sourceforge.net/>`_, il est donc nécessaire de 
configurer le Data Source Name (DSN) si le pilote de l'outil MDB est utilisé 
(vérifiez les instructions ci-dessous).

Dans le but de faciliter la compatibilité avec différentes configurations, l'option 
de configuration *GEOMEDIA_DRIVER_TEMPLATE* a été ajoutée pour fournir un moyen 
pour définir le DSN automatiquement avec le nom du fichier comme argument. Dans 
les cas où le nom du pilote est connu, cela permet la construction du DSN basé 
sur cette information d'une manière similaire à la valeur par défaut (utilisé 
pour l'accès Windows au pilote Microsoft Access).

OGR traite toutes les tables de features comme des couches. La plupart des types 
de géométries devrait être gérées (arcs ne l'est pas encore). Les informations 
du système de projection n'est pas géré pour l'instant.

Pour le moment le pilote de géodatabase Personnelle d'OGR ne tire aucun avantage 
des indexes spatiaux pour les requêtes spatiales rapides.

Par défaut, les commandes SQL sont envoyées directement au moteur de base de 
données MDB. Il est également possible d'interroger le pilote pour prendre en 
charge les commandes SQL avec le moteur :ref:`gdal.ogr.sql`,  en passant la chaîne 
**"OGRSQL"** à la méthode *ExecuteSQL()* comme nom du dialect SQL.

Comment utiliser le pilote Geomedia avec unixODBC et les outils MDB (sous Unix et Linux)
-----------------------------------------------------------------------------------------

À partir de  GDAL/OGR 1.9.0, le pilote :ref:`gdal.ogr.formats.mdb` est une 
alternative pour la lecture des fichiers .mdb de Geomedia sans nécessité 
unixODBC et les outils MDB.

Référez vous à la section similaire du pilote :ref:`gdal.ogr.formats.pgeo`. Le 
préfixe à utiliser pour ce pilote est *Geomedia:*.

Voir également
---------------

* :ref:`gdal.ogr.formats.mdb`

.. yjacolin at free.fr, Yves Jacolin - 2011/07/10 (trunk 21551)