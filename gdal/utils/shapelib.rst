.. `gdal.utils.shapelib`:

ShapeLib
=========

 * Site : http://shapelib.maptools.org/
 * Thématique : outils en ligne de commande de gestion de données au format Shapefile
 * Documentation : http://shapelib.maptools.org/shapelib-tools.html

Description
-------------
(ceci est une traduction du site).

La bibliothèque C Shapefile fournie la possibilité d'écrire de simple programme 
en c pour lire, écrire et mettre à jour (dans une étendue limitée) des Shapefile 
d'ESRI, et leur attribut associé (.dbf). Des outils à utiliser en ligne de 
commande sont fournies avec cette bibliothèque.

Outils
--------
Liste des outils :

  * dbfcreate
  * dbfadd
  * dbfdump
  * shpcreate
  * shpadd
  * shpdump
  * shprewind
  * Outils du répertoire 'contrib' de ShapeLib

    * dbfinfo
    * dbfcat
    * shpinfo
    * shpcat
    * shpcentrd
    * shpdxf
    * shpfix
    * shpproj

dbfcreate
***********

 * **Objectif :** créer un nouveau fichier .dbf vide.
 * **Usage :** dbfcreate xbase_file [ [ -s field_name width ],[ -n field_name width decimals ] ]...

   * *xbase_file :* le nom du fichier xBase à créer. Pas besoin de spécifier 
     l'extension.
   * *-s field_name width :* créer un champ *string* nommé *field_name* et une 
     taille de *width*.
   * *-n field_name width decimals :* créer un champ numérique nommé *field_name*, 
     de longueur *width*et avec un nombre de décimal de *decimals*.

**Exemple :**
::
    
    $ dbfcreate testbase -s NAME 20, -n AREA 9 3, -n VALUE 9 2
    # this will create a file named testbase.dbf with 3 fields:
    NAME ( string (20)), AREA ( float (9,3)) and VALUE ( float (9,2))

dbfadd
********

 * **Objectif :** ajoute un enregistrement dans un fichier .dbf existant.
 * **Usage :** dbfadd xbase_file field_values

   * *xbase_file :* le nom du fichier xBase existant.
   * *field_values :* liste valeurs à insérer dans le fichier xBase. Vous devez 
     spécifier un nombre de valeur égale au nombre de champ que possède le fichier 
     xBase. L'ordre des valeurs doit également refléter l'ordre des champs dans 
     le fichier xBase.

**Exemple :**
  $ dbfadd testbase.dbf REGION1 25.656 150.22
  # en supposant que testbase.dbf possède 3 champs ( NAME, AREA and VALUE), cette commande insérera un 
  nouvel enregistrement dans *testbase.dbf* avec les valeurs "REGION1" pour le champ NAME, '25.656' 
  pour le champ AREA et '150.22' pour le champ VALUE.

dbfdump
********

 * **Objectif :** dump le contenu d'un fichier xBase vers la console.
 * **Usage :** dbfdump [-h] [-r] [-m] xbase_file

   * *-h :* affiche les informations de l'en-tête (descriptions des champs) ;
   * *-r :* résultat brute des informations des champs, valeurs numériques non 
     reformatées ;
   * *-m :* résultat une ligne par champ ;
   * *xbase_file :* le nom d'un fichier xBase existant.

**Exemple :**
::
    
    $ dbfdump -h testbase.dbf
    # en supposant que testbase.dbf a un enregistrement (inséré par l'exemple précédent en utilisant 
    ''dbfadd''), cette commande produira les données suivantes :
    Field 0: Type=String, Title=`NAME', Width=20, Decimals=0
    Field 1: Type=Double, Title=`AREA', Width=9, Decimals=3
    Field 2: Type=Double, Title=`VALUE', Width=9, Decimals=2
    NAME AREA VALUE
    REGION1 25.656 150.22 

shpcreate
***********

  * **Objectif :** créé un nouveau fichier shapefile vide.
  * **Usage :** shpcreate shp_file [point|arc|polygon|multipoint]

    * *shp_file :* le nom du shapefile à créer. Ne nécessite pas d'extension.
    * *point/arc/polygon/multipoint :* le type de shapefile que vous voulez créer. Vous devez définir une option valide.

**Exemple :**
::
    
    $ shpcreate testpolygon polygon
    # Cela créera un shapefile ponctuel nommé *testpolygon* (en fait testpolygon.shp et testpolygon.shx 
    seront créé). 

shpadd
********

 * **Objectif :** ajoute un shape dans un shapefile existant.
 * **Usage :** shpadd shp_file [ [x y] [+] ]*

   * *shp_file :* le nom d'un shapefile existant.
   * *x1 y1 x2 y2 ... xn yn :* l'ensemble des coordonnées x,y qui décrivent le 
     shape que vous désirez ajouter. Notez que vous devez définir le nombre 
     correcte de paramètres pour un type données de shapefile. Par exemple : 
     pour les shapefiles ponctuels vous devez passer une paire de coordonnées 
     XY et pour un shapfile polygonale vous devez passer au moins 4 paires de 
     coordonnées XY (où le premier et le dernier point doivent avoir les mêmes 
     coordonnées).

**Exemple :**
::
    
    $ shpadd testpolygon 100000 7000000 250000 6500000 200000 6000000 100000 7000000
    # en supposant que testpolygon est un shapefile polygonal, cette commande insérera un nouveau shape (un 
    triangle) dans *testpolygon* avec les coordonnées XY suivantes :
    vertice 0: 100000 7000000 (cela sera également le sommet où le shape démarre et se termine)
    vertice 1: 250000 6500000
    vertice 2: 200000 6000000
    vertice 3: 100000 7000000

shpdump
********

 * **Objectif :** dump le contenu d'un shapefile en affichant l'information comme 
   le type de shape, l'étendue du fichier, le nombre total d'objets et les 
   coordonnées des sommets.
 * **Usage :** shpdump [-validate] shp_file

   * *-validate :* compte le nombre d'objets qui possède un ordonnancement 
     incorrect de l'anneau.
   * *shp_file :* le nom du shapefile existant.

**Exemple :**
::
    
    $ shpdump testpolygon
    # en supposant que *testpolygon* est un shapefile existant déjà créé, cette commande affichera le 
    résultat suivant :
    
        Shapefile Type: Polygon   # of Shapes: 1
        
        File Bounds: (  100000.000, 6000000.000,0,0)
                to  (  250000.000, 7000000.000,0,0)
        
        Shape:0 (Polygon)  nVertices=4, nParts=1
        Bounds:(  100000.000, 6000000.000, 0, 0)
            to (  250000.000, 7000000.000, 0, 0)
            (  100000.000, 7000000.000, 0, 0) Ring
            (  250000.000, 6500000.000, 0, 0)
            (  200000.000, 6000000.000, 0, 0)
            (  100000.000, 7000000.000, 0, 0)

shprewind
**********

 * **Objectif :** valide et reset l'ordre d'enroulement de l'anneau dans les 
   géométries polygonales pour correspondre aux nécessités de la spécification 
   des shapefile. Cela est utile pour les shapefile ayant des problèmes avec un 
   'shpdump -validate'.
 * **Usage :** shprewind in_shp_file out_shp_file

   * *in_shp_file :* le nom d'un shapefile existant.
   * *out_shp_file :* le nom d'un nouveau shapefile corrigé qui sera créé.

**Exemple :**
::
    
    $ shprewind badshapefile newshapefile 

dbfinfo
**********

 * **Objectif :** affiche des informations basiques pour un fichier xBase donné, 
   comme le nombre de colonne, le nombre d'enregistrement et le type de chaque 
   colonne.
 * **Usage :** dbfinfo xbase_file

  * *xbase_file :* le nom d'un fichier xBase existant.

**Exemple :**
::
    
    $ dbfinfo testbase
    
    Info pour testbase.dbf
    3 Columns,  1 Records in file
           NAME          string  (20,0)
           AREA           float  (9,3)
          VALUE           float  (9,2)

dbfcat
*******

 * **Objectif :** ajoute les enregistrements d'un fichier xBase source dans un 
   fichier xBase finale. Les deux fichiers doivent avoir le même nombre de champs.
 * **Usage :** dbfcat [-v] [-f] from_DBFfile to_DBFfile

  * *-v :* mode verbeux.
  * *-f :* force la conversion des données si les types des champs des données 
    n'est pas le même dans les deux fichiers ou s'il y a des valeurs null dans 
    *from_DBFfile*.
  * *from_DBFfile :* fichier xBase source.
  * *to_DBFfile :* fichier xBase final.

**Exemple :**
::
    
    $ dbfcat -v testbase1 testbase2 

shpinfo
********

 * **Objectif :** affiche des informations basiques pour un shapefile donné, 
   comme le type de shapefile, le nombre d'objets et leurs étendues.
 * **Usage :** shpinfo shp_file

   * *shp_file :* le nom d'un shapefile existant.

**Exemple :**
::
    
    $ shpinfo testpolygon
    
    Info for testpolygon
    Polygon(5), 1 Records in file
    File Bounds: (         100000,        6000000)
            (         250000,        7000000)

shpcat
*******

 * **Objectif :** ajoute le contenu d'un shapfile source dans un shapefile final. 
   Les deux fichiers doivent avoir le même type de shapefile.
 * **Usage :** shpcat from_shpfile to_shpfile

  * *from_shpfile :* shapefile source
  * *to_shpfile :* shapefile final

**Exemple :**
::
    
    $ shpcat shapefile1 shapefile2 

shpcentrd
***********

 * **Objectif :** calcule le centroid XY pour des shapefile polygonaux.
 * **Usage :** shpcentrd shp_file new_shp_file

   * *shp_file :* le nom d'un shapefile polygonale existant
   * *new_shp_file :* le nom d'un shapefile ponctuel qui sera créé.

**Exemple :**
::
    
    $ shpcentrd apolygonfile pointcentrd 

shpdxf
******

 * **Objectif :** créé un fichier DXF à partir d'un fichier shapefile existant.
 * **Usage :** shpdxf shapefile {idfield}

   * *shapefile :* le nom d'un shapefile existant.
   * *idfield :* *à faire*

**Exemple :**
::
    
    $ shpdxf testshapefile IDFIELD
    # ...

shpfix
*******

 * **Objectif :** progamme qui corrige les valeurs nulles et inconsistante dans 
   des Shapefiles comme cela arrive de temps en temps.
 * **Usage :** shpfix shpfile new_file <Record# to Blank>

   * *shpfile :* fichier en entré
   * *new_file :* fichier en sortie

**Exemple :**
::
    
    $ shpfix broken fixed 

shpproj
********

 * **Objectif :** Reprojette des Shapefiles en utilisant PROJ.4
 * **Usage :** shpproj shp_file new_shp ( -i=in_proj_file | -i="in_params" | -i=geographic ) ( -o=out_info_file | -o="out_params" | -o=geographic )

Entré
``````

L'entré peut provenir d'un des trois sources. Un fichier de paramètre de 
projection, directement via des paramètres ou géographique. Si le shapefile 
possède un fichier prj, de même nom que le shapefile mais finissant par ".prj" 
il sera utilisé par défaut et tous les autres paramètres seront ignorés. Si 
l'entré est omise sa valeur par défaut est géographique, sauf si le fichier prj 
existe.

Sortie
```````

La sortie peut provenir d'un des trois sources. Un fichier de paramètre de 
projection, directement via des paramètres ou géographique. Si la sortie est 
omise sa valeur par défaut est géographique.

Fichier de paramètres de projection
````````````````````````````````````

Ce fichier **doit** se terminer avec l'extension ".prj". Il est sous la forme 
d'un paramètre projection par ligne. Les paramètres peuvent être dans n'importe 
quel ordre. Les paramètres de projection sont ceux utilisé pour définir une 
projection PROJ.4.

Paramètres de projection
``````````````````````````

Les paramètres de projection sont les mêmes que ceux utilisés par proj et invproj. Utilisez

 * proj -lP : pour voir les projections disponibles
 * proj -lu : pour voir les unités disponibles
 * proj -le : pour voir les ellipsoïdes disponibles

Ou visitez la page web du projet PROJ.4 sur http://www.remotesensing.org/proj pour plus de détails.

**Exemples :**

Les exemples suivants projettent un fichier *rowtest* vers *row3*, déplace des données de *Stateplane NAD83 zone 1002* vers *utm zone 16* en mètres

::
    
    shpproj rowtest row -i="init=nad83:1002 units=us-ft" -o="proj=utm zone=16 units=m"
    
    shpproj rowtest row3 -o="proj=utm zone=18 units=m" -i="zone=16 proj=utm units=us-ft"
    
    shpproj rowtest row3 -o="proj=utm zone=18 units=m" 
    
    shpproj rowtest row3 -i=myfile.prj -o=geographic
    shpproj rowtest row3 -is=myfile.prj

