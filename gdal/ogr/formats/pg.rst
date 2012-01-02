.. _`gdal.ogr.formats.pg`:

PostgreSQL / PostGIS
=====================

Le pilote implémente la gestion de l'accès aux tables spatiales dans PostgreSQL 
étendue par la gestion des données spatiales PostGIS. Une gestion existe dans 
le pilote pour utiliser PostgreSQL sans `PostGIS`_ 
mais avec moins de fonctionnalité.

Ce pilote nécessite une connexion à une base Postgres. Si vous voulez préparer un 
dump SQL pour l'injecter plus tard dans une base Postgres, vous pouvez utiliser 
plutôt :ref:`gdal.ogr.formats.pgdump` (GDAL/OGR >= 1.8.0).

Vous pouvez trouver des informations additionnelles sur le pilote dans la page 
:ref:`gdal.ogr.formats.pg_advanced`.

Connexion à une base de données
-------------------------------

Pour se connecter à une source de données Postgres, utilisez une chaîne de 
connections définissant le nom de la base de données, avec autant de paramètres 
supplémentaires que nécessaire :
::
    
    PG:dbname=databasename

ou

::
    
    PG:"dbname='databasename' host='addr' port='5432' user='x' password='y'"

Il est également possible d'omettre le nom de la base de données et se connecter 
à celle par défaut, avec le même nom comme le nom d'utilisateur. 

.. note:: 
    on utilise *PQconnectdb()* pour réaliser la connexion, n'importe quelles 
    autres options et valeurs par défauts qui pourraient s'y appliquer, s'applique 
    au nom (référez vous à la documentation du serveur PostgreSQL ici pour 
    `PostgreSQL 8.4 <http://www.postgresql.org/docs/8.4/interactive/libpq-connect.html>`_).
    Le préfixe PG: est utilisé pour marquer le nom en tant que chaîne de connexion 
    postgres.

Les colonnes géométriques
---------------------------

Si la table *geometry_columns* existe, alors toutes les tables listées et les 
vues nommées seront traitées comme des couches OGR. Autrement toutes les tables 
utilisateurs attributaires seront traitées comme des couches.

À partir de GDAL 1.7.0, le pilote gère également la colonne de type 
`geography <http://postgis.refractions.net/documentation/manual-svn/ch04.html#PostGIS_Geography>`_ 
introduit dans PostGIS 1.5.

Requêtes SQL
------------

Le pilote PostgreSQL envoie les commandes SQL directement à PostgreSQL par 
défaut, plutôt que de les évaluer en interne lors de l'utilisation de l'appel 
*ExecuteSQL()* sur *OGRDataSource*, ou l'option en ligne de commande *-sql* 
pour ``ogr2ogr``. Les expressions des requêtes attributaires sont également 
envoyées à PostgreSQL. Il est aussi possible de questionner le pilote pour 
prendre en charge les commandes avec le moteur :ref:`gdal.ogr.sql`, en passant 
la chaine *OGRSQL* à la méthode *ExecuteSQL()*, comme nom du dialecte SQL.

Le pilote PostgreSQL dans OGR gère les appels *OGRDataSource::StartTrasaction()*, 
*OGRDataSource::CommitTransaction()* et *OGRDataSource::RollbackTransaction()* 
dans le sens normal de SQL.

Problèmes lors de la création
------------------------------

Le pilote PostgreSQL ne gère pas la création de nouveau jeu de données (une 
base de données dans PostgreSQL), mais il permet la création de nouvelles 
couches dans une base de données existante.

Comme mentionné au-dessus, le système du type est pauvre, et plusieurs types 
d'OGR ne sont pas mappés correctement dans PostgreSQL.

Si la base de données a les types PostGIS chargés (c'est à dire le type 
*geometry*) les nouvelles couches crées seront crées avec le type géométrique de 
PostGIS. Autrement elles utiliseront un type OID. Par défaut il est supposé que 
le texte envoyé à Postgres est encodé au format UTF-8. Cela convient pour 
l'ASCII, mais peut entrainer des erreurs pour les caractères étendus (ASCII 155+ 
par exemple). Bien que OGR ne fournisse aucun contrôle direct pour cela, vous 
pouvez définir la variable d'environnement *PGCLIENTENCODING* pour indiquer le 
format qui est utilisé. Par exemple, si votre texte est LATIN1 vous pouvez 
définir la variable d'environnement à LATIN1 avant d'utiliser OGR et les données 
en entrées seront supposées être en LATIN1 au lieu de UTF-8.

Un moyen alternatif pour définir l'encodage du client est d'utiliser la commande 
SQL suivante avec *ExecuteSQL()* : "``SET client_encoding TO encoding_name``" où 
*encoding_name* est LATIN1, etc.

Les erreurs peuvent être récupérées en englobant cette commande avec la paire 
*CPLPushErrorHandler()/CPLPopErrorHandler()*.

Options de création de jeu de données
*************************************

Aucune.

Options de création de couches
********************************

* **GEOM_TYPE :** l'option de création de couche *GEOM_TYPE* peut être 
  définie à *Geometry*, "geography" (PostGIS >= 1.5), *BYTEA* ou *OID* pour forcer le type de la géométrie 
  utilisée pour une table. Pour une base de données PostGIS, "geometry" est la 
  valeur par défaut.
* **OVERWRITE :** Il peut être définie à *YES* pour forcer une couche 
  existante du nom désiré à être détruite avant la création de la couche demandée.
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
  schéma public ou autres. Notez que l'utilisation de l'option *-overwrite* 
  de ``ogr2ogr`` et de l'option *-lco SCHEMA=* en même temps ne fonctionnera 
  pas, puisque la commande ``ogr2ogr`` ne comprendra pas que la couche existante 
  doit être détruite dans le schéma défini. Utilisez l'option *-nln* de 
  ``ogr2ogr`` à la place, ou mieux la chaîne de connexion *active_schema*.  
  Voir ci-dessous les exemples.
* **SPATIAL_INDEX :** (à partir de GDAL 1.6.0) Définie à *ON* par défaut. 
  Créer un index spatial sur la colonne géométrique pour accélérer les requêtes. 
  Définissez-la à *OFF* pour la désactiver (a un effet seulement quand PostGIS 
  est disponible).
* **TEMPORARY :** (à partir de GDAL 1.8.0) définie à OFF par défaut. créé une table 
  temporaire au lieu d'une table permanente.
* **NONE_AS_UNKNOWN :** (à partir de GDAL 1.8.1) peut être définie à TRUE pour 
  forcer les couches non-spatiales (wkbNone) à être créées comme table spatiale 
  de type GEOMETRY (wkbUnknown), qui était le comportement avant GDAL 1.8.0. NO 
  par défaut, auquel cas une table régulière est créée et non enregistré dans la 
  table geometry_columns de PostGIS.
* **FID :** (à partir de GDAL 1.9.0) nom de la colonne FID à créer. 'ogc_fid' par 
  défaut.
* **EXTRACT_SCHEMA_FROM_LAYER_NAME :** (à partir de GDAL 1.9.0) peut être définie 
  à NO pour éviter de considérer le caractère "." comme séparateur entre le schéma 
  et le nom de la table. YES par défaut.

Options de configuration
*************************

Il y a une variété d'`options de configuration <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 
qui aide à contrôler le comportement de ce pilote.

* **PG_USE_COPY :** il peut être à "YES" pour utiliser *COPY* pour l'insertion 
  de données dans PostgreSQL. ''COPY'' est moins robuste que *INSERT*, mais 
  significativement plus rapide.
* **PGSQL_OGR_FID :** définie le nom d'une clé primaire au lieu de 'ogc_fid'.
  Utiliser seulement lors de l'ouverture d'une couche dont la clé primaire ne 
  peut pas être autodétectée.
  Ignoré par *CreateLayer()* qui utilise l'option de création FID.
.. Little interest to advertize PG_USE_TEXT... Just to keep it mind it exists for example for debugging
.. * **PG_USE_TEXT :** (GDAL >= 1.8.0) If set to "YES", geometries will be 
.. fetched as text instead of their default HEXEWKB form.
* **PG_USE_BASE64 :** (GDAL >= 1.8.0) si définie à "YES", les géométries seront 
  récupérées encodées en EWKB BASE64 au lieu de la forme canonique EWKB HEX.
  Cela réduit la quantité de données transférée de 2 N à 1.333 N, où N est la 
  taille des données EWKB. Cependant, cela peut être un peu plus lent que récupérer 
  la forme canonique quand le client et le serveur sont sur la même machine, la 
  valeur par défaut est donc NO.

Exemples
---------

* Des traductions simples de shapefile dans PostgreSQL. la table 'abc' sera crée 
  avec les géométries de *abc.shp* et les attributs de *abc.dbf*. L'instance de 
  base de données (warmerda) doit déjà exister, et la table *abc* ne doit pas 
  être crée.
  ::
    
    % ogr2ogr -f PostgreSQL PG:dbname=warmerda abc.shp

* Ce second exemple charge une couche des limites des pays à partir d'un VPF 
  (via le pilote OGDI), et renomme le nom énigmatique de la couche OGDI en un 
  nom plus lisible. Si une table existante du nom désiré existe, elle sera écrasée.
  ::
    
    % ogr2ogr -f PostgreSQL PG:dbname=warmerda \
              gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia \
              -lco OVERWRITE=yes -nln polbndl_bnd 'polbndl@bnd(*)_line'

* Dans cet exemple nous fusionnons des données lignes tiger de deux répertoires 
  différents de fichier tiger dans une table. Notez que la seconde invocation 
  utilise *-append* et pas *OVERWRITE=yes*.
  ::
    
    % ogr2ogr -f PostgreSQL PG:dbname=warmerda tiger_michigan \
           -lco OVERWRITE=yes CompleteChain
    % ogr2ogr -update -append -f PostgreSQL PG:dbname=warmerda tiger_ohio \
           CompleteChain

* Cet exemple montre l'utilisation d'``ogrinfo`` pour évaluer une commande de 
  requête SQL dans PostgreSQL. Des requêtes PostGIS plus sophistiquées peuvent 
  être utilisées également via la commande -sql dans ``ogrinfo``.
  ::
    
    ogrinfo -ro PG:dbname=warmerda -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

* Cet exemple montre l'utilisation de ``ogrinfo`` pour lister les couches 
  PostgreSQL/PostGIS sur un hôte différent.
  ::
    
    ogrinfo -ro PG:'host=myserver.velocet.ca user=postgres dbname=warmerda'

FAQ
*****

* Pourquoi ne puis pas voir mes tables ? PostGIS est installé et j'ai des données.
    Vous devez avoir les permissions sur toutes les tables que vous voulez lire 
    *et* geometry_columns et spatial_ref_sys.
    
    Un comportement erroné peut ne renvoyer aucun message d'erreur si vous n'avez 
    pas la permission à ces tables. Les problèmes de permission sur les tables 
    *geometry_columns* et/ou *spatial_ref_sys* peut être généralement confirmés 
    si vous pouvez voir les tables en définissant l'option de configuration 
    *PG_LIST_ALL_TABLES* à YES. (par exemple ``ogrinfo --config PG_LIST_ALL_TABLES YES PG:xxxxx``).

Lisez également
----------------

* :ref:`gdal.ogr.formats.pg_advanced`
* :ref:`gdal.ogr.formats.pgdump`
* `Page principale de PostgreSQL <http://www.postgresql.org/>`_
* `PostGIS <http://postgis.org/>`_
* `PostGIS en Français <http://postgis.fr>`_
* `Page d'exemples dans le wiki sur PostGIS / OGR <http://trac.osgeo.org/postgis/wiki/UsersWikiOGR>`_


.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 22801)
