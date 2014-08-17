.. _`gdal.ogr.formats.geoconcept`:

======================================================
GeoConcept Export (disponible à partir de GDAL 1.6.0)
======================================================

Geoconcept est un SIG développé par la société GeoConcept SA. Il s'agit d'un 
SIG orienté-objet, dont les éléments sont nommés "objets", et le type d'éléments 
"type/sous-type" (les attributs sont transmissibles).

Le pilote OGR GeoConcept traite un fichier GeoConcept simple dans un dossier 
comme un jeu de données comprenant plusieurs couches. Actuellement, le pilote 
ne gère que les multi-polygones, les lignes et les points.

Le format "fichier texte" de GeoConcept (GXT)
==============================================

Parmi ses formats d'import/export, GeoConcept propose un format texte simple 
nommé .GXT (auparavant .TXT), qui peut contenir des objets de différents 
types/sous-types.

Les fichiers textes d'export GeoConcept devraient être disponibles en lecture et 
en écriture.

Les définitions de champs sont stockés dans un fichier .GCT associé, qui n'est 
utilisé que pour la création.

Problèmes de création
=======================

Les fichiers GeoConcept peuvent contenir différentes sortes de géométrie (une 
par couche). Ceci rend très difficile la traduction d'une géométrie multiple 
d'un autre format vers GéoConcept avec ogr2ogr, car ce dernier ne permet pas 
de séparer les différents types de géométrie d'un fichier source.

Les sous-types sont considérés comme des éléments OGR. Le nom d'une couche est 
donc l'agrégation du **nom du type** de la couche, d'un **"."** et du **nom du 
sous-type** de la couche.

Les champs (fichier .GCT) connaissent un certain nombre de contraintes (TODO) :

* Les noms des attributs ne sont pas limités en longueur.
* Seuls les champs de types entier, réel et chaîne de caractère sont gérés. 
  Les autres types ne peuvent pas être créés pour le moment, même s'ils existent 
  dans le modèle GeoConcept.

Le pilote OGR pour GeoConcept ne gère pas les fonctions de suppression.

Options de création de jeux de données
========================================

*EXTENSION=TXT|GXT* : indique l'extension de l'export GeoConcept.

*CONFIG=chemin_du_GCT* : Dans le fichier GCT, chaque ligne doit commencer avec 
%%//#%% suivi par un mot-clé. Les lignes commençant par %%//%% sont des commentaires.

* Section de configuration : le fichier GCT commence avec %%//#SECTION CONFIG%% 
  et finit avec %%//#ENDSECTION CONFIG%%. L'ensemble de la configuration est 
  contenue entre ces marqueurs.

* Section Carte : uniquement pour documentation au moment de l'écriture de ce 
  document. Cette section commence avec %%//#SECTION MAP%% et finit avec 
  %%//#ENDSECTION MAP%%.

* Section Type : définit une classe de caractéristiques. Un type a un nom (Name) 
  et un identifiant (ID). Un type contient des sous-types et des champs. 
  Marqueurs : %%//#SECTION TYPE%% en début et %%//#ENDSECTION%% TYPE en fin.

* Section Sous-type : cette sous-section définit un type de caractéristique dans 
  une classe. Un sous-type a un nom (Name), un identifiant (ID), un type de 
  géométrie (Kind) et une dimension. Les types suivants de géométrie sont gérés : 
  POINT, LINE et POLYGON. La version actuelle du pilote ne gère pas la géométrie 
  TEXT. Les dimensions peuvent être 2D, 3DM ou 3D. Un sous-type contient les 
  champs. Marqueurs : %%//#SECTION SUBTYPE%% et %%//#ENDSECTION SUBTYPE%%.

* Section Champs : Définit les champs de l'utilisateur. Un champ a un nom 
  (Name), un identifiant (ID), un type (Kind). Les types suivants sont gérés : 
  Entier, (INT), Réel (REAL), MEMO, Choix (CHOICE), Date, Heure (TIME), Longueur 
  (LENGHT), Aire (AREA). Marqueurs : %%//#SECTION FIELD%% et %%//#ENDSECTION FIELD%%.

Les règles suivantes s'appliquent dans la section "champs" :

* Les champs aux noms privés commencent avec un @ (''Identifier, Class, 
  Subclass, Name, NbFields, X, Y, XP, YP, Graphics, Angle'').
* Quelques champs privés sont obligatoires (ils doivent apparaître dans la 
  configuration) : *Identifier*, *Class*, *Subclass*, *Name*, *X*, 
  *Y*.
* Si le sous-type est linéaire (LINE), les champs suivants doivent être déclarés 
  XP, YP.
* Si le sous-type est linéaire ou polygonal (LINE, POLYGON), ''Graphics'' doit 
  être déclaré.
* Si le sous-type est ponctuel ou textuel (POINT, TEXT), ''Angle'' doit être 
  déclaré.
  Quand cette option n'est pas utilisée,le pilote gère les types et sous-types 
  soit sur la base du nom de la couche, soit en utilisant l'option ''-nln''.

Options de création de couche
===============================

FEATURETYPE=TYPE.SUBTYPE : définit les éléments à créer. TYPE correspond à un 
des noms (Name) présents dans le fichier .GCT pour une section "type". SUBTYPE 
correspond au nom (Name) présent dans la section sous-type de la section type 
concernée.

At the present moment, coordinates are written with 2 decimales for cartesian
+spatial reference systems (including height) or with 9 decimales for
+geographical spatial reference systems.

Exemples
==========

Exemple de fichier .GCT
************************

  ::
    
    //#SECTION CONFIG
    //#SECTION MAP
    //# Name=SCAN1000-TILES-LAMB93
    //# Unit=m
    //# Precision=1000
    //#ENDSECTION MAP
    //#SECTION TYPE
    //# Name=TILE
    //# ID=10
    //#SECTION SUBTYPE
    //# Name=TILE
    //# ID=100
    //# Kind=POLYGON
    //# 3D=2D
    //#SECTION FIELD
    //# Name=IDSEL
    //# ID=101
    //# Kind=TEXT
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=NOM
    //# ID=102
    //# Kind=TEXT
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=WITHDATA
    //# ID=103
    //# Kind=INT
    //#ENDSECTION FIELD
    //#ENDSECTION SUBTYPE
    //#ENDSECTION TYPE
    //#SECTION FIELD
    //# Name=@Identifier
    //# ID=-1
    //# Kind=INT
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@Class
    //# ID=-2
    //# Kind=CHOICE
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@Subclass
    //# ID=-3
    //# Kind=CHOICE
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@Name
    //# ID=-4
    //# Kind=TEXT
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@X
    //# ID=-5
    //# Kind=REAL
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@Y
    //# ID=-6
    //# Kind=REAL
    //#ENDSECTION FIELD
    //#SECTION FIELD
    //# Name=@Graphics
    //# ID=-7
    //# Kind=REAL
    //#ENDSECTION FIELD
    //#ENDSECTION CONFIG

Exemple de fichier .GXT
************************
  ::
    
    //$DELIMITER "	"
    //$QUOTED-TEXT "no"
    //$CHARSET ANSI
    //$UNIT Distance=m
    //$FORMAT 2
    //$SYSCOORD {Type: 2001}
    //$FIELDS Class=TILE;Subclass=TILE;Kind=4;Fields=Private#Identifier	Private#Class	Private#Subclass	Private#Name	Private#NbFields	IDSEL	NOM	WITHDATA	Private#X	Private#Y	Private#Graphics
    -1      TILE    TILE    TILE    3       000-2007-0050-7130-LAMB93               0       50000.00        7130000.00      4       600000.00       7130000.00      600000.00       6580000.00      50000.00        6580000.00      50000.00        7130000.00
    +-1     TILE    TILE    TILE    3       000-2007-0595-7130-LAMB93               0       595000.00       7130000.00      4       1145000.00      7130000.00      1145000.00      6580000.00      595000.00       6580000.00      595000.00       7130000.00
    +-1     TILE    TILE    TILE    3       000-2007-0595-6585-LAMB93               0       595000.00       6585000.00      4       1145000.00      6585000.00      1145000.00      6035000.00      595000.00       6035000.00      595000.00       6585000.00
    +-1     TILE    TILE    TILE    3       000-2007-1145-6250-LAMB93               0       1145000.00      6250000.00      4       1265000.00      6250000.00      1265000.00      6030000.00      1145000.00      6030000.00      1145000.00      6250000.00
    +-1     TILE    TILE    TILE    3       000-2007-0050-6585-LAMB93               0       50000.00        6585000.00      4       600000.00       6585000.00      600000.00       6035000.00      50000.00        6035000.00      50000.00        6585000.00
 

Exemple d'utilisation
**********************

  Création d'un GXT :
  ::
    
    ogr2ogr -f "Geoconcept" -a_srs "+init=IGNF:LAMB93" -dsco EXTENSION=txt 
    -dsco CONFIG=tile_schema.gct tile.gxt tile.shp -lco FEATURETYPE=TILE.TILE

  Annexer de nouveaux éléments à un fichier .GXT existant :
  ::
    
    ogr2ogr -f "Geoconcept" -update -append tile.gxt tile.shp -nln TILE.TILE

  traduire un fichier .GXT en fichier Mapinfo :
  ::
    
    ogr2ogr -f "MapInfo File" -dsco FORMAT=MIF tile.mif tile.gxt TILE.TILE

.. seealso::

  * `Site officiel de GeoConcept <http://www.geoconcept.com>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/07/10 (trunk 16683)
