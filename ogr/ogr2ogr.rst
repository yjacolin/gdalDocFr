.. _`gdal.ogr.ogr2ogr`:

========
ogr2ogr
========

Convertie des données *simple features* entre divers formats de fichiers.

Usage
======

::
    
    ogr2ogr [--help-general] [-skipfailures] [-append] [-update]
          [-select field_list] [-where restricted_where] 
          [-progress] [-sql <sql statement>] [-dialect dialect]
          [-preserve_fid] [-fid FID]
          [-spat xmin ymin xmax ymax]
          [-a_srs srs_def] [-t_srs srs_def] [-s_srs srs_def]
          [-f format_name] [-overwrite] [[-dsco NAME=VALUE] ...]
          dst_datasource_name src_datasource_name
          [-lco NAME=VALUE] [-nln name] [-nlt type] [-dim 2|3] [layer [layer ...]]

Options avancées :

::
    
          [-gt n]
          [-clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent]
          [-clipsrcsql sql_statement] [-clipsrclayer layer]
          [-clipsrcwhere expression]
          [-clipdst [xmin ymin xmax ymax]|WKT|datasource]
          [-clipdstsql sql_statement] [-clipdstlayer layer]
          [-clipdstwhere expression]
          [-wrapdateline]
          [[-simplify tolerance] | [-segmentize max_dist]]
          [-fieldTypeToString All|(type1[,type2]*)]
          [-splitlistfields] [-maxsubfields val]
          [-explodecollections] [-zfield field_name]
          [-gcp pixel line easting northing [elevation]]* [-order n | -tps]

Ce programme peut être utilisé pour convertir des données *simple features* 
dans des formats de fichiers tout en réalisant des opérations diverses pendant 
le processus comme des sélections spatiales ou attributaires, la réduction 
d'ensemble d'attributs, la définition du système de coordonnées en sortie ou 
même la reprojection des objets pendant la translation.

* **-f format_name :** retourne le fichier au format, (ESRI Shapefile par 
  défaut), des valeurs possibles sont :

  * **-f "ESRI Shapefile"**
  * **-f "TIGER"**
  * **-f "MapInfo File"**
  * **-f "GML"**
  * **-f "PostgreSQL"**

* **-append :** ajoute à la couche existante au lieu d'en créer une nouvelle.
* **-overwrite :** efface la couche en sortie et en recréer une vide.
* **-update :** ouvre une source de donnes existantes en mode mise à jour plutôt 
  que d'essayer d'en créer une autre.
* **-select field_list :** liste séparé par une virgule de champs à partir de la 
  couche en entrée à copier à la nouvelle couche. Un champ est ignoré s'il est 
  déjà mentionné précédemment dans la liste même si la couche en entré possède 
  des noms de champs dupliqués (toutes par défaut ; un champ est ignoré si un 
  champ subséquent si un champ de même nom est trouvé).
* **-progress :** (à partie de GDAL 1.7.0) affiche un barre de progression dans 
  la console. Fonctionne seulement si les couches en entrée possèdent la 
  capacité "*fast feature count*".
* **-sql sql_statement :** requête SQL à exécuter. La couche/table résultante 
  sera sauvé vers la sortie.
* **-dialect dialect :** dialecte SQL. Dans certains car permet d'utiliser 
  le SQL d'OGR (non optimisé) au lieu du SQL natif d'un SGBDR en passant OGRSQL.

  .. versionadded:: 1.10 Le dialect "SQLITE" peut aussi être utilisé avec 
     n'importe quelle source de données.
* **-where restricted_where :** requête attributaire (identique à la requête 
  SQL WHERE)
* **-skipfailures :** continue après un échec, ignorant l'objet en échec.
* **-spat xmin ymin xmax ymax :** requête sur l'étendue spatiale. Seule les 
  features dont les géométries intersectent les extends seront sélectionnés. 
  Les géométries ne seront pas découpé sauf si l'option *-clipsrc* est spécifiée.
* **-dsco NAME=VALUE :** option de création du jeu de données (spécifique au 
  format)
* **-lco NAME=VALUE :** option de création de couche (spécifique au format)
* **-nln name :** assigne un nom alternatif à la nouvelle couche.
* **-nlt type :** définie le type de géométrie pour la couche crée. Un parmi 
  *NONE*, *GEOMETRY*, *POINT*, *LINESTRING*, *POLYGON*, *GEOMETRYCOLLECTION*, 
  *MULTIPOINT*, *MULTILINE*, *MULTIPOLYGON* ou *MULTILINESTRING*. Ajouter "25D" 
  au nom pour obtenir des versions en 2.5D.

  .. versionadded:: 1.10 PROMOTE_TO_MULTI peut être utilisé pour automatiquement 
     promouvoir les couches qui mélangent polygones ou multipolygones en 
	 multipolygones, et les couches qui mélangent linestrings ou multilinestrings 
	 en multilinestrings. Peut être utile lors de la conversion des shapefiles 
	 vers PostGIS (et d'autres pilotes cibles) qui implémentent une stricte 
	 vérification des types de géométries.
* **-dim val :** (à partir de GDAL 1.10) Force la dimension des coordonnées à 
  *val* (des valeurs valide sont 2 ou 3). Cela affecte à la fois le type de 
  géométrie de la couche et la géométrie de l'entité.
* **-a_srs srs_def :** assigne un SRS en sortie.
* **-t_srs srs_def :** reprojète/transforme dans ce SRS en sortie.
* **-s_srs srs_def :** écrase la source SRS.
* **-fid fid :** si fournit, seulement l'objet avec cet identifiant sera 
  renvoyé. Opère de façon exclusive aux requêtes spatiales ou attributaires. 
  
  .. note::
    si vous voulez sélectionner plusieurs features basées sur leur feature_id, 
    vous pouvez également utilisé le fait que le 'fid' est un champ spécial 
    reconnu par le SQL d'OGR. Donc, '-where “fid in (1,3,5)”' sélectionnera les 
    features 1, 3 et 5.

*Srs_def* peut être une définition WKT complète (difficile d'échappé 
proprement), ou une définition *well known* (par exemple *EPSG:4326*) ou un 
fichier avec une définition WKT.

Options avancées :

* **-gt n :** regroupe n objets par transaction (200 par défaut). Augmentez la 
  valeur pour de meilleure performance lors de l'écriture dans un pilote de 
  SGBD qui gère les transactions.
* **-clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent :** (à partir de 
  GDAL 1.7.0) 
  (à partir de GDAL 1.7.0) découpe les géométries dans la bounding box définie
  (exprimée dans la projection source), géométrie WKT (POLYGON ou MULTIPOLYGON), 
  à partir d'une source de données ou de l'étendue sptiale de l'option *-spat*
  si vous utilisez le mot clé *spat_extent*. Lors de l'utilisation d'une source 
  de données, vous désirez généralement l'utiliser en combinaison des options 
  -clipsrclayer, -clipsrcwhere ou -clipsrcsql 
* **-clipsrcsql sql_statement :** sélectionne les géométries désirées en 
  utilisant une requête SQL à la place.
* **-clipsrclayer layername :** sélectionne le nom de la couche à partir de la 
  source de données source du clip.
* **-clipsrcwhere expression :** restreint les géométries désirées basées sur 
  une requête attributaire.
* **-clipdst xmin ymin xmax ymax :** (à partir de GDAL 1.7.0) découpe les 
  géométries après la reprojection avec la bounding box définie (exprimé en SRS 
  destinataire), géométrie WKT (POLYGON ou MULTIPOLYGON) ou à partir d'une 
  source de données. Lorsqu'une source de données est définie, vous voudrez 
  généralement l'utiliser en combinaison des options *-clipdstlayer*, 
  *-clipdstwhere* ou *-clipdstsql*.
* **-clipdstsql sql_statement :** sélectionne les géométries désirées en 
  utilisant une requête SQL à la place.
* **-clipdstlayer layername :** sélectionne le nom de la couche à partir de la 
  source de données de destination du clip.
* **-clipdstwhere expression :** restreint les géométries désirées basées sur 
  une requête attributaire.
* **-wrapdateline :** (à partir de GDAL 1.7.0) découpe les géométries qui croise 
  le méridien "final" (long. = +/- 180deg)
* **-simplify tolerance :** (à partir de GDAL 1.9.0) tolérance de la distance 
  pour la simplification. Note : l'algorithme utilisé préserve la topologie 
  par entité, en particulier pour les géométries polygonales, mais pas pour 
  la couche complète.
* **-segmentize max_dist :** (à partir de GDAL 1.6.0)  distance maximale entre 
  deux noeuds. Utilisé pour créer des points intermédiaires.
* **-fieldTypeToString type1, ... :** (à partir de GDAL 1.7.0) convertie un 
  champs du type définie vers le type String dans la couche de destination. Les 
  types valides sont : Integer, Real, String, Date, Time, DateTime, Binary, 
  IntegerList, RealList, StringList. La valeur spéciale *All* peut être utilisée 
  pour convertir tous les champs en String. C'est une manière alternative pour 
  utiliser l'opérateur *CAST* du SQL d'OGR, qui peut éviter d'entrer une longue 
  requête SQL. 
* **-splitlistfields :** (à partir de GDAL 1.8.0) découpe les champs de type 
  StringList, RealList ou IntegerList dans autant de champs de type String, 
  Real ou Integer que nécessaire.
* **-maxsubfields val :** pour combiné avec l'option *-splitlistfields* pour 
  limiter le nombre de sous champs créé pour chaque champs découpés.
* **-explodecollections :** (à partir de GDAL 1.8.0) produit un feature pour 
  chaque géométrie dans n'importe quelle collection géométrique du fichier source.
* **-zfield *field_name* :** (à partir de GDAL 1.8.0) utilise le champ définie 
  pour remplir les coordonnées Z des géométries.
* **-gcp ungeoref_x ungeoref_y georef_x georef_y elevation :** (à partir de 
  GDAL 1.10.0) Ajoute le point d'amer indiqué. Cette option peut être utilisé 
  plusieurs fois pour fournir plusieurs points d'amer.
* **-order n :** (à partir de GDAL 1.10.0) ordre de la fonction polynomiale 
  utilisé pour la transformation (1 à 3). La valeur par défaut est de 
  sélectionner un ordre polynomial basé sur le nombre de point d'amer.
* **-tps :** (à partir de GDAL 1.10.0) Force l'utilisation de la transformation 
  *thin plate splines* basé sur les points d'amer disponibles.

Astuces de performances
========================

Lors de l'écriture dans une transation SGDB (SQLite/PostgreSQL,MySQL, etc...), 
il peut être bénéfique d'accroitre le nombre de requêtes INSERT éxécutées entre 
les requêtes BEGIN TRANSACTION et COMMIT TRANSACTION.
Ce nombre est définie avec l'option *-gt*. Par exemple, pour SQLite, définir 
explictement **-gt 1024** améliore grandement les performances ; définir une 
valeur plus importante **-gt 65536** permet d'avoir des performances optimales 
pour remplir les tables contenant plusieurs 100 de millier de lignes. Cependant 
notez que si les insertions échouent, l'étendue de l'option *-skipfailures* est 
l'ensemble de la transaction.

Pour PostgreSQL, l'option de configuration *PG_USE_COPY* peut être définie à 
*YES* pour une amélioration significative des performances. Voir la page de 
documentation du pilote PG.

Plus généralement, consultez la page de documentation des pilotes d'entrés et 
de sorties pour des astuces de performance.

Exemples
=========

Exemple ajoutant une couche existante (les deux options nécessites d'être 
utilisé) :

::
    
    % ogr2ogr -update -append -f PostgreSQL PG:dbname=warmerda abc.tab

Exemple reprojetant les données à partir de ETRS_1989_LAEA_52N_10E vers 
EPSG:4326 et découpant les features par une bounding box :

::
    
    % ogr2ogr -wrapdateline -t_srs EPSG:4326 -clipdst -5 40 15 55 france_4326.shp europe_laea.shp

Des exemples supplémentaires sont données dans les pages des formats.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/23 (http://www.gdal.org/ogr2ogr.html Trunk r25332)
