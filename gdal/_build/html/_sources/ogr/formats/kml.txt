.. _`gdal.ogr.formats.kml`:

==============================
KML - Keyhole Markup Language
==============================

Keyhole Markup Language (KML) est un langage basé sur XML pour la gestion de 
l'affichage des données géospatiales 3D. KML a été accepté comme standard OGC, 
et est géré d'une manière ou d'une autre par les navigateurs spatiaux majeurs. 
Remarquez que KML par définition utilise seulement une seule projection, 
*EPSG:4326*. Tous les exports KML d'OGR se présenteront en *EPSG:4326*. Par 
conséquent, OGR créera toutes les couches dans le système de coordonnées 
correcte et transformera toutes les géométries.

Pour l'instant, seulement les couches vectorielles sont prises en charge par 
le pilote KML *(il existe des scripts supplémentaires fournies avec le projet 
GDAL qui peuvent construire des export d'autres sortes)*.

Lecture du KML
==============

La lecture du KML est seulement disponible si GDAL/OGR est compilé avec le 
parser XML Expat, autrement seule l'écriture du KML sera gérée.

Les types de géométrie gérés sont Point, Linestring, Polygon, MultiPoint, 
MultiLineString, MultiPolygon et MultiGeometry. 
Il y a des limitations également, par exemple : les répertoires inclus dans 
un fichier KML source sont perdus ; les balises <description> des répertoires 
ne sera pas transmit à la sortie. Depuis GDAL 1.6.1, les répertoires contenant des 
types de géométries multiples, comme les points et les polygones, sont gérés.

Écriture du KML
================

Puisque toutes les géométries du KML ne sont pas représenté dans le modèle de 
géométrie *Features*, vous ne pourrez pas générer plusieurs attributs 
spécifiques au KML à partir de GDAL/OGR. Testez quelques fichiers pour voir ce 
qui est possible.

Lors de l'export du KML, le pilote KML d'OGR traduira chaque couche OGR dans un 
répertoire KML, vous pouvez rencontrer des comportements inattendus si vous 
tentez de mélanger les types de géométries d'éléments dans une couche, par 
exemple des données *LINESTRING* et *POINT*.

Le pilote KML renommera certaines couches, ou des noms de répertoires du KML 
source, par des noms qu'il considère valide, par exemple 'Layer #0', le nom par 
défaut de la première couche non nommée, deviendra 'Layer__0'.

KML est un mélange de mise en forme et de données géométriques. La balise 
<description> d'un *Placemark* sera affiché dans la plupart des navigateurs 
spatiaux comme une bulle contenant du html. Lors de l'écriture du KML, les 
attributs de l'élément *Layer* sont ajoutés  comme de simples champs schéma. 
Cela préserve au mieux l'information du type de l'objet.

Une gestion limitée est disponible pour le remplissage (fill), couleur des 
lignes et autres attributs de styles. Essayez sur des échantillons pour avoir 
une meilleure vision des possibilités.

Problèmes d'encodage
---------------------

La bibliothèque Expat gère la lecture des encodages internes suivants :

* US-ASCII
* UTF-8
* UTF-16
* ISO-8859-1

OGR 1.8.0 ajoute la gestion des encodages pour Windows-1252 (pour les versions 
précédentes, modifier l'encodage mentionné dans l'en-tête XML en ISO-8859-1 peut 
fonctionner dans certains cas).

Le contenu retourné par OGR sera encodé en UTF-8, après la conversion de l'encodage 
mentionné dans l'en-tête du fichier.

Si votre fichier KML n'est pas encodé dans l'un des encodages précédents, il ne 
sera pas parsé par le pilote KML. Vous devrez le convertir dans l'un des encodages 
gérés par la commande *iconv* par exemple et changer la valeur du paramètre 
*encoding* dans l'en-tête XML.

Lors de l'écriture du fichier KML, le pilote s'attend à du contenu en UTF-8.

Options de création
--------------------

Les options de création suivantes sont gérées :

* **NameField :** permet de définir le champ à utiliser pour l'élément 
  <name> du KML. La valeur par défaut est 'Name'.
  ::
    
    ogr2ogr -f KML output.kml input.shp -dsco NameField=RegionName

* **DescriptionField :** permet de définir le champ à utiliser pour l'élément 
  <description> du KML. La valeur par défaut est 'Description'
* **AltitudeMode :** permet de définir *AltitudeMode* à utiliser pour les 
  géométries du KML. Cela affectera seulement les géoémtries 3D et doit être 
  une des options KML valide. Lisez la 
  `documentation de référence du KML <http://code.google.com/apis/kml/documentation/kml_tags_21.html#altitudemode>`_ 
  pour plus de détails.
  ::
    
    ogr2ogr -f KML output.kml input.shp -dsco AltitudeMode=absolute

Exemple
========

La commande ``ogr2ogr`` peut être utilisé pur faire un dump d'une requête PostGIS 
vers le format KML :
::
    
    ogr2ogr -f KML output.kml PG:'host=myserver dbname=warmerda' -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

Pour faire un dump d'un fichier .kml comme OGR le voit :
::
    
    ogrinfo -ro somedisplay.kml

Avertissement
=============

Google Earth semble avoir quelques limites avec le nombre de coordonnées dans 
des géométries complexes comme les polygone. Si le problème apparait, les 
géométries problématiques sont affichées complètement ou partiellement couvert 
par des rayures verticales. malheureusement, il n'y a pas de nombre exact donné 
dans la spécification KML à propos de cette limitation, le pilote KML ne 
préviendra pas sur des problèmes potentiels. Un des solutions testées possibles 
est de simplifier les lignes ou les polygones pour enlever quelques coordonnées. 
Voici la discussion sur ce problème sur le 
`Forum développeur de Google KML <http://groups.google.com/group/kml-support>`_, 
dans le thread `polygone affiché avec des rayures verticales <http://groups.google.com/group/kml-support-getting-started/browse_thread/thread/e6995b8073e69c41>`_.

Voir également
===============

* `Spécification KML <http://earth.google.com/kml/kml_intro.html>`_
* `Cours KML <http://www.keyhole.com/kml/kml_tut.html>`_

.. yjacolin at free.fr, Yves Jacolin  2011/08/02 (trunk 18832)