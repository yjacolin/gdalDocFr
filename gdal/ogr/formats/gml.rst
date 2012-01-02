.. _`gdal.ogr.formats.gml`:

GML - Geography Markup Language
================================

OGR a une gestion limité pour la lecture et l'écriture du GML. La mise à jour 
de fichier existant n'est pas géré.

Version de GML gérées :

+-----------------------+-----------------------+------------------+
+ OGR version		+ Read			+ Write		   +
+=======================+=======================+==================+
+ OGR >= 1.8.0		+ GML2 et GML3 qui 	+ GML 2.1.2 ou GML +
+			+ peut être traduit 	+ 3 SF-0 (GML 3.1.1+
+			+ en modèle simple 	+ Compliance 	   +
+			+ feature 		+ level SF-0)      +
+-----------------------+-----------------------+------------------+
+ OGR < 1.8.0		+ GML2 et GML3 limité   +GML 2.1.2	   +
+-----------------------+-----------------------+------------------+

Parseur
--------

La première fois qu'un fichier GML est ouvert il est complètement scanné dans le 
but d'obtenir l'ensemble des *featuretypes*, les attributs associés pour 
chacun d'eux et d'autres informations au niveau du jeu de données. Ces 
informations sont stockées dans un fichier .gfs avec le même nom que le fichier 
GML cible. Un accès ultérieur au même fichier GML utilisera ce fichier .gfs pour 
prédéfinir les informations de niveau du jeu de données accélérant son accès. 
Pour une étendues limité le fichier .gfs peut être édité manuellement pour 
modifier la manière dont le fichier GML sera parsé. Soyez avertie que le fichier 
.gfs sera automatiquement régénéré si le .gml associé a un timestamp supérieur.

Lors du pré-scan du fichier GML pour déterminer la liste des types d'objets, et 
les champs, les contenus des champs sont scannée pour tenter de déterminer le 
type du champ. Dans certaines applications cela est plus facile si tous les champs 
sont traité comme des champs de chaines de caractères. Cela peut être réalisé 
en définissant l'option de configuration *GML_FIELDTYPES* à la valeur 
*ALWAYS_STRING*.

OGR 1.8.0 ajoute la gestion pour détecter les attributs des feature dans les 
éléments GML imbriqués (hiérarchie d'attribut non plat) qui peut être trouvé dans 
certains profiles GML tels que ceux MasterMap de l'Ordnance Survey UK. OGR 1.8.0 
apporte également la gestion de la lecture des champs de types IntegerList, 
RealList et StringList  quand un élément GML a plusieurs occurrences.

Depuis OGR 1.8.0, un pilote GML spécialisé - pilote :ref:`gdal.ogr.formats.nas` 
- est disponible pour lire le format d'échange GML AAA allemand (NAS/ALKIS).

Les options de configuration peuvent être définie via la fonction 
*CPLSetConfigOption()* ou comme variables d'environnement.

Lecture des géométries
-----------------------

Lors de la lecture d'une feature, le pilote prendra par défaut seulement en compte 
la dernière géométrie GML reconnu trouvée (dans le cas où il y en a plusieurs) 
dans le sous arbre XML décrivant la feature.

À partir de OGR 1.8.0, l'utilisateur peut changer le fichier .gfs pour 
sélectionner la géométrie appropriée en spécifiant son chemin avec l'élément 
<GeometryElementPath>. Voyez la description de la syntaxe .gfs plus bas.

.. <!-- Voluntary commented : a bit experimental for now and perhaps a better solution
..      will emerge later -->
.. <!--
.. OGR 1.8.0 adds support to "merge" the multiple geometries found in a feature by
.. setting the configuration option **GML_FETCH_ALL_GEOMETRIES** to **YES**. The geometries
.. will be collected into a GeometryCollection (or Multipolygon if individual geometries
.. are polygons or multipolygons). This can be usefull when reading some GML application profiles.
.. If a <GeometryElementPath> element is specified in the .gfs, the fetching will be limited
.. to paths that match the value of <GeometryElementPath>.
.. -->

OGR 1.8.0 ajoute la gestion de plusieurs géométries GML incluant TopoCurve, 
TopoSurface, MultiCurve. Le type géométrie GML TopoCurve peut être interprété 
comme l'un des deux types de géométries. Les éléments Edge interne contiennent 
des courbes et leurs noeuds correspondants. Par défaut seules les courbes, la 
géométrie principale, sont retournées comme OGRMultiLineString. Pour récupérer 
les noeuds, sous forme de OGRMultiPoint, l'option de configuration 
**GML_GET_SECONDARY_GEOM** doit être définie à la valeur **YES**. Lorsque cela est 
fait seul les géométries secondaires sont renvoyées.

Résolution gml:xlink 
---------------------

OGR 1.8.0 ajoute la gestion de la résolution des gml:xlink. Quand le *résolveur* 
trouve un élément contenant une balise xlink:href, il tente de trouver l'élément 
correspondant avec le gml:id dans le même fichier gml, d'autre fichier gml dans le 
système de fichier ou sur le web en utilisant cURL. Définissez l'option de 
configuration **GML_SKIP_RESOLVE_ELEMS** à **NONE** pour activer la résolution.

Par défaut le fichier résolu sera sauvé dans le même répertoire que le fichier 
originel avec l'extension ".resolved.gml", s'il n'existe pas déjà. Ce 
comportement peut être changé en utilisant l'option de configuration 
**GML_SAVE_RESOLVED_TO**. Définie le à **SAME** pour écraser le fichier original. 
Définissez le à **un nom de fichier finissant par .gml** pour le sauver à cet 
endroit. Toutes autres valeurs seront ignorées. Si le *résolveur* ne peut pas 
écrire dans le fichier pour n'importe quel raison, il tentera de le sauver dans 
un fichier temporaire généré par *CPLGenerateTempFilename("ResolvedGML");* sinon 
la résolution échouera.

Notez que l'algorithme de résolution n'est pas optimisé pour les gros fichiers. 
Pour les fichiers avec plus de 2000 balises xlink:href, le process peut durer plus 
que quelques minutes. Une progression approximative est affichée grâce à 
*CPLDebug()*  tous les 256 liens. Il peut être vue en définissant la variable 
d'environnement CPL_DEBUG. Le temps de résolution peut être réduit si vous 
connaissez les éléments qui ne sont pas nécessaire. Mentionnez une liste de noms 
séparés par des virgules des éléments avec l'option de configuration 
**GML_SKIP_RESOLVE_ELEMS**. Définissez à **ALL** pour ne pas réaliser la 
résolution en même temps (défaut). Définissez à **NONE** pour résoudre tous les 
xlinks.

Problèmes d'encodage
---------------------

La bibliothèque Expat gère la lecture des encodages internes suivants :

* US-ASCII
* UTF-8
* UTF-16
* ISO-8859-1

Lorsqu'il est utilisé avec la bibliothèque Expat, OGR 1.8.0 ajoute la gestion de 
l'encodage Windows-1252 (pour les versions précédentes, modifier l'encodage 
mentionnée dans l'en-tête XML à ISO-8859-1 peut fonctionner dans certain cas).

Le contenu renvoyé par OGR sera encodé en UTF-8, après la conversion à partir de 
l'encodage mentionné dans l'en-tête du fichier.

Si le fichier GML n'est pas encodé dans l'un des encodages précédents et que le 
seul parseur disponible est Expat, il ne sera pas parsé par le pilote GML. Vous 
pouvez le convertir dans l'un des encodages gérés avec la commande *iconv* par 
exemple et changer la valeur du paramètre *encoding* dans l'en-tête XML en 
conséquence.

Feature id (fid / gml:id)
-------------------------

À partir de OGR 1.9.0, le pilote expose le contenu de l'attribut *gml:id* comme 
champ de chaîne de caractères appelé *gml_id*, lors de la lecture des documents 
GML des WFS. Lors de la création d'un document GML3, si un champ est appelé 
*gml_id*, son contenu sera également utilisé pour écrire le contenue de l'attribut 
*gml:id* de la feature créée.

À partir de OGR 1.9.0, le pilote auto-détecte la présence d'un attribut fid 
(GML2) (resp. gml:id (GML3)) au début du fichier, et, si présent, l'expose par 
défaut en tant que champ *fid* (resp. *gml_id*). L'auto-détection peut être 
écrasée en spécifiant l'option de configuration **GML_EXPOSE_FID** ou 
**GML_EXPOSE_GML_ID** à **YES** ou **NO**.

À partir de OGR 1.9.0, lors de la création d'un document GML2, si un champ est 
appelé *fid*, son contenu sera également utilisé pour écrire le contenu de 
l'attribut fid de la feature créée.

Problèmes lors de création
--------------------------

Lors de l'export, toutes les couches sont écrites dans un seul fichier GML dans 
une seule collection d'objet. Chaque nom de couche est utilisé comme nom 
d'élément pour les objets à partir de cette couche. Les géométries sont toujours 
écrites comme un élément *ogr:geometryProperty* dans l'objet.

Le pilote GML gère  en écriture les options de création de jeu de données 
suivantes :

* **XSISCHEMAURI :** si fournit, l'uri sera inséré comme location du schéma. 
  Notez que le fichier schéma n'est pas réellement accédé par OGR, il est du 
  ressort de l'utilisateur de s'assurer que le schéma correspond au fichier 
  données GML produit par GML.
* **XSISCHEMA :** peut être *EXTERNAL*, *INTERNAL* ou *OFF* et par 
  défaut à *EXTERNAL*. Cela écrit un fichier schéma GML vers un fichier .xsd 
  correspondant (avec le même nom). Si *INTERNAL* est utilisé le schéma est écrit 
  dans le fichier GML, mais cela est expérimental et probablement pas valide 
  XML. *OFF* désactive la génération du schéma (et est implicite si 
  *XSISCHEMAURI* est utilisé).
* **FORMAT :** (OGR >= 1.8.0) peut être définie à GML3 pour écrire des fichiers 
  GML qui suivent le profile GML3 SF-0. Autrement GML2 sera utilisé.
* **GML3_LONGSRS=YES/NO :** (OGR >= 1.8.0, seulement valide quand FORMAT=GML3) YES 
  par défaut. Si YES, SRS avec l'autorité EPSG sera écrit avec le préfixe 
  "urn:ogc:def:crs:EPSG::". Dans ce cas, si la projection est une projection 
  géographique sans ordre d'axe explicite, mais avec ce même code d'autorité de 
  la projection importé avec *ImportFromEPSGA()* doit être traité comme lat/long, 
  alors la fonction prendra soin d'échanger l'ordre des coordonnées. Si définie 
  à NO, la projection avec l'autorité EPSG sera écrit avec le préfixe "EPSG:", même 
  s'ils sont dans l'ordre lat/long.
* **SPACE_INDENTATION=YES/NO :** (OGR >= 1.8.0) YES par défaut. Si YES, la sortie 
  sera indentée avec des espaces pour une meilleure lisibilité, mais avec une 
  augmentation de la taille.


Syntaxe des fichiers .gfs par l'exemple
-----------------------------------------

Considérons le fichier test.gml suivant :

::
    
    <?xml version="1.0" encoding="UTF-8"?>
    <gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml">
	<gml:featureMember>
	    <LAYER>
		<attrib1>attrib1_value</attrib1>
		<attrib2container>
		    <attrib2>attrib2_value</attrib2>
		</attrib2container>
		<location1container>
		    <location1>
			<gml:Point><gml:coordinates>3,50</gml:coordinates></gml:Point>
		    </location1>
		</location1container>
		<location2>
		    <gml:Point><gml:coordinates>2,49</gml:coordinates></gml:Point>
		</location2>
	    </LAYER>
	</gml:featureMember>
    </gml:FeatureCollection>

et le fichier associé .gfs suivant :

::
    
    <GMLFeatureClassList>
	<GMLFeatureClass>
	    <Name>LAYER</Name>
	    <ElementPath>LAYER</ElementPath>
	    <GeometryElementPath>location1container|location1</GeometryElementPath>
	    <PropertyDefn>
		<Name>attrib1</Name>
		<ElementPath>attrib1</ElementPath>
		<Type>String</Type>
		<Width>13</Width>
	    </PropertyDefn>
	    <PropertyDefn>
		<Name>attrib2</Name>
		<ElementPath>attrib2container|attrib2</ElementPath>
		<Type>String</Type>
		<Width>13</Width>
	    </PropertyDefn>
	</GMLFeatureClass>
    </GMLFeatureClassList>


Notez la présence du caractère '|' dans les éléments <ElementPath> et 
<GeometryElementPath> pour définir l'élément géométrie/champ désiré qui est 
l'élément XML imbriqué. Les éléments champs imbriqués sont seulement géré à partir 
d'OGR 1.8.0, ainsi que spécifier <GeometryElementPath>. Si GeometryElementPath 
n'est pas définie, le pilote GML utilisera le dernier élément géométrie reconnu.

La sortie de *ogrinfo test.gml -ro -al* est :
::
    
    Layer name: LAYER
    Geometry: Unknown (any)
    Feature Count: 1
    Extent: (3.000000, 50.000000) - (3.000000, 50.000000)
    Layer SRS WKT:
    (unknown)
    Geometry Column = location1container|location1
    attrib1: String (13.0)
    attrib2: String (13.0)
    OGRFeature(LAYER):0
	attrib1 (String) = attrib1_value
	attrib2 (String) = attrib2_value
	POINT (3 50)

Exemple
--------

La commande ogr2ogr peut être utilisé pour faire un dump des résultats d'une 
requête Oracle en GML :
::
    
    ogr2ogr -f GML output.gml OCI:usr/pwd@db my_feature -where "id = 0"

La commande ogr2ogr peut être utilisé pour faire un dump des résultats d'une 
requête PostGIS en GML :
::
    
    ogr2ogr -f GML output.gml PG:'host=myserver dbname=warmerda' -sql 
        "SELECT pop_1994 from canada where province_name = 'Alberta'"


Voir aussi
----------

* `Spécifications du GML <http://www.opengeospatial.org/standards/gml>`_
* `Profile GML 3.1.1 simple features <http://portal.opengeospatial.org/files/?artifact_id=15201>`_
* `Xerces <http://xml.apache.org/xerces2-j/index.html>`_
* :ref:`gdal.ogr.format.nas`

.. yjacolin at free.fr, Yves Jacolin - 2011/07/21 (trunk 22494)