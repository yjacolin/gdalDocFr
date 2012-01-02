.. _`gdal.ogr.formats.odbc`:

ODBC RDBMS
===========

OGR gère en option les tables spatiales et non spatiales accédé via ODBC. ODBC 
est une couche d'accès générique pour l'accès à plusieurs systèmes de bases de 
données, et les données qui peuvent être représentée sous forme de base de 
données (collection de tables). La gestion d'OBDC est potentiellement disponible 
sous les plateformes Unix et Windows, mais est seulement inclus dans les 
compilations Unix par des options spéciales de configuration.

Les sources de données sont accédé en utilisant le nom de la source de données 
sous la forme *ODBC:userid/password@dsn,schema.tablename(geometrycolname),...:srs_tablename(sridcolumn,srtextcolumn)*. 
Avec des paramètres optionnels  comme ceux qui suivent sont aussi disponible :

* *ODBC:userid/password@dsn*
* *ODBC:userid@dsn,table_list*
* *ODBC:dsn,table_list*
* *ODBC:dsn*
* *ODBC:dsn,table_list:srs_tablename*

Le dsn est le nom de la source de données d'ODBC. Normalement les sources de 
données ODBC sont configurées en utilisant un outil d'Administration d'ODBC et 
assigne un DSN. Ce DSN est ce qui est utilisé pour accéder à la source de données.

Par défaut ODBC recherche la table *GEOMETRY_COLUMNS*. Si elle est trouvée elle 
est utilisée pour identifier l'ensemble des tables spatiales qui doivent être 
traitées comme couches par OGR. Si elle n'est pas trouvée, alors toutes les 
tables dans la source de données sont renvoyé comme des couches non spatiales. 
Cependant, si une liste de table (une liste séparé par des virgules de noms de 
table) est fournie, alors seule ces tables seront représentées comme couches 
(non-spatial). Cherchez l'ensemble des définitions de toutes les tables dans 
une base de données complexe peut être consommatrice de temps, la possibilité 
de restreindre l'ensemble des tables à accéder est donc d'abord un problème de 
performance.

Si la table *GEOMETRY_COLUMNS* est trouvée, elle est utilisée pour sélectionner 
la colonne pour la source de la géométrie. Si les tables sont passées dans le 
nom de la source de données, alors la colonne géométrique associée avec une 
table peut être inclus entre parenthèses après le nom de la table. Il y a pour 
l'instant l'hypothèse codée en dur que la géométrie est au format Well Known 
Binary (WKB) si le champ est binaire, ou Well Known Text (WKT) sinon. La table 
*GEOMETRY_COLUMNS* doit avoir au moins les colonnes *F_TABLE_NAME*, 
*F_GEOMETRY_COLUMN* et *GEOMETRY_TYPE*.

Si la table a une colonne géométrique, et possède des champs appelés *XMIN*, 
*YMIN*, *XMAX* et *YMAX* alors les requêtes directes sur la table avec un 
filtre spécial accélère la requête spatiale. Les champs *XMIN*, *YMIN*, *XMAX* 
et *YMAX* doivent représenter l'étendue de la géométrie de la ligne dans le 
système de coordonnées de la table.

Par défaut, les commandes SQL sont envoyées directement au moteur de la base de 
données sous-jacent. Il est également possible de lancer une requête au pilote 
pour prendre en charge les commandes SQL avec le moteur :ref:`gdal.ogr.sql`, en 
passant la chaine "OGRSQL" à la méthode *ExecuteSQL()*, comme nom du dialecte SQL.

Problèmes de création
----------------------

Pour l'instant le pilote ODBC d'OGR est ne lecture seule, les applications 
utilisant OGR ne peuvent donc pas créer de nouvelles géométries, tables et 
sources de données. Cette limitation sera supprimé dans le futur.

Lisez également
----------------

* `Référence de l'API ODBC MSDN <http://msdn.microsoft.com/en-us/library/ms714562(VS.85).aspx">MSDN ODBC API Reference>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 17870)