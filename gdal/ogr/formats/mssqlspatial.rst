.. _`gdal.ogr.formats.mssqlspatial`:

MSSQLSpatial - Microsoft SQL Server Spatial Database
====================================================

Ce pilote implémente la gestion de l’accès aux tables spatiales dans Microsoft SQL 
Server 2008+ qui contiennent les types de données géométriques et géographiques 
pour représenter les colonnes géométrie.

Se connecter à une base de données
------------------------------------

Pour se connecter à un source de données MSSQL, utilisez une chaîne de connexion 
définissant le nom de la base de données avec des paramètres supplémentaires si 
nécessaire. La chaîne de connexion doit être préfixé par '*MSSQL:*'.
::
    
    MSSQL:server=.\MSSQLSERVER2008;database=dbname;trusted_connection=yes

En plus des paramètres standards du format de la 
`chaîne de connexion <http://msdn.microsoft.com/en-us/library/ms130822.aspx>`_ 
les paramètres personnalisés suivants peuvent également être utilisés avec la 
syntaxe suivante :

* **Tables=schema1.table1(geometry column1),schema2.table2(geometry column2) :** 
    en utilisant ce paramètre vous pouvez définir le sous jeu de données des 
    couches à utiliser par le pilote. Si ce paramètre n'est pas définie, les 
    couches sont récupérées à partir de la table de métadonnées *geometry_column*. 
    vous pouvez omettre de spécifier la partie sur le schéma et la colonne 
    géométrique de la syntaxe.
* **GeometryFormat=native|wkb|wkt :** 
    Le format désiré dans lequel les géométries doivent être récupérées à partir 
    du serveur. La valeur par défaut est '*native*' dans ce cas le format de 
    sérialisation natif SqlGeometry et SqlGeography est utilisé. Lors de 
    l'utilisation de '*wkb*' ou '*wkt*' la représentation de la géométrie est 
    convertie en '*Well Known Binary*' et '*Well Known Text*' dans le serveur. 
    Cette conversion nécessite une surcharge significative côté serveur et rend 
    l'accès aux features plus lente qu'en utilisant le format natif.

Les noms des paramètres ne sont pas sensible à la casse dans la chaîne de 
connexion. La définition du paramètre **Database** est nécessaire pour le pilote 
afin de sélectionner la base de données correctement.

Requêtes SQL
-------------

Le pilote MS SQL Spatial envoie les requêtes SQL directement à MS SQL par défaut, 
plutôt que de les évaluer en interne en utilisant l'appel à *ExecuteSQL()* du 
*OGRDataSource*, ou l'option de la commande *-sql* d'``ogr2ogr``. Les expressions 
des requêtes attributaires sont aussi envoyé directement à MSSQL. Il est aussi 
possible de demander au pilote MSSQL d'OGR de prendre en charge les commandes SQL 
avec le moteur :ref:`gdal.ogr.sql`, en passant la chaîne **"OGRSQL"** à la méthode 
*ExecuteSQL()*, comme le nom du dialect SQL.

Le pilote MSSQL dans OGR gère les appels *OGRLayer::StartTrasaction()*, 
*OGRLayer::CommitTransaction()* et *OGRLayer::RollbackTransaction()* dans le 
sens normal de SQL.

Problèmes lors de la création
-----------------------------

Ce pilote ne gère pas la création d'une nouvelle base de données, vous devrez 
utiliser l'*Outils client du Serveur Microsoft SQL* pour cela, mais il permet la 
création de nouvelles couches dans une base existante.

Options de création de couche
*****************************

* **GEOM_TYPE**: l'option de création *GEOM_TYPE* peut être définie parmi 
  "geometry" ou "geography". Si cette option n'est pas définie la valeur par 
  défaut est "geometry". Pour créer la colonne géométrie de type "geography", 
  ce paramètre doit être définie en "geography". Dans ce cas, la couche doit 
  avoir une référence spatiale valide de l'un des systèmes de coordonnées 
  géographiques définies dans la table de métadonnées du serveur SQL 
  **sys.spatial_reference_systems**. Les systèmes de coordonnées projetées ne 
  sont pas pris en charge dans ce cas.
* **OVERWRITE**: doit être à "YES" pour forcer une couche existante au nom définie 
  à être détruite avant la création de la couche demandée.
* **LAUNDER**: doit être à "YES" pour forcer le nettoyage des nouveaux champs 
  créés dans cette couche dans une forme compatible avec MSSQL. Cela les convertie 
  en minuscule et certains caractères spéciaux comme "-" et "#" en "_". Si "NO" 
  les noms exactes sont préservés.
  La valeur par défaut est "YES". Si activé le nom de la table (couche) sera 
  aussi nettoyer.
* **PRECISION**: doit être à "YES" pour forcer les nouveaux champs créés sur cette 
  couche de tenter et de représenter les informations sur la largeur et la 
  précision, si disponible en utilisant les types *numeric(width,precision)* ou 
  *char(width)*. Si "NO" alors les types *float*, *int* et *varchar* seront 
  utilisé. La valeur par défaut est "YES".
* **DIM={2,3}**: contrôle la dimension de la couche.  3 par défaut.
* **GEOM_NAME**: définie le nom de la colonne géométrique dans la nouvelle table. 
  si omis par défaut *ogr_geometry*.
* **SCHEMA**: définie le nom du schéma pour la nouvelle table.
  Si ce paramètre n'est pas géré le schéma par défaut est "*dbo"*.
* **SRID**: définie l'id de la référence spatiale de la nouvelle table 
  explicitement. L'entrée correspondante doit déjà existé dans la table de 
  métadonnées *spatial_ref_sys*. Si ce paramètre n'est pas définie le SRID est 
  dérivé à partir du code d'autorité du SRS de la couche source.

Création d'index spatial
************************

Par défaut le pilote MS SQL Spatial ne créé par d'index spatiaux pour la table 
pendant la création de la couche. Cependant vous devez créer un index spatial en 
utilisant l'option sql suivante :

::
    
    create spatial index on schema.table

L'index spatial peut aussi être supprimé en utilisant la syntaxe suivante :
::
    
    drop spatial index on schema.table

Exemples
---------

Créer une couche à partir d'un source de données OGR :
::
    
    ogr2ogr -overwrite -f MSSQLSpatial "MSSQL:server=.\MSSQLSERVER2008;database=geodb;trusted_connection=yes" "rivers.tab"

Se connecter à une couche et dumper son contenu :
::
    
    ogrinfo -al "MSSQL:server=.\MSSQLSERVER2008;database=geodb;tables=rivers;trusted_connection=yes"

Créer un index spatial :
::
    
    ogrinfo -sql "create spatial index on rivers" "MSSQL:server=.\MSSQLSERVER2008;database=geodb;trusted_connection=yes"

.. yjacolin at free.fr, Yves Jacolin - 2011/08/02 (trunk 21578)