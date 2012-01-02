.. _`gdal.ogr.formats.mysql`:

MySQL
======

Le pilote implémente l'accès en lecture et écriture pour les données spatiale 
dans les tables `MySQL <http://www.mysql.org/>`_.  Cette fonctionnalité a été 
introduite dans GDAL/OGR 1.3.2.

Lors de l'ouverture d'une base de données, son nom doit être définie sous la 
forme "MYSQL:dbname[,options]" où *options* peut inclure des informations 
séparées par des virgules comme "user=*userid*", "password=*password*", 
"host=*host*" et "port=*port*".

De même, une option "tables=*table*;*table*..." peut être ajouté pour 
restreindre l'accès à une liste spécifique de tables dans la base de données. 
Cette option est d'abord utile lorsqu'une base de données contient beaucoup de 
tables, et scanner tout le schéma prendrait beaucoup de temps.

Pour l'instant toutes les tables habituelles sont supposées être des couches 
d'un point de vue d'OGR., avec les noms des tables comme nom de couche. Les vues 
nommées ne sont pas gérées pour l'instant.

Si un champ d'entier simple est une clé primaire, il sera utilisé comme FID 
autrement le FID sera assigné séquentiellement et la recherche par FID sera 
extrêmement lente.

Par défaut, les requêtes SQL sont passé directement au moteur de base de 
données MySQL. Il est également possible de questionner le pilote pour prendre 
en charge les commandes SQL avec le [[ogr_sql|moteur SQL d'OGR]], en passant 
la chaine "OGRSQL" à la méthode *ExecuteSQL()*, en tant que nom du dialecte 
SQL.

Avertissements
--------------

* Dans le cas d'une couche définie par une commande SQL, les champs soit qui 
  sont nommés "OGC_FID" soit ceux qui sont définie NOT NULL, ceux qui sont une 
  clé primaire (*PRIMARY KEY*), et ceux qui sont un champ de type entier seront 
  supposé être un FID.
* Les champs géométriques sont lu à partir de MySQL en utilisant le format WKB. 
  Les version plus ancienne que 5.0.16 de MySQL sont connus pour avoir un 
  problème avec certaine génération de WKB et peuvent ne pas fonctionner 
  proprement.
* La colonne OGR_FID, qui peut être écrasée avec l'option de création de couche 
  MYSQL_FI, est implémenté comme un champ *INT UNIQUE NOT NULL AUTO_INCREMENT*. 
  Cela semble créer implicitement un index sur le champ.
* la colonne géométrique, par défaut à *SHAPE* et qui peut être écrasée avec 
  l'option de création de couche *GEOMETRY_NAME*, est crée comme une colonne 
  NOT NULL à moins que SPATIAL_INDEX soit désactivé. Par défaut, un index 
  spatial est crée au moment de la création de la table.
* L'information SRS est stocké en utilisant *Simple Features* de l'OGC, avec la 
  création des tables de méta-données *geometry_columns* et *spatial_ref_sys* 
  dans la base de données définies si elles ne le sont pas déjà. La table 
  *spatial_ref_sys* n'est pas pré-rempli avec les valeurs EPSG et SS comme 
  PostGIS. Si aucun code EPSG n'ait présent  pour une table donnée, la valeur 
  MAX(SRID) sera utilisée.
* Le timeouts de la connection au serveur peut être définie par la variable 
  d'environnement*MYSQL_TIMEOUT*. Par exemple, *SET MYSQL_TIMEOUT=3600*. Il est 
  possible que cette variable ait un impact seulement quand le système du 
  serveur MySQL est Windowss.
* Le pilote MySQL ouvre une connection à la base de données en utilisant le 
  mode *CLIENT_INTERACTIVE*. Vous pouvezajuster ce paramètre 
  (*interactive_timeout*) dans le fichier *mysql.ini* ou *mysql.cnf* de votre 
  serveur.
* Nous utilisons le WKT pour insérer les géométries dans la base de données. Si 
  vous insérez de grosse géométrie, vous devez faire attention du paramètre 
  *max_allowed_packet* dans la configuration MySQL. Par défaut, il est définie 
  à 1 M, mais cela peut ne pas être asse important pour les très grosses 
  géométries. Si vous obtenez un message d'erreur du type : *Got a packet bigger 
  than 'max_allowed_packet' bytes*, vous devez augmenter ce paramètre.

Problèmes de création
---------------------

Le pilote MySQL ne gère pas la création de nouveaux jeu de données (une base de 
données dans MySQL), mais il permet la création de nouvelles couches dans une 
base existante.

Par défaut, le pilote MySQL tentera de préserver la précision des géométries OGR 
lors de la création et la lecture des couches MySQL. Pour les champs d'entier 
avec une longueur définie, il utilisera DECIMAL comme type de champ MySQL avec 
une précision définie de 0. Pour les champs de type réel, il utilisera DOUBLE 
de largeur et précision définie. Pour les champs caractères avec une largeur 
définie, VARCHAR sera utilisé.

Le pilote MySQL n'essaye pas de comprendre l'encodage des caractères pour le 
moment.

Le pilote MySQL n'est pas transactionnel pour le moment.

Options de création de couche
-----------------------------

* **OVERWRITE :** elle peut être définie à "YES" pour forcer les couches 
  existantes de même nom à être détruite avant la création de la couche demandée.
* **LAUNDER :** elle peut être définie à "YES" pour forcer les champs crées à 
  avoir leur nom traduit sous une forme plus compatible avec MySQL. Cela les 
  convertit en minuscule et certains caractères spéciaux comme "-" et "#" en 
  "_". Si "NO" les noms exacts sont préservés. La valeur par défaut est "YES".
* **PRECISION :** elle peut être à "TRUE" pour tenter de préserver la largeur et 
  la précision des champs lors de la création et la lecture des couches MySQL. 
  La valeur par défaut est "TRUE".
* **MYSQL_GEOM_COLUMN :** cette option définie le nom de la colonne géométrique. 
  La valeur par défaut est "SHAPE".
* **MYSQL_FID :** cette option définie le nom de la colonne FID. La valeur par 
  défaut est "OGR_FID"
* **SPATIAL_INDEX :** elle peut être définie "NO" pour arrêter la création 
  automatique d'un index spatial sur la colonne géométrique, permettant des 
  géométries NULL et probablement un chargement plus rapide.
* **ENGINE :** définie optionnellement le moteur de la base de données à 
  utiliser. Pour MySQL 4.x cela doit être définie à MyISAM pour les tables 
  spatiales.

L'exemple suivant du nom de la source de données ouvre le schéma *westholland* 
de la base de données dont le mot de passe est *psv9570* pour l'utilisateur 
*root* sur le port 3306. Aucune nom d'hôte n'est fournit, donc localhost est 
utilisé. La directive *table=* est scanné et présenté comme la couche à utiliser.
::
    
    MYSQL:westholland,user=root,password=psv9570,port=3306,tables=bedrijven

L'exemple suivant utilise ogr2ogr pour créer une copie de la couche des 
frontières mondiales à partir d'une shapefile dans une table MySQL. Il écrase 
la table *borders2* existante, définie une option lors de la création pour 
définir le nom de la colonne géométrique *SHAPE2*.
::
    
    ogr2ogr -f MySQL MySQL:test,user=root world_borders.shp -nln borders2 -update -overwrite -lco GEOMETRY_NAME=SHAPE2 

L'exemple suivant utilise ogrinfo pour renvoyer des informations synthétique 
sur la couche *borders2* dans la base de données *test* :
::
    
    ogrinfo MySQL:test,user=root borders2 -so

        Layer name: borders2
        Geometry: Polygon
        Feature Count: 3784
        Extent: (-180.000000, -90.000000) - (180.000000, 83.623596)
        Layer SRS WKT:
        GEOGCS["GCS_WGS_1984",
            DATUM["WGS_1984",
                SPHEROID["WGS_84",6378137,298.257223563]],
            PRIMEM["Greenwich",0],
            UNIT["Degree",0.017453292519943295]]
        FID Column = OGR_FID
        Geometry Column = SHAPE2
        cat: Real (0.0)
        fips_cntry: String (80.0)
        cntry_name: String (80.0)
        area: Real (15.2)
        pop_cntry: Real (15.2)

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 21:39 (trunk 11456)