.. _`gdal.ogr.formats.edigeo`:

========
EDIGEO
========

(GDAL/OGR >= 1.9.0)

Ce pilote lit les fichiers encodés dans le format d'échange français EDIGEO, un 
format de fichier texte dont l'objectif est l'échange d'informations géographiques 
entre SIG, avec de puissantes possibilité de description, modélisation 
topologique, etc.

Le pilote a été développé pour lire les fichiers du PCI (Plan Cadastral 
Informatisé) français produit par la DGI (Direction Générale des Impôts). Le 
pilote doit pouvoir aussi être capable d'ouvrir d'autres produits basé sur la 
norme EDIGEO.

Le fichier .THF décrivant l'échange EDIGEO doit être fournie au pilote et celui-ci 
lira les fichiers .DIC, .GEO, .SCD, .QAL and .VEC  associés.

Dans l'objectif de définir correctement la projection des couches, le fichier 
IGNF qui contient la définition des SRS IGN doit être placé dans le répertoire des 
fichiers ressources PROJ.4.

L'ensemble des fichiers sera parsé en mémoire. Cela peut être une limitation s'il 
faut gérer un gros échange de fichier EDIGEO.

.. <!-- Default to YES.
.. If you define the configuration option / environment variable OGR_EDIGEO_SORT_FOR_QGIS to YES,
.. the layers of the French PCI will be ordered such as they overlay nicely when opened from QGIS.
.. -->

Étiquettes
============

Pour les fichiers PCI d'EDIGEO, les étiquettes sont contenu dans la couche 
ID_S_OBJ_Z_1_2_2. OGR exportera les styles en suivant la 
`spécification des styles des features d'OGR <http://gdal.org/ogr/ogr_feature_style.html>`_.

Il ajoutera également les champs suivants :

* **OGR_OBJ_LNK :** l'id du projet qui est lié à cette étiquette ;
* **OBJ_OBJ_LNK_LAYER :** le nom de la couche de l'objet lié ;
* **OGR_ATR_VAL :** la valeur de l'attribut à afficher (trouvé dans l'attribut 
  ATR de l'objet *OGR_OBJ_LNK*) ;
* **OGR_ANGLE :** l'angle de rotation en degré (0 = horizontal, orienté dans le 
  sens inverse des aiguilles d'une montre) ;
* **OGR_FONT_SIZE :** la valeur de l'attribut HEI multiplié par la valeur de 
  l'option de configuration *OGR_EDIGEO_FONT_SIZE_FACTOR* dont la valeur par 
  défaut est 2.

Combinés avec les attributs FON (font family), ils peuvent être utilisé pour 
définir le style dans QGIS par exemple.

Par défaut, OGR créera des couches spécifiques (xxx_LABEL) pour expédier en 
différente couche ID_S_OBJ_Z_1_2_2 en fonction de la valeur de 
xxx=OBJ_OBJ_LNK_LAYER. Cela peut être désactivé en définissant 
*OGR_EDIGEO_CREATE_LABEL_LAYERS* à NO.

.. seealso::

*  `Introduction au standard EDIGEO <http://georezo.net/wiki/main/donnees/edigeo>`_ (en Français)
*  `Standard EDIGEO - AFNOR NF Z 52000 <http://georezo.net/wiki/_media/main/geomatique/norme_edigeo.zip>`_ (en Français)
*  `Standard d'échange des objets du PCI selon la norme EDIGEO <href="http://www.craig.fr/contenu/resources/dossiers/pci/pdf/EDIGeO_PCI.pdf>`_ (en Français)
*  `Page principale du Cadastre français <http://www.cadastre.gouv.fr>`_ (en Français)
*  `Description du module EDIGEO dans Geotools <http://docs.codehaus.org/pages/viewpage.action?pageId=77692976>`_ (en anglais)
*  `Échantillon de données EDIGEO <http://svn.geotools.org/trunk/modules/unsupported/edigeo/src/test/resources/org/geotools/data/edigeo/test-data/>`_

.. yjacolin at free.fr, Yves Jacolin - 2014/11/30 (trunk 28039)