.. _`gdal.ogr.formats.gml`:

================================
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


Parseurs
=========

The reading part of the driver only works if OGR is built with Xerces linked in. Starting with OGR 1.7.0, when Xerces is unavailable, read support also works if OGR is built with Expat linked in. XML validation is disabled by default. GML writing is always supported, even without Xerces or Expat.

Note: starting with OGR 1.9.0, if both Xerces and Expat are available at build time, the GML driver will preferentially select at runtime the Expat parser for cases where it is possible (GML file in a compatible encoding), and default back to Xerces parser in other cases. However, the choice of the parser can be overriden by specifying the GML_PARSER configuration option to EXPAT or XERCES.

CRS support
============

Since OGR 1.8.0, the GML driver has coordinate system support. This is only reported when all the geometries of a layer have a srsName attribute, whose value is the same for all geometries. For srsName such as "urn:ogc:def:crs:EPSG:", for geographic coordinate systems (as returned by WFS 1.1.0 for example), the axis order should be (latitude, longitude) as required by the standards, but this is unusual and can cause issues with applications unaware of axis order. So by default, the driver will swap the coordinates so that they are in the (longitude, latitude) order and report a SRS without axis order specified. It is possible to get the original (latitude, longitude) order and SRS with axis order by setting the configuration option GML_INVERT_AXIS_ORDER_IF_LAT_LONG to NO.

There also situations where the srsName is of the form "EPSG:XXXX" (whereas "urn:ogc:def:crs:EPSG::XXXX" would have been more explicit on the intent) and the coordinates in the file are in (latitude, longitude) order. By default, OGR will not consider the EPSG axis order and will report the coordinates in (latitude,longitude) order. However, if you set the configuration option GML_CONSIDER_EPSG_AS_URN to YES, the rules explained in the previous paragraph will be applied.

Since OGR 1.10, the above also applied for projected coordinate systems whose EPSG preferred axis order is (northing, easting).

Schéma
=======

In contrast to most GML readers, the OGR GML reader does not require the presence of an XML Schema definition of the feature classes (file with .xsd extension) to be able to read the GML file. If the .xsd file is absent or OGR is not able to parse it, the driver attempts to automatically discover the feature classes and their associated properties by scanning the file and looking for "known" gml objects in the gml namespace to determine the organization. While this approach is error prone, it has the advantage of working for GML files even if the associated schema (.xsd) file has been lost.

Starting with OGR 1.10, it is possible to specify an explicit filename for the XSD schema to use, by using "a_filename.gml,xsd=another_filename.xsd" as a connection string.

La première fois qu'un fichier GML est ouvert, si le fichier .xsd est absent ou 
ne peut être parsé, il est complètement scanné dans le but d'obtenir l'ensemble 
des types des entités, les attributs associés pour 
chacun d'eux et d'autres informations au niveau du jeu de données. Ces 
informations sont stockées dans un fichier .gfs avec le même nom que le fichier 
GML cible. Un accès ultérieur au même fichier GML utilisera ce fichier .gfs pour 
prédéfinir les informations de niveau du jeu de données accélérant son accès. 
Pour une étendue limité, le fichier .gfs peut être édité manuellement pour 
modifier la manière dont le fichier GML sera parsé. Mais sachez que le fichier 
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
=======================

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
======================

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

Starting since OGR 1.9.0 an alternative resolution method is available.
This alternative method will be activated using the configuration option
**GML_SKIP_RESOLVE_ELEMS HUGE**. In this case any gml:xlink will be 
resolved using a temporary SQLite DB so to identify any corresponding
gml:id relation. At the end of this SQL-based process, a resolved file
will be generated exactly as in the <b>NONE</b> case but without their limits. 
The main advantages in using an external (temporary) DBMS so to resolve 
gml:xlink and gml:id relations are the followings:

* no memory size constraints. The *NONE* method stores the whole
  GML node-tree in-memory; and this practically means that no GML
  file bigger than 1 GB can be processed at all using a 32-bit
  platform, due to memory allocation limits. Using a file-system
  based DBMS avoids at all this issue.
* by far better efficiency, most notably when huge GML files containing
  many thousands (or even millions) of xlink:href / gml:id relational 
  pairs.
* using the **GML_SKIP_RESOLVE_ELEMS HUGE** method realistically allows 
  to succesfully resolve some really huge GML file (3GB+) containing many 
  millions xlink:href / gml:id in a reasonable time (about an hour or so on).
* The **GML_SKIP_RESOLVE_ELEMS HUGE** method supports the followind further
  configuration option:

    * you can use **GML_GFS_TEMPLATE** *path_to_template.gfs*
      in order to unconditionally use a predefined GFS file. This option is really useful
      when you are planning to import many distinct GML files in subsequent steps [*-append*] 
      and you absolutely want to preserve a fully consistent data layout for the whole GML set.
      Please, pay attention not to use the *-lco LAUNDER=yes* setting when using *GML_GFS_TEMPLATE*; 
      this should break the correct recognition of attribute names between subsequent GML import runs.

TopoSurface interpretation rules [polygons and internal holes]
================================================================

Starting since OGR 1.9.0 the GML driver is able to recognize two different interpretation
rules for TopoSurface when a polygon contains any internal hole:

* the previously supported interpretation rule assumed that:

  * each TopoSurface may be represented as a collection of many Faces</li>
  * *positive* Faces [i.e. declaring <b>orientation="+"</b>] are assumed to
    represent the Exterior Ring of some Polygon.
  * *negative* Faces [i.e. declaring <b>orientation="-"</b>] are assumed to
     represent an Interior Ring (aka <i>hole</i>) belonging to the latest declared 
     Exterior Ring.
   * ordering any Edge used to represent each Ring is important: each Edge is expected
     to be exactly adjacent to the next one.

* the new interpretation rule now assumes that:

  * each TopoSurface may be represented as a collection of many Faces
  * the declared <b>orientation</b> for any Face has nothing to deal with Exterior/Interior Rings
  * each Face is now intended to represent a complete Polygon, eventually including any possible Interior 
    Ring (*holes*)
  * the relative ordering of any Edge composing the same Face is completely not relevant.
               
The newest interpretation seems to fully match GML 3 standard recommendations; so this latest
is now assumed to be the default interpretation supported by OGR.

.. note:: Using the newest interpretation requires GDAL/OGR to be built against the GEOS library.

Using the *GML_FACE_HOLE_NEGATIVE*> configuration option you can anyway select the
actual interpretation to be applied when parsing GML 3 Topologies:

* setting *GML_FACE_HOLE_NEGATIVE NO* (*default* option) will activate
  the newest interpretation rule
* but explicitly setting *GML_FACE_HOLE_NEGATIVE YES* still enables to activate
  the old interpretation rule

Problèmes d'encodage
=====================

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

.. note:: The .xsd schema files are parsed with an integrated XML parser which
   does not currently understand XML encodings specified in the XML header. It expects encoding to be always
   UTF-8. If attribute names in the schema file contains non-ascii characters, it is
   better to use *iconv* utility and convert the .xsd file into UTF-8 encoding first.

Feature id (fid / gml:id)
===========================

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

Problèmes de performance avec les gros fichiers GML multi-couches
==================================================================

Il y a seulement un parseur GML par source de données GML partagé entre les 
différentes couches. Par défaut, le pilote GML recommencera la lecture du 
début du fichier, chaque fois qu'une couche est accédée pour la première fois, 
ce qui entraine une perte des performances avec les gros ficheirs GML.

À partir de OGR 1.9.0, l'option de configuration **GML_READ_MODE** peut être 
définie à **SEQUENTIAL_LAYERS** si toutes les entités appartenant à la même 
couche sont écris séquentiellement dans le fichier. Le lecteur évitera alors 
les resets inutiles lorsque les couches sont lues complètement l'une après 
l'autre. Pour obtenir les meilleures performances, les couches doivent être 
lues dans l'ordre où elles apparaissent dans le fichier.

Si aucun fichiers .xsd et .gfs ne sont trouvé, le parseur détectera le layout 
des couches lors de la construction du fichier .gfs? Si les couches sont 
définies comme séquentielles, un élement *<SequentialLayers>true</SequentialLayers>* 
sera écrit dans le fichier  .gfs, afni que le mode GML_READ_MODE soient automatiquement 
initialisé à MONOBLOCK_LAYERS si non explicitement définie par l'utilisateur.

À partir d'OGR 1.9.0, L'option de configuration GML_READ_MODE peut être définie 
à INTERLEAVED_LAYERS pour permettre de lire un fichier GML dont les entités dans 
différentes couches sont entrelacées. Dans ce cas, la sémantique de la fonction 
GetNextFeature() sera sensiblement altéré d'une manière à ce que les valeurs NULL 
ne signifie pas nécessairement que toutes les entités de la couche actuelle 
doivent être lues, mais cela peut aussi signifieer qu'il y a encore une entité 
à lire mais qu'elle appartient à une autre couche. Dans ce cas, le fichier doit 
être lu avec le code de cette façon :

::
  
    int nLayerCount = poDS->GetLayerCount();
    int bFoundFeature;
    do
    {
        bFoundFeature = FALSE;
        for( int iLayer = 0; iLayer &lt; nLayerCount; iLayer++ )
        {
            OGRLayer   *poLayer = poDS->GetLayer(iLayer);
            OGRFeature *poFeature;
            while((poFeature = poLayer->GetNextFeature()) != NULL)
            {
                bFoundFeature = TRUE;
                poFeature->DumpReadable(stdout, NULL);
                OGRFeature::DestroyFeature(poFeature);
            }
        }
    } while (bInterleaved &amp;&amp; bFoundFeature);

Problèmes lors de création
============================

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
* **FORMAT :** (OGR >= 1.8.0) peut être définie à 

    * *GML3* pour écrire des fichiers GML qui suivent le profile GML3 SF-0. 
    * *GML3Deegree* À partir d'OGR 1.9.0 afin de produire un schema .XSD GML 
      3.1.1, avec quelques variations en respect des recommandations du 
      profile GML3 SF-0, mais cela sera mieux accepté par certains logiciels 
      (comme Deegree 3). 
    * *GML3.2* À partir d'OGR 1.9.0 dans le but de produire des fichiers GML 
      qui suivent le profile GML 3.2.1 SF-0.
    
    Autrement GML2 sera utilisé.
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

Gestion de l'API de gestion des fichiers virtuels
==================================================

(Certaines fonctions ci-dessous peuvent nécessiter OGR >= 1.9.0).
 
Le pilote gère la lecture et l'écriture vers les fichiers gérés par l'API 
du Système de Fichier Virtual VSI, ce qui inclus les fichiers "normaux" 
ainsi que les fichiers dans les domaines /vsizip/ (lecture-écriture), 
/vsigzip/ (lecture-écriture), /vsicurl/ (lecture seule).

L'écriture vers /dev/stdout ou /vsistdout/ est également géré. Notez que 
dans ce cas, seulement le contenu du fichier GML sera écrit vers la sortie 
standard (et pas le .xsd). L'élément <boundedBy> ne sera pas écrit. C'est 
également le cas si vous écrivez vers /vsigzip/.

Syntaxe des fichiers .gfs par l'exemple
==========================================

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
=========

La commande ogr2ogr peut être utilisé pour faire un dump des résultats d'une 
requête Oracle en GML :
::
    
    ogr2ogr -f GML output.gml OCI:usr/pwd@db my_feature -where "id = 0"

La commande ogr2ogr peut être utilisé pour faire un dump des résultats d'une 
requête PostGIS en GML :
::
    
    ogr2ogr -f GML output.gml PG:'host=myserver dbname=warmerda' -sql 
        "SELECT pop_1994 from canada where province_name = 'Alberta'"


.. seealso::

 * `Spécifications du GML <http://www.opengeospatial.org/standards/gml>`_
 * `Profile GML 3.1.1 simple features - OGC(R) 06-049r1 <http://portal.opengeospatial.org/files/?artifact_id=15201>`_
 * `Xerces <http://xml.apache.org/xerces2-j/index.html>`_
 *  :ref:`gdal.ogr.format.nas`
 
Crédits
========

* Implémentation pour **GML_SKIP_RESOLVE_ELEMS HUGE** a été une contribution de 
  A.Furieri, financé par la Région Toscane.
 
.. yjacolin at free.fr, Yves Jacolin - 2013/05/02 (trunk 2445)