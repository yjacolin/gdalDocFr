.. _`gdal.ogr.formats.geojson`:

========
GeoJSON
========

Ce pilote implémente la gestion en lecture et écriture pour l'accès aux géométries encodé au format `GeoJSON <http://geojson.org/>`_. Le GeoJSON est un langage basé sur `JavaScript Object Notation (JSON) <http://json.org/>`_. Le JSON est un format léger textuel pour l'échange de données et GeoJSON n'est rien d'autre que sa spécialisation pour le contenu géographique.

Au moment d'écrire ce texte, GeoJSON est géré comme format de sortie de services implémenté par `FeatureServer <http://featureserver.org/>`_, 
`GeoServer <http://docs.codehaus.org/display/GEOSDOC/GeoJSON+Output+Format>`_ et 
`CartoWeb <http://exportgge.sourceforge.net/kml/>`_.

Le pilote GeoJSON d'OGR traduit une donnée encodée en GeoJSON vers des objets 
du `model Simple Feature d'OGR <http://gdal.org/ogr/ogr_arch.html>`_ : jeu de 
données, couche, objet, géométrie. L'implémentation est basée sur le 
`brouillon de spécification de GeoJSON, v5.0 <http://wiki.geojson.org/GeoJSON_draft_version_5>`_.

À partir de OGR 1.8.0, le pilote GeoJSON peut lire les sorties JSON des requêtes 
de services de Feature qui suivent les `spécifications REST des GeoServices 
<http://www.esri.com/industries/landing-pages/geoservices/geoservices.html>`_, comme 
implémenté par l'`API du serveur REST d'ArcGIS <http://help.arcgis.com/en/arcgisserver/10.0/apis/rest/index.html>`_.

Source de données
==================

Le pilote GeoJSON d'OGR accepte trois types de sources de données :

* *Uniform Resource Locator* (`URL <http://en.wikipedia.org/wiki/URL>`_) - une 
  adresse web pour réaliser des requêtes 
  `HTTP <http://en.wikipedia.org/wiki/HTTP>`_
* des fichiers textuels avec des données GeoJSON - identifié à partir de 
  l'extension du fichier .geojson ou .json
* du texte passé directement et encodé en GeoJSON

Couche
=======

Un jeu de données GeoJSON est traduit à un objet *OGRLayer* simple avec un nom prédéfinie *OGRGeoJson* :
::
    
    ogrinfo -ro http://featureserver/data/.geojson OGRGeoJSON

Il est également valide de faire l'hypothèse que 
*OGRDataSource::GetLayerCount()* pour la source de données GeoJSON retourne 
toujours 1.

Accéder un service Web comme source de données (par exemple FeatureServer), 
chaque requête produira une nouvelle couche. Ce comportement se conforme à la 
nature *stateless* des transactions HTTP et est similaire à la façon dont opère 
les navigateurs : une requête = une page.

Si un membre de plus haut niveau des données GeoJSON est d'un autre type que 
FeatureCollection,le pilote produira une couche avec seulement un objet. 
Autrement, une couche consistera d'un ensemble d'objets.

Objet
=======

Le pilote GeoJSON d'OGR relie chaque objet des types suivants aux nouveaux 
objets *OGRFeature* : Point, LineString, Polygon, GeometryCollection, Feature.

Selon les spécification GeoJSON, seul l'objet *Feature* doit avoir un 
membre avec un nom de propriété. Chaque membre des propriétés est traduit 
vers un objet OGR du type de *OGRField* et ajouté à l'objet *OGRFeature* 
correspondant.

La spécification GeoJSON ne nécessite pas que tous les objets géométriques dans 
une colection doivent avoir le même schéma de propriétés. Si les objets 
géométriques dans un ensemble définie par un objet FeatureCollection ont 
différents schéma de propriétés, il en résulte alors un schéma de champs dans 
*OGRFeatureDefn* est généré comme 
l'`union <http://en.wikipedia.org/wiki/Union_(set_theory)>`_ de toutes les 
propriétés géométriques.

Il est possible de dire au pilote de ne pas traiter les attributs en définissant 
la variable d'environnement *ATTRIBUTES_SKIP=YES*. Le comportement par défaut 
est de préserver tous les attributs (comme une union, voir paragraphe précédent), 
ce qui est équivalent à définir *ATTRIBUTES_SKIP=NO*.

Géométrie
==========

Comme pour le problème des objets avec des propriétés mixtes, le brouillon de 
la spécification GeoJSON ne nécessite pas que tous les objets géométriques dans 
une collection doivent avoir une géométrie de même type. Heureusement le modèle 
objet d'OGR permet d'avoir des géométries de plusieurs types dans une seule 
couche - un couche hétérogène. Par défaut, le pilote GeoJSON préserve le type 
de la géométrie.

Cependant, parfois il nécessite de générer une couche hétérogène à partir d'un 
ensemble d'objet géométrique hétérogène. Pour cela, il est possible de dire au 
pilote d'englober toutes les géométries avec un type *OGRGeometryCollection* 
comme un dénominateur commun. Ce comportement peut être contrôler par la 
variable d'environnement *GEOMETRY_AS_COLLECTION=YES* (NO par défaut).


Variables d'environnement
*************************

* *GEOMETRY_AS_COLLECTION* - utilisé pour contrôler la traduction des 
  géométries : YES - englobe les géométries avec le type *OGRGeometryCollection*
* *ATTRIBUTES_SKIP* - contrôle la traduction des attributs : YES - ignore les 
  attributs

Option de création de couche
=============================

* **WRITE_BBOX = YES/NO :** (OGR >= 1.9.0) définie à YES pour écrire une propriété 
  bbox avec la bounding box des géométries au niveau de la feature et de la 
  collection de feature. NO par défaut.
* **COORDINATE_PRECISION = int_number :** (OGR >= 1.9.0) nombre maximal de 
  chiffre à écrire après la virgule pour les coordonnées. 15 par défaut. Une 
  coupure intelligente permettra de supprimer les zéros en trop.

Gestion de l'API de Système de Fichier Virtuel
================================================

.. warning:: Certaines fonctionnalités ci-dessous peuvent nécessité OGR >= 1.9.0

Le pilote gère la lecture et l'écriture vers les fichiers géré par l'API du Système de Fichier Virtuel ce qui inclus 
les fichiers "normaux", ainsi que les fichiers dans les domaines /vsizip/ (lecture-écriture), /vsigzip/ (lecture-écriture) , /vsicurl/ (lecture-seule).

L'écriture vers /dev/stdout ou /vsistdout/ est également gérée.

Exemples
==========

Comment faire un dump du contenu d'un fichier .geojson :
::
    
    ogrinfo -ro point.geojson

Comment réaliser une requête sur les objets à partir un service distant avec un 
filtre sur un attribut :
::
    
    ogrinfo -ro http://featureserver/cities/.geojson OGRGeoJSON -where "name=Warsaw"

Comment traduire un certain nombre d'objets à partir d'une requête d'un 
FeatureServer vers un shapefile d'ESRI :
::
    
    ogr2ogr -f "ESRI Shapefile" cities.shp http://featureserver/cities/.geojson OGRGeoJSON

Lire le résultat d'une requête FeatureService en fonction d'un serveur GeoServices 
REST :
::
    
    ogrinfo -ro -al
      "http://sampleserver3.arcgisonline.com/ArcGIS/rest/services/Hydrography/Watershed173811/FeatureServer/0/query?where=objectid+%3D+objectid&amp;outfields=*&amp;f=json"

.. seealso::

* `GeoJSON <http://geojson.org/>`_ - encoding geographic content in JSON
* `JSON <http://json.org/>`_ - JavaScript Object Notation
* `JSON-C <http://oss.metaparadigm.com/json-c/>`_ - Une implémentation JSON en C
* `[Gdal-dev] OGR GeoJSON Driver <http://lists.osgeo.org/pipermail/gdal-dev/2007-November/014746.html>`_ - driver announcement
* `Spécification REST des GeoServices <http://www.esri.com/industries/landing-pages/geoservices/geoservices.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/04/03 (trunk 23022)