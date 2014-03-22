.. _`gdal.ogr.formats.gml`:

================================
GML - Geography Markup Language
================================

OGR a une gestion limité pour la lecture et l'écriture du GML. La mise à jour 
de fichier existant n'est pas géré.

Version de GML gérées :

+-----------------------+-----------------------+------------------+
+ OGR version           + Read                  + Write            +
+=======================+=======================+==================+
+ OGR >= 1.8.0          + GML2 et GML3 qui      + GML 2.1.2 ou GML +
+                       + peut être traduit     + 3 SF-0 (GML 3.1.1+
+                       + en modèle simple      + Compliance       +
+                       + feature               + level SF-0)      +
+-----------------------+-----------------------+------------------+
+ OGR < 1.8.0           + GML2 et GML3 limité   + GML 2.1.2        +
+-----------------------+-----------------------+------------------+


Parseurs
=========

The reading part of the driver only works if OGR is built with Xerces linked in. Starting with OGR 1.7.0, when Xerces is unavailable, read support also works if OGR is built with Expat linked in. XML validation is disabled by default. GML writing is always supported, even without Xerces or Expat.

.. note:: starting with OGR 1.9.0, if both Xerces and Expat are available at build time, the GML driver will preferentially select at runtime the Expat parser for cases where it is possible (GML file in a compatible encoding), and default back to Xerces parser in other cases. However, the choice of the parser can be overriden by specifying the GML_PARSER configuration option to EXPAT or XERCES.

Gestion des SCR
================

.. versionadded:: OGR 1.8.0, the GML driver has coordinate system support. This is only reported when all the geometries of a layer have a srsName attribute, whose value is the same for all geometries. For srsName such as "urn:ogc:def:crs:EPSG:", for geographic coordinate systems (as returned by WFS 1.1.0 for example), the axis order should be (latitude, longitude) as required by the standards, but this is unusual and can cause issues with applications unaware of axis order. So by default, the driver will swap the coordinates so that they are in the (longitude, latitude) order and report a SRS without axis order specified. It is possible to get the original (latitude, longitude) order and SRS with axis order by setting the configuration option GML_INVERT_AXIS_ORDER_IF_LAT_LONG to NO.

Il y a aussi des situations où le srsName est de la forme "EPSG:XXXX" (où 
"urn:ogc:def:crs:EPSG::XXXX" aurait été plus explicite sur l'intention) et les 
coordonées dans le fichier sont dans l'ordre (latitude, longitude). Par défaut, 
OGR ne considérera pas l'ordre des axes EPSG et raportera les cooronnées dans 
l'ordre (latitude,longitude). Cependant, si vous définissez l'option de 
configuration *GML_CONSIDER_EPSG_AS_URN* à YES, les règles expliquées dans le 
paragraphe précédent seront appliquées.

.. versionadded:: OGR 1.10, ce qui précède s'applique également pour les 
  systèmes de coordonnées projetés dont l'ordre des axes préféré de l'EPSG 
  est (northing, easting).

Schéma
=======

Contrairement à la plupart des lecteurs GML, Le lecteur GML d'OGR ne nécessite 
pas la présence d'une définition de Schéma XML des classes d'entités (fichier 
avec l'extension .xsd) pour être capable de lire le fichier GML. Si le fichier 
.xsd est absent ou si OGR n'est pas capbable de le lire, le pilote tente 
automatiquement de découvrir les classes d'entités et leurs propriétés associées 
en sannant le fichier et cherchant des objets gml *connus* dans l'espace de 
nom gml pour déterminer l'organisation. Bien que cette approche implique des 
erreurs, elle a l'avantage de fonctionner pour les fichiers GML même si le schéma 
associé (.xsd) a été perdu.

.. versionadded:: OGR 1.10, il est possible de définir un nom de fichier spécifique 
  pour le schéma XSD, en utilisant "un_fichier.gml,xsd=autre_fichier.xsd" comme chaîne 
  de connexion.

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

Les options de configuration peuvent être définie via la fonction 
*CPLSetConfigOption()* ou en tant que variable d'environnement.

Application particulière du schéma GML
======================================

.. versionadded:: OGR 1.8.0 ajoute la gestion pour détecter les attributs des feature dans les 
  éléments GML imbriqués (hiérarchie d'attribut non plat) qui peut être trouvé dans 
  certains profiles GML tels que ceux MasterMap de l'Ordnance Survey UK. OGR 1.8.0 
  apporte également la gestion de la lecture des champs de types IntegerList, 
  RealList et StringList  quand un élément GML a plusieurs occurrences.

Depuis OGR 1.8.0, un pilote GML spécialisé - pilote :ref:`gdal.ogr.formats.nas` 
- est disponible pour lire le format d'échange GML AAA allemand (NAS/ALKIS).


.. versionadded:: OGR 1.8.0, le pilote GML gèer partiellement la lecture des fichiers 
  AIXM ou CityGML files.
 
.. versionadded:: OGR 2.0, le pilote GML gère la lecture :

  * des `fichiers GML du Finnish National Land Survey (a.k.a MTK GML) pour les données topographiques 
    <http://xml.nls.fi/XML/Schema/Maastotietojarjestelma/MTK/201202/Maastotiedot.xsd>`_ ;
  * `Finnish National Land Survey GML files pour les données cadastrales <http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/>`_ ;
  * `Données cadastrales dans les schémas GML Inspire <http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd>`_.
  
Lecture des géométries
=======================

Lors de la lecture d'une feature, le pilote prendra par défaut seulement en compte 
la dernière géométrie GML reconnu trouvée (dans le cas où il y en a plusieurs) 
dans le sous arbre XML décrivant la feature.

.. versionadded:: OGR 2.0, si el schéma .xsd est compris par le lecteur XSD et 
qu'il déclare plusieurs champs géométriques, ou que le fichier .gfs déclare 
plusieurs champs géométriques, les champs géométriques multiples seront reportés 
parl e pilote GML selon la `RFC 41 <http://trac.osgeo.org/gdal/wiki/rfc41_multiple_geometry_fields>`_.

.. versionadded:: 1.10 dans le cas où plusieurs occurences de la 
  géométrie apparaissent, si une géométrie est dans un élément <geometry>, celle-ci sera celle 
  sélectionnée. Cela permet un commportement par défaut consistent avec les objets 
  Inspire.

.. versionadded:: OGR 1.8.0, l'utilisateur peut changer le fichier .gfs pour 
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

.. versionadded:: OGR 1.8.0 ajoute la gestion de plusieurs géométries GML incluant TopoCurve, 
  TopoSurface, MultiCurve. Le type géométrie GML TopoCurve peut être interprété 
  comme l'un des deux types de géométries. Les éléments Edge interne contiennent 
  des courbes et leurs noeuds correspondants. Par défaut seules les courbes, la 
  géométrie principale, sont retournées comme OGRMultiLineString. Pour récupérer 
  les noeuds, sous forme de OGRMultiPoint, l'option de configuration 
  **GML_GET_SECONDARY_GEOM** doit être définie à la valeur **YES**. Lorsque cela est 
  fait seul les géométries secondaires sont renvoyées.

Résolution gml:xlink 
======================

.. versionadded:: OGR 1.8.0 ajoute la gestion de la résolution des gml:xlink. Quand le *résolveur* 
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
Pour les fichiers avec plus de 2 000 balises xlink:href, le process peut durer plus 
que quelques minutes. Une progression approximative est affichée grâce à 
*CPLDebug()*  tous les 256 liens. Il peut être vue en définissant la variable 
d'environnement CPL_DEBUG. Le temps de résolution peut être réduit si vous 
connaissez les éléments qui ne sont pas nécessaire. Mentionnez une liste de noms 
séparés par des virgules des éléments avec l'option de configuration 
**GML_SKIP_RESOLVE_ELEMS**. Définissez à **ALL** pour ne pas réaliser la 
résolution en même temps (défaut). Définissez à **NONE** pour résoudre tous les 
xlinks.

.. versionadded:: à partir de OGR 1.9.0 une méthode de résolution alternative est 
  disponible. Cette méthode alternative sera activée en utilisant l'option de 
  configuration **GML_SKIP_RESOLVE_ELEMS HUGE**. Dans ce cas n'importe quel 
  gml:xlink sera résolu en utilisant une base de données SQLite temporaire
  afin d'identifier les relations gml:id correspondantes. À la fin de ce processus 
  basé sur du SQL, un fichier de résolution sera généré exactement de la même 
  manière que dans le cas **NONE** mais sans ses limitations. Les principaux 
  avantages d'utliser un SGBD externe (temporaire) afin de résoudre les relations 
  gml:id et gml:xlink sont les suivantes :

* pas de contraintes de taille de mémoire. La méthode *NONE* stockes l'ensemble 
  de l'arbre des noeuds GML en mémoire ; et cela signifie qu'aucun fichier dont 
  la taille est supérieur à 1 Go peut être traité en utilisant une plateforme 
  32 bit, dû aux limites d'allocation mémoire. Utiliser un SGDB basé sur des 
  fichiers évite tout ces problèmes.
* de loin le plus efficace, plus particulièrement pour les gros fichiers GML 
  contenant plusieurs milleirs (ou même millions) de pairs de relation 
  xlink:href / gml:id.
* en utilisant la méthode **GML_SKIP_RESOLVE_ELEMS HUGE** permet réellement de 
  résoudre de gros fichier GML (3 Go et plus) contenant plusieurs millions de 
  xlink:href / gml:id en un temps raisonable (environ une bonne heure).
* la méthode **GML_SKIP_RESOLVE_ELEMS HUGE** gère les options de configuration 
  suivantes :

    * vous pouvez utilisez **GML_GFS_TEMPLATE** *path_to_template.gfs* dans le 
      but d'utiliser de manière inconditionnelle un fichier GFS pré-définie. Cette 
      option est réellement utile lorsque vous plannifiez d'importer plusieurs 
      fichier GML lors d'étapes supplémentaires [*-append*] et que vous voulez 
      absolument préserver une structure consistante des données pour l'ensemble 
      du jeu GML. Faîtes attention, s'il vous plait,à ne pas utiliser le paramètre 
      *-lco LAUNDER=yes* lors de l'utilisation de *GML_GFS_TEMPLATE* ; cela 
      empechera la bonne reconnaissance  des noms d'attribut entre les cycles 
      supplémentaires de l'import GML.

TopoSurface interpretation rules [polygons and internal holes]
================================================================

.. versionadded:: 1.9.0 le pilote GML est capable de reconaitre deux règles 
  d'interprétations différentes pour TopoSurface quand un polygone contient un 
  anneau interne :

* La règle d'interprétation précédente assume que :

  * chaque TopoSurface peut être représenté comme une collection de plusieurs *Faces*
  * les *Faces* *positives* [i.e. déclarant **orientation="+"**] sont supposées 
    représenter l'anneau Extérieur du polygone.
  * les *Faces* *négatives* [i.e. déclarant **orientation="-"**] sont supposées 
     représenter un anneau Intérieur (aka *troue*) appartenant au dernier anneau 
     Extérieur.
   * ordonner un Edge utilisé pour représenter chaque anneau (*Ring*) est 
     important : chaque Edge est censé être exactement adjacent au prochain.

* La nouvelle règle d'interprétation assume maintenat que :

  * chaque TopoSurface peut être représenté comme une collection de plusieurs Faces
  * l'**orientation** déclaré pour les *Face* n'a rien à voir avec les anneaux 
    Extérieur/Intérieur
  * chaque *Face* a maintenant comme but de représenter un polygone complet, 
    éventuellement en incluant n'importe quel anneau intérieur (*troues*)
  * l'ordre relatif des segments (*Edges*) composant la même *Face* n'est plus 
    pertinent.
               
L'interpretation la plus récente semble correspondre pleinement aux 
recommandations du standard GML 3 ; par conséquent cette dernière est 
maintenant l'interprétation par défaut géré par OGR.

.. note:: Utiliser l'interprétation la plus récente nécessite que GDAL/OGR soit 
   compilé avec la bibliothèque GEOS.

En utilisant l'option de configuration *GML_FACE_HOLE_NEGATIVE* vous pouvez 
sélectionner l'interprétation actuelle afin qu'elle soit appliqué lors de la 
lecture de la topologie dans GML 3.

* définir *GML_FACE_HOLE_NEGATIVE NO* (option par *défaut*) activera la règle 
  d'interpretation la plus récente.
* mais définir explictement *GML_FACE_HOLE_NEGATIVE YES* activera toujours 
  l'ancienne règle d'interprétation.

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

.. note:: Les fichiers schémas .xsd sont lu avec un lecteur XML intégré qui ne 
   comprend par pour le moment les encodages XML définie dans l'en-tête XML. 
   Il s'attend à ce que l'encodage soit toujours UTF-8. Si les noms d'attributs 
   dans le fichier schéma contiennent des caractères non-ascii, il est conseillé 
   d'utiliser la commande *iconv* et de convertir le fichier .xsd en UTF-8 d'abord.


Feature id (fid / gml:id)
===========================

.. versionadded:: OGR 1.9.0, le pilote expose le contenu de l'attribut *gml:id* comme 
  champ de chaîne de caractères appelé *gml_id*, lors de la lecture des documents 
  GML des WFS. Lors de la création d'un document GML3, si un champ est appelé 
  *gml_id*, son contenu sera également utilisé pour écrire le contenue de l'attribut 
  *gml:id* de la feature créée.

.. versionadded:: OGR 1.9.0, le pilote auto-détecte la présence d'un attribut fid 
  (GML2) (resp. gml:id (GML3)) au début du fichier, et, si présent, l'expose par 
  défaut en tant que champ *fid* (resp. *gml_id*). L'auto-détection peut être 
  écrasée en spécifiant l'option de configuration **GML_EXPOSE_FID** ou 
  **GML_EXPOSE_GML_ID** à **YES** ou **NO**.

.. versionadded:: OGR 1.9.0, lors de la création d'un document GML2, si un champ est 
  appelé *fid*, son contenu sera également utilisé pour écrire le contenu de 
  l'attribut fid de la feature créée.

Problèmes de performance avec les gros fichiers GML multi-couches
==================================================================

Il y a seulement un parseur GML par source de données GML partagé entre les 
différentes couches. Par défaut, le pilote GML recommencera la lecture du 
début du fichier, chaque fois qu'une couche est accédée pour la première fois, 
ce qui entraine une perte des performances avec les gros ficheirs GML.

.. versionadded:: OGR 1.9.0, l'option de configuration **GML_READ_MODE** peut être 
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

.. versionadded:: OGR 1.9.0, L'option de configuration GML_READ_MODE peut être définie 
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
        for( int iLayer = 0; iLayer < nLayerCount; iLayer++ )
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
* **PREFIX** (OGR >= 1.10) 'ogr' par défaut. Ceci est le préfix pour l'espace 
  de nom cible de l'application.
* **STRIP_PREFIX** (OGR >= 2.0) FALSE par défauts. Peut être définie à TRUE 
  afin d'éviter l'écriture du préfixe de l'espace de nom cible de l'application 
  dans le fichier GML.
* **TARGET_NAMESPACE** (OGR >= 1.10) 'http://ogr.maptools.org/' par défaut. 
  Ceci est l'espace de nom cible de l'application.
* **FORMAT :** (OGR >= 1.8.0) peut être définie à 

    * *GML3* pour écrire des fichiers GML qui suivent le profile GML3 SF-0. 
    * *GML3Deegree* À partir d'OGR 1.9.0 afin de produire un schema .XSD GML 
      3.1.1, avec quelques variations en respect des recommandations du 
      profile GML3 SF-0, mais cela sera mieux accepté par certains logiciels 
      (comme Deegree 3). 
    * *GML3.2* À partir d'OGR 1.9.0 dans le but de produire des fichiers GML 
      qui suivent le profile GML 3.2.1 SF-0.
    
    Autrement GML2 sera utilisé.
    
    .. versionadded:: OGR 2.0, les champs de type StringList, RealList ou 
      IntegerList peuvent être écrit. Cela impliquera une alerte dans le 
      profile SF-1 dans le schéma .XSD (ces types ne sont pas géré par SF-0).
      
* **GML3_LONGSRS=YES/NO :** (OGR >= 1.8.0, seulement valide quand FORMAT=GML3) YES 
  par défaut. Si YES, SRS avec l'autorité EPSG sera écrit avec le préfixe 
  "urn:ogc:def:crs:EPSG::". Dans ce cas, si la projection est une projection 
  géographique sans ordre d'axe explicite, mais avec ce même code d'autorité de 
  la projection importé avec *ImportFromEPSGA()* doit être traité comme lat/long, 
  alors la fonction prendra soin d'échanger l'ordre des coordonnées. Si définie 
  à NO, la projection avec l'autorité EPSG sera écrit avec le préfixe "EPSG:", même 
  s'ils sont dans l'ordre lat/long.
* **WRITE_FEATURE_BOUNDED_BY**=YES/NO. (OGR >= 2.0, valide seulement quand 
  FORMAT=GML3/GML3Degree/GML3.2) Yes par défaut. Si définie à NO, l'élément 
  <gml:boundedBy> ne sera pas écrit pour chaque entités.
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

L'élément <GeometryType> peut être définie pour forcer le type de géométrie.
Les valeurs acceptées sont : 0 (n'imoprte quel type de géométrie), 1 (point), 
2 (linestring), 3 (polygon), 4 (multipoint), 5 (multilinestring), 6 
(multipolygon), 7 (geometrycollection).

.. versionadded:: OGR 2.0, les éléments <GeometryElementPath> et <GeometryType> 
  peuvent être définie autant de fois qu'il y a de champs géométriques dans le 
  le fichier GML.

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

Syntaxe avancé .gfs (OGR >= 2.0)
==================================
 
Obtenir des attributs XML en tant que champs OGR
**************************************************

La synthaxe element@attribute peut être utilisé dans <ElementPath> afin de 
définir que la valeur de l'attribut 'attribute' de l'élément 'element' doit 
être récupéré.

Considérons le fichier *test.gml* suivant :

::
  
  <?xml version="1.0" encoding="UTF-8"?>
  <gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml">
    <gml:featureMember>
      <LAYER>
        <length unit="m">5</length>
      </LAYER>
    </gml:featureMember>
  </gml:FeatureCollection>
  </pre>

et le fichier .gfs associé.

::
  
  <GMLFeatureClassList>
    <GMLFeatureClass>
      <Name>LAYER</Name>
      <ElementPath>LAYER</ElementPath>
      <GeometryType>100</GeometryType> <!-- no geometry -->
      <PropertyDefn>
        <Name>length</Name>
        <ElementPath>length</ElementPath>
        <Type>Real</Type>
      </PropertyDefn>
      <PropertyDefn>
        <Name>length_unit</Name>
        <ElementPath>length@unit</ElementPath>
        <Type>String</Type>
      </PropertyDefn>
    </GMLFeatureClass>
  </GMLFeatureClassList>


La sortie de *ogrinfo test.gml -ro -al* est :

::
  
  Layer name: LAYER
  Geometry: None
  Feature Count: 1
  Layer SRS WKT:
  (unknown)
  gml_id: String (0.0)
  length: Real (0.0)
  length_unit: String (0.0)
  OGRFeature(LAYER):0
    gml_id (String) = (null)
    length (Real) = 5
    length_unit (String) = m

Using conditions on XML attributes
************************************

Un élément *<Condition>* peut être définie comme élément enfant d'un élément 
*<PropertyDefn>*. Le contenu de l'élément Condition suit une syntaxe XPath  
minimaliste. Il doit être de la forme `@attrname[=|!=]'attrvalue' [and|or other_cond]*.`

Notez que les opérateurs 'and' et 'or' ne peuvent pas être mélangés (leur 
précédence n'est pas pris en compte).

Plusieurs éléments *<PropertyDefn>* peuvent être définies avec le même élément 
*<ElementPath>*, mais avec des éléments *<Condition>* qui peuvent être 
mutuellement exclusif.

Considérons le fichier *testcondition.gml* suivant :

::
  
  <?xml version="1.0" encoding="utf-8" ?>
  <ogr:FeatureCollection
      xmlns:ogr="http://ogr.maptools.org/"
      xmlns:gml="http://www.opengis.net/gml">
    <gml:featureMember>
      <ogr:testcondition fid="testcondition.0">
        <ogr:name lang="en">English name</ogr:name>
        <ogr:name lang="fr">Nom francais</ogr:name>
        <ogr:name lang="de">Deutsche name</ogr:name>
      </ogr:testcondition>
    </gml:featureMember>
  </ogr:FeatureCollection>

et le fichier .gfs associé.

::
  
  <GMLFeatureClassList>
    <GMLFeatureClass>
      <Name>testcondition</Name>
      <ElementPath>testcondition</ElementPath>
      <GeometryType>100</GeometryType>
      <PropertyDefn>
        <Name>name_en</Name>
        <ElementPath>name</ElementPath>
        <Condition>@lang='en'</Condition>
        <Type>String</Type>
      </PropertyDefn>
      <PropertyDefn>
        <Name>name_fr</Name>
        <ElementPath>name</ElementPath>
        <Condition>@lang='fr'</Condition>
        <Type>String</Type>
      </PropertyDefn>
      <PropertyDefn>
        <Name>name_others_lang</Name>
        <ElementPath>name@lang</ElementPath>
        <Condition>@lang!='en' and @lang!='fr'</Condition>
        <Type>StringList</Type>
      </PropertyDefn>
      <PropertyDefn>
        <Name>name_others</Name>
        <ElementPath>name</ElementPath>
        <Condition>@lang!='en' and @lang!='fr'</Condition>
        <Type>StringList</Type>
      </PropertyDefn>
    </GMLFeatureClass>
  </GMLFeatureClassList>

La sortie de *ogrinfo testcondition.gml -ro -al* est :
::
  
  Layer name: testcondition
  Geometry: None
  Feature Count: 1
  Layer SRS WKT:
  (unknown)
  fid: String (0.0)
  name_en: String (0.0)
  name_fr: String (0.0)
  name_others_lang: StringList (0.0)
  name_others: StringList (0.0)
  OGRFeature(testcondition):0
    fid (String) = testcondition.0
    name_en (String) = English name
    name_fr (String) = Nom francais
    name_others_lang (StringList) = (1:de)
    name_others (StringList) = (1:Deutsche name)

Registre pour des schémas d'application GML (OGR >= 2.0)
==========================================================

Le répertoire "data" de l'installation de GDAL contient un fichier 
"gml_registry.xml" qui lie les types d'entités des schémas d'application 
GML vers les fichiers .xsd ou .gfs qui contienent leur définition. Cela 
est utilisé dans le cas où des fichiers .gfs ou .xsd invalides sont trouvés 
à côté du fichier GML.

Une localisation alternative pour le fichier de registre peut être définie en 
définissant son chemin complet dans l'option de configuration *GML_REGISTRY*.

Un exemple d'un tel fichier est :
::
  
  <gml_registry>
      <!-- Finnish National Land Survey cadastral data -->
      <namespace prefix="ktjkiiwfs" uri="http://xml.nls.fi/ktjkiiwfs/2010/02" useGlobalSRSName="true">
          <featureType elementName="KiinteistorajanSijaintitiedot"
                  schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/KiinteistorajanSijaintitiedot.xsd"/>
          <featureType elementName="PalstanTunnuspisteenSijaintitiedot"
                  schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/palstanTunnuspisteenSijaintitiedot.xsd"/>
          <featureType elementName="RekisteriyksikonTietoja"
                  schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/RekisteriyksikonTietoja.xsd"/>
          <featureType elementName="PalstanTietoja"
                  schemaLocation="http://xml.nls.fi/XML/Schema/sovellus/ktjkii/modules/kiinteistotietojen_kyselypalvelu_WFS/Asiakasdokumentaatio/ktjkiiwfs/2010/02/PalstanTietoja.xsd"/>
      </namespace>
  
      <!-- Inspire CadastralParcels schema -->
      <namespace prefix="cp" uri="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" useGlobalSRSName="true">
          <featureType elementName="BasicPropertyUnit"
                      gfsSchemaLocation="inspire_cp_BasicPropertyUnit.gfs"/>
          <featureType elementName="CadastralBoundary"
                      gfsSchemaLocation="inspire_cp_CadastralBoundary.gfs"/>
          <featureType elementName="CadastralParcel"
                      gfsSchemaLocation="inspire_cp_CadastralParcel.gfs"/>
          <featureType elementName="CadastralZoning"
                      gfsSchemaLocation="inspire_cp_CadastralZoning.gfs"/>
      </namespace>
  </gml_registry>


Les fichiers (.xsd) de définition des schémas XML sont pointé par l'attribut 
schemaLocation, tandis que les fichiers .gfs d'OGR sont pointés par l'atribut 
*gfsSchemaLocation*. Dans les deux cas, le nom du fichier peut être une URL 
(http://, https://), un nom de fichier absolut absolute, ou un nom de fichier 
relatif (relatif à l'endroit du fichier gml_registry.xml).

Le schéma est utilisé si et seulement si le préfixe de l'espace de nom et l'URI 
sont trouvés dans les premiers octets du fichier GML (e.g. 
*xmlns:ktjkiiwfs="http://xml.nls.fi/ktjkiiwfs/2010/02"*), et que le type de 
l'entité est aussi détecté dans les premiers octets du fichier GML 
(e.g. *ktjkiiwfs:KiinteistorajanSijaintitiedot*).

Construire des tables de jonction
===================================

Le script `ogr_build_junction_table.py <http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/ogr_build_junction_table.py>`_ 
peut être utilisé pour construire une `table de jonction <http://en.wikipedia.org/wiki/Junction_table>`_ 
à partir des couches OGR qui contient les champs "XXXX_href".

Considérons la sortie suivante d'un fichier GML avec des liens vers d'autres 
entités :

::
  
  OGRFeature(myFeature):1
    gml_id (String) = myFeature.1
    [...]
    otherFeature_href (StringList) = (2:#otherFeature.10,#otherFeature.20)
  
  OGRFeature(myFeature):2
    gml_id (String) = myFeature.2
    [...]
    otherFeature_href (StringList) = (2:#otherFeature.30,#otherFeature.10)


Après avoir lancé *ogr2ogr -f PG PG:dbname=mydb my.gml* pour l'importer dans 
PostGIS et *python ogr_build_junction_table.py PG:dbname=mydb*, une table 
*myfeature_otherfeature* sera créé et contiendra le contenu suivant :

+-------------------+----------------------+
+ myfeature_gml_id  + otherfeature_gml_id  +
+===================+======================+
+ myFeature.1       + otherFeature.10      +
+-------------------+----------------------+
+ myFeature.1       + otherFeature.20      +
+-------------------+----------------------+
+ myFeature.2       + otherFeature.30      +
+-------------------+----------------------+
+ myFeature.2       + otherFeature.10      +
+-------------------+----------------------+

Exemple
=========

La commande *ogr2ogr* peut être utilisé pour faire un dump des résultats d'une 
requête Oracle en GML :
::
    
    ogr2ogr -f GML output.gml OCI:usr/pwd@db my_feature -where "id = 0"

La commande *ogr2ogr* peut être utilisé pour faire un dump des résultats d'une 
requête PostGIS en GML :
::
    
    ogr2ogr -f GML output.gml PG:'host=myserver dbname=warmerda' -sql 
        "SELECT pop_1994 from canada where province_name = 'Alberta'"


.. seealso::

 * `Spécifications du GML <http://www.opengeospatial.org/standards/gml>`_
 * `Profile GML 3.1.1 simple features - OGC(R) 06-049r1 <http://portal.opengeospatial.org/files/?artifact_id=15201>`_
 * `Profile du Geography Markup Language des entités simples (GML) (avec correction) (GML 3.2.1) - OGC(R) 10-100r3 <https://portal.opengeospatial.org/files/?artifact_id=42729>`_
 * `Xerces <http://xml.apache.org/xerces2-j/index.html>`_
 *  :ref:`gdal.ogr.format.nas`
 
Crédits
========

* Implémentation pour **GML_SKIP_RESOLVE_ELEMS HUGE** a été une contribution de 
  A.Furieri, financé par la Région Toscane.
 
.. yjacolin at free.fr, Yves Jacolin - 2013/11/07 (trunk 26591)