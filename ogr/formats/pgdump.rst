.. _`gdal.ogr.formats.pgdump`:

Dump SQL pour PostgreSQL 
========================

(GDAL/OGR >= 1.8.0)

Ce pilote en écriture seul implémente la gestion de la génération de fichier dump 
SQL qui peut être injecté plus tard dans une instance live de PostgreSQL. Il gère 
la version étendue de PostgreSQL avec les géométries `PostGIS <http://www.postgis.org/">`_.

Ce pilote est très similaire à la commande shp2pgsql de PostGIS.

La plupart des options de création sont partagé avec le pilote normale PostgreSQL.

Le pilote ouvre le fichier en sortie via l'API VSIF Large, il est donc possible 
de définir /vsistdout/ comme fichier en sortie pour tout envoyer dans la sortie 
standard.

Options de création 
-------------------

Options de création de jeu de données
**************************************

* **LINEFORMAT :** par défaut les fichiers sont créés avec la convention de 
  terminaison de ligne de la plateforme locale (CR/LF sous win32 ou LF sur tous 
  les autres systèmes). 
  Cela peut être écrasé par l'utilisation de l'option de création de couche 
  LINEFORMAT qui peut avoir les valeurs **CRLF** (format DOS) ou **LF** (format Unix). 

Options de création de couche
******************************

* **GEOM_TYPE :** l'option de création de couche *GEOM_TYPE* peut être 
  définie à *Geometry*, "geography" (PostGIS >= 1.5), pour forcer le type de la géométrie 
  utilisée pour une table. "geometry" est la valeur par défaut.
* **LAUNDER :** Il peut être définie à *YES* pour forcer les nouveaux champs 
  crées sur cette couche à avoir les noms de champs "nettoyer" dans une forme 
  compatible avec PostgreSQL. Cela convertie en minuscule et convertie certains 
  caractères  spéciaux comme "-" et "#" en "_". Si *NO* les noms exacts seront 
  préservés. La valeur par défaut est *YES*. Si activé le nom de la table 
  (couche) sera également nettoyer.
* **PRECISION :** Il peut être définie à *YES* pour forcer la création de 
  nouveaux champs dans cette couche pour essayer de représenter l'information de 
  précision et longueur, si disponible en utilisant les types 
  *NUMERIC(width,precision)* ou *CHAR(width)*. Si *NO* alors les types *FLOAT8*, 
  *INTEGER* et *VARCHAR* seront utilisé à la place. *YES* pas défaut.
* **DIM={2,3} :** Contrôle la dimension de la couche. 3 par défaut. Important 
  à définir à 2 pour les couches 2D avec PostGIS 1.0+ puisqu'il a des 
  contraintes sur la dimension de la géométrie pendant le chargement.
* **GEOMETRY_NAME :** définie le nom de la colonne géométrique dans une 
  nouvelle table. S'il est omis, sera définie par défaut à *wkb_geometry* pour 
  GEOM_TYPE=geometry, ou *the_geog* pour GEOM_TYPE=geography..
* **SCHEMA :** Définie le nom du schéma pour une nouvelle table. L'utilisation 
  d'un même nom de couche dans un schéma différent est gérée, mais pas dans un 
  schéma public ou autres.
* **CREATE_SCHEMA :** (OGR >= 1.8.1) à utiliser en combinaison avec SCHEMA. Définie 
  à ON par défaut afin que l'instruction CREATE SCHEMA soit émise. Placez à OFF 
  pour empêcher CREATE SCHEMA d'être envoyée.
* **SPATIAL_INDEX :** définie à *ON* par défaut. Créé un index spatial sur la 
  colonne géométrique pour accélérer les requêtes. Définissez-la à *OFF* pour la 
  désactiver (a un effet seulement quand PostGIS est disponible).
* **TEMPORARY :** définie à OFF par défaut. Créé une table temporaire au lieu 
  d'une table permanente.
* **WRITE_EWKT_GEOM :** définie à OFF par défaut. Placez à ON pour écrire des 
  géométrie EWKT au lieu de géométries HEX. Cette option n'aura pas d'effet si la 
  variable d'environnement PG_USE_COPY est à YES.
* **CREATE_TABLE :** définie à ON par défaut afin que les tables soient recréées 
  si nécessaire. Placer à OFF pour désactiver cela et utiliser une structure de 
  table existante.
* **DROP_TABLE :** (OGR >= 1.8.1) définie à ON par défaut afin que les tables 
  soient détruites avant d'être recréées. Placer à OFF pour éviter que ``DROP TABLE`` 
  ne soit envoyé. Définissez le en IF_EXISTS dans le but d'émettre ``DROP TABLE 
  IF EXISTS`` (nécessite PostgreSQL >= 8.2).
* **SRID :** définie le SRID de la géométrie. -1 par défaut sauf si un SRS est 
  associé avec la couche. Dans ce cas, si le code EPSG est mentionné, il sera 
  utilisé comme SRID (Notez que la table spatial_ref_sys doit être correctement 
  remplie avec le SRID définie).

Variables d'environnement
**************************

* **PG_USE_COPY :** peut être à "YES" pour utiliser COPY lors de l'insertion des 
  données dans Postgresql. COPY est moins robuste que INSERT, mais est 
  significativement plus rapide.

Exemple
********

* translation simple d'un shapefile vers PostgreSQL dans un fichier abc.sql. 
  la table 'abc' sera créée avec les features à partir de abc.shp et les données 
  attributaires à partir de abc.dbf. Le SRID est spécifié. PG_USE_COPY est définie à 
  YES pour améliorer les performances.

  ::
    
    % ogr2ogr --config PG_USE_COPY YES -f PGDump abc.sql abc.shp -lco SRID=32631

* renvoyer la sortie du pilote PGDump vers la commande psql.
  ::
    
    % ogr2ogr --config PG_USE_COPY YES -f PGDump /vsistdout/ abc.shp | psql -d my_dbname -f -

Voir également
---------------

* :ref:`gdal.ogr.formats.pg`
* `Page principale de PostgreSQL <http://www.postgresql.org/>`_
* `PostGIS <http://www.postgis.org/>`_
* `Page d'exemple sur PostGIS / OGR Wiki <http://trac.osgeo.org/postgis/wiki/UsersWikiOGR>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 22137)