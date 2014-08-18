.. _`gdal.ogr.formats.ingres`:

INGRES
======

Le pilote implémente la lecture et l'écriture pour les données spatiales dans 
des tables de base de donnés INGRES. Cette fonctionnalité a été introduite dans 
GDAL/OGR 1.6.0.

Lors de l'ouverture d'une base de données, son nom doit être définie dans la 
forme *@driver=ingres,dbname=dbname[,options]* où les options peuvent être 
listées séparé par des virgules comme *username=*userid*, password=*password*, 
timeout=*timeout*, tables=table1/table2*. Le pilote (driver) et les valeurs de 
*dbname* sont nécessaires alors que le reste est optionnel. Si le nom de 
l'utilisateur et le mot de passe ne sont pas fournie une tentative est faite 
pour s'authentifier comme l'utilisateur encors.

Exemples :
::
    
    @driver=ingres,dbname=test,userid=warmerda,password=test,tables=usa/canada
    
    @driver=ingres,dbname=mapping

Si la liste des tables n'est pas fournie, une tentative est réalisée pour 
énumérer toutes les tables non système comme couches, autrement seul les tables 
listées sont représentées comme couches. Cette option est surtout utile 
lorsqu'une base de données possède beaucoup de tables, et scanner tous les 
schémas pourrait prendre trop de temps.

Si un champ entier nommé "ogr_fid" existe dans une table celui-ci sera nommée 
comme FID, autrement les FIDs seront assignés séquentiellement. Cela implique 
que différents FIDs seront assigné à une enregistrement/objets en fonction des 
filtres de requête attributaire et spatial en un temps données.

Par défaut, les requêtes SQL sont envoyé directement au moteur de base de 
données INGRES. Il est aussi possible de réaliser une requête au pilote pour 
prendre en charge les commandes SQL avec le moteur SQL d'OGR en envoyant la 
chaîne "OGRSQL" à la méthode *ExecuteSQL()* comme nom du dialecte SQL. Pour 
l'instant le pilote INGRES gère seulement les vieux types de données spatiales 
d'INGRES tels que *POLYGON*, *POINT*, *LINE*, *LONG POLYGON*, *LONG LINE*, etc. 
Il est prévue dans le futur qu'un nouvel ensemble de type spatial conforme à 
l'OGC soit géré.

Avertissements
---------------

* Les types spéciaux CIRCLE et ICIRCLE ne sont pas géré pour l'instant en lecture.
* Aucun index spatial rapide n'est utilisé lors de la lecture, les filtres 
  spatiaux sont donc implémenté en lisant et parsant tous les enregistrements, 
  et ceux qui ne satisferaient pas le filtre spatial sont ignorés.
* Il n'y a pas de gestion pour les systèmes de coordonnées.

Problèmes lors de la création
-------------------------------

Le pilote INGRES ne gère pas la création de nouveaux jeux de données (une base 
de données dans INGRES) mais il permet la création de nouvelles couches (tables) 
dans une instance de base de données existante.

* Le pilote INGRES ne permet pas l'encodage de caractères pour le moment.
* Le pilote INGRES n'est pas transactionnel pour le moment.
* les types spatiaux BOX et IBOX ne sont pas gérés pour la création et 
  lorsqu'ils sont lu sont représentés comme des polygones.
* Les types *non-LONG* (tels que *LINE*, *ILINE*, et *POLYGON*) gère seulement 
  un nombre limité de sommet. Toute tentative pour créer des objets avec plus 
  que le maximum de sommet possible pour cette couche échouera.
* Les vieux types spatiaux d'ingres sont très particulier pour les validations 
  géométriques et toute tentative pour insérer (créer) des objets avec des 
  géométries invalides échouera. Les raisons de l'invalidité incluent 
  auto-intersection de polyligne, et auto-intersection de polygones.

Options de création de couche
------------------------------

* **OVERWRITE :** il peut être à "YES" pour forcer une couche existante au 
  nom désiré à être détruite avant la création de la couche voulues.
* **LAUNDER :** il peut être à "YES" pour forcer les nouveaux champs créés sur 
  cette couche pour avoir leur noms de champs "nettoyés" dans une forme 
  compatible avec MySQL. Cela les passe les caractères en minuscule et 
  convertie certains caractères spéciaux comme "-" et "#" en "_". Si "NO" les 
  noms exactes sont préservés. La valeur par défaut est "YES".
* **PRECISION :** il peut être à "TRUE" pour tenter de préserver la largeur et 
  la précisions des champs pour la création et la lecture des couches MySQL. La 
  valeur par défaut est "TRUE".
* **GEOMETRY_NAME :** cette option définie le nom de la colonne géométrique. La 
  valeur par défaut est "SHAPE".
* **INGRES_FID :** cette option définie le nom de la colonne FID. La valeur par 
  défaut est "OGR_FID".
* **GEOMETRY_TYPE :** définie le type d'objet pour la colonne géométrique. Il 
  peut être l'un de *POINT*, *LSEG*, *LINE*, *LONG LINE*, *POLYGON*, ou *LONG 
  POLYGON*. Par défaut *POINT*, *LONG LINE* ou *LONG POLYGON* sont utilisés en 
  fonction du type de couche.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/28 21:36 (trunk 14468)