.. _`gdal.ogr.sql`:

=============
SQL dans OGR
=============

*OGRDataSource* gère l'exécution de commandes en opposition à la source de 
données via la méthode *OGRDataSource::ExecuteSQL()*. Bien qu'en théorie 
n'importe quelle commande peut être prise en charge de cette manière, en 
pratique le mécanisme est utilisé pour fournir un sous ensemble des possibilités 
de SELECT de SQL aux applications. Cette page discute de l'implémentation de 
SQL générique dans OGR, et des problèmes avec la gestion des SQL spécifique au 
pilote.

Syntaxe SQL gérée
===================

La classe *OGRLayer* gère également l'application d'un filtre de requête 
attributaire aux features retournées en utilisant la méthode 
*OGRLayer::SetAttributeFilter()*. La syntaxe pour le filtre attributaire est la 
même que la clause WHERE dans la requête SELECT du SQL d'OGR. Donc tout ce 
qui concerne ici la clause WHERE s'applique également dans le contexte de la 
méthode *SetAttributeFilter()* 

.. note:: 
    OGR SQL a été implémenté pour la version 1.8.0 de GDAL/OGR. Plusieurs 
    fonctionnalités présentées ci-dessous, notamment les expressions arithmétiques 
    et les expressions dans la liste des champs, n'étaient pas gérées dans la 
    version 1.7.x ou plus ancienne de GDAL/OGR. Voyez la RFC 28 pour les détails 
    des nouvelles fonctionnalités dans la version 1.8.0 de GDAL/OGR.


SELECT
=======

La requête SELECT est utilisée pour récupérer les objets d'une couche (analogue 
aux lignes des tables dans un RDBMS) avec le résultat de la requête représentée 
comme une couche temporaire d'objets. Les couches de la source de données sont 
analogues aux tables dans un RDBMS et les attributs des objets sont analogues 
aux valeurs des colonnes. La forme la plus simple d'une requête SELECT du SQL 
d'OGR ressemble à cela :

::
    
    SELECT * FROM polylayer

Dans ce cas tous les objets sont récupérés de la couche nommée *polylayer*, et 
tous les attributs de ces objets sont renvoyés. C'est essentiellement équivalent 
à accéder à la couche directement. Dans cet exemple l'"*" est la liste de tous 
les champs à récupérer de la couche, avec "*" signifiant que tous les champs sont 
récupérés.

Cette forme sensiblement plus sophistiquée renvoie encore tous les objets d'une 
couche mais le schéma contiendra les attributs *EAS_ID* et *PROP_VALUE*. 
N'importe quel attribut sera ignoré.

::
    
    SELECT eas_id, prop_value FROM polylayer


Un SELECT un petit peu plus ambitieux, restreignant les objets récupérés avec 
une clause WHERE et classant les résultats, ressemblera à ceci :

::
    
    SELECT * from polylayer WHERE prop_value > 220000.0 ORDER BY prop_value DESC

Cette requête SELECT produira une table avec juste un objet, avec un attribut 
(nommé *count_eas_id*) contenant le nombre de valeur distincte des attributs 
*eas_id*.
::
    
    SELECT COUNT(DISTINCT eas_id) FROM polylayer


Opérateurs de liste de champs
------------------------------

La liste de champs est une liste séparée par des virgules de champs pour 
rapporter les objets en sortie de la couche source. Ils apparaitront sur les 
objets en sortie dans l'ordre où ils apparaissent dans la liste des champs, 
cette liste peut donc être utilisé pour ré-ordonner les champs.

Une forme spéciale de la liste des champs utilise le mot-clé DISTINCT. Cela 
renvoie une liste de valeurs distinctes de l'attribut nommé. Quand le mot-clé 
DISTINCT est utilisé, seulement un attribut peut apparaitre dans la liste. Ce 
mot-clé peut être utilisé avec n'importe quel type de champ. Pour l'instant le 
test pour faire la distinction entre les valeurs est sensible à la casse dans 
le SQL d'OGR. Le résultat d'un SELECT avec le mot-clé DISTINCT est une couche 
avec une colonne (nommé de la même manière que le champs sur lequel la sélection 
s'opère), et un objet par valeur distinct. Les géométries sont ignorées. Les 
valeurs distinctes sont assemblée en mémoire, donc cela peut utiliser beaucoup 
de mémoire pour des jeux de données avec un grand nombre de valeurs distinctes.

::
    
    SELECT DISTINCT areacode FROM polylayer


Il y a également plusieurs opérateurs de synthèse qui peuvent être appliqués aux 
colonnes. Quand un opérateur de synthèse est appliqué à un champ, alors un 
opérateur de synthèse doit être appliqué sur tous les champs. Les opérateurs de 
synthèses sont COUNT (compte le nombre d'instance), AVG (moyenne arithmétique), 
SUM (somme numérique), MIN (sémantique ou minimum numérique) , et MAX 
(sémantique ou maximum numérique). Cet exemple produit diverses informations de 
synthèse sur les valeurs des propriétés des parcelles :

::
    
    SELECT MIN(prop_value), MAX(prop_value), AVG(prop_value), SUM(prop_value), 
       COUNT(prop_value) FROM polylayer WHERE prov_name = "Ontario"


Un cas spécial, on peut donner l'argument "*" à l'opérateur COUNT() à la place 
du nom du champs qui est une forme raccourcit pour compter tous les 
enregistrements bien qu'il donnera le même résultat en utilisant n'importe quels 
noms de colonne. Il est également possible d'appliquer l'opérateur COUNT() à un 
SELECT DISTINCT pour obtenir le nombre de valeurs distinctes, par exemple :

::
    
    SELECT COUNT(DISTINCT areacode) FROM polylayer


Les noms des champs peuvent également être préfixé par le nom d'une table bien 
que cela soit réellement significatif que pour les jointures. Cela est démontré 
plus loin dans la section JOIN.

Les définitions de champs peuvent aussi être des expressions complexes en 
utilisant des opérateurs arithmétiques et fonctionnels. Cependant, le mot-clé 
DISTINCT, et les opérateurs d'agrégation MIN, MAX, AVG et SUM ne peuvent pas être 
appliqués aux expressions de champs.

::
    
    SELECT cost+tax from invoice
ou

::
    
    SELECT CONCAT(owner_first_name,' ',owner_last_name) from properties


Utiliser les alias des noms de champs
--------------------------------------

SQL d'OGR gère le renommage des champs en suivant la spécifications SQL92 en 
utilisant le mot-clé AS comme pour l'exemple suivant :

::
    
    SELECT *, OGR_STYLE AS 'STYLE' FROM polylayer


L'alias du nom du champ peut être utilisé comme la dernière opération dans la 
spécification de la colonne. Par conséquent nous ne pouvons pas renommer les 
champs à l'intérieure d'un opérateur, mais nous pouvons renommer toute 
l'expression de la colonne, comme ces deux exemples :

::
    
    SELECT COUNT(areacode) AS 'count' FROM polylayer
    SELECT dollars/100.0 AS cents FROM polylayer


Changer le type des champs
----------------------------

À partir de GDAL 1.6.0, SQL d'OGR gère le changement du type des colonnes en 
utilisant l'opérateur CAST conforme SQL92 comme pour l'exemple suivant :

::
    
    SELECT *, CAST(OGR_STYLE AS character(255)) FROM rivers

Pour l'instant la transformation vers les cibles suivantes sont gérées :

- *character(field_length)*, field_length=1 par défaut
- *float(field_length)*
- *numeric(field_length, field_precision)*
- *integer(field_length)*
- *date(field_length)*
- *time(field_length)*
- *timestamp(field_length)*

Définir *field_length* et/ou *field_precision* est optionel. Une valeur zéro 
explicite peut être utilisée comme la largeur d'un champ character() pour indiquer 
la largeur de la variable. La conversion vers les types de données OGR 
'liste d'entier', 'liste double' et 'liste de caractères' ne sont pas gérés, ce 
qui n'est pas conforme aux spécification SQL92.

Bien que l'opérateur CAST peut être appliqué n'importe où dans une expression, 
dont la clause WHERE, le contrôle du format du champ en sortie est seulement géré 
si l'opérateur CAST est l'opérateur le plus à l'extérieur sur un champ dans une 
liste de définition de champs. Dans d'autres contexte il est encore utile de 
convertir entre les types de donnée numérique, chaîne et date.

WHERE
-------

L'argument de la clause WHERE est une expression logique assez simpliste utilisé 
pour sélectionner les enregistrements d'une couche source. En plus de cette 
utilisation dans la requête WHERE, la prise en charge de la clause WHERE est 
également utilisé par les requêtes attributaires d'OGR sur les couches normales 
via *OGRLayer::SetAttributeFilter()*.

En plus des opérateurs arithmétiques et autres opérateurs fonctionnels disponibles 
dans l'expression dans la clause de définition des champs de la requête SELECT, les 
opérateurs logiques sont aussi disponible dans la clause WHERE et la valeur 
évaluée de l'expression doit être logique(true ou false).

Les opérateurs logiques disponibles sont =, !=, <>, <, >, <=, >=, LIKE, 
ILIKE, BETWEEN et IN.

La plupart des opérateurs s'expliquent par eux-mêmes, mais il n'est pas évident 
que ''!='' ne soit pas équivalent à ''<>'', la chaine égalité n'est pas sensible 
à la casse, mais les opérateurs <, >, <= et >= sont sensible à la casse. À la 
fois LIKE et ILIKE sont insensible à la casse.

L'argument valeur à l'opérateur LIKE est un motif avec lequel la chaine de valeur 
est recherché. Dans ce motif le signe pourcentage (%) correspond à un nombre de 
caractères, et underscore (_) correspond à un seul caractère. Une clause 
optionnelle ESCAPE *escape_char* peut être ajoutée afin que les caractères % ou 
\_ puissent être recherchés comme caractères normaux, en étant précédé de 
*escape_char*.

+---------------+-----------+-----------+
+ String        + Pattern   + Matches?  +
+===============+===========+===========+
+ Alberta       + ALB%      + Yes       +
+---------------+-----------+-----------+
+ Alberta       + _lberta   + Yes       +
+---------------+-----------+-----------+
+ St. Alberta   + _lberta   + No        +
+---------------+-----------+-----------+
+ St. Alberta   + %lberta   + Yes       +
+---------------+-----------+-----------+
+ Robarts St.   + %Robarts% + Yes       +
+---------------+-----------+-----------+
+ 12345         + 123%45    + Yes       +
+---------------+-----------+-----------+
+ 123.45        + 12?45     + No        +
+---------------+-----------+-----------+
+ N0N 1P0       + %N0N%     + Yes       +
+---------------+-----------+-----------+
+ L4C 5E2       + %N0N%     + No        +
+---------------+-----------+-----------+

L'opérateur IN prendre une liste de valeur comme argument et teste la présence 
dans cet ensemble de la valeur de l'attribut.

+-----------+----------------------+------------+
+ Value     + Value Set            +  Matches?  +
+===========+======================+============+
+ 321       + IN (456,123)         +  No        +
+-----------+----------------------+------------+
+ "Ontario" + IN ("Ontario","BC")  +  Yes       +
+-----------+----------------------+------------+
+ "Ont"     + IN ("Ontario","BC")  +  No        +
+-----------+----------------------+------------+
+ 1         + IN (0,2,4,6)         +  No        +
+-----------+----------------------+------------+

La syntaxe de l'opérateur BETWEEN est "*field_name BETWEEN value1 AND value2*" et 
il est équivalent à "*field_name >= value1 AND field_name <= value2*".

En plus des opérateurs binaire ci-dessus, il y a des opérateurs additionnels 
pour tester si un champ est null ou pas. Ce sont les opérateursIS NULL et IS 
NOT NULL.

Les tests de champ basic peuvent être combiné dans des prédicats plus compliqué 
en utilisant les opérateurs logique AND, OR, et le prédicat logique unaire NOT. 
Les sous-expressions doivent être mis entre parenthèse pour permettre une claire 
priorité. quelques prédicats plus compliqués :
::
    
    SELECT * FROM poly WHERE (prop_value >= 100000) AND (prop_value < 200000)
    SELECT * FROM poly WHERE NOT (area_code LIKE "N0N%")
    SELECT * FROM poly WHERE (prop_value IS NOT NULL) AND (prop_value < 100000)


Limitations de la clause WHERE
-------------------------------

- Les champs doivent tous venir de la table primaire (celle listée dans la 
  clause FROM.
- Toutes les comparaisons de chaine sont insensible à la casse sauf pour <, >, 
  <= et >=.

ORDER BY
---------

La clause ORDER BY est utilisé pour forcer les objets renvoyés à être ordonné 
(ascendant ou descendant) sur un des champs. L'ordre ascendant (augmentant) est 
celui par défaut si aucun des mot-clés ASC ou DESC n'est fournie. Par exemple :
::
    
    SELECT * FROM property WHERE class_code = 7 ORDER BY prop_value DESC
    SELECT * FROM property ORDER BY prop_value 
    SELECT * FROM property ORDER BY prop_value ASC
    SELECT DISTINCT zip_code FROM property ORDER BY zip_code

Notez que les clauses ORDER BY entraine de passage sur l'ensemble des objets. Le 
premier pour construire la table des valeurs correspondantes des champs en 
mémoire avec l'id des objets, et le second passage pour récupérer les objets par 
id dans l'ordre. Pour les formats dont les id des objets ne peuvent pas être lu 
efficacement d'une manière aléatoire cela peut être une opération couteuse.

L'ordonnancement de valeurs de champs de type chaine est sensible à la casse, et 
pas insensible à la casse comme dans la plupart des cas dans SQL d'OGR.

Clause JOIN
------------

SQL d'OGR gère une forme limité de jointure une à une. Cela permet à des 
enregistrements d'une table secondaire d'être utilisé pour la recherche avec une 
clé partagée entre elle et la table primaire lors d'une requête. Par exemple, 
une table de location de ville pourrait inclure une colonne *nation_id* qui peut 
être utilisé comme référence dans une table *nation* secondaire pour récupérer 
les noms des pays. Une requête par jointure pourrait ressembler à ceci :

::
    
    SELECT city.*, nation.name FROM city 
     LEFT JOIN nation ON city.nation_id = nation.id

Cette requête renverrait une table avec tous les champs de la table *city*, et 
un champ supplémentaire *nation.name* avec le pays à l'intérieur récupérer de 
la table *nation* en cherchant les enregistrements dans la table nation qui ont 
le champ *id* avec la même valeur que le champ *city.nation_id*.

Les jointures introduisent des problèmes supplémentaires. Parmi ceux là le 
concept de référencement de table sur les noms de champ. Par exemple, se référer 
à *city.nation_id* plutôt que juste *nation_id* pour indiquer le champ 
*nation_id* de la couche *city*. La référence du nom de la table peut seulement 
être utilisé dans la liste des champs, et dans la clause ON d'une jointure.

Les caractères de substitution sont parfois impliqué. Tous les champs d'une 
table primaire (*city* dans notre cas) et la table secondaire (*nation* dans ce 
cas) peuvent être sélectionné en utilisant le caractère * de substitution. Mais 
les champs d'une seul table primaire ou secondaire peuvent être sélectionné en 
préfixant l'astérix avec le nom de la table.

Les noms des champs dans la couche de la requête résultante sera qualifié du nom 
de la table, si le nom de la table est donné comme référence dans la liste des 
champs. De plus les noms des champs seront qualifiés avec un nom de table s'ils 
ne rentrent pas en conflit avec un nom de champs existant. Par exemple, la 
requête select suivante pourrait résulter dans un ensemble de champ *name*, 
*nation_id*, *nation.nation_id* et *nation.name* si les tables *city* et 
*nation* ont tout deux le champs *nation_id* et *names*.

::
    
    SELECT * FROM city LEFT JOIN nation ON city.nation_id = nation.nation_id


D'un autre côté si la table *nation* a un champ *continent_id* mais pas la table 
*city*, alors ce champs ne nécessitera pas d'être référencé dans l'ensemble de 
résultat. Cependant, si la requête select ressemble à la commande suivante, tous 
les champs résultant seront référencés par le nom de la table :

::
    
    SELECT city.*, nation.* FROM city 
        LEFT JOIN nation ON city.nation_id = nation.nation_id


Dans les exemples au-dessus, la table *nation* a été trouvé dans la même source 
de données que la table *city*. Cependant, la gestion de jointure d'OGR inclus 
la possibilité de joindre une table dans une source de données différente, 
éventuellement d'un format différent. Cela est indiqué en référençant la table 
secondaire avec le nom d'une source de données. Dans ce cas la source de 
données secondaire est ouverte en utilisant une sémantique normale d'OGR et 
utilisée pour accéder à la table secondaire jusqu'à ce que le résultat de la 
requête n'est plus nécessaire.

::
    
    SELECT * FROM city 
        LEFT JOIN '/usr2/data/nation.dbf'.nation ON city.nation_id = nation.nation_id


Bien que pas forcément nécessaire, il est également possible d'introduire des 
alias de table pour simplifier certaines requêtes SELECT. Cela peut aussi être 
utile pour enlever tout ambigüité lorsque des tables de même noms sont utilisé 
de différents sources de données. Par exemple, si les noms des tables réels 
n'étaient pas soignées nous voudrions réaliser quelque chose comme :

::
    
    SELECT c.name, n.name FROM project_615_city c
        LEFT JOIN '/usr2/data/project_615_nation.dbf'.project_615_nation n 
            ON c.nation_id = n.nation_id

Il est possible de réaliser des jointures multiples dans une seule requête :

::
    
    SELECT city.name, prov.name, nation.name FROM city
        LEFT JOIN province ON city.prov_id = province.id
        LEFT JOIN nation ON city.nation_id = nation.id


Limitations de la clause JOIN
------------------------------

- Les jointures peuvent être des opérations couteuses si la table secondaire 
  n'est pas indexée sur le champ clé de la jointure.
- Les champs joins ne peuvent pas être utilisés dans les clauses WHERE, ou ORDER 
  BY en même temps. La jointure est essentiellement évalué après que tous les 
  sous-ensemble des tables primaires soient complète et après le passage du 
  ORDER BY.
- Les champs joins ne peuvent pas être utilisé comme clé dans une future 
  jointure. Vous ne pouvez donc pas utiliser l'id de la province dans une ville 
  pour rechercher les données de la provinces, puis utiliser un id d'un pays à 
  partir de la province pour récupérer les données du pays. Cela est quelque 
  chose qui pourrait être développé, mais n'est pas actuellement géré.
- Les noms des sources de données pour les tables jointes sont évalué par 
  rapport au répertoire de travail du processus en cours, et pas du chemin de 
  la source de données primaire.
- Il n'y a pas de réelle jointure LEFT ou RIGHT au sens RDBMS. Qu'un 
  enregistrement secondaire existe ou non, une et une seule copie de 
  l'enregistrement primaire est renvoyée dans l'ensemble des résultats. Si un 
  enregistrement secondaire nepeut pas être trouvé, les champs dérivés 
  secondaires sera NULL. Si plus d'une correspondance du champs secondaire est 
  trouvé, seul le premier enregistrement sera utilisé.

Champs spéciaux
================

Le processeur de requête SLQ d'OGR traite certains attributs d'objets comme des 
champs spéciaux interne et peuvent être utilisé dans les requêtes SQL comme tout 
autres champs. Ces champs peuvent être placé dans la liste des select, les 
clauses WHERE et ORDER BY. Les champs spéciaux ne seront pas inclus dans le 
résultat par défaut mais ils peuvent être explicitement inclus en les ajoutant 
à la liste du select. Lors de l'accès à la valeur du champ les champs spéciaux 
prennent la priorité sur tous les autres champs avec le même nom dans la source 
de données.

FID
-----

Normalement l'id de l'objet est une propriété spéciale d'un objet et n'est pas 
traité comme un attribut d'objet. Dans certains cas il est pratique de pouvoir 
utiliser l'id de l'objet dans des requêtes et des résultats comme un champ 
normal. Pour cela utiliser le nom FID. L'utilisation du caractère de 
substitution de champ n'inclura pas l'id de l'objet, mais il peut être 
explicitement inclus en utilisant la syntaxe suivante :

::
    
    SELECT FID, * FROM nation

OGR_GEOMETRY
-------------

Certaines sources de donnés (comme les fichiers tab de MapInfo) peuvent prendre 
en charge des géométries de différents types dans la même couche. Le champ 
spécial *OGR_GEOMETRY* représente le type de géométrie renvoyé par la méthode 
*OGRGeometry::getGeometryName()* et peut être utilisé pour distinguer les 
différents types. En utilisant ce champ on peut sélectionner des types 
particulier des géométries :

::
    
    SELECT * FROM nation WHERE OGR_GEOMETRY='POINT' OR OGR_GEOMETRY='POLYGON'

OGR_GEOM_WKT
-------------

La représentation *Well Known Text* d'une géométrie peut aussi être utilisé 
comme champ spécial. Pour sélectionner le WKT d'une géométrie *OGR_GEOM_WKT* 
peut être inclus dans la liste de select :

::
    
    SELECT OGR_GEOM_WKT, * FROM nation

En utilisant *OGR_GEOM_WKT* et l'opérateur LIKE dans la clause WHERE nous 
pouvons avoir des effets similaire à l'utilisation de *OGR_GEOMETRY* :
::
    
    SELECT OGR_GEOM_WKT, * FROM nation WHERE OGR_GEOM_WKT
        LIKE 'POINT%' OR OGR_GEOM_WKT LIKE 'POLYGON%'


OGR_GEOM_AREA
--------------

(à partir de GDAL 1.7.0)

Le champ spécial **OGR_GEOM_AREA** retourne la surface de la géométrie de la 
feature calculée par la méthode *OGRSurface::get_Area()*. Pour 
*OGRGeometryCollection* et *OGRMultiPolygon* la valeur est la somme des surface 
de ses membres. Pour les géométries non surfacique la surface retournée est 0.0.

Par exemple, pour sélectionner seulement les polygones plus grand qu'une surface 
donnée :

::
    
    SELECT * FROM nation WHERE OGR_GEOM_AREA > 10000000'

OGR_STYLE
-----------

Le champs spécial *OGR_STYLE* représente la chaine de style d'un objet renvoyé 
par la méthode *OGRFeature::GetStyleString()*. En utilisant ce champ et 
l'opérateur LIKE le résultat d'une requête peut être filtré par le style. Par 
exemple nous pouvons sélectionner  l'objet annotation avec :
::
    
    SELECT * FROM nation WHERE OGR_STYLE LIKE 'LABEL%'


CREATE INDEX
=============

Certains pilotes SQL d'OGR gère la création d'indexes attributaires. Pour 
l'instant cela inclus le pilote Shapefile. Un inde accélère  les requêtes 
attributaires de la forme *nomChamp = valeur*, ce qui est utilisé par la 
jointure. Pour créer un index attributaire sur le champs *nation_id* de la 
table *nation* une commande telle que celle-ci peut être utilisée :

::
    
    CREATE INDEX ON nation USING nation_id

Limitations des Index
----------------------

- Les index ne sont pas maintenu dynamiquement lors de l'ajout ou la 
  suppression d'une couche d'un nouvel objet.
- Les chaines très longue (plus longue que 256 caractères) ne peuvent pas 
  pour l'instant être indexé.
- Pour recréer un index il est nécessaire de supprimer tous les indexes sur 
  la couche et de toutes les recréer.
- Les indexes ne sont pas utilisés dans toutes les requêtes complexes. Pour 
  l'instant la seule requête qui sera accélérée est la requête simple *champ = 
  valeur*.

DROP INDEX
===========

La commande SQL d'OGR DROP INDEX peut être utilisé pour supprimer tous les 
indexes sur une table particulière ou juste l'index d'une colonne particulière.
::
    
    DROP INDEX ON nation USING nation_id
    DROP INDEX ON nation

ExecuteSQL()
=============

SQL est exécuté en fonction de *OGRDataSource,*, et pas en fonction d'une couche 
spécifique. L'appel ressemblera à ceci :
::
    
    OGRLayer * OGRDataSource::ExecuteSQL( const char *pszSQLCommand,
                                      OGRGeometry *poSpatialFilter,
                                      const char *pszDialect );

L'argument *pszDialect* a pour objectif théorique de permettre la gestion de 
différents langages de commande en fonction d'un provider, mais pour l'instant 
les applications doivent toujours passer une chaine vide (pas NULL) pour avoir 
le dialecte par défaut.

L'argument *poSpatialFilter* est une géométrie utilisé pour sélectionner un 
rectangle de limite pour les objets à renvoyés d'une manière similaire à la 
méthode *OGRLayer::SetSpatialFilter()*. Il peut être NULL pour aucune 
restriction spatiale.

Le résultat d'un appel *ExecuteSQL()* est habituellement un OGRLayer temporaire 
représentant l'ensemble des résultats de la requête. C'est le cas des requêtes 
SELECT par exemple. La couche temporaire renvoyée doit être publiée avec la 
méthode *OGRDataSource::ReleaseResultsSet()* quand elle n'est plus nécessaire. 
L'échec de la publication avant que la source de données ne soit détruite 
entrainera un crash.

SQL hors OGR
=============

Tous les pilotes d'OGR pour les systèmes de bases de données : MySQL, PostgreSQL 
et PostGIS (:ref:`gdal.ogr.formats.postgresql`), Oracle 
(:ref:`gdal.ogr.formats.oci`), SQLite, ODBC; les Géodatabases Personnelles d'ESRI 
(:ref:`gdal.ogr.formats.pgeo`) et MS SQL Spatial (:ref:`gdal.ogr.formats.mssqlspatial`)
écrasent la fonction *OGRDataSource::ExecuteSQL()* par une 
implémentation dédiée et, par défaut, envoie les requêtes SQL directement au 
RDBMS sous-jacent. Dans ces cas la syntaxe SQL varie plus ou moins du SQL d'OGR. 
Aussi, tout ce qui est possible en SQL peut alors être accomplie pour ces bases 
de données particulières. Seul le résultat des requêtes WHERE SQL sera renvoyé 
comme des couches.

.. yjacolin at free.fr, Yves Jacolin - 2011/06/30 (http:*www.gdal.org/ogr/ogr_sql.html trunk 22454)