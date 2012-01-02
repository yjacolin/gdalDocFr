.. _`gdal.gdal.gdaladdo`:

gdaladdo
=========

Construit ou reconstruit les images d'aperçus.

**Usage :**
::
    
    gdaladdo [-r {nearest,average,gauss,cubic,average_mp,average_magphase,mode}]
         [-ro] [-clean] [--help-general] filename levels

Le programme ``gdaladdo`` peut être utilisé pour construire ou reconstruire les 
images d'aperçu pour la plupart des formats supportés avec un ou plusieurs 
algorithmes.

* **-r {nearest (default),average,gauss,cubic,average_mp,average_magphase,mode} :** 
  Sélectionne un algorithme de re-échantillonnage.
* **-ro :** (Disponible à partir de gdal 1.6.0) Ouvre le jeu de données en mode 
  lecture seul, dans le but de générer un aperçu externe (notamment pour les 
  GeoTIFF).
* **-clean :** (disponible à partir de GDAL 1.7.0) enlève les aperçues.
* **filename :** Le fichier pour lequel on veut construire les aperçus (ou dont 
  les aperçues doivent être enlevés).
* **levels :** Une liste de niveaux d'aperçu à construire. Ignoré avec l'option 
  *-clean*.

Le *mode* (disponible à partir de gdal 1.6.0) sélectionne la valeur de tous les 
points de l'échantillon qui apparaît le plus souvent. *average_mp* n'est pas 
utilisable. *Average_magphase* donne une moyenne des données complexes dans 
l'espace mag/phase. *Nearest* et *average* sont applicable aux données des 
images normales. *Nearest* applique un re-échantillonnage du plus proche voisin 
(échantillonnage simple), tandis que *average* calcul la moyenne de tous les 
pixels différents de NODATA. Le re-échantillonnage *Cubic* (disponible à partir 
de GDAL 1.7.0) applique un motif de convolution cubique approximativement de 
4x4. *Gauss resampling* (disponible à partir de gdal 1.6.0) applique une 
transformation de Gaussian avant le calcul de l'aperçu ce qui peut améliorer 
les résultats par rapport à une moyenne simple dans le cas des bords nets avec 
un fort contraste ou avec du bruit. Les valeurs des niveaux conseillés devraient 
être 2, 4, 8 ... afin qu'un ré-échantillonnage Guassien de 3x3 soit sélectionné.

``gdaladdo`` honorera correctement les tuples *NODATA_VALUES* (méta-donnée 
spéciale du jeu de données) afin que seul un triplet RGB donné (dans le cas 
d'une image RGB) sera considéré comme valeur *nodata* et pas chaque valeur du 
triplet indépendamment pour chaque bande.

La sélection d'une valeur de niveau 2 entraîne le calcul d'un niveau d'aperçu 
de la moitié de la résolution (pour chaque dimension) de la couche de base. Si 
le fichier possède des niveaux de résolution au niveau sélectionné, ces niveaux 
seront recalculés et écrits de nouveau.

Certains pilotes de format ne supportent pas les aperçus. Plusieurs pilotes de 
formats rangent les aperçus dans un fichier secondaire avec l'extension .ovr 
qui est en réalité un format tiff. Par défaut le pilote GeoTIFF range les 
aperçus à l'intérieure du fichier utilisé (s'il peut être écrasé), sauf si 
l'option ``-ro`` est définie.

La plupart des pilotes gère également un format d'aperçu alternatif en utilisant 
le format Erdas Imagine. Pour déclencher ceci, utilisez l'option de 
configuration *USE_RRD=YES*. Cela placera les aperçus dans un fichier .aux 
associé disponible pour une utilisation directe avec Imagine ou ArcGIS ainsi 
que les applications GDAL (par exemple --config USE_RRD YES).

Aperçus externes dans le format GeoTIFF
----------------------------------------

Les aperçus externes créés dans un format TIFF peuvent être compressés en 
utilisant l'option de configuration ``COMPREES_OVERVIEW``. Toutes les méthodes 
de compression, supportées par le pilote GeoTIFF, sont disponibles ici (par 
exemple ``--config COMPRESS_OVERVIEW DEFLATE)``. L'interprétation photométrique 
peut être définie avec ``--config PHOTOMETRIC_OVERVIEW {RGB,YCBCR,...} ``, et 
l'entrelacement avec ``--config INTERLEAVE_OVERVIEW {PIXEL|BAND}``.

Pour les aperçus externes compressés en JPEG, la qualité JPEG peut être définie 
avec "--config JPEG_QUALITY_OVERVIEW value" (GDAL 1.7.0 ou plus récent).

Pour les aperçus externes compressés en LZW ou DEFLATE, la valeur prédite peut 
être définie avec "--config PREDICTOR_OVERVIEW 1|2|3" (GDAL 1.8.0 ou plus 
récent).

Pour produire des aperçus en JPEG dans TIFF le plus petit possible, vous devez 
utiliser :
::
    
    --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL

À partir de GDAL 1.7.0, les aperçues externes peuvent être créé au format 
BigTIFF en utilisant l'option de configuration ``BIGTIFF_OVERVIEW`` : 
``--config BIGTIFF_OVERVIEW {IF_NEEDED|IF_SAFER|YES|NO}``. La valeur par défaut 
est ``IF_NEEDED``. Le comportement de cette option est exactement le même que 
l'option de création ``BIGTIFF`` documentée dans la documentation du pilote 
:ref:`gdal.gdal.formats.gtiff`.

* YES force BigTIFF.
* NO force des TIFF classiques.
* IF_NEEDED créera seulement un BigTIFF si cela est clairement nécessaire (non 
  compressé, et des aperçues plus grande que 4Go).
* IF_SAFER créera un BigTIFF si le fichier résultant *pourrait* excéder 4Go.

Voyez la documentation du pilote GeoTIFF pour des explications supplémentaires 
sur toutes ces options.

**Exemple :**

Créer des aperçus, inclus dans le fichier TIFF fournit :
::
    
    gdaladdo -r average abc.tif 2 4 8 16

Créer un fichier d'aperçu externe en GeoTIFF compressé à partir du fichier ERDAS .IMG :
::
    
    gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE erdas.img 2 4 8 16

Créer un fichier d'aperçu du GeoTIFF compressé en JPEG à partir d'un jeu de 
données RVB à 3 bandes (si le jeu de données est un GeoTiff que l'on peut écrire, 
Vous avez également besoin d'ajouter l'option *-ro* pour forcer la génération des 
aperçues externes) :
::
    
    gdaladdo --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR
         --config INTERLEAVE_OVERVIEW PIXEL rgb_dataset.ext 2 4 8 16

Créer des aperçus au format Erdas Imagine pour le fichier JPEG indiqué :
::
    
    gdaladdo --config USE_RRD YES airphoto.jpg 3 9 27 81

.. yjacolin at free.fr, Yves Jacolin - 2010/12/27 18:20* (http://gdal.org/gdaladdo.html Trunk 21320)
