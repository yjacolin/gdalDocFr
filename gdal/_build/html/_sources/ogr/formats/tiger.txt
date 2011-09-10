.. _`gdal.ogr.formats.tiger`:

========================
U.S. Census TIGER/Line
========================

Les ensembles de fichier TIGER/Line sont gérés en lecture.

Les fichiers TIGER/Line sont un base de données numérique d'objet géographique, 
tels que les routes, les rails, les rivières, les lacs, les frontières 
politiques, les limites des recensements statistique, etc. couvrant entièrement 
les États-Unis. La base de données contient des informations sur ces objets tel 
que leur location en latitude et longitude, le nom, le type de l'objet, la 
précision de l'adresse pour la plupart à la rue, la relation géographique aux 
autres objets, et aux autres informations liées. Ce sont des produits publiques 
créés à partir des bases de données d'information géographique TIGER 
(*Topologically Integrated Geographic Encoding and Referencing*) du Bureau du 
Recensement. TIGER a été développé au Bureau du Recensement pou gérer la 
cartographie et les activités liées à la géographie nécessaire par le recensement 
décennal et les programmes de sondage. Notez que les produits TIGER/Line n'inclut 
pas de statistique du recensement démographique. Ceux-ci sont vendu par le 
Bureau de Recensement dans un format séparé (pas directement géré par FME), mais 
ces statistiques sont liés aux blocs *census* dans les fichiers TIGER/Line.

Pour ouvrir un jeu de données TIGER/Line, sélectionnez le répertoire contenant 
un ou plusieurs ensembles de fichiers de données. Les étendues sont des régions, 
ou équivalent à une région. Chaque région consiste à une série de fichier avec 
un nom de base, et différentes extensions. Par exemple, la région 1 dans l'état 
26 (Michigan) consiste à l'ensemble des fichiers suivants définie dans Tiger98.
::
    
    TGR26001.RT1
    TGR26001.RT2
    TGR26001.RT3
    TGR26001.RT4
    TGR26001.RT5
    TGR26001.RT6
    TGR26001.RT7
    TGR26001.RT8
    TGR26001.RT9
    TGR26001.RTA
    TGR26001.RTC
    TGR26001.RTH
    TGR26001.RTI
    TGR26001.RTP
    TGR26001.RTR
    TGR26001.RTS
    TGR26001.RTZ

Le système de coordonnées de TIGER/Line est codé en dur à NAD83 lat/long, degré. 
Cela doit être approprié pour toutes les années récentes de la production 
TIGER/Line.

Il n'y a pas de gestion de mise à jour ou de création dans le pilote TIGER/Line.

Le lecteur a été implémenté pour les fichiers TIGER/Line de 1998, mais des 
développements ont permis de s'assurer de la compatibilité avec les produits 
TIGER/Line de 1992, 1995, 1997, 1999, 2000, 2002, 2003 et 2004. Les produits 
2005 fonctionne également correctement selon des retours. Tous les produits 
TIGER/Line à partir de 1988 devrait fonctionner avec le lecteur, avec des pertes 
d'informations spécifique à certaine version.

Représentation des objets
==========================

Avec quelques exceptions, un objet est créé pour chaque enregistrement d'un 
fichier de données TIGER/Line. Chaque fichier (c'est à dire, .RT1, .RTA) est 
traduit en un type d'objet OGR approprié, avec des noms d'attributs correspondant 
à ceux dans le manuel du produit TIGER/Line.

Les attributs *RT* (*record type*) et *VERSION* de TIGER/Line sont généralement 
ignorés, mais l'attribut *MODULE* est ajouté à chaque objet. L'attribut *MODULE* 
contient le nom de base (par exemple *TGR26001*) du module région à partir 
duquel est originaire l'objet. Pour certaines clés (telles que *LAND*, *POLYID*, 
et *CENID*)cet attribut *MODULE* est nécessaire pour rendre la clé unique quand 
le jeu de données (répertoire) consiste à des données de plus d'une région.

Ce qui suit est une liste de types d'objet, et leur lien avec le produit TIGER/Line.

CompleteChain
--------------

Une *CompleteChain* est une polyligne avec un TLID associé (TIGER/Line ID). Les 
objets *CompleteChain* sont établi à partir d'un enregistement de type 1 
(Enregistrement de Données Basiques de Chaine Complète, *Complete Chain Basic 
Data Record*),, et is disponible est associé avec un enregistrement de type 3 
(Codes d'Entité Géographique de Chaîne Complète, *Complete Chain Geographic 
Entity Codes*).Également, n'importe quels enregistrements de type 2 (Coordonnées 
de Forme de Chaîne Complète, *Complete Chain Shape Coordinates*) disponible sont 
utilisés pour remplir les points de forme intermédiaire sur l'arc. Le TLID est 
la clé primaire, et est unique dans la couverture nationale entière de TIGER/Line.

Ces objets ont toujours une géométrie 'line'.

AltName
--------

Ces objets sont dérivés des enregistrement de type 4 (Index pour Alterner des 
Identifiants d'objet, *Index to Alternate Feature Identifiers*), et liés à un 
TLID de 1 à 4 numéros de noms d'objet (l'attribut *FEAT*) qui sont gardé 
séparément comme objets *FeatureIds*. La pipeline du lecteur standard attache 
le nom à partir des objets *FeatureIds* comme des attributs array *ALT_FEDIRS{}*, 
*ALT_FEDIRP{}*, *ALT_FENAME{}* et *ALT_FETYPE{}*. *ALT_FENAME{}* est une liste 
de noms d'objets associée avec le TLID sur l'objet *AltName*.

Notez que zéro, un ou plusieurs enregistrement *AltName* peu(ven)t exister pour 
un TLID dpnnée, et chaque enregistrement *AltName* peut contenir entre un et 
quatre noms alternatifs. Parce que cela est encore très difficile d'utiliser les 
objets *AltName* pour lier des noms alternatifs à *CompleteChains*, il est 
anticipé que la pipeline du lecteur standard pour les fichiers TIGER/Line seront 
mis à jour dans un futur proche, entrainant la simplification des noms 
alternatifs.

Ces objets n'ont pas de géométrie associée.

FeatureIds
-----------

Ces objets sont dérivés des enregistrement du type 5 (Identifiants d'Objet de 
chaîne Complète, *Complete Chain Feature Identifiers*). Chaque objet contient 
un nom d'objet (*FENAME*),  et son code d'identifiant d'objet associé (*FEAT*). 
L'attribut *FEAT* est la clé primaire, et est unique dans le module région. 
*FeatureIds* possède une relation un à plusieurs avec les objets *AltName* et 
*KeyFeatures*.

Ces objets n'ont pas de géométrie associée.

ZipCodes
---------

Ces objets sont dérivés des enregistrements detype 6 (Données des Codes Postaux 
et des Précisions d'Adresse Aditionnelle, *Additional Address Range and ZIP Code 
Data*). Ces objets ont pour objectif d'augmenter les informations du Code ZIP 
gardé directement dans les objets *CompleteChain*, et il y a une relation 
plusieurs à un entre les objets *ZipCodes* et *CompleteChain*.

Ces objets n'ont pas de géométrie associée.

Landmarks
-----------

Ces objets sont dérivés des enregistrements de type 7 (Objets Landmark, 
*Landmark Feature*). Ils sont liés à un point ou à une zone de repère 
(*landmark*). Pour les zones de repère il y a une relation de un à un avec un 
enregistrement *AreaLandmark*. L'attribut *LAND* est une clé primaire et unique 
dans un module région.

Ces objets peuvent avoir une géométrie ponctuelle associée. Les points de 
repères associés avec des polygones n'auront pas la géométrie polygonale 
attachée. Il sera nécessaire de le collecter (via l'objet *AreaLandmark*) à 
partir d'un objet Polygone.

AreaLandmarks
--------------

Ces objets sont dérivé des enregistrement de type 8 (Polygone lié aux zone de 
repérage, *Polygons Linked to Area Landmarks*). Chacun associé un objet landmark 
(attribut *LAND*) avec un objet polygone (attribut *POLYID*). Cet objet a une 
relation plusieurs à plusieurs avec les objets polygones.

Ces objets n'ont pas de géométrie associée.

KeyFeatures
-------------

Ces objets sont dérivés des enregistrements de type 9 (Codes d'entité 
Géographique des Polygones, *Polygon Geographic Entity Codes*). Ils peuvent être 
associé avec un objet *FeatureIds* (via l'attribut *FEAT*), et un objet polygone 
(via l'attribut *POLYID*).

Ces objets n'ont pas de géométrie associée.

Polygon
--------

Ces objets sont dérivées des enregistrements de type A (Codes d'Entité des 
Polygones Géographiques, *Polygon Geographic Entity Codes*) et si disponible le 
type S relié (Codes d'Entité Additionnel Géographique, *Polygon Additional 
Geographic Entity Codes*). L'attribut *POLYID* est la clé primaire, identifiant 
d'une manière unique un polygone dans un module *country*.

Ces objets n'ont pas de géométrie associée avec eux puisqu'il est lu par le 
pilote TIGER d'OGR. Il doit être lié en externe en utilisant le *PolyChainLink*. 
Le script ''gdal/pymod/samples/tigerpoly.py'' peut être utilisé pour lire un 
jeu de données TIGER et extraire la couche polygone avec une géométrie comme un 
shapefile.

EntityNames
------------

Ces objets sont dérivées des enregistrements de type C (Nomes d'Entité 
Géographique).

Ces objets n'ont pas de géométrie associée.

IDHistory
-----------

Ces objets sont dérivés des enregistrements de type H (Historique des ID de 
TIGER/LINE, *TIGER/Line ID History*). Ils peuvent être utilisés pour tracer le 
découpage, la fusion, la création et la suppression des objets *CompleteChain*.

Ces objets n'ont pas de géométrie associée.

PolyChainLink
--------------

Ces objets sont dérivés des enregistrement de type I (Liens entre les Polygones 
et les Chaines Complète, *Link Between Complete Chains and Polygons*). Ils sont 
normalement tous consommés par la pipeline du lecteur standard pendant le 
rattachement des géométries *CompleteChain* aux objets polygones pour établir 
leur géométries polygonales. Les objets *PolyChainLink* ont une relation 
plusieurs à un avec les objets polygones, et une relation d'un à un avec les 
objets *CompleteChain*.

Ces objets n'ont pas de géométrie associée.

PIP
----

Ces objets sont dérivés des enregistrements de type P (Point interne à un 
Polygone, *Polygon Internal Point*). Ils sont reliés à un objet Polygone vie 
l'attribut *POLYID*, et peuvent être utilisé pour établir un point interne pour 
les objets polygones.

Ces objets n'ont pas de géométrie associée. 

ZipPlus4
---------

Ces objets sont dérivés des enregistrements de type Z (Codes ZIP + 4). Les 
objets *ZipPlus4* ont une relation plusieurs à un avec les objets *CompleteChain*.

Ces objets n'ont pas de géométrie associée. 

Voir également
===============

* http://www.census.gov/geo/www/tiger/ : Plus d'information sur le format de 
  fichier TIGER/Line, et les produits de données peuvent être trouvés sur cette 
  page web de Census US.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/25 (trunk 10470)