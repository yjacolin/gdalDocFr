.. _`gdal.ogr.formats.gpx`:

==========================
GPX - GPS Exchange Format
==========================

(à partir de GDAL 1.5.0)

Le format GPX (format d'échange de GPS) est un format de données en XML léger 
pour l'échange de données GPS (waypoints, routes et tracks) entre des 
applications et des webservices sur Internet.

OGR gère la lecture et l'écriture du GPX (si GDAL est compilé avec la gestion 
de la bibliothèque *expat*).

Les versions gérées sont GPX 1.0 et 1.1 en lecture, GPX 1.1 en écriture.

Le pilote OGR gère la lecture et l'écriture de tous les types de géométrie GPX :

* **waypoints :** couche d'objet de type *wbbpoint* d'OGR ;
* **routes :** couche d'objet de type *wkbLineString* d'OGR ;
* **tracks :** couche d'objet de type *wkbMultiLineString* d'OGR.

Il gère également la lecture des points routes et des points tracks dans des 
couches indépendantes (route_points et track_points), ainsi leurs propres 
attributs peuvent être utilisé par OGR.

En plus de ses attributs GPX, chaque point route d'une route a un *route_fid* 
(clé étrangère au FID de sa route dont il fait partie) et un *route_point_id* 
qui est le numéro de séquence dans la route.

La même chose s'applique pour les points tracks avec *track_fid*, *track_seg_id* 
et *track_seg_point_id*. Toutes les coordonnées sont relatives au datum WGS84 
(EPSG:4326).

Si la variable d'environnement *GPX_ELE_AS_25D* est définie à *YES*, l'élément 
d'élévation sera utilisé pour définir la coordonnée Z des waypoints, des points 
routes et des points tracks.

OGR/GPX lit et écrite les attributs GPX pour les waypoints, routes et tracks.

Par défaut, jusqu'à 2 éléments <link> peuvent être pris en compte par objet 
géométrique. Le nombre par défaut peut être changé par la variable 
d'environnement *GPX_N_MAX_LINKS*.

Problèmes d'encodage
=====================

La bibliothèque Expat gère la lecture des encodages internes suivants :

* US-ASCII
* UTF-8
* UTF-16
* ISO-8859-1

OGR 1.8.0 ajoute la gestion des encodages Windows-1252 (pour les versions 
antérieures, modifier l'encodage mentionné dans l'en-tête XML à ISO-8859-1 peut 
fonctionner dans certains cas).

Le contenu retourné par OGR sera encodé en UTF-8, après la conversion à partir de 
l'encodage mentionné dans l'en-tête du fichier.

Si votre fichier GPX n'est pas encodé dans un de ces encodages précédents, il 
ne sera pas parsé par le pilote GPX. Vous devrez le convertir dans un des 
encodages gérés avec la commande ''iconv'' par exemple et changer en fonction de 
la valeur du paramètre d'encodage dans l'en-tête du XML.

Lors de l'écriture d'un fichier GPX, le pilote s'attend à du contenu en UTF-8.

Lecture des l'élément extensions
=================================

Si l'élément <extensions> est détecté dans le fichier GPX, OGR exposera le 
contenu de ses sous-éléments comme champs. Un contenu complexe des sous-éléments 
sera exposé comme un blob XML.

Le contenu GPX de la séquence suivante :
::
    
    <extensions>
        <navaid:name>TOTAL RF</navaid:name>
        <navaid:address>BENSALEM</navaid:address>
        <navaid:state>PA</navaid:state>
        <navaid:country>US</navaid:country>
        <navaid:frequencies>
        <navaid:frequency type="CTAF" frequency="122.900" name="CTAF"/>
        </navaid:frequencies>
        <navaid:runways>
        <navaid:runway designation="H1" length="80" width="80" surface="ASPH-G">
        </navaid:runway>
        </navaid:runways>
        <navaid:magvar>12</navaid:magvar>
    </extensions>

sera interprété dans un modèle *Simple Feature* d'OGR comme :
::
    
    navaid_name (String) = TOTAL RF
    navaid_address (String) = BENSALEM
    navaid_state (String) = PA
    navaid_country (String) = US
    navaid_frequencies (String) = <navaid:frequency type="CTAF" frequency="122.900" name="CTAF" ></navaid:frequency>
    navaid_runways (String) = <navaid:runway designation="H1" length="80" width="80" surface="ASPH-G" ></navaid:runway>
    navaid_magvar (Integer) = 12

.. note::
    Le pilote GPX affichera le contenu de l'élément extension seulement s'il est 
    trouvé dans les premiers enregistrements du fichier GPX. Si les extensions 
    apparaissent plus tard, vous pouvez forcer le parsage explicite de 
    l'ensemble du fichier avec la variable d'environnement *GPX_USE_EXTENSIONS*.

Problème de création
=====================

Lors de l'export, toutes les couches sont écrites dans un seul fichier GPX. La 
mise à jour de fichier existant n'est pas pour l'instant gérée.

Si le fichier en sortie existe déjà, l'écriture ne se fera pas. Vous devez 
effacer le fichier existant d'abord.

Géométries gérées :

* les objets géométriques de type *wkbPoint/wkbPoint25D* sont écrits dans 
  l'élément wpt.
* les objets géométriques de type *wkbLineString/wkbLineString25D* sont écrits 
  dans l'élément rte.
* les objets géométriques de type *wkbMultiLineString/wkbMultiLineString25D* 
  sont écrit dans l'élément trk.
* les autres types de géométrie ne sont pas gérés.

Pour les points des routes et les points de trace, s'il y a une coordonnée Z, 
celui-ci est utilisé pour remplir l'élément élévation des points correspondants.

À partir de GDAL/OGR 1.8.0, si une couche est nommée "track_points" avec des 
géométries wkbPoint/wkbPoint25D, le tracks dans le fichier GPX sera construit à 
partir de la séquence de features dans cette couche. C'est la manière de définir 
les attributs GPX pour chaque point d'une trace, en plus des coordonnées brutes. Les 
points appartenant au même trace sont identifiés grâce à la même valeur du champ 
'track_fid' field  (et sera découpé en segments de trace en fonction de la valeur 
du champ 'track_seg_id'). Ils doivent être écrits en séquence afin que les objets 
trace soient correctement reconstruit. Le champ 'track_name' peut être définie sur 
le premier point de la trace pour remplir l'élément <name> de la trace.

De la même manière, si une couche est nommée "route_points" avec des géométries 
wkbPoint/wkbPoint25D, les routes dans le fichiers GPX sera construit à partir de 
la séquence de points avec la même valeur du champ 'route_fid'. Le champ 
'route_name' peut être définie au premier point trace pour remplir l'élément 
<name> sur la route.

Le pilote GPX gère en écriture les options de création suivantes pour les 
couches :

* **FORCE_GPX_TRACK :** par défaut lors de l'écriture d'une couche dont les 
  objets géométriques sont de type *wkbLineString*, le pilote GPX choisit de 
  les écrire comme routes.
  
  Si *FORCE_GPX_TRACK=YES* est définie, ils seront écrits comme tracks.
* **FORCE_GPX_ROUTE :** par défaut lors de l'écriture d'une couche dont les 
  objets sont de type *wkbMultiLineString*, le pilote GPX choisit de les écrire 
  comme tracks.
  
  Si *FORCE_GPX_ROUTE=YES* est définie, ils seront écrits comme routes, 
  seulement si les multilignes ne sont composées que de ligne simple.

Le pilote GPX gère en écriture les options de création suivantes pour les jeux 
de données :

* **GPX_USE_EXTENSIONS :** Par défaut, le pilote GPX ignorera les champs 
  attributaires qui ne correspondront pas à la définition du schéma XML du GPX 
  (name, cmt, etc...).
  Si *GPX_USE_EXTENSIONS=YES*  est définie, des champs supplémentaires seront 
  écrits dans la balise <extension>.
* **GPX_EXTENSIONS_NS :** Seulement utilisé si *GPX_USE_EXTENSIONS=YES* et 
  *GPX_EXTENSIONS_NS_URL* sont définies.
  La valeur de l'espace de nom utilisée pour les balises extension. Par 
  défaut, "ogr".
* **GPX_EXTENSIONS_NS_URL :** Seulement utilisé si *GPX_USE_EXTENSIONS=YES* et 
  *GPX_EXTENSIONS_NS* sont définies.
  Le chemin de l'espace de nom est par défaut "http://osgeo.org/gdal".
* **LINEFORMAT :** (GDAL/OGR >= 1.8.0) Par défaut les fichiers sont créés avec la 
  convetion de fin de ligne de la plateforme locale (CR/LF sur win32 ou LF sur 
  tous les autres systèmes). Cela peut être écrasé par l'utilisation de l'option 
  de création de couche LINEFORMAT  qui accepte les valeurs **CRLF**
  (format DOS) ou **LF** (format Unix).

Waypoints, routes et tracks doivent être écrit dans cet ordre en fonction du 
schéma XML.

Lors de la traduction à partir d'une source de jeu de données, il peut être 
nécessaire de renommer les noms des champs à partir de la source du jeu de 
données par les noms des attributs GPX attendus, tels que <name>, <desc>, etc. 
Cela peut être réalisé avec un jeu de données :ref:`gdal.ogr.formats.vrt`, ou en 
utilisant l'option "-sql" de la commande ``ogr2ogr``.

Problèmes lors de la traduction en Shapefile
=============================================
 
* Lors de la traduction de la couche *track_points* vers un Shapefile, les noms 
  des champs "track_seg_id" et "track_seg_point_id" sont tronqué en 10 caractères 
  dans le fichier .DBF, entraînant une duplication du nom. Pour éviter cela à 
  partir de GDAL 1.6.1, vous pouvez définir l'option de configuration GPX_SHORT_NAMES 
  à TRUE pour les définir respectivement à "trksegid" et "trksegptid", ce qui leur 
  permet d'être unique une fois traduit en DBF. Le champ "route_point_id" de la 
  couche *route_points* sera également renommé en "rteptid".
  Mais notez qu'aucun traitement particulier ne sera réalisé pour n'importe quelle 
  extension de noms de champ.

  Pour traduire la couche track_points d'un fichier GPX à un ensemble de 
  shapefiles :
  ::
    
    ogr2ogr --config GPX_SHORT_NAMES YES out input.gpx track_points

* Shapefile ne gère pas les champs de type DateTime. Il gère seulement les champs 
  de type Date. Par défaut, vous perdrez donc la partie hour:minute:second de 
  l'élément *Time* d'un fichier GPX.
  À partir de GDAL 1.6.0, vous pouvez utiliser l'opérateur CAST du SQL d'OGR pour 
  convertir le champ *time* en string :
  ::
    
    ogr2ogr out input.gpx -sql "SELECT ele, CAST(time AS character(32)) FROM waypoints"

  À partir de GDAL 1.7.0, il y a des façons plus aisées pour sélectionner tous les 
  champs et demander la conversion d'un type donné en strings :
  ::
    
    ogr2ogr out input.gpx -fieldTypeToString DateTime


Exemple
========

La commande ogrinfo peut être utilisée pour faire un dump du contenu d'un 
fichier de données GPX :
::
    
    ogrinfo -ro -al input.gpx

La commande ogr2ogr peut être utilisé pour une traduction du format GPX au 
format GPX :
::
    
    ogr2ogr -f GPX output.gpx input.gpx waypoints routes tracks

.. note::
    Dans le cas de la traduction du format GPX au format GPX, vous devez 
    définir le nom des couches, dans le but d'éviter les couches route_points 
    et track_points.

Utilisez la baliser <extensions> pour la sortie :
::
    
    ogr2ogr -f GPX  -dsco GPX_USE_EXTENSIONS=YES output.gpx input

qui renverra ce qui suit :
::
    
    <?xml version="1.0"?>
    <gpx version="1.1" creator="GDAL 1.5dev"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:ogr="http://osgeo.org/gdal"
    xmlns="http://www.topografix.com/GPX/1/1"
    xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
    <wpt lat="1" lon="2">
    <extensions>
        <ogr:Primary_ID>PID5</ogr:Primary_ID>
        <ogr:Secondary_ID>SID5</ogr:Secondary_ID>
    </extensions>
    </wpt>
    <wpt lat="3" lon="4">
    <extensions>
        <ogr:Primary_ID>PID4</ogr:Primary_ID>
        <ogr:Secondary_ID>SID4</ogr:Secondary_ID>
    </extensions>
    </wpt>
    </gpx>


Utilisez l'option -sql pour remaper les noms des champs par un permis par le schéma GPX !
::
    
    ogr2ogr -f GPX output.gpx input.shp -sql "SELECT field1 AS name, field2 AS desc FROM source_layer"

Voir également
===============

* `Page web pour le format GPX format <http://www.topografix.com/gpx.asp>`_
* `Documenation du format GPX 1.1 <http://www.topografix.com/GPX/1/1/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/07/21 (trunk 19794)