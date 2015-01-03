.. _`gdal.gdal.formats.l1b`:

===================================================
L1B -- NOAA Polar Orbiter Level 1b Data Set (AVHRR)
===================================================

GDAL gère le format  NOAA Polar Orbiter Level 1b Data Set en lecture. Il peut 
lire maintenant les jeux de données NOAA-9(F) --- NOAA-17(M). Remarque : seul 
ces instruments AVHRR sont gérés pour l'instant, si vous désirez lire des 
données provenant d'autres instruments écrivez moi (Andrey Kiselev, 
dron@ak4719.spb.edu).  AVHRR LAC/HRPT (résolution de 1 km) et GAC (résolution 
de 4 km)  devraient être traité correctement.

Géo-référencement
==================

Notez que le modèle de géoréférencement par affine simple de GDAL est 
complètement inutilisable pour les données NOAA. Vous ne devez pas le relier. 
Il est recommandé d'utiliser le *wrapper thin plane spline* (tps). La 
rectification automatique d'image peut être réalisé avec des points d'amer (GCP 
en anglais) à partir du fichier d'entrée. Le format NOAA range 51 points d'amer 
par ligne scannée à la fois dans les jeux de données LAC et GAC. En fait, vous 
pouvez avoir moins de 51 points d'amer, spécialement à la fin des lignes 
scannées. Une autre approche pour la rectification est la sélection manuelle 
des points d'amer en utilisant des sources externes d'information de 
géoréférencement.

Avant GDAL 1.10.2, un maximum de 11 x 20 points d'amer étaient reporté. Cela peut 
être inapproprié pour une transformation correcte. À partir de GDAL 1.10.2, une 
plus haute densité sera reportée à moins que l'option de configuration 
*L1B_HIGH_GCP_DENSITY* soit définie à *NO*.

La précision de la détermination des points d'amer dépend du type de satellite. 
Dans les jeux de données NOAA-9 – NOAA-14 les coordonnées géographiques des 
points d'amer sont rangés sous la forme de valeur entière eau 128 :sup:`ème` de degré. 
Nous ne pouvions pas déterminer les positions plus précisément que 1/28 = 
0,0078125 de NOAA-15 – NOAA-17 nous avons beaucoup plus de position précise, 
ceux-ci sont rangés sous forme de 10 000 :sup:`ème` de degré.

.. versionaddedd:: 1.11, Les points d'amers seront reportés comme un 
   `tableau de geolocation <http://trac.osgeo.org/gdal/wiki/rfc4_geolocate>`_, 
   avec une interpolation de Lagrangian de 51 point d'amers par ligne de scan au 
   nombre de pixels par largeur de ligne de scan.

Les images seront toujours retournées avec la ligne scannée la plus au nord 
localisée en haut de l'image. Si vous désirez déterminer la direction réelle du 
déplacement du satellite vous devez regarder la méta-données LOCATION.

Données
========

Dans le cas du NOAA-10 dans le canal 5 vous obtiendrez la répétition du canal 4 
des données. Les instruments AVHRR/3 (NOAA-15 – NOAA-17) est un radiomètre à six 
canaux, mais seulement cinq canaux sont transmis au sol à n'importe quel moment. 
Les canaux 3A et 3B ne peuvent pas être utilisé au même moment. Regardez le 
champ description du canal  reporté par ``gdalinfo`` pour déterminer quel sorte 
de canal est contenu dans le fichier de traitement.

Méta-données
=============

Plusieurs paramètres, obtenu à partir du jeu de données sont rangés comme 
enregistrement de méta-données.

Les enregistrements des méta-données :

* **SATELLITE :** nom du satellite
* **DATA_TYPE :** type de la donnée, rangée dans le niveau 1b du jeu de données 
  (AVHRR HRPT/LAC/GAC). 
* **REVOLUTION :** numéro de l'orbite. Notez que cela peut être décalé d'un ou 
  de deux numéro de l'orbite correcte (selon la documentation).
* **SOURCE :** nom de la station réceptrice.
* **PROCESSING_CENTER :** nom du centre de traitement de la données.
* **START :** heure du début de l'acquisition de la ligne scannée (année, 
  jour de l'année, milliseconde du jour).
* **STOP :** heure de la fin de l'acquisition de la ligne scannée (année, 
  jour de l'année, milliseconde du jour).
* **LOCATION :** indication de la localisation par rapport à la terre de 
  l'AVHRR (AVHRR Earth location indication). Ce sera soit *Ascending* quand 
  le satellite se déplace des faibles latitudes vers les hautes latitudes, et 
  *Descending* pour les autres cas.

.. versionaddedd:: 1.11, la plupart des enregistrements des métadonnées peuvent 
  être écrite dans un fichier .CSV quand l'option de configuration 
  *L1B_FETCH_METADATA* est définie à *YES*. Par défaut, le nom du fichier sera 
  nommé "[l1b_dataset_name]_metadata.csv", et localisé dans le même répertoire 
  que le jeu de données L1B. En définissant l'option de configuration 
  *L1B_METADATA_DIRECTORY*, il est possible de créer ce fichier dans un autre 
  répertoire. La documentation pour interpréter ces métadonnées est 
  `PODUG 3.1 <http://www.ncdc.noaa.gov/oa/pod-guide/ncdc/docs/podug/html/c3/sec3-1.htm>`_ 
  pour NOAA <=14 et `KLM 8.3.1.3.3.1 <http://www.ncdc.noaa.gov/oa/pod-guide/ncdc/docs/klm/html/c8/sec83133-1.htm>`_
  pour NOAA >=15.

Sous jeu de données
====================

(à partir de GDAL 1.11)

Les jeux de données NOAA <=14 préviennent les sous jeux de données 
L1B_SOLAR_ZENITH_ANGLES:"l1b_dataset_name" qui contiennent un maximum de 51 
angles zénithaux solaires pour chaque ligne de scan (en partant d'un échantillon 
de 5 avec un saut de 8 échantillons pour les données GAC, en partant d'un 
échantillon de 25 avec un daute de 40 échantillons pour les données 
HRPT/LAC/FRAC).

Les jeux de données NOAA >=15 préviennent les sous jeux de données
L1B_ANGLES:"l1b_dataset_name" qui contiennent 3 bandes (angles zénithaux 
solaires, angles zénithaux satellitaux et angles azimuth relatif) avec 51 valeurs 
pour chaque ligne de scan (en partant d'un échantillon de 5 avec un saut de 8 
échantillons pour les données GAC, en partant d'un échantillon de 25 avec un saut 
de 40 échantillons pour les données HRPT/LAC/FRAC).

Les jeux de données NOAA >=15 préviennent les sous jeux de données 
L1B_CLOUDS:"l1b_dataset_name" qui contiennent une bande de même dimension que les 
bandes du principal jeu de données L1B. Les valeurs de chaque pixel sont 0 = 
inconnus ; 1 = clair; 2 = nuageux ; 3 = partiellement nuageux.

Masque Nodata
==============

(à partir de GDAL 2.0)

Les jeux de données NOAA >=15 qui retourne dans leur en-tête qu'ils ont des 
lignes de scan manquantes exposera une bande de masque par jeu de données (selon 
`RFC 15 : Masques de bande <https://trac.osgeo.org/gdal/wiki/rfc15_nodatabitmask>`_) 
pour indiquer de telles lignes de scan.

.. seealso::

  * Implémenté dans gdal/frmts/l1b/l1bdataset.cpp.
  * NOAA Polar Orbiter Level 1b Data Set est documenté dans ``POD User's Guide`` 
    (TIROS-N -- NOAA-14 satellites) et dans ``NOAA KLM User's Guide`` (NOAA-15 -- 
    NOAA-16 satellites). Vous pouvez trouver ces manuels sur la page 
    d'introduction de la documentation technique de laNOAA : 
    http://www2.ncdc.noaa.gov/docs/intro.htm
  * un excellent et complet rapport est contenu dans le livre imprimé 
    ``The Advanced Very High Resolution Radiometer (AVHRR)`` par Arthur P. 
    Cracknell, Taylor et Francis Ltd., 1997, ISBN 0-7484-0209-8. 
  * des données NOAA peuvent être téléchargées à partir du site  Comprehensive 
    Large Array-data Stewardship System (CLASS) : http://www.class.noaa.gov/ 
    (anciennement SAA). En réalité ce sont  des jeux de données de niveau 1B 
    selon l'auteur du pilote, son implémentation a été testé seulement avec ces 
    fichiers.
  * page de statuts des brouillons de la NOAA : http://www.oso.noaa.gov/poesstatus/
  * http://www.lizardtech.com/


.. yjacolin at free.fr, Yves Jacolin - 2014/09/11 (trunk 27663)