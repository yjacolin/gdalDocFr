.. _`gdal.gdal.formats.USGSDEM`:

USGSDEM -- USGS ASCII DEM (et CDED)
====================================

GDAL inclut la gestion de la lecture des fichiers USGS ASCII DEM. C'est le 
format traditionnel utilisé par l'USGS avant d'être remplacé par le SDTS, et 
est le format utilisé pour les données CDED DEM du Canada. La plupart des 
variations populaires sur les fichiers USGS DEM doivent être géré, en incluant 
la reconnaissance correcte des systèmes de coordonnée et le géoréférencement.
Les fichiers DEM de l'USGS de 7,5 minutes (grille UTM) ont généralement des 
zones de données manquante près des bords, et ceux-ci sont proprement noté avec 
des valeurs *nodata*. Les valeurs d'élévation dans les fichiers DEM de l'USGS 
peuvent être en mètre ou en pied, et cela sera indiqué par la valeur retour de 
``GDALRasterBand::GetUnitType()`` (soit "m" soit "ft").

Notez que les fichiers DEM de l'USGS sont représentés par une seule tuile. Cela 
peut induire des problèmes de cache si la taille du cache des tuiles de GDAL est 
petite. Il en résultera également un délai substantiel lorsque le premier pixel 
est lu tandis que le fichier entier sera importé.

Une partie de code pour implémenter ce format est dérivé du code de VTP par Ben 
Discoe. Voyez le projet Virtual Terrain (http://www.vterrain.org/) pour plus 
d'information sur VTP.

Problèmes de création
---------------------

GDAL gère l'export des fichiers de données DEM de l'USGS  et CDED en 
géographique (et UTM), ainsi que la possibilité de générer des produits CDED 
2.0 50K selon les spécifications du gouvernement fédéral Canadien.

Les données en entrées doivent déjà être échantillonné dans un système de 
coordonnées UTM ou en coordonnées géographiques. Par défaut la zone entière du 
fichier d'entrée sera exportée, mais pour les produits CDED50K le fichier créé 
sera échantillonné à la résolution définie à la production et dans les limites 
des tuiles du produit.

Si le fichier en entré a des informations définies appropriées sur le système 
de coordonnée, l'export vers des formats de produit spécifique peut prend une 
entrée dans différents systèmes de coordonnées (c'est à dire projection Albers 
vers géographique NAD83 pour la production CDED 50K).

**Options de création :**

* **PRODUCT=DEFAULT/CDED50K :** quand CDED50K est sélectionné, le fichier de 
  sortie sera obligé d'adhérer aux spécifications CDED 50K. La sortie aura 
  toujours une taille de 1201x1201 et généralement une tuile de 15 minute par 
  15 minute (bien que plus large dans les longitudes dans les zones plus au 
  nord).
* **TOPLEFT=long,lat :** pour les produits CDED50K, cela est utilisé pour 
  définir le coin en haut à  gauche de la tuile à générer. Il doit être sur une 
  limite de 15 minutes et peut être donnée en degrés décimal ou en degrés et 
  minutes (par exemple ``TOPLEFT=117d15w,52d30n``). 
* **RESAMPLE=Nearest/Bilinear/Cubic/CubicSpline :** définie le noyau 
  d'échantillonnage utilisé pour échantillonner les données à la grille cible. 
  A un effet seulement lorsque un produit particulier comme CDED50K est produit. 
  *Bilinear* par défaut.
* **DEMLevelCode=integer :** niveau DEM (1, 2 ou 3 si définie). 1 par défaut.
* **DataSpecVersion=integer :** version/révision données et spécification (par 
  exemple. 1020)
* **PRODUCER=text :** jusqu'à 60 caractères peuvent être placé dans le champ 
  producteur du fichier généré.
* **OriginCode=text :** jusqu'à 4 caractères peuvent être placé dans le champ 
  code d'origine du fichier généré (YT pour Yukon).
* **ProcessCode=code :** Un seul caractère peut être placé dans le champ code 
  du processus du fichier généré (8=ANUDEM, 9=FME, A=TopoGrid).
* **TEMPLATE=filename :** pour n'importe quel fichier de sortie, un ficher 
  modèle peut être définie. Un certain nombre de champ (Data Producer inclut) 
  sera copié du fichier modèle s'il est fournit, et sera sinon laissé vide.
* **ZRESOLUTION=float :** les MNT stockent les informations d'élévation sous 
  forme d'entier positif, et ces entiers sont échelonné en utilisant la 
  « résolution z ». Par défaut, cette résolution est de 1.http:\*0. Cependant, 
  vous pouvez définir ici une résolution différente, si vous voulez que vos 
  entiers soient échantillonnés dans des points flottants.
* **NTS=name :** nom du Mapsheet NTS, utilisé pour dériver TOPLEFT. A seulement 
  un effet lorsque les produits particulier  comme CDED50K ont été produit.
* **INTERNALNAME=name :** nom du jeu de données écrit dans l'en-tête du 
  fichier. A seulement un effet quand des produits particulier comme CDED50K ont 
  été produit.

**Exemple :** La commande suivante générera un tuile simple CDED50K, en 
extrayant d'une couverture plus large du MNT yk_3arcsec pour une tuile avec 
un coin en haut à gauche à -117w,60n. Le fichier  *yk_template.dem* est utilisé 
pour définir des champs du produit incluant les champs Producteur de Données 
(Data Producter), Code du Processus et Code d'Origine.
::
    
    gdal_translate -of USGSDEM -co PRODUCT=CDED50K -co TEMPLATE=yk_template.dem \
               -co TOPLEFT=-117w,60n yk_3arcsec 031a01_e.dem

.. note::
    implémenté dans *gdal/frmts/usgsdem/usgsdemdataset.cpp*.

Le code de lecture des MNT de l'USGS dans GDAL est dérivé de l'importateur du 
logiciel VTP (http://www.vterrain.org/). Les possibilité d'export a été 
développé avec l'aide financière du *Yukon Department of Environment*.

.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 21:56 (trunk 14519)