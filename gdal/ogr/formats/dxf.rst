.. _`gdal.ogr.formats.dxf`:

DXF d'AutoCAD
=============

OGR gère la lecture de la plupart des versions DXF d'AutoCAD et l'écriture des 
fichiers de versions AutoCAD 2000. DXF est un format ascii utilisé pour 
l'échange de données AutoCAD entre différents logiciels de l'éditeur. Le contenu 
complet du fichier est représenté comme un couche unique nommée "entities".  

Les fichiers DXF sont considéré sans informations de géo-référencement via OGR. 
Les features possèderont toutes les attributs génériques suivants :

* Layer : le nom de la couche DXF. Par défaut "0".
* SubClasses : si disponible, une liste de classes à laquelle un élément appartient.
* ExtendedEntity : si disponible, attributs de l'entité étendue toute empilée 
  pour former un attribut texte unique.
* Linetype : si disponible, le type de ligne utilisée pour cette entité.
* EntityHandle : de quoi gérer l'entité en hexadecimal. Une sorte d'identifiant 
  de la feature.
* Text : le texte des étiquettes.


Éléments gérés
---------------

Les types d'éléments suivants sont gérés :

* POINT : produit une feature de géométrie de type point.
* MTEXT, TEXT : produit une feature de géométrie de type point avec des 
  informations de style de LABEL.
* LINE, POLYLINE, LWPOLYLINE : traduit en LINESTRING ou POLYGON  s'il est fermé 
  ou non. Les polylignes arrondis (ceux avec leur sommet déplacé d'attributs [1]_) 
  seront tesselés. Les polylignes à unique sommet sont traduit en POINT.
* CIRCLE, ELLIPSE, ARC :  traduit en LINESTRING, en tesselant l'arc en segment 
  de lignes.
* INSERT : une tentative est faite pour insérer la définition du block comme 
  définie dans l'insert. Les blocks linework sont agrégés dans une seule feature 
  avec une collection de géométrie. Les blocs de texte sont renvoyés comme un ou 
  plusieurs features texte. Afin d'éviter la fusion de blocs dans une collection 
  de géométrie l'option de configuration *DXF_MERGE_BLOCK_GEOMETRIES* peut être 
  définie à *FALSE*.
* DIMENSION : cet élément est découpé en feature en arrows et leaders, et une 
  feature avec une étiquette dimension.
* HATCH : ligne et arc sont collectés comme des géométries polygone, mais aucun 
  effort n'est entreprise actuellement pour représenter le style de remplissage 
  d'entité HATCH.

Une tentative raisonnable est réalisée pour préserver la couleur, la largeur de 
la ligne, la taille et l'orientation du texte via les informations de styles des 
features lors de la traduction des éléments. Pour l'instant aucun effort n'est 
réalisé pour préserver les styles de remplissage ou les attributs de styles des 
lignes complexes.

L'approximation des arcs, ellipses, cercles et polylignes arrondis comme linestring 
est réalisée en découpant les arcs en sous-arcs inférieure au seuil d'un angle. 
Cet angle est définie par *OGR_ARC_STEPSIZE*. Par défaut à 4 degrés, mais peut être 
écrasé par la variable de configuration *OGR_ARC_STEPSIZE*.

DXF_INLINE_BLOCKS
-------------------

Le comportement par défaut pour les entités INSERT est d'être étendue avec la 
géométrie du bloc qu'ils référencent. Cependant si l'option de configuration 
*DXF_INLINE_BLOCKS* est définie à la valeur *FALSE*, alors le comportement est 
différent comme décrit ici.

* Une nouvelle couche nommée bloc sera disponible. Elle contiendra une ou 
  plusieurs features, elle aura également un attribut *BlockName* qui indique 
  quel bloc ils font partie.
* La couche entité aura de nouveau attributs BlockName, BlockScale, 
  et BlockAngle. 
* Les entités INSERT remplira ces nouveaux champs avec les informations 
  correspondantes (ils sont null poru toutes les autres entités).
* Les entités INSERT ne contiendront pas de bloc géométrie - ils auront à la place 
  une géométrie ponctuelle pour le point d'insertion.

L'intention est qu'avec le paramètre *DXF_INLINE_BLOCKS* désactivé, les blocs de 
références resteront comme références et le bloc original de définition sera 
disponible via la couche blocs. En export cette configuration entrainera la 
création de blocs identiques.

Encodages des caractères
--------------------------

Normalement les fichiers DXF sont dans l'encodage ANSI_1252 / Win1252.  GDAL/OGR 
tente de traduire cela vers l'UTF-8 lors de la lecture puis en ANSI_1252 pour 
l'écriture. Les fichiers DXF peuvent aussi avoir un champ en-tête ($DWGCODEPAGE) 
indiquant l'encodage du fichier. Dans GDAL 1.8.x et plus ancien cela était ignoré 
mais à partir de GDAL 1.9.0 et plus récent une tentative est réalisée pour utiliser 
cela pour re-encoder des autres encodages vers l'UTF-8.  Cela fonctionnera en 
fonction du nom du code d'encodage et si GDAL/OGR a été compilé avec la 
bibliothèque iconv pour le re-encodage des caractères.


Dans certains as le paramètre *$DWGCODEPAGE* dans le fichier DXF sera erroné, ou 
ne sera pas reconnu par OGR. Il peut être édité manuellement, ou la variable de 
configuration *DXF_ENCODING* peut être utilisée pour écraser l'id qui sera utilisé 
par OGR lors du transcodage. La valeur de *DXF_ENCODING* doit être un nom 
d'encodage géré par *CPLRecode()* (ie un nom iconv), et pas un nom $DWGCODEPAGE 
du DXF. Utiliser le nom "UTF-8" pour le *DXF_ENCODING* évitera toute tentative de 
re-encodage lors de la lecture.

Problèmes de création
----------------------

Les fichiers DXF sont écrits au format AutoCAD 2000. Un en-tête standard (Tout 
jusqu'au mot clé ENTITIES) est écrit à partir du fichier *$GDAL_DATA/header.dxf*, 
et le fichier *$GDAL_DATA/trailer.dxf* est ajouté après les entités. Une seule 
couche peut être créée dans le fichier output.

Les features points avec un style de LABEL sont écrit comme des entités MTEXT 
basé sur les informations de style.

Les features points sans style de LABEL sont écrits sous forme d'entité POINT.

LineString, MultiLineString, Polygon et MultiPolygons sont écrit sous forme d'une 
ou plusieurs entités LWPOLYLINE, fermé dans le cas d'un anneau polygonale. Un 
effort est réalisé pour préserver la largeur des lignes et leur couleur.

La création de jeu de données gère les options de création de jeu de données 
suivants :

* **HEADER=filename :** écrase le fichier d'en-tête utilisé - au lieu de header.dxf. 
* **TRAILER=filename :** écrase le fichier trailer utilisé - au lieu de trailer.dxf.

Notez que dans GDAL 1.8 et supérieur, les modèles d'en-tête et trailer peut être 
des fichiers DXF complet. Le pilote les scannera et extraira seulement les 
portions nécessaires (portion avant ou après la section ENTITIES). 

Références des blocs
*********************

Il est possible d'exporter un "bloc" de couche vers le DXF en plus de la couche 
"entities" dans le but de produire les définitions des BLOCKs réel DXF dans le 
fichier en sortie. Il est également possible d'écrire les entités INSERT si un 
nom de bloc est fournie pour une entité. Pour que cela fonctionne les conditions 
suivantes s'appliquent :

* une couche "blocks" peut être créée, et elle doit être créé avant la couche 
  entité.
* les entités dans la couche blocks doivent avoir le champs BlockName remplis.
* Les objets à écrire comme INSERTs dans la couche entités doivent avoir une 
  géométrie POINT et le champ BlockName définie. 
* si un bloc (nom) est déjà définie dans l'en-tête modèle, celui-ci sera utilisé 
  sans vérifier si une nouvelle définition a été fournie dans la couche block.

L'intention est qu'une simple traduction à partir d'un DXF avec *DXF_INLINE_BLOCKS* 
définie à FALSE reproduira approximativement les blocs originaux et gardera les 
entités INSERT comme des entités INSERT plutôt que des les éclater.

Définitions des couches
***********************

Lors de l'écriture des entités, si il est rempli  le champs LayerName est utilisé 
pour définir la couche entités écrite. Si la couche n'est pas déjà définie dans 
le modèle d'en-tête alors une nouvelle définition de couche sera introduite, copiée 
de la définition de la couche par défaut ("0").

Définitions de type de ligne
*****************************

Lors de l'écriture des entités LWPOLYLINE les règles suivantes s'appliquent au 
regard des définitions Linetype.

* Si le champ Linetype est définie sur les features écrites et que Linetype est 
  déjà définie dans le modèle d'en-tête alors il sera référencé à partir des 
  entités sans vérifier si un style OGR existe.
* Si le Linetype est définie mais que le Linetype n'est pas prédéfinie dans le 
  modèle d'en-tête alors une définition sera ajoutée si la feature possède un 
  style OGR avec un outil PEN et ne définition de motif "p".
* Si la feature n'a pas de champs Linetype définie, mais possède un style OGR avec 
  un outil PEN avec un motif "p" définie alors un LineType automatiquement nommée 
  sera créé dans le fichier en sortie.
* Il est supposé que les motifs utilisent les unités "g" (géoréférencé) pour 
  définir le motif de la ligne. Sinon la mise à l'échelle des motifs DXF sera 
  probablement fausse - potentiellement complètement fausse.

L'objectif est que le motif de style "dot dash" soient préservé lors de l'écriture 
vers le DFX et que les linetypes spécifiques puisse être prédéfinie dans le 
modèle d'en-tête et référencé en utilisant le champ Linetype si désiré.

.. [1] [NdT] *those with their budge of vertices attributes set*

.. yjacolin at free.fr, Yves Jacolin - 2011/07/03 (trunk 22011)