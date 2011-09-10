.. _`gdal.ogr.formats.libkml`:

==========================
Pilote LIBKML (.kml .kmz)
==========================

Le pilote LIBKML est un client de `Libkml <http://code.google.com/p/libkml/>`_ 
de Google, une implémentation de référence du `KML <http://www.opengeospatial.org/standards/kml/>`_ 
en lecture et écriture, sous la forme d'une biliothèque C++ multi-plateforme. 
Vous devez compiler et installer Libkml dans le but d'utiliser ce pilote OGR.

Notez que si vous compilez et incluez le pilote LIBKML, il deviendra le lecteur 
par défaut du KML pour OGR, écrasant le pilote KML précédent. Vous pouvez toujours 
définir soit KML ou LIBKML comme pilote de sortie via la ligne de commande.

Libkml de Google fournit des services de lecture pour un fichier KML valide.
Toutefois, s'il vous plaît notez que certaines installations KML ne correspondent 
pas aux spécifications Simple Feature qu'ogr utilise comme structure interne.
Par conséquent, un meilleur effort sera fait par le pilote pour comprendre le 
contenu d'un dossier KML lu par libkml dans OGR, mais votre version peut varier.
S'il vous plaît essayez quelques fichiers KML comme échantillons pour avoir une 
idée de ce qui est bien interprété. En particulier, l'imbrication de features
définit dans plus d'une profondeur seront aplaties pour être géré par le format 
interne d'OGR.
  
Datasource
=========== 

Vous pouvez définir un `datasource <http://www.gdal.org/ogr/ogr_arch.html#ogr_arch_data_source>`_ 
comme fichier kml ``somefile.kml``, un répertoire ``somedir/``, ou un fichier kmz 
``somefile.kmz``.

Par défaut, sur les sources de données kmz et répertoire, un fichier index de 
toutes les couches sera lu ou écrit à partir ou vers le fichier doc.xml. Il 
contient `<NetworkLink> <http://code.google.com/apis/kml/documentation/kmlreference.html#networklink>`_ 
pour chaque fichier couche dans le datasource. Cette fonctionnalité peut être 
désactivée en définissant la variable d'environnement *LIBKML_USE_DOC.KML* à "no".
 
StyleTable
-----------  

Les tables des styles des datasource sont écrit dans le 
`<Document> <http://code.google.com/apis/kml/documentation/kmlreference.html#document>`_ 
dans un .kml, style/style.kml dans un fichier kmz, or style.kml dans un répertoire, 
sous forme d'un ou plusieurs éléments 
`<Style> <http://code.google.com/apis/kml/documentation/kmlreference.html#style>`_. 
Tous les `styles de feature d'OGR <http://www.gdal.org/ogr/ogr_feature_style.html>`_
ne peuvent être traduit en KML.

Layer
=====

`Layers <http://www.gdal.org/ogr/ogr_arch.html#ogr_arch_layer>`_ sont déclarées 
dans les fichiers kml en tant que 
`<Document> <http://code.google.com/apis/kml/documentation/kmlreference.html#document>`_ ou 
`<Folder> <http://code.google.com/apis/kml/documentation/kmlreference.html#folder>`_, 
et dans les fichiers kmz ou les répertoires  comme des fichiers kml séparés.

Style
======

Les tables de style des couches ne peuvent pas être lues ou écrites à partir 
de/vers une couche kml qui est un 
`<Folder> <http://code.google.com/apis/kml/documentation/kmlreference.html#folder>`_, 
sinon ils sont dans le 
`<Document> <http://code.google.com/apis/kml/documentation/kmlreference.html#document>`_ 
d'une couche.

Schéma
=======

La lecture et l'écriture de `<Schema> <http://code.google.com/apis/kml/documentation/kmlreference.html#schema>`_ 
est géré pour les fichiers .kml, .kmz et les répertoires.

Feature
========

Une `feature <http://www.gdal.org/ogr/ogr_arch.html#ogr_arch_feature>`_ OGR se 
traduit en kml en tant que `<Placemark> <http://code.google.com/apis/kml/documentation/kmlreference.html#placemark>`_.
  
Style
------

Les chaînes de style au niveau de la feature sont déclarées dans le KML soit en 
tant que 
`<Style> <http://code.google.com/apis/kml/documentation/kmlreference.html#style>`_ 
ou `<StyleUrl> <http://code.google.com/apis/kml/documentation/kmlreference.html#styleurl>`_ 
dans chaque 
`<Placemark> <http://code.google.com/apis/kml/documentation/kmlreference.html#placemark>`_.

Lors de la lecture d'une feature kml et que la variable d'environnement 
*LIBKML_RESOLVE_STYLE* est positionnée à yes, les urls de styles sont recherchés 
dans les tableaux de style et les chaînes de style des features sont défini sur 
le style à partir de la table. C'est pour permettre la lecture de styles partagés 
par les applications, comme MapServer, qui ne lisent pas de tables de style.

Lors de la lecture d'une feature kml et que la variable d'environnement 
*LIBKML_EXTERNAL_STYLE* est positionnée à yes, une url de style qui est externe 
à la source de données est lu à partir du disque ou récupérés sur le serveur et 
analysée dans la table de style de la datasource. Si le style KML ne peut être 
lu ou *LIBKML_EXTERNAL_STYLE* est positionnée à no, alors l'url du style est 
copiée à la chaîne de style.

Champs
=======

Les champs OGR (attributs des feature) sont traduit vers le kml avec 
`<Schema> <http://code.google.com/apis/kml/documentation/kmlreference.html#schema>`_ 
et `<SimpleData> <http://code.google.com/apis/kml/documentation/kmlreference.html#simpledata>`_, 
sauf pour certains champs spéciaux comme noté ci-dessous.

Un ensemble riche de variables d'environnement est disponible pour définir 
comment les champs en entrée et en sortie, sont traduit en kml 
`<Placemark> <http://code.google.com/apis/kml/documentation/kmlreference.html#placemark>`_. 
Par exemple, si vous voulez un champ appelé 'Cities' pour être traduit dans la balise 
`<name> <http://code.google.com/apis/kml/documentation/kmlreference.html#name>`_ 
en KML, vous pouvez définir une variable d'environnement.

* **Name :** 
      Ce champ de caractère traduit vers le kml la balise 
      `<name> <http://code.google.com/apis/kml/documentation/kmlreference.html#name>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_NAME_FIELD*.
* **description :** 
      Ce champ de caractère traduit vers le kml la balise 
      `<description> <http://code.google.com/apis/kml/documentation/kmlreference.html#description>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_DESCRIPTION_FIELD*.
* **timestamp :** 
      Ce champ de caractère ou datetime ou date et/ou time traduit vers le kml 
      la balise 
      `<timestamp> <http://code.google.com/apis/kml/documentation/kmlreference.html#timestamp>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_TIMESTAMP_FIELD*.
* **begin :** 
      Ce champ de caractère ou datetime ou date et/ou time traduit vers le kml 
      la balise 
      `<begin> <http://code.google.com/apis/kml/documentation/kmlreference.html#begin>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_BEGIN_FIELD*.
* **end :** 
      Ce champ de caractère ou datetime ou date et/ou time traduit vers le kml 
      la balise 
      `<end> <http://code.google.com/apis/kml/documentation/kmlreference.html#end>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_END_FIELD*.
* **altitudeMode :** 
      Ce champ de caractère traduit vers le kml la balise 
      `<altitudeMode> <http://code.google.com/apis/kml/documentation/kmlreference.html#altitudemode>`_ 
      ou
      `<gx:altitudeMode> <http://code.google.com/apis/kml/documentation/kmlreference.html#gxaltitudemode>`_.
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_ALTITUDEMODE_FIELD*.
* **tessellate :** 
      Ce champ d'entier traduit vers le kml la balise 
      `<tessellate> <http://code.google.com/apis/kml/documentation/kmlreference.html#tessellate>`_
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_TESSELLATE_FIELD*.
* **extrude :** 
      Ce champ d'entier traduit vers le kml la balise 
      `<extrude> <http://code.google.com/apis/kml/documentation/kmlreference.html#extrude>`_
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_EXTRUDE_FIELD*.
* **visibility :** 
      Ce champ d'entier traduit vers le kml la balise `<visibility> <http://code.google.com/apis/kml/documentation/kmlreference.html#visibility>`_. 
      Le nom du champ ogr peut être changé avec la variable d'environnement 
      *LIBKML_VISIBILITY_FIELD*.
* **OGR_STYLE :** 
      Ce champ de caractère traduit vers un style de feature, OGR li ce champs 
      s'il n'y a pas de chaînes de style définie sur la feature.

  
Géométrie
=========

Traduction de la `Geometry <http://www.gdal.org/ogr/ogr_arch.html#ogr_arch_geometry>`_ 
d'OGR vers la géométrie KML est assez simple, avec seulement quelques exceptions. 
Point vers `<Point> <http://code.google.com/apis/kml/documentation/kmlreference.html#point>`_, 
LineString vers `<LineString> <http://code.google.com/apis/kml/documentation/kmlreference.html#linestring>`_, 
LinearRing vers `<LinearRing> <http://code.google.com/apis/kml/documentation/kmlreference.html#linearring>`_, 
et Polygon vers `<Polygon> <http://code.google.com/apis/kml/documentation/kmlreference.html#polygon>`_. 

Dans OGR un polygone contient un tableau de LinearRings, le premier est celui à 
l'extérieur. KML a la balise `<outerBoundaryIs> <http://code.google.com/apis/kml/documentation/kmlreference.html#outerboundaryis>`_ 
et `<innerBoundaryIs> <http://code.google.com/apis/kml/documentation/kmlreference.html#innerboundaryis>`_
pour différencier les deux. OGR possède plusieurs types Multi des géométries :
GeometryCollection, MultiPolygon, MultiPoint, et MultiLineString. Quand cela est 
possible, OGR tentera de traduire 
`<MultiGeometry> <http://code.google.com/apis/kml/documentation/kmlreference.html#multigeometry>`_ 
vers le type de géométrie OGR la plus précise (MultiPoint, MultiLineString ou 
MultiPolygon), et pas défaut vers GeometryCollection dans le cas de contenu 
mixte.

Parfois, la géométrie kml couvrira la Dateline, dans des applications comme QGIS 
ou MapServer cela va créer des lignes horizontales sur tout le pourtour du globe.
En réglant la variable d'environnement *LIBKML_WRAPDATELINE* à "yes", contraindra 
le pilote libkml à diviser la géométrie à la Dateline lorsqu'il est lu.

Exemple
========

Le script bash suivant construira un fichier `csv <http://www.gdal.org/ogr/drv_csv.html>`_ 
et un fichier :ref:`gdal.ogr.formats.vrt`, puis les traduira en KML en utilisant 
:ref:`gdal.ogr.ogr2ogr` dans un fichier .kml avec un timestamp et des styles.
 
::
    
    #!/bin/bash
    # Copyright (c) 2010, Brian Case
    #
    # Permission is hereby granted, free of charge, to any person obtaining a
    # copy of this software and associated documentation files (the "Software"),
    # to deal in the Software without restriction, including without limitation
    # the rights to use, copy, modify, merge, publish, distribute, sublicense,
    # and/or sell copies of the Software, and to permit persons to whom the
    # Software is furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included
    # in all copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    # THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    # DEALINGS IN THE SOFTWARE.
    
    
    icon="http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"
    rgba33="#FF9900"
    rgba70="#FFFF00"
    rgba150="#00FF00"
    rgba300="#0000FF"
    rgba500="#9900FF"
    rgba800="#FF0000"
    
    function docsv {
    
        IFS=','
        
        while read Date Time Lat Lon Mag Dep
        do
            ts=$(echo $Date | sed 's:/:-:g')T${Time%%.*}Z
            rgba=""
            
            if [[ $rgba == "" ]] && [[ $Dep -lt 33 ]]
            then
                rgba=$rgba33
            fi
            
            if [[ $rgba == "" ]] && [[ $Dep -lt 70 ]]
            then
                rgba=$rgba70
            fi
            
            if [[ $rgba == "" ]] && [[ $Dep -lt 150 ]]
            then
                rgba=$rgba150
            fi
            
            if [[ $rgba == "" ]] && [[ $Dep -lt 300 ]]
            then
                rgba=$rgba300
            fi
            
            if [[ $rgba == "" ]] && [[ $Dep -lt 500 ]]
            then
                rgba=$rgba500
            fi
            
            if [[ $rgba == "" ]]
            then
                rgba=$rgba800
            fi
            
            
            
            style="\"SYMBOL(s:$Mag,id:\"\"$icon\"\",c:$rgba)\""
            
            echo $Date,$Time,$Lat,$Lon,$Mag,$Dep,$ts,"$style"
        done
            
    }
    
    
    wget http://neic.usgs.gov/neis/gis/qed.asc -O /dev/stdout |\
    tail -n +2 > qed.asc
    
    echo Date,TimeUTC,Latitude,Longitude,Magnitude,Depth,timestamp,OGR_STYLE > qed.csv
    
    docsv < qed.asc >> qed.csv
    
    cat > qed.vrt << EOF
    <OGRVRTDataSource>
        <OGRVRTLayer name="qed">
            <SrcDataSource>qed.csv</SrcDataSource>
            <GeometryType>wkbPoint</GeometryType>
            <LayerSRS>WGS84</LayerSRS>
            <GeometryField encoding="PointFromColumns" x="Longitude" y="Latitude"/>
        </OGRVRTLayer>
    </OGRVRTDataSource>
    
    EOF
    
    ogr2ogr -f libkml qed.kml qed.vrt

.. yjacolin at free.fr, Yves Jacolin  2011/08/02 (trunk 20731)