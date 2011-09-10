.. _`gdal.ogr.formats.vrt`:

==============
Virtual Format
==============

Le format Virtuel d'OGR est un pilote qui transforme les objets lu à partir 
d'autres pilotes sur des critères définie dans un fichier de contrôle XML. Il 
est d'abord utilisé pour profiter des couches spatiales provenant de tables à 
plat avec des informations spatiales dans des colonnes attributaires. Il peut 
être également utilisé pour associer des information de système de coordonnées 
avec une source de données, merger des couches de sources de données différentes 
dans une seule source de données, ou même juste fournir un fichier de soutient 
pour l'accès à une source de données pas sous forme de fichier.

Les fichiers virtuel sont pour l'instant normalement préparés à la main.

Problèmes de création
======================

Avant GDAL 1.7.0, le pilote VRT d'OGR était en lecture seule.

Depuis GDAL 1.7.0, les opération *CreateFeature()*, *SetFeature()* et *DeleteFeature()* 
sont gérées sur la couche d'un jeu de données VRT, si les conditions suivantes 
sont remplies :

* le jeu de données VRT est ouvert en mode update ;
* la couche source sous-jascente gère ces opérations ;
* l'élément *SrcLayer* est utilisé (en opposition à l'élément *SrcSQL*) ;
* le FID des features VRT est le même que le FID des features sources, c'est à dire, 
  l'élément *FID* n'est pas définie.

Format de fichier virtuel
==========================

L'élément racine d'un fichier de contrôle XML est *OGRVRTDataSource*. il a un 
enfant *OGRVRTLayer* pour chaque couche dans la source de données virtuelle. Cet 
élément doit avoir un attribut **name** avec le nom de la couche, et peut avoir 
les sous-éléments suivants :

* **SrcDataSource (obligatoire) :** La valeur est le nom de la source de 
  données dont cette couche sera dérivée. L'élément peut en option avoir un 
  attribut *relativeToVRT* dont la valeur par défaut est "0", mais "1" indique 
  que la source  de données doit être interprétée comme relative au fichier 
  virtuel. Cela peut être un jeu de données géré par OGR, incluant ODBC, CSV, 
  etc. L'élément peut également avoir un attribut partagé pour contrôler si la 
  source de données doit être ouverte en mode partagé. OFF par défaut pour 
  l'utilisation de *SrcLayer* et ON pour l'utilisation de *SrcSQL*.
* **SrcLayer (optionnel) :** la valeur est le nom de la couche dans la source 
  de données dont cette couche virtuelle sera dérivée. Si cet élément n'est pas 
  fournit, alors l'élément *SrcSQL* doit être fournit.
* **SrcSQL* (optionnel) :** une requête SQL pour exécuter la génération de la 
  couche désirée résultante. Ceci doit être fournie à la place de *StcLayer* pour 
  les résultats dérivés de requêtes. certaines limitations peuvent s'appliquer 
  pour les couches dérivées du SQL.
* **FID (optionnel) :** nom de la colonne attributaire à partir duquel le FID .
  des objets doivent être dérivés. S'il n'est pas fourni, le FID des objets 
  sources sera utilisé directement.
* **Style (optionnelle) :** nom de la colonne attributaire à partir duquel le 
  style des features doit être dérivé. Si non fournie, le style de la feature 
  source sera utilisé directement.
* **GeometryType (optionnel) :** le type de la géométrie à assigner à la couche. 
  S'il n'est pas fournie il sera récupéré à partir de la couche source. La 
  valeur doit être un parmi *wkbNone*, *wkbUnknown*, *wkbPoint*, 
  *wkbLineString*, *wkbPolygon*, *wkbMultiPoint*, *wkbMultiLineString*, 
  *wkbMultiPolygon, ou *wkbGeometryCollection"*. En option *25D* peut ajouté 
  pour marquer l'utilisation des coordonnées Z. Par défaut *wkbUnknown* indique 
  que n'importe quelle géométrie est autorisée.
* **LayerSRS (optionnel) :** la valeur de cet élément est la référence 
  spatiale à utiliser pour la couche. Si elle n'est pas fournie, elle est 
  héritée de la couche source. La valeur peut être en WKT ou dans n'importe 
  quel autre format accepté par la méthode *OGRSpatialReference::SetUserInput()*.
  Si la valeur est NULL, alors aucun SRS ne sera utilisé pour la couche.
* **GeometryField (optionnel) :** cet élément est utilisé pour définir comment 
  la géométrie pour les objets doit être dérivée. Si elle n'est pas fournie la 
  géométrie de l'objet source est copié directement. Le type de l'encodage de la 
  géométrie est indiqué avec l'attribut d'encodage qui peut avoir les valeurs 
  *WKT*, *WKB* ou *PointFromColumns*. Si l'encodage est *WKT* ou *WKB* alors le 
  champ attributaire aura le nom du champ contenu la géométrie WKT ou le WKB. Si 
  l'encodage est *PointFromColumns* alors les attributs x, y et z aura les noms 
  des colonnes à utilisées pour les coordonnées X, Y et Z. L'attribut z est 
  optionnel. À partir de GDAL 1.7.0, l'attribut optionnel **reportSrcColumn** 
  peut être utilisé pour définir si les champs géométriques sources (l'ensemble 
  des champs dans les attributs **field**, **x**, **y** ou **z**) doivent être 
  reporté comme champs de la couche vrt. TRUE par défaut.
  Si définie à FALSE, les champs géométriques sources seront utilisé seulement 
  pour construire la géométrie de la feature de la couche VRT.
* **SrcRegion (optionnel, à partir de GDAL 1.7.0) :** Cet élément est utilisé 
  pour définir un filtre spatial initial pour les features sources. Ce filtre 
  spatial sera combiné avec n'importe quel filtre spatial explicitement définie 
  sur la couche VRT avec la méthode *SetSpatialFilter()*. La valeur de l'élément 
  doit être une chaîne WKT valide définissant un polygone. Un attribut *clip* 
  optionnel peut être définie à "TRUE" pour découper les géométries à la région 
  source, sinon les géométries sources ne sont pas modifiées.
* **Field (optionnel, à partir de GDAL 1.7.0) :** un ou plusieurs champs 
  attributaires peuvent être définie avec les éléments Field. Si aucun élément 
  Field ne sont définie, les champs de ma couche/sql source sera définie sur la 
  couche vrt. L'élément Field peut avoir les attributs suivants :

  * **name (nécessaire) :** le nom du champs.
  * **type :** le type du champs, un parmi "Integer", "IntegerList", "Real", 
    "RealList", "String", "StringList", "Binary", "Date", "Time", ou "DateTime" 
    - "String" par défaut.
  * **width :** la largeur du champ, inconnus par défaut.
  * **precision :** la précision du champs, 0 par défaut.
  * **src :** le nom du champ source qui doit être copié dans celui-ci. par 
    défaut, la valeur de "name".

Exemple : couche ponctuelle ODBC
=================================

Dans l'exemple suivant (disease.ovf) la mauvaise table à partir de la base de 
données ODBC DISEASE est utilisée pour créer une couche spatiale. Le fichier 
virtuel utilise les colonnes "x" et "y" pour obtenir la localisation spatiale. 
La couche est également définie comme une couche point, et comme étant dans le 
système de coordonnées WGS84.
::
    
    <OGRVRTDataSource>
    
        <OGRVRTLayer name="worms">
            <SrcDataSource>ODBC:DISEASE,worms</SrcDataSource> 
            <SrcLayer>worms</SrcLayer> 
            <GeometryType>wkbPoint</GeometryType> 
            <LayerSRS>WGS84</LayerSRS>
            <GeometryField encoding="PointFromColumns" x="x" y="y"/> 
        </OGRVRTLayer>
    
    </OGRVRTDataSource>

Exemple : renommer des attributs
=================================

Il peut être utile dans certaines circonstance de pouvoir renommer les noms des 
champs à partir d'une couche source en un nom différent. Cela est 
particulièrement vrai quand on veut traduire vers un format dont les schéma est 
imposé, tel que le format GPX (<name>, <desc>, etc.). Cela peut être accomplit 
en utilisant SQL de cette manière :
::
    
    <OGRVRTDataSource>
        <OGRVRTLayer name="remapped_layer">
            <SrcDataSource>your_source.shp</SrcDataSource>
            <SrcSQL>SELECT src_field_1 AS name, src_field_2 AS desc FROM your_source_layer_name</SrcSQL>
        </OGRVRTLayer>
    </OGRVRTDataSource>

Cela peut aussi être accomplie (à partir de GDAL 1.7.0) en utilisant des 
définitions de champs explicites :

::
    
    <OGRVRTDataSource>
        <OGRVRTLayer name="remapped_layer">
            <SrcDataSource>your_source.shp</SrcDataSource>
            <SrcLayer>your_source</SrcSQL>
            <Field name="name" src="src_field_1" />
            <Field name="desc" src="src_field_2" type="String" width="45" />
        </OGRVRTLayer>
    </OGRVRTDataSource>


Exemple : Filtre spatial transparent (GDAL >= 1.7.0)
=====================================================
 
L'exemple suivant retournera seulement les features à partir de la couche source 
qui intersecte la région (0,40)-(10,50). De plus, les géométries retournées seront 
découpées pour correspondre à cette région.

::
    
    <OGRVRTDataSource>
        <OGRVRTLayer name="source">
            <SrcDataSource>source.shp</SrcDataSource>
            <SrcRegion clip="true">POLYGON((0 40,10 40,10 50,0 50,0 40))</SrcRegion>
        </OGRVRTLayer>
    </OGRVRTDataSource>


Autres remarques
================

* Quand *GeometryField* est *WKT*, les filtres spatiaux sont appliqués après 
  extractions de toutes les lignes à partir de la source de données. 
  Essentiellement, cela signifie qu'il n'y a pas de filtre spatial rapide sur 
  les géométries dérivées WKT.
* Quand *GeometryField* est *PointFromColumns*, et qu'un *SrcLayer* (en 
  opposition à *SrcSQL*) est utilisé, et qu'un filtre spatial est effectif sur 
  la couche virtuelle alors le filtre spatial sera traduit en interne en un 
  filtre attribut sur les colonnes X et Y dans *SrcLayer*. Au cas où des filtres 
  spatiaux rapide soient importants, il peut être utile d'indexer les colonnes 
  X et Y dans le stockage des données source, si cela est possible. Par exemple 
  si la source est un RDBMS. Vous pouvez désactiver cette fonctionnalité en 
  définissant l'attribut *useSpatialSubquery* de l'élément GeometryField à FALSE.
* Normalement la *SrcDataSource* est au format tabulaire non-spatial (tel que 
  MySQL, SQLite, CSV, OCI, ou ODBC) mais il peut être également une base de 
  données spatiales auquel cas la géométrie peut être directement copiée.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/04 (trunk 17729)