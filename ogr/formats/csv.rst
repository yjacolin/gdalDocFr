.. _`gdal.ogr.formats.csv`:

============================
Comma Separated Value (.csv)
============================

OGR gère la lecture et l'écriture de données essentiellement tabulaire 
non-spatiale dans des fichiers CSV texte. Les fichiers CSV sont des formats 
d'échange commun entre les logiciels gérant les données tabulaires et sont 
également facilement produit manuellement avec un éditeur de texte ou avec un 
programme ou des scripts écrit par l'utilisateur.

Bien qu'en théorie les fichiers csv peuvent avoir n'importe quelle extension, 
dans le but de reconnaitre automatiquement le format OGR gère seulement les 
fichiers se terminant avec l'extension csv. Le nom de la source de données peut 
être soit un fichier seul ou un répertoire. Pour qu'un répertoire soit reconnu 
comme une source de données csv au moins la moitié des fichiers dans le 
répertoire doivent avoir l'extension csv. Une couche (table) est produite pour 
chaque fichiers csv accédés.

Starting with GDAL 1.8.0, for files structured as CSV, but not ending with 
.CSV extension, the 'CSV:' prefix can be added before the filename to force
loading by the CSV driver.

Le pilote CSV d'OGR gère la lecture et l'écriture. Parce que le format CSV a 
des lignes de longueur variable, la lecture est réalisée séquentiellement. La 
lecture des géométries dans un ordre aléatoire sera généralement très lente. 
Les couches CSV d'OGR n'ont jamais de systèmes de coordonnées pour les objets. 
Lors de la lecture d'un champ nommé "WKT" il est supposé contenir une géométrie 
WKT, mais est également traité comme un champ normal. Le pilote CSV d'OGR 
renverra tous les attributs des colonnes avec un type chaine de caractère s'il 
n'y a aucun fichier d'information sur le type des champs (avec l'extension 
.csvt) n'est disponible.

Une reconnaissance limitée des types peut être réalisé pour les entiers 
(Integer), les réels (Real), les chaines de caractères (String), les dates 
(Date : YYYY-MM-DD), Time (HH:MM:SS+nn) et DateTime (YYYY-MM-DD HH:MM:SS+nn) 
par un fichier descriptif de même nom que le fichier CSV, mais avec l'extension 
.csvt. Les types de chaque colonne doivent être listés en une seule ligne : 
entouré de guillemet double et séparé par des virgules (par exemple, "Integer",
"String"). Il est également possible de définir explicitement la largeur et la 
précision de chaque colonne,par exemple "Integer(5)","Real(10.7)","String(15)". 
Le pilote utilisera alors ces types comme spécifiés pour les colonnes CSV.

Format
=======

Les fichiers CSV ont une ligne pour chaque objet (enregistrement) dans la couche 
(table). Les valeurs du champ attributaire sont séparées par des virgules. Au 
moins deux champs par ligne doivent être présent. Les lignes peuvent se terminer 
par une terminaison de ligne du style DOS (CR/LF) ou Unix (LF). Chaque 
enregistrement doit avoir le même nombre de champs. À partir de GDAL 1.7.0, le 
pilote acceptera une virgule ou une tabulation comme séparateur de champs. Cette 
auto-détection  fonctionnera seulement s'il n'y a pas d'autres séparateurs 
potentiels  à la première ligne du ficheir CSV. Sinon la virgule sera la valeur 
par défaut comme séparateur.

Les valeurs des attributs complexes (tels que ceux contenant des virgules, des 
guillemets ou de nouvelles lignes) peuvent être placé entre double guillemet. 
N'importe quelle occurrence de guillemet double dans une chaine entre guillemet 
doit être doublé pour la protéger.

Le pilote tente de traiter la première ligne du fichier comme une liste de noms 
de champ pour tous les champs. Cependant, si un ou plusieurs champs sont 
numérique il est supposé que la première ligne est en réalité des valeurs de 
données et des noms de champs factices sont générés en interne ((field_1 à 
field_n) et le premier enregistrement est traité comme un objet. 

.. versionadded:: 1.9.0 Les valeurs numériques sont traités comme noms de 
   champs si elles sont entourées de guillemets doubles.

Tous les fichiers CSV sont traité comme encodé en UTF-8. À partir de GDAL 
1.9.0, un *Byte Order Mark* (BOM) en début de fichier sera interprété 
correctement. À partir de la 1.9.2 l'option *WRITE_BOM* peut être 
utilisée pour créer un fichier avec un *Byte Order Mark*, ce qui peut 
améliorer la compatibilité avec certain logiciel (particulièrement Exczel).

Exemple (employee.csv) :

::
    
    ID,Salary,Name,Comments
    132,55000.0,John Walker,"The ""big"" cheese."
    133,11000.0,Jane Lake,Cleaning Staff

Notez que la valeur *Comments* pour le premier enregistrement de données est 
placé entre guillemet double à cause de la valeur contenant un guillemet, et ces 
guillemets doivent être doublé pour que nous sachions que nous avons pas atteint 
la fin de la chaine du guillemet.

Plusieurs variations des entrées textuel sont parfois appelées fichiers à Valeur 
Séparée par des Virgules (*Comma Separated Value*), incluant les fichiers sans 
virgule, mais à colonne à largeur fixe, ceux utilisant des tabulations comme 
séparateur ou ceux avec données auxiliaire définissant des types de champs ou 
de structure. Ce pilote ne tente pas de gérer de tel fichier mais à la place 
gère des fichiers .csv simple qui peuvent être reconnus automatiquement. Des 
scripts ou d'autres mécanismes peuvent généralement convertir les autres 
variations sous une forme qui est compatible avec le pilote CSV d'OGR.

Lecture de fichier CSV contenant des informations spatiales
===========================================================

Il est possible d'extraire l'information spatiale (points) d'un fichier CSV qui 
possède des colonnes pour les coordonnées X et Y, par l'utilisation du pilote 
VRT.

Considérez le fichier CSV suivant (test.csv) :

::
    
    Latitude,Longitude,Name
    48.1,0.25,"First point"
    49.2,1.1,"Second point"
    47.5,0.75,"Third point"

Vous pouvez écrire le fichier VRT associé (test.vrt) :

::
    
    <OGRVRTDataSource>
        <OGRVRTLayer name="test">
            <SrcDataSource>test.csv</SrcDataSource>
            <GeometryType>wkbPoint</GeometryType>
            <LayerSRS>WGS84</LayerSRS>
            <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude"/>
        </OGRVRTLayer>
    </OGRVRTDataSource>


et ``ogrinfo -ro -al test.vrt`` renverra :

::
    
    OGRFeature(test):1
        Latitude (String) = 48.1
        Longitude (String) = 0.25
        Name (String) = First point
        POINT (0.25 48.1 0)

    OGRFeature(test):2
        Latitude (String) = 49.2
        Longitude (String) = 1.1
        Name (String) = Second point
        POINT (1.1 49.200000000000003 0)

    OGRFeature(test):3
        Latitude (String) = 47.5
        Longitude (String) = 0.75
        Name (String) = Third point
        POINT (0.75 47.5 0)

Problèmes lors de la création
==============================

Le pilote gère la création de nouvelles base de données (comme un répertoire de 
fichier .csv), en ajoutant de nouveaux fichiers csv à un répertoire existant un 
fichier csv ou en ajoutant des objets à une table CSV existante. La suppression 
ou le remplacement d'objets existants n'est pas gérés.

Options de création de couche :

* **LINEFORMAT :** par défaut lors de la création d'un nouveau fichier csv 
  ceux-ci sont créés avec les conventions de fin de ligne de la plateforme local 
  (CR/LF sous win32 ou LF sur tous les autres systèmes). cela peut être écrasé 
  par l'utilisation de l'option de création de couche *LINEFORMAT* qui peut 
  avoir les valeurs *CRLF* (format DOS) ou *LF* (format Unix).
* **GEOMETRY (débute avec GDAL 1.6.0) :** par défaut, la géométrie d'un objet 
  écrit dans un fichier csv est ignoré. Il est possible d'exporter la géométrie 
  dans sa représentation WKT en spécifiant ``GEOMETRY=AS_WKT``. Il est également 
  posible d'exporter les géométries ponctuelles dans leurs composants X,Y,Z 
  (différentes colonnes dans le fichier csv) en spécifiant ``GEOMETRY=AS_XYZ``, 
  ``GEOMETRY=AS_XY`` ou *GEOMETRY=AS_YX*. Les colonnes géométriques seront 
  ajoutées à la colonne avec les valeurs des attributs.
* **CREATE_CSVT=YES/NO (débute avec GDAL 1.7.0) :** créer le fichier associé 
  .csvt (voir plus haut dans le paragraphe) pour décrire le type de chaque 
  colonne de la couche et ses largeurs et précisions optionnelles. Valeur par 
  défaut : NO
* **SEPARATOR=COMMA/SEMICOLON/TAB (à partir de GDAL 1.7.0):** caractère de 
  séparateur de champ. Valeur par défaut : COMMA
* **WRITE_BOM =YES/NO :** (À partir de GDAL >1.9.2) Écrit un *Byte Order Mark* 
  UTF-8 (BOM) au début du fichier. Valeur par défaut: *NO*.

Gestion de l'API du Système de Fichier Virtuel VSI
===================================================

(Certaines fonctions ci-dessous peuvent nécessiter OGR >= 1.9.0).
 
Le pilote gère la lecture et l'écriture vers les fichiers gérés par l'API 
du Système de Fichier Virtual VSI, ce qui inclus les fichiers "normaux" 
ainsi que les fichiers dans les domaines /vsizip/ (lecture-écriture), 
/vsigzip/ (lecture-écriture), /vsicurl/ (lecture seule).

L'écriture vers /dev/stdout ou /vsistdout/ est également géré.

Exemples
*********

* cet exemple montre l'utilisation d``'ogr2ogr`` pour transformer un shapefile 
  avec une géométrie ponctuelle en un fichier .csv avec les coordonnées X,Y,Z 
  des points comme premières colonnes dans le fichier .csv
  ::
    
      ogr2ogr -f CSV output.csv input.shp -lco GEOMETRY=AS_XYZ

Sources de données particulières
=================================

Le pilote CSV peut également lire des fichiers dont la structure est proche des 
fichiers CSV :

* Fichier données Airport NfdcFacilities.xls, NfdcRunways.xls, NfdcRemarks.xls et NfdcSchedules.xls
  trouve sur le `FAA website <http://www.faa.gov/airports/airport_safety/airportdata_5010/menu/index.cfm">`_ (OGR >= 1.8.0)
* Fichier du `USGS GNIS <http://geonames.usgs.gov/domestic/download_data.htm">`_ (Geographic Names Information System) (OGR >= 1.9.0)
* The allCountries file from `GeoNames <http://www.geonames.org>`_ (OGR >= 1.9.0 for direct import)
* `Fichiers .TSV d'Eurostat <http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=read_me.pdf>`_

Autres remarques
=================

* le développement du pilote CSV d'OGR a été financé par 
  `DM Solutions Group <http://www.dmsolutions.ca/>`_ et `GoMOOS <http://www.gomoos.org/>`_. 

.. yjacolin at free.fr, Yves Jacolin - 2013/01/23 (trunk 25355)
