.. _`gdal.ogr.formats.htf`:

==================================
HTF - Hydrographic Transfer Format
==================================

(GDAL/OGR >= 1.8.0)

Ce pilote lit les fichiers contenant des sondages qui suivent le Format de Transfert 
Hydrographique (HTF), qui est utilisé par l'*Australian Hydrographic Office* (AHO).

Le pilote a été développé en se basant sur la spécification 2.02 HTF.

Le fichier doit être géoréférencé en UTM WGS84 pour être considéré valide par le 
pilote.

Le pilote renvoie deux couches spatiales : une couche nommée "polygon" et une 
couche nommée "sounding".

Il y a également une couche "cachée", nommée "metadata", qui peut être récupéré 
par *GetLayerByName()*, et qui contient une seule feature, composée de lignes 
d'en-tête du fichier.

Polygons sont utilisés pour distinguer les différentes catégories de surveillance, 
tels que n'importe quel changement significatif dans la précision de la 
position/profondeur ou/et un changement dans la couverture des fonds marins 
entraînera un contour de polygone séparé contenant des polygones.

La couche "polygon" contient les champs suivants :

* *DESCRIPTION* : définie les polygones de chaque région avec des critères de 
  surveillance ou de thème similaire.
* *IDENTIFIER* : identifiant unique du polygone pour cette transmission.
* *SEAFLOOR_COVERAGE* : toutes features de fond sous-marin significatif détecté 
  (ensonification complète / balayer) ou couverture complète non achevée et des 
  features non cartographiées peuvent exister.
* *POSITION_ACCURACY* : +/- NNN.n mètres à 95% CI (2.45) en fonction du datum donné.
* *DEPTH_ACCURACY* : +/- NN.n mètres à 95% CI (2.00) à des profondeurs critiques.

La couche "sondage" doit contenir - au minimum - les 20 champs suivants :

* *REJECTED_SOUNDING* : si 0 le sondage est valide ou si 1 le sondage a été 
  rejeté (flagged).
* *LINE_NAME* : nom/numéro de ligne de l'enquête comme identifiant unique au 
  sein de l'enquête.
* *FIX_NUMBER* : numéro séquentiel fixe du sondage, unique dans l'enquête.
* *UTC_DATE* : date UTC pour le sondage CCYYMMDD.
* *UTC_TIME* : temps UTC pour le sondage HHMMSS.ss.
* *LATITUDE* : latitude du sondage +/-NNN.nnnnnn (degrés d'arc, le sud est 
  négative).
* *LONGITUDE* : longitude du sondage +/-NNN.nnnnnn (degrés d'arc, l'est est 
  négative).
* *EASTING* : Grille de coordonnée de la position du sondage en mètres NNNNNNN.n.
* *NORTHING* : Grille de coordonnée de la position du sondage en mètres NNNNNNN.n.
* *DEPTH* : valeur sonore réduite en mètres avec des corrections appliquées comme 
  indiqué dans les champs concernés, les sondages sont positifs et les hauteurs 
  de séchage sont négatifs +/-NNNN.nn mètres.
* *POSITIONING_SENSOR* : indique le numéro du système de position rempli dans 
  l'enregistrement de l'en-tête du HTF.
* *DEPTH_SENSOR* : indique le numéro du système de sondage de la profondeur rempli 
  dans l'enregistrement de l'en-tête du HTF.
* *TPE_POSITION* : erreur Totale propagée de la composante horizontale de la sonde.
* *TPE_DEPTH* : erreur totale propagée de la composante verticale de la sonde.
* *NBA FLAG* : option *No Bottom at*, si 0 pas de profondeur NBA ou si 1 la 
  profondeur est NBA, des eaux plus profondeur existe probablement.
* *TIDE* : Valeur de la correction de la marée appliquée  +/- NN.nn mètres.
* *DEEP_WATER_CORRECTION* : valeur de la vitesse de sondage de l'eau profonde 
  appliquée +/- NN.nn mètres.
* *VERTICAL BIAS_CORRECTION* : valeur du biais vertical appliqué +/- NN.nn 
  mètres. eg correction de la profondeur du transducteur.
* *SOUND_VELOCITY* : vitesse du son mesurée utilisé pour traiter le sondage en 
  mètres par seconde IIII
* *PLOTTED_SOUNDING* : si 0 alors la profondeur réduite ne figurait pas sur le 
  fairsheet original ou si 1 alors la profondeur réduite est apparu sur le 
  fairsheet original.

Certains champs peuvent n'être jamais définie, en fonction de la valeur du champ 
de la Clé de Population du Champ. Les champs supplémentaires peuvent aussi être 
ajoutés.

Voir également
==============

* `Page principale du format HTF - Hydrographic Transfer Format <http://www.hydro.gov.au/tools/htf/htf.htm>`_
* `Spécification technique HTF <http://www.hydro.gov.au/tools/htf/htf.pdf>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/01 (trunk 20735)