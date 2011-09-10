.. _`gdal.ogr.formats.ntf`:

========
UK .NTF
========

Le Format de Transfert National (*National Transfer Format*)), principalement 
utilisé par le *UK Ordnance Survey*, est géré en lecture seule.

Ce pilote traite un répertoire comme un jeu de données et tente de fusionner 
tous les fichiers .NTF du répertoire, produisant une couche pour chaque type de 
géométrie (mais généralement pas pour chaque fichier source). Un répertoire 
contenant plusieurs fichiers *landlines* aura donc 3 couches (*LANDLINE_POINT*, 
*LANDLINE_LINE* et *LANDLINE_NAME*) sans regard du nombre de fichier *landline*.

Les géométries NTF sont toujours envoyées avec le système de coordonnées *British 
National Grid*. Cela peut être inapproprié pour les fichiers NTF écrit par 
d'autre organisation que le *UK Ordnance Survey*.

**Voir également :**

* `Information Générale sur le NTF UK <http://home.gdal.org/projects/ntf/index.html>`_

Implementation Notes
=====================

Produits (et couches) gérés
----------------------------

* **Landline (et Landline Plus) :**

  * *LANDLINE_POINT*
  * *LANDLINE_LINE*
  * *LANDLINE_NAME*

* **Panorama Contours :**

  * *PANORAMA_POINT*
  * *PANORAMA_CONTOUR*
  * attribut *HEIGHT* gère l'élévation.

* **Strategi :**

  * *STRATEGI_POINT*
  * *STRATEGI_LINE*
  * *STRATEGI_TEXT*
  * *STRATEGI_NODE*
* **Meridian :**
  * *MERIDIAN_POINT*
  * *MERIDIAN_LINE*
  * *MERIDIAN_TEXT*
  * *MERIDIAN_NODE*

* **Boundaryline :**

  * *BOUNDARYLINE_LINK*
  * *BOUNDARYLINE_POLY*
  * *BOUNDARYLINE_COLLECTIONS*
  * La couche *_POLY* a des liens vers des liens permettant les polygones 
    réels d'être formés (autrement les couches *_POLY* seulement on un point 
    nécessaire pour la géométrie). Les collections sont des collections de 
    polygones (également sans géométrie comme lu). C'est le seul produit à 
    partir duquel les polygones peuvent être construit.

* **BaseData.GB :**

  * *BASEDATA_POINT*
  * *BASEDATA_LINE*
  * *BASEDATA_TEXT*
  * *BASEDATA_NODE*

* **OSCAR Asset/Traffic :**

  * *OSCAR_POINT*
  * *OSCAR_LINE*
  * *OSCAR_NODE*

* **OSCAR Network :**

  * *OSCAR_NETWORK_POINT*
  * *OSCAR_NETWORK_LINE*
  * *OSCAR_NETWORK_NODE*

* **Address Point :**

  * *ADDRESS_POINT*

* **Code Point :**

  * *CODE_POINT*

* **Code Point Plus :** 

  * *CODE_POINT_PLUS*

Le jeu de données en entier possèdera également une couche *FEATURE_CLASSES* 
contenant une table vierge relatant les nombres *FEAT_CODE* avec les noms des 
classes d'objet (*FC_NAME*). Ceci s'applique à tous les produits dans le jeu de 
données. Quelques types de couche (tel que les produits *Code point* et *Address 
Point*) n'incluent pas de classes d'objet. Certain produits utilisent des 
classes d'objets qui ne sont pas définie dans le fichier, et ils n'apparaitront 
donc pas dans la couche *FEATURE_CLASSES*.

Schémas des produits
---------------------

L'approche entreprise pour ce lecteur est de traiter un fichier, ou un 
répertoire de fichier comme un simple jeu de données. Tous les fichiers dans le 
jeu de données sont scannés à l'ouverture. Pour chaque produit particulier (listé 
au dessus) un ensemble de couches est créé ; cependant ces couches peuvent être 
extraites de plusieurs fichiers du même produit.

Les couches sont basées sur un type d'objet de faible niveau dans le fichier NTF, 
mais contiendront généralement des objets de plusieurs codes d'objet (attribut 
*FEAT_CODE*). Différents objets dans une couche données peuvent avoir une variété 
d'attribut dans le fichier ; cependant le schéma est établit en fonction de 
l'union de tous les attributs possible des objets d'un type particulier (par 
exemple les points) de cette famille de produit (par exemple le réseau OSCAR).

Si un produit NTF lu ne correspondant pas à un des schéma connu il sera géré par 
un parseur générique différent qui gère  seulement des couches de type 
*GENERIC_POINT* et *GENERIC_LINE*. Seul l'objet aura un attribut *FEAT_CODE*.

Les détails sur quelles couches de quels produits ont quels attributs peuvent 
être trouvés dans la méthode *NTFFileReader::EstablishLayers()* à la fin du 
fichier *ntf_estlayers.cpp*. Ce fichier contient également tous les codes de 
traduction spécifique au produit.

Attributs spéciaux
-------------------

* **FEAT_CODE :** code générale entier de l'objet, peut être utilisé pour 
  rechercher un nom dans la table/couche *FEATURE_CLASSES*.
* **TEXT_ID/POINT_ID/LINE_ID/NAME_ID/COLL_ID/POLY_ID/GEOM_ID :** identifiant 
  unique pour un objet de type approprié.
* **TILE_REF :** Toutes ces couches (sauf *FEATURE_CLASSES*) contiennent un 
  attribut *TILE_REF* qui indique de quelle tuile (fichier) provient l'objet. 
  De manière générale les numéros d'id sont seulement unique dans la tuile et 
  dont *TILE_REF* peut être utilisé pour restreindre les liens des id dans les 
  objets du même fichier.
* **FONT/TEXT_HT/DIG_POSTN/ORIENT :** Des informations détaillées sur la 
  police, la hauteur du texte, la position de digitalisation, et l'orientation 
  du texte ou les noms des objets. Lisez le manuel du produit OS pour comprendre 
  les unités, la signification de ces codes.
* **GEOM_ID_OF_POINT :** 	Pour les objets *\_NODE* cela définie le 
  *POINT_ID* de l'objet de la couche ponctuelle auquel ce nœud correspond. De 
  manière générale les nœuds ne portent pas une géométrie eux-même. Le nœud doit 
  être lié à un point pour établir sa position.
* **GEOM_ID_OF_LINK :** une liste d'objet *_LINK* ou *_LINE* pour démarrer ou 
  finir à un nœud. Les nœuds et ce champ ont généralement seulement une valeur 
  lors de l'établissement de la connection des objets lignes pour l'analyse de 
  réseau. Notez que cela doit être lié à l'objet cible *GEOM_ID*, et pas à son 
  *LINE_ID*. Sur la couche *BOUNDARYLINE_POLY* cet attribut contient le 
  *GEOM_ID* des lignes qui forme un contour de polygone.
* **POLY_ID :** un liste de *POLY_ID* de la couche *BOUNDARYLINE_POLY* associée 
  avec une collection donnée dans la couche *BOUNDARYLINE_COLLECTIONS*.

Produits génériques
--------------------

Dans le cas où un fichier n'est pas identifier comme faisant partie d'un produit 
connus existant il sera traité d'une manière générique. Dans ce cas le jeu de 
donnés complet est scanné pour établir quels objets ont quels attributs. À cause 
de cela, ouvrir un jeu de données générique peut être beaucoup plus lent qu'ouvrir 
un jeu de données reconnus. En se basant sur ce scan une liste d'objet générique 
(couches) est définie à partir de l'ensemble suivant :
::
    
    GENERIC_POINT
    GENERIC_LINE
    GENERIC_NAME
    GENERIC_TEXT
    GENERIC_POLY
    GENERIC_NODE
    GENERIC_COLLECTION

Les produits génériques sont d'abord pris en charge par le module 
*ntf_generic.cpp* tandis que les produits spécifiques dans *ntf_estlayers.cpp*.

Parce qu'on a trouvé des produits de données (des jeux de données OSNI) ne 
provenant pas de l'*Ordnance Survey* ayant des groupes d'enregistrement  dans 
un ordre inhabituel comparé à ce que fait l'*Ordnance Survey* anglais, il a été 
nécessaire de mettre en cache tous les enregistrements des produits génériques 
de niveau 3 et au dessus, et de construire des groupes d'enregistrement par 
référence d'identifiant à partir de ce cache plutôt que de dépendre d'un ordre 
d'enregistrement pratique. Cela est accomplit par la capacité d'indexage de 
*NTFFileReader* quasiment à la fin du fichier *ntffilereader.cpp*. À cause de ce 
cache en mémoire Les jeux de données génériques qui accèdent à l'indexage peuvent 
demander plus de mémoire qu'accéder à des produits de données connus, bien qu'il 
ne soit pas nécessaire pour les produits générique de niveau 1 et 2.

Il est possible de forcer un produit connus pour qu'il soit traité comme 
générique en définissant l'option *FORCE_GENERIC* à *ON* en utilisant 
*OGRNTFDataSource::SetOptionsList()* comme il est indiqué dans le fichier 
*ntfdump.cpp*. Cela peut également être accomplit en dehors des applications 
*OGR* en définissant la variable d'environnement *OGR_NTF_OPTIONS* à 
"*FORCE_GENERIC=ON*".

.. yjacolin at free.fr, Yves Jacolin - 2009/02/25 (trunk 8437)