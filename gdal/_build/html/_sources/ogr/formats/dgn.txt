.. _`gdal.ogr.formats.dgn`:

=================
Microstation DGN
=================

Les fichiers DGN de Microstation des versions antérieures à 8.0 de Microstation 
sont gérés en lecture. Le fichier complet est représenté comme une couche 
(nommé "élément").

Les fichiers DGN sont considérés avoir des informations de géoréférencement à 
travers OGR. Les objets possèderont les attributs générique suivants :

* **Type :** le code *integer* du type comme listé ci-dessous dans les 
  éléments gérés.
* **Level :** le numéro de niveau de DGN (0-63).
* **GraphicGroup :** le numéro de groupe graphique.
* **ColorIndex :** l'index de la couleur dans la palette DGN.
* **Weight :** le poids du dessin (minceur) pour l'élément.
* **Style :** la valeur du style pour l'élément. 

Les fichiers DGN ne contiennent pas d'indexes spatiaux ; cependant, le pilote 
DGN utilise les informations d'étendues au début de chaque élément pour 
minimiser le traitement des éléments en dehors de la fenêtre du filtre spatial 
courant quand cela est possible.

Éléments gérés
=================

Les types d'élément suivants sont gérés :

* **Line (3) :** géométrie linéaire ;
* **Line String (4) :** géométrie linéaire multi-segment ;
* **Shape (6) :** géométrie polygonale ;
* **Curve (11) :** approximé comme une géométrie linéaire ;
* **B-Spline (21) :** traité (avec inexactitude) comme une géométrie linéaire ;
* **Arc (16) :** approximé comme une géométrie linéaire ;
* **Ellipse (15) :** approximé comme une géométrie linéaire ;
* **Text (17) :** traité comme une géométrie ponctuelle 

De manière générale tout concept d'objets complexes, et de cellules comme 
composant associé est perdu. Chaque composant d'un objet complexe ou d'une 
cellule est traité comme un objet indépendant.

Information de style
=====================

Certaine information de dessin sur les objets peuvent être extraite à partir 
des attributs génériques *ColorIndex*, *Weight* et *Style* ; cependant pour 
tous les objets, une chaine style d'OGR a été préparé avec les valeurs encodées 
sous une forme prête à être utilisée pour les applications utilisant les chaines 
style d'OGR.

Les différents sortes de géométries linéaires apporteront des informations de 
style indiquant la couleur, l'épaisseur et le style de la ligne (c'est à dire 
pointillé, solide etc.).

Les polygones (éléments Shape) apporteront les informations de style pour les 
bords ainsi que une couleur de remplissage si elle est fournie. Les motifs de 
remplissage ne sont pas gérés.

Les éléments textuels contiendront les informations sur le texte, l'angle, la 
couleur et la taille (exprimé en unité de groupe) dans la chaine style.

Options de création
====================

Les fichiers DGN 2D peuvent être écrit avec OGR avec des limitations 
significatives :

* les objets en sortie ont les attributs usuel DGN fixés. Toutes tentatives de 
  créer de nouveau champ échouera.
* Quasiment aucun effort n'est pour l'instant réalisé pour traduire les chaines 
  styles des objet OGR en information de représentation DGN.
* Les géométries POINT  qui n'ont pas de texte (le texte est NULL, et la chaine 
  style de l'objet n'est pas un LABEL) sera traduit comme élément ligne 
  dégénéré (longueur 0).
* Les objets polygone, et multi-polygone seront traduit en simples polygones 
  avec tous les anneaux après le premier omis.
* Les chaines polygones et ligne avec trop de sommet seront découpées en groupe 
  d'éléments préfixé avec un élément *Complex Shape Header* ou *Complex Chain 
  Header* comme approprié.
* Un fichier d'ensemencement doit être fournit (ou s'il ne l'est pas, 
  *$PREFIX/share/gdal/seed_2d.dgn* sera utilisé). Plusieurs aspects du fichier 
  DGN résultant sont déterminés par ce fichier, et ne peut être affecté par OGR, 
  tel que la fenêtre de vue initiale.
* Les diverses géométries collection autre que *MultiPolygon* sont complètement 
  ignoré pour l'instant.
* Les géométries qui tombent en dehors du "*design plane*" du fichier 
  d'ensemencement seront ignorées, ou corrompu d'une manière imprévisible.
* Les fichiers DGN peuvent seulement avoir une couche. Toutes tentatives pour 
  créer plus d'une couche dans nue fichier DGN échouera.

La création de jeu de donnés gère les options suivantes :

* **3D=YES or NO :** détermine si les fichiers d'ensemencement 2D (*seed_2d.dgn*) 
  ou 3D (*seed_3D.dgn*)) doivent être utilisés. Cette option est ignorée si 
  l'option *SEED* est fournie.
* **SEED=filename :** écrase le fichier d'ensemencement à utiliser.
* **COPY_WHOLE_SEED_FILE=YES/NO :** indique si tout le fichier d'ensemencement 
  doit être copié. Si non, seulement les trois premiers éléments (et 
  éventuellement la table de couleur) seront copiés. *NO* par défaut.
* **COPY_SEED_FILE_COLOR_TABLEE=YES/NO :** indique si la table de couleur doit 
  être copiée à partir du fichier d'encemensement. Par défaut elle est définie 
  à *NO*.
* **MASTER_UNIT_NAME=name :** écrase le nom de l'unité maitre à partir du 
  ficher d'ensemencement avec celui d'un ou de deux caractères fournit.
* **SUB_UNIT_NAME=name :** écrase le nom de la sous unité à patir du fichier 
  d'ensemencement avec celui d'un ou de deux caractères fournit.
* **SUB_UNITS_PER_MASTER_UNIT=count :** écrase le nombre de sus unité par unité 
  maitre. La valeur du fichier d'ensemencement est utilisé par défaut.
* **UOR_PER_SUB_UNIT=count :** écrase le nombre de UOR (Unité de Résolution, 
  *Units of Resolution*) par sous unité. La valeur du fichier d'ensemencement 
  est utilisée par défaut.
* **ORIGIN=x,y,z :** écrase l'origine du *design plane*. L'origine du fichier 
  d'ensemencement est utilisée par défaut.

Voir également
==============

* `Page Dgnlib <http://dgnlib.maptools.org/>`_
* `Spécification des Styles des objets d'OGR <http://home.gdal.org/projects/opengis/ogr_feature_style.html>`_ 

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 21:37 (trunk 9815)