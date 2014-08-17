.. _`gdal.ogr.formats.dwg`:

============
AutoCAD DWG
============

OGR gère la lecture la plupart des versions DWG d'AutoCAD lorsqu'il est compilé 
avec la bibliothèque Teiga de l'Open Design Alliance. DWG est un format binaire 
de travail utilisé pour les dessins AutoCAD. Un effort raisonnable a été fait 
pour rendre le fonctionnement du pilote DWG d'OGR similaire au pilote DXF d'OGR 
qui partage un modèle de données commun. L'intégralité du contenu du fichier 
.dwg est représentée comme une couche unique nommé «entités».

Les fichiers DWG sont considérés sans information de géoréférencement via OGR. 
Les entités possèderont les attributs génériques suivants :

* **Layer :** le nom de la couche DXF. La couche par défaut est "0".
* **SubClasses :** lorsque c'est disponible, une liste de de classes à laquelle 
  apaprtient un éléemnt.
* **ExtendedEntity :** lorsque c'est disponible, attributs d'entitées étendues 
  aggrégés pour former un attribut texte unique.
* **Linetype :** lorsque c'est disponible, le type de ligne utilisé pour cette 
  entité.
* **EntityHandle :** La prise en charge de l'entité héxadecimale. Une sorte d'id 
  d'entité.
* **Text :** le texte des étiquettes.

Une tentative raisonnable est réalisée pour préserver les couleurs et la largeur 
des lignes, la taille et l'orientation du texte via les informations de styles 
des entités d'OGR lors de la traduction des éléments. Pour le moment aucun effort 
n'est fait pour préserver les styles de remplissage ou les styles de ligne complexe.

L'approximation des arcs, ellipses, cercles et polylignes arrondies comme linestring 
est réalisée en découpant l'arc en sous-arcs inférieur à seuil d'angle. Cet angle 
est OGR_ARC_STEPSIZE.  Par défaut à 4 degrés, mais peut être écrasé en définissant 
la variable de configuration ``OGR_ARC_STEPSIZE``.

DWG_INLINE_BLOCKS
=================

Le comportement par défaut pour les références des blocs est d'être étendues avec 
la géométrie du bloc qu'ils référencent. Cependant, si l'option de configuration 
DWG_INLINE_BLOCKS est définie à la valeur FALSE alors le comportement est différent 
comme décrit ici.

* Une nouvelle couche sera disponible appellée blocks. Il contiendra une ou plusieurs 
  entités pour chaque blocs définie dans le fichier. En plus des attributs habituels, 
  ceux-ci auront un attribut BlockName qui indique quel bloc ils font partie.
* La couche entité aura de nouveaux attributs BlockName, BlockScale,
  et BlockAngle.
* Les blocs réféerencés rempliront ces nouveaux champs avec l'information 
  correspondante (ils seront null pour tous les autres entités).
* Les références de bloc n'auront pas de géométrie du bloc en ligne - à la place ils 
  auront une géométrie point pour le point d'intersection.

L'intention est qu'avec DWG_INLINE_BLOCKS désactivé, les références de bloc resteront 
comme références et les définitions de bloc original seront disponible via la couche 
des blocs.

Compilation
============

La compilation du pilote DWG est pour le moment adhoc. Sous Linux le fonctionnement 
normal est d'éditer à la main gdal/ogr/ogrsf_frmts/dwg/GNUmakefile, mettre à jour 
les chemins puis alors de compiler le pilote comme plugin en utilisant la cible 
"make plugin".

.. yjacolin at free.fr 2013/01/24 (trunk r23625)
