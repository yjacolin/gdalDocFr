.. _`gdal.ogr.formats.idb`:

IDB
======

Ce pilote implémente la gestion de l'accès aux tables spatiales dans un 
Informix d'IBM étendue avec le module spatial DataBlade.

Lors de l'ouverture d'une base de données, son nom doit être définie sous la 
forme :
::
    
    "IDB:dbname={dbname} server={host} user={login} pass={pass} table={layertable}".

Le préfixe *IDB:* est utilisé pour marquer le nom comme une chaine de 
connection IDB.

Si la table *geometry_columns* existe, alors toutes les tables listées et les 
vues nommées seront traitées comme des couches OGR. Autrement toutes les tables 
attributaires seront traitées comme des couches.

Les tables attributaires (non spatiale) peuvent être accédées, et renverront des 
objets avec des attributs mais sans géométrie. Si la table a un champ "*st_\**", 
celui-ci sera traité comme un table spatiale. Le type du champ est analysé pour 
déterminer comment le lire.

Le pilote gère la détection automatique des FID.

Variables d'environnement
--------------------------

* **INFORMIXDIR :** il doit être définie au répertoire d'installation du SDK 
  client d'Informix
* **INFORMIXSERVER :** nom du serveur Informix par défaut
* **DB_LOCALE :** locale de la base de données d'Informix
* **CLIENT_LOCALE :** locale du client
* **IDB_OGR_FID :** définie le nom de la clé primaire au lieu de '*ogc_fid*'. 

Pour plus d'information sur les variables d'Informix lisez la documentation du 
SDK client d'Informix.

Exemple
--------

Cet exemple montre l'utilisation de ''ogrinfo'' pour lister les couches 
DataBlade d'Informix sur un hôte différent :
::
    
    ogrinfo -ro IDB:'server=demo_on user=informix dbname=frames'

.. yjacolin at free.fr, Yves Jacolin - 2009/02/25 22:23 (trunk 10402)