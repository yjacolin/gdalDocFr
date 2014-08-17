.. _`gdal.ogr.formats.gft`:

===========================
GFT - Google Fusion Tables
===========================

(GDAL/OGR >= 1.9.0)

Ce pilote peut se connecter au service Google Fusion Tables. GDAL/OGR doit être 
compilé avec la gestion de Curl pour que le pilote GFT soit compilé.

Le pilote gère la lecture et l'écriture des opérations.

Syntaxe des noms des jeux de données
=====================================

La syntaxe minimale pour ouvrir une source de données GFT est : ``GFT:``

Des paramètres supplémentaires optionnels peuvent être définie après le signe 
':' comme :

* **tables=table_id1[,table_id2] :** une liste des ID des tables. Cela est nécessaire 
  lorsque vous devez accéder aux tables publiques.
  Si vous voulez l'ID d'une table publique, où n'importe quelle table qui n'appartient 
  pas à l'utilisateur authentifié, vous devez allez voir la table dans le site 
  Google Fusion Tables et noter le numéro à la fin de l'URL.
* **protocol=https :** pour utiliser le protocole HTTPS pour toutes les opérations. 
  HTTP est utilisé par défaut sauf pour les opérations d'authentification où 
  HTTPS est toujours utilisé.
* **auth=auth_key :** une clé d'authentification comme décrit ci-dessous.
* **access_token=access_token :** un token d'authentification comme décrit plus bas.
* **access=access_token :** un token d'accès comme décrit plus bas.
* **refresh=refresh_token :** un token de rafraichissement comme décrit plus bas.

Si plusieurs paramètres sont définie, ils doivent être séparés par un espace.

Authentification
=================

La plupart des opérations, en particulier celles pour écrire, nécessite un compte 
Google valide pour fournir les informations d'authentification au pilote. La seule 
exception est l'accès en lecture seule des tables publiques.

Afin de créer une clé d'autorisation, il est nécessaire de se `loguer et d'autoriser  <http://www.google.com/url?q=https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%3Fscope%3Dhttps%253A%252F%252Fwww.googleapis.com%252Fauth%252Ffusiontables%26state%3D%252Fprofile%26redirect_uri%3Durn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob%26response_type%3Dcode%26client_id%3D265656308688.apps.googleusercontent.com>`_
l'accès aux tables fusion pour un compte google (ie. gmail). La clé d'autorisation 
résultante peut être transformée en un jeton de rafraichissement à utiliser avec le 
script gdal/swig/python/scripts/gdal_auth.py d'OGR distribué avec GDAL (GDAL/OGR 
>= 1.10.0). Notez que les jetons peuvnet être seulement utilisé une fois tandis 
que le jeton de rafraichissement dure indéfiniment.

::
  
  gdal_auth.py auth2refresh auth_token

Ce token de rafraichissement peut être soit définie comme option de configuration 
(GFT_REFRESH_TOKEN) soit inclus dans la chaine de connection 
(ie. GFT:refresh=*refresh_token*).

En général les droits OAuth2 peuvent être fournie via ces mécanismes :

* En spécifiant un *access token* via la variable de configuration ``GFT_ACCESS_TOKEN``.
* En spécifiant un *access token* via la clause ``access=`` dans la chaine de connection GFT:.
* En spécifiant un *refresh token* via la variable de configuration ``GFT_REFRESH_TOKEN``.
* En spécifiant un *refresh token* via la clause ``refresh=`` dans la chaine de connection GFT:.
* En spécifiant un *auth key* via la variable de configuration ``GFT_AUTH``.
* En spécifiant un *auth key* via la clause ``auth=`` dans la chaine de connection GFT:.

Géométrie
==========

Les géométries dans les tables GFT doivent être exprimées dans la projection 
géodésique WGS84. GFT autorise qu'elle soit encodées sous différentes formes :

* une seule colonne avec une chaîne "lat lon" ou "lat,lon", où lat et lon sont 
  exprimées en degré décimal.
* un seule colonne avec une chaîne KML qui est la représentation d'un Point, une 
  LineString ou un Polygon.
* deux colonnes, une avec la latitude et l'autre avec la longitude, toutes deux 
  exprimées en degré décimal.
* une seule colonne avec une adresse connu par le service de géocodage de Google 
  Maps.

Seul les trois premiers types sont géré par OGR, pas le dernier.

Fusion tables peut avoir plusieurs colonnes géométriques par table. Par défaut, 
OGR utilisera la première colonne géométrique qu'il trouvera. Il est possible de 
sélectionner une autre colonne comme colonne géométrique en spécifiant 
*table_name(geometry_column_name)* comme nom de couche envoyé à *GetLayerByName().*

Filtre
========

Le pilote fera parvenir n'importe quel filtre spatial définie avec 
*SetSpatialFilter()* au serveur. Il fera de même pour les filtres attributaires 
définie via *SetAttributeFilter()*.

Pagination
===========

Les features sont récupérées à partir du serveur par tranche de 500 par défaut. 
Ce nombre peut être modifié avec l'option de configuration *GFT_PAGE_SIZE*.

Gestion de l'écriture
======================

La création et la suppression de table est possible. Notez que les champs ne 
peuvent qu'être ajouté à une table dans laquelle il n'y a pas de feature encore 
créé.

La gestion en écriture est seulement activée lorsque la source de données est 
ouverte en mode update.

La correspondance entre les opérations du service GFT et les concepts OGR est la 
suivante :

* OGRFeature::CreateFeature() <==> INSERT operation
* OGRFeature::SetFeature() <==> UPDATE operation
* OGRFeature::DeleteFeature() <==> DELETE operation
* OGRDataSource::CreateLayer() <==> CREATE TABLE operation
* OGRDataSource::DeleteLayer() <==> DROP TABLE operation

Lors de l'insertion d'une nouvelle feature avec *CreateFeature()*, et si la 
commande est réussie, OGR récupérera le rowid renvoyé et l'utilisera comme FID. 
OGR reprojetera automatiquement ses géométries dans la projection géodésique 
WGS84 si nécessaire (si la projection originale est liée à la géométrie).

Gestion de l'écriture et transactions OGR
==========================================

Les opérations ci-dessus sont par défaut déclenchées vers le serveur synchrone 
avec l'appel à l'API d'OGR. Cela peut cependant causer des problèmes de 
performances lors de l'envoie de plusieurs commandes dû à de nombreux échanges 
client/serveur.

Il est possible d'encapsuler l'opération *CreateFeature()* entre 
*OGRLayer::StartTransaction()* et *OGRLayer::CommitTransaction()*. Les opérations 
seront stockées en mémoire et seulement exécutées lors de l'appel de 
*CommitTransaction()*. Notez que le service GFT gère seulement jusqu'à 500 
INSERTs et jusqu'à 1 Mo de contenu par transaction.

.. note::
    Seule *CreateFeature()* active l'utilisation du mécanisme des transactions 
    OGR. *SetFeature()* et *DeleteFeature()* seront toujours déclenchés 
    immédiatement.

SQL
====

Les commandes SQL envoyées aux appels *OGRDataSource::ExecuteSQL()* sont exécutées 
côté serveur, sauf si le dialecte OGRSQL est définie. Le sous ensemble de SQL 
géré par le service GFT est décrit dans le lien à la fin de cette page.

Le SQL géré par le serveur comprend seulement les id des tables et pas les noms 
des tables renvoyés par OGR. Pour convenance, cependant OGR modifiera vos 
commandes SQL pour remplacer le nom de la table par son id.

Exemples
=========

* Lister les tables et les vues de l'utilisateur authentifié :
  ::
    
    ogrinfo -ro "GFT:email=john.doe@example.com password=secret_password"

* Créer et peupler une table à partir d'un shapefile :
  ::
    
    ogr2ogr -f GFT "GFT:email=john.doe@example.com password=secret_password" shapefile.shp

* Afficher le contenu d'une table publique avec des filtres attributaires et 
  spatiaux :
  ::
    
    ogrinfo -ro "GFT:tables=224453" -al -spat 67 31.5 67.5 32 -where "'Attack on' = 'ENEMY'"

* Obtenir la clé d'authentification :
  ::
    
    ogrinfo --config CPL_DEBUG ON "GFT:email=john.doe@example.com password=secret_password"

  renvoie :
  ::
    
    HTTP: Fetch(https://www.google.com/accounts/ClientLogin)
    HTTP: These HTTP headers were set: Content-Type: application/x-www-form-urlencoded
    GFT: Auth key : A_HUGE_STRING_WITH_ALPHANUMERIC_AND_SPECIAL_CHARACTERS

  Maintenant vous pouvez définir la variable d'environnement GFT_AUTH à cette 
  valeur et utiliser simplement "GFT:" comme DSN.

.. seealso::

  * `Guide du développeur de Google Fusion Tables <http://code.google.com/intl/fr/apis/fusiontables/docs/developers_guide.html>`_
  * `Référence des développeurs de Google Fusion Tables <http://code.google.com/intl/fr/apis/fusiontables/docs/developers_reference.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/05/01 (trunk 25705)