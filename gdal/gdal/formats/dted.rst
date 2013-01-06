.. _`gdal.gdal.formats.dted`:

================================
DTED -- Military Elevation Data
================================

GDAL gère les données d'élévation DTED de niveau 0, 1 et 2 en accès en lecture. 
Les données d'élévation sont retournées comme des entiers signés sur 16 bits. 
Une projection appropriée (toujours WGS84) et des informations de géo-référencement 
sont également retourné. Une diversité de champs d'en-tête sont renvoyé comme 
méta-données de niveau du jeu de données.

Problèmes de lecture
=====================

Vitesse de lecture
******************

Les données d'élévation dans les fichiers DTED sont organisé par colonne. Cette 
organisation des données ne fonctionne pas très bien avec les algorithmes de 
scan par ligne et peut causer des ralentissements, spécialement pour les jeux de 
données DTED de niveau 2. En définissant *GDAL_DTED_SINGLE_BLOCK=TRUE*, un 
jeu de données DTED complet sera considéré comme un bloc simple. Le premier 
accès au fichier sera lente, mais un nouvel accès sera beaucoup plus rapide. 
Utiliser seulement cette option si vous avez besoin de réaliser un calcul sur 
le fichier complet.

Problèmes de géoréférencement
******************************

La spécification DTED (`MIL-PRF-89020B <http://www.nga.mil/ast/fm/acq/89020B.pdf>`_) 
affirme que le datum horizontal doit être le système Géodésique Mondiale (World 
Geodetic System, WGS 84). Cependant, il y a encore des gens pour utiliser 
d'ancien fichier de données géoréférencé en WGS 72. Un champ d'en-tête indique 
le code du datum horizontal, nous pouvons donc détecter et prendre en compte cette 
situation.

* si le datum horizontal définie dans le fichier DTED est le WGS 84 le pilote 
  DTED représentera le WGS 84 comme SRS ;
* si le datum horizontal définie dans le fichier DTED est le WGS 72, le pilote 
  DTED représentera le WGS 72 comme SRS et retrounera  un problème.
* si le datum horizontal définie dans le fichier DTED est ni le WGS 84 ni le 
  WGS 72, le pilote DTED représentera le WGS 84 comme SRS et enverra un message 
  d'erreur.


Problèmes de checksum
**********************

le comportement par défaut du pilote DTED est d'ignorer le checksum lors de la 
lecture des données à parti du fichier. Cependant, vous pouvez définir la 
variable d'environnement DTED_VERIFY_CHECKSUM=YES si vous voulez que le checksum 
soit vérifié. Dans certain cas, le checksum écrit dans le fichier DTED est 
incorrecte (le producteur de données a mal fait son travail). Cela sera retourné 
comme un message important. Si le checksum écrit dans le fichier DTED et le 
checksum calculé à partir des données ne correspond pas, une erreur sera 
retournée.

Problèmes lors de la création
==============================

Le pilote DTED doit gérer les nouveaux fichiers, mais les données en entrée 
doivent être formaté exactement comme une cellule de niveau 0, 1 ou 2. C'est à 
dire que la taille et les limites doivent être appropriées pour la cellule.

.. seealso::

* Implémenté dans *gdal/frmts/dted/dteddataset.cpp*.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/22 19:33 (trunk 14661)