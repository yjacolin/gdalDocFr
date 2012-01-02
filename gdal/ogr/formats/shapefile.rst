.. _`gdal.ogr.formats.shapefile`:

ESRI Shapefile
===============

Toutes les variétés de Shapefiles d'ESRI devraient être disponibles en lecture 
et les fichiers 3D simple peuvent être créés.

Normalement le pilote OGR Shapefile traite un ensemble de répertoire contenant 
des shapefiles comme source de données, et un shapefile dans ce répertoire comme 
couche. Dans ce cas le nom du répertoire doit être utilisé comme nom de la 
source de données. Cependant, il est également possible un seul des fichiers 
(.shp, .shx or .dbf) dans le jeu du shapefile comme nom du jeu de données, et 
il sera alors traité comme un jeu de données avec une couche;

Notez que lors de la lecture d'un Shapefile de type *SHPT_ARC*, la couche 
correspondante sera reportée comme de type *wkbLineString* mais en fonction 
du nombre de parts de chaque géométrie, le type réel de la géométrie pour chaque 
objet peut être soit *OGRLineString* soit *OGRMultiLineString*. La même 
chose s'applique pour les Shapefiles *SHPT_POLYGON*, reporté comme couches de 
type *wkbPolygon* mais en fonction du nombre de parts de chaque géométrie, 
le type réel peut être soit *OGRPolygon* ou *OGRMultiPolygon*.
 
Les nouvelles valeurs de mesures d'ESRI seront ignorées si rencontrées. Les 
fichiers multipatch sont lu et chaque patch de la géométrie est retourné dans une 
représentation multipolygone avec un polygone par triangle dans les mailles et 
les fans du triangle.

Si des fichiers .prj dans l'ancien style Arc/Info ou le nouveau style ESRI en 
WKT de l'OGC sont présent, ils seront lus et utilisés pour associer une 
projection avec les géométries.

Le pilote de lecture suppose que les polygones multipart suivent la 
spécification, c'est-à-dire que les sommets des anneaux externes doivent être 
orientés dans le sens des aiguilles d'une montre sur le plan x/y, et ceux de 
l'anneau intérieur en sens inverse. Si un Shapefile est cassé, il est possible 
de définir l'option de configuration *OGR_ORGANIZE_POLYGONS=DEFAULT* afin de 
procéder à une analyse complète basée sur les relations topologiques des 
parties des polygones afin que les polygones résultants soient correctement 
définie selon la convention OGC Simple Feature.

Une tentative est faite pour lire la définition du LDID/codepage à partir du 
fichier .dbf et l'utiliser pour traduire les champs de chaîne en UTF-8 lors de 
la lecture, puis vers l'écriture. LDID "87 / 0x57" est considéré comme ISO8859_1 
qui peut ne pas être approprié.

L'`option de configuration <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ 
SHAPE_ENCODING peut être utilisé pour écraser l'interprétation de l'encodage du 
shapefile par n'importe quel encodage géré par CPLRecode ou par "" pour éviter 
n'importe quel enregistrement (la gestion de l'enregistrement est nouveau dans 
GDAL/OGR 1.9.0).

Indexe spatiale et attributaire
--------------------------------

Le pilote OGR shapefile gère l'indexage spatial et une forme limitée d'indexage 
attributaire.

L'indexage spatial utilise les mêmes fichiers d'index spatial *quadtree* .qix 
qui sont utilisés par MapServer. !il ne gère pas les fichiers d'inde spatiale 
d'ESRI (.sbn / .sbx). L'index spatial peut accélérer les parsages avec des 
filtres spatiaux pour d'importants jeux de données pour récupérer une portion 
d'une zone rapidement.

Pour créer un index spatial, envoyer une commande SQL de la forme :
::
    
    CREATE SPATIAL INDEX ON nomTable [DEPTH N]

où le paramètre optionnel ''DEPTH'' peut être utilisé pour contrôler le nombre 
de niveaux de l'arbre d'index généré. Si ''DEPTH'' est omis, la profondeur de 
l'arbre est estimée sur la base de nombre de géométrie dans un shapefile et son 
domaine de valeur de 1 à 12.

Pour effacer un index spatial, envoyez une commande de la forme :
::
    
    DROP SPATIAL INDEX ON nomTable

Autrement, la commande shptree de `MapServer <http://mapserver.org>`_ peut être 
utilisée.

::
    
    shptree <shpfile> [<depth>] [<index_format>]

Plus d'information est disponible sur cette commande sur la page 
`shptree de MapServer <http://mapserver.org/utilities/shptree.html>`_.

Pour l'instant le pilote OGR shapefile gère seulement les indexes d'attribut 
pour rechercher des valeurs spécifiques dans une colonne de clé unique. Pour 
créer un index d'attribut pour une colonne, envoyez une commande SQL de la 
forme *CREATE INDEX ON nomTable USING nomchamp*. Pour supprimer des index 
d'attribut envoyez une commande de la forme *DROP INDEX ON nomTable*. L'index 
d'attribut accélèrera les recherches des clauses *WHERE* de la forme *nomChamp 
= valeur*. L'index d'attribut est en réalité stocké comme un index au format 
mapinfo et n'est pas compatible avec toute autre application shapefile.


Problèmes de création
----------------------

Le pilote shapefile traite un répertoire comme un jeu de données, et chaque 
ensemble Shapefile (.shp, .shx, and .dbf) comme une couche. Le nom du jeu de 
données sera créé comme un nom de répertoire. Si le répertoire existe déjà il 
est utilisé et les fichiers existants dans le répertoire sont ignorés. Si le 
répertoire n'existe pas, celui-ci sera créé.

Une tentative de création d'un nouveau jeu de données avec une extension .shp 
résultera en un ensemble de fichiers crée à la place d'un répertoire.

Les shapefile d'ESRI peuvent seulement stocker un type de géométrie par couche 
(shapefile). En création cela peut être basé sur le fichier source (si un type 
de géométrie uniforme est connu par le pilote source), ou il peut être défini 
directement par l'utilisateur avec l'option de création SHPT (indiqué plus bas). 
S'il n'est pas connu, la création de la couche échouera. Si des géométries d'un 
type incompatible sont écrites vers la couche, l'envoi en sortie échouera avec 
un message d'erreur.

Notez qu'il peut rendre plus difficile la translation d'une couche de géométrie 
mixte d'un format vers un format Shapefile en utilisant ``ogr2ogr``, puisque 
``ogr2ogr`` ne gère pas la séparation des géométries d'une couche source. 
Lisez la FAQ pour une solution.

Les attributs des géométries du Shapefile sont stockés dans un fichier .dbf 
associé, et donc les attributs souffrent d'un certain nombre de limitations :

* les noms des attributs ne peuvent avoir qu'au maximum 10 caractères. Les noms 
  plus longs seront tronqués. Cela peut entraîner des noms de colonnes qui ne 
  sont pas uniques, qui sans aucun doute poseront problème plus tard.
* À partir de la version 1.7, le pilote Shapefile d'OGR tente de générer des noms 
  de champs uniques. Des noms de champs dupliqués successifs, incluant ceux créés 
  par troncation à 10 caractères, seront tronqué à 8 caractères et un numéro 
  ajouté de 1 à 99. 
  
  Par exemple :
  
  * a -> a, a -> a_1, A -> A_2;
  * abcdefghijk -> abcdefghij, abcdefghijkl -> abcdefgh_1

* Seul des champs de type *entier*, *réel* et *chaine de caractère* sont gérés 
  (pas DateTime, juste year/month/day). Les champs de types *liste diverse* et 
  *binaire* ne peuvent pas être crée.
* La largeur du champ et la précision sont directement utilisées pour établir 
  la taille de stockage dans le fichier .dbf. Cela signifie que les chaines plus 
  longues que la largeur du champ, ou les nombres qui ne remplissent pas les 
  conditions du format du champ seront tronquées.
* les champs d'*entier* sans une largeur explicite sont traité avec une largeur 
  de 11.
* les champs *réel* (point flottant) sans une largeur explicite sont traité avec 
  une largeur de 24 avec 15 chiffres pour les décimales.
* les champs *caractères* sans une largeur assignée sont traité avec une largeur 
  de 80 caractères.

Également, les fichiers .dbf doivent avoir au moins un champ. Si aucun n'est 
créé par l'application, un champ "FID" sera automatiquement créé et remplit des 
numéros d'enregistrement.

Le pilote shapefile d'OGR gère la réécriture des shapes existant dans un 
shapefile ainsi que la suppression des shapes. La suppression des shapes est 
notée comme supprimé dans le fichier .dbf, et seront ainsi ignoré par OGR. Pour 
les supprimer réellement (entrainant une renumérotation des FID) appeler la 
fonction SQL 'REPACK' par la méthode *ExecuteSQL()* de la source de données.

Étendue spatiale
----------------

Shapefiles stocke l'étendue spatiale de al couche dans le fichier .SHP. L'étendue 
spatiale de la couche est automatiquement mis à jour lors de l'insertion d'une 
nouvelle feature dans le shapefile. Cependant lors de la mise à jour d'une feature 
existante, si la forme précédente a touché la bounding box de l'étendue spatiale 
mais la forme mise à jour ne touche pas le nouvelle étendue, l'étendue calculée 
ne sera pas correcte. Il sera alors nécessaire de forcer le calcul en invoquant 
la commande SQL 'RECOMPUTE EXTENT ON <tablename>' via la méthode *ExecuteSQL()* 
de la source de données. La même chose s'applique pour la suppression d'une shape.

.. note:: RECOMPUTE EXTENT ON est disponible à partir d'OGR >= 1.9.0.

Problèmes sur les tailles
--------------------------

* Geometry : le format Shapefile utilise explicitement des offsets de 32 bits et 
  ne put donc pas dépasser 8 Go (il utilise en réalité des offsets de 32 bit vers 
  des mots de 16 bits). Par conséquent il n'est pas recommendé d'utiliser un 
  fichier de plus de 4 Go.

* Attributs : le format dbf ne contient aucun offsets, il peut donc être 
  arbitrairement large.

Options de création de jeu de données
--------------------------------------

Aucune option.

Options de création de couches
--------------------------------

* **SHPT=type :** écrase le type de shapefile crée. Peut être une parmi NULL 
  pour un simple fichier .dbf. avec aucun fichier .shp, *POINT*, *ARC*, 
  *POLYGON* ou *MULTIPOINT* pour la 2D, ou *POINTZ*, *ARCZ*, *POLYGONZ* ou 
  *MULTIPOINTZ* pour la 3D. Les shapefiles avec des valeurs de mesure ne sont 
  pas gérés, ni les fichiers *MULTIPATCH*.
* **ENCODING=value :** définie la valeur de l'encodage dans le fichier DBF. La 
  valeur par défaut est "LDID/87". Il n'est pas clair quelles autres valeurs 
  peuvent être appropriées.

Exemples
---------

Un merge de deux shapefile *file1.shp* et *file2.shp* dans un nouveau fichier 
*file_merged.shp* est réalisée de cette manière :
::
    
    % ogr2ogr file_merged.shp file1.shp
    % ogr2ogr -update -append file_merged.shp file2.shp -nln file_merged

La seconde commande ouvre le fichier file_merged.shp en mode 'mise à jour' et 
tente de trouver des couches existantes et d'ajouter des géométries en copie.

L'option *-nln* définie le nom de la couche à copier.

Lisez également
----------------

* `Shapelib Page <http:*shapelib.maptools.org/>`_
* `ESRI Shapefile Technical Description <http://www.esri.com/library/whitepapers/pdfs/shapefile.pdf>`_
* Notes utilisateurs sur le pilote Shapefile d'OGR <http://trac.osgeo.org/gdal/wiki/UserDocs/Shapefiles>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/09/03 (trunk 22176)
