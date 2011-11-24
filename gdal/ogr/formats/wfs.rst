.. _`gdal.ogr.formats.wfs`:

======================
WFS - Service WFS OGC
======================

(GDAL/OGR >= 1.8.0)

Ce pilote peut se connecter à un service WFS de l'OGC. Il gère les protocoles WFS 
1.0.0 et WFS 1.1.0. GDAL/OGR doit être compilé avec la gestion de Curl dans le but 
de compiler le pilote WFS. Habituellement les requêtes WFS renvoie les résultats 
au format GML, le pilote GML doit donc généralement être définie pour la gestion 
de la lecture (nécessite donc que GDAL/OGR soit compilé avec la gestion de Xerces 
ou Expat). Il est parfois possible d'utiliser un formats sous-jascent quand le 
serveur les gère (tel que OUTPUTFORMAT=json).

Le pilote gère les services en lecture seul, ainsi que ceux en mode 
Transactionnel (WFS-T).

Syntaxe des noms de jeux de données
====================================

La syntaxe minimale pour ouvrir une source de données WFS est : 
*WFS:http://path/to/WFS/service* ou *http://path/to/WFS/service?SERVICE=WFS*

Des paramètres optionnels additionnels peuvent être définie tels que *TYPENAME*, 
*VERSION*, *MAXFEATURES* comme spécifié dans la spécification WFS.

Il est également possible de définir le nom d'un fichier XML dont le contenu 
correspond à la syntaxe suivante (l'élément <OGRWFSDataSource> doit être le premier 
octet du fichier) :
::
    
    <OGRWFSDataSource>
        <URL>http://path/to/WFS/service[?OPTIONAL_PARAMETER1=VALUE[&amp;OPTIONNAL_PARAMETER2=VALUE]]</URL>
    </OGRWFSDataSource>

À la première ouverture, le contenu du résultat de la requête *GetCapabilities* sera ajouté au fichier, 
afin de mettre en cache pour une ouverture ultérieure du jeu de données. La même chose 
s'applique pour la requête *DescribeFeatureType* réalisée pour découvrir la définition des champs 
de chaque couche.

Le fichier de description de service possède les éléments additionnels suivants 
comme enfant immédiat de l'élément ``OGRWFSDataSource`` qui peuvent être définie 
en option.

* **Timeout :** la valeur du timeout à utiliser pour les requêtes des services 
  distants. Si non définie la valeur par défaut de libcurl est utilisée.
* **UserPwd :** peut fournir un couple *userid:password* pour envoyer un userid 
  et un mot de passe au serveur distant.
* **HttpAuth :** peut être BASIC, NTLM ou ANY pour contrôler la méthode 
  d'authentification à utiliser.
* **Version :**  définie une version spécifique du WFS à utiliser (soit 1.0.0 ou 1.1.0).
* **PagingAllowed :** définir à ON pour que la pagination soit activée. Voir la 
  section :ref:`gdal.ogr.formats.wfs.pagination`.
* **PageSize :** taille de la page quand la pagination est activée. Voir la 
  section :ref:`gdal.ogr.formats.wfs.pagination`.

.. _`gdal.ogr.formats.wfs.pagination`:

Pagination des requêtes
========================

Généralement, lors de la lecture de la première feature d'une couche, le contenu 
de la couche entière sera récupérée du serveur.

Certains serveurs (comme MapServer >= 6.0) gère une option spécifique du 
fournisseur, STARTINDEX, qui permet de faire une requête par "page", et donc 
d'éviter le téléchargement de tout le contenu de la couche en une seule requête. 
Le client WFS d'OGR utilisera la pagination quand l'option de configuration 
*OGR_WFS_PAGING_ALLOWED* est définie à ON. La taille de la page (nombre de feature 
récupérée en une seule requête) est limité à 100 par défaut. Elle peut être changée 
en définissant l'option de configuration *OGR_WFS_PAGE_SIZE*. Ces deux options 
peuvent également être définie dans le fichier XML de description WFS.

Filtrage
=========

Le pilote renverra n'importe quel filtre spatial avec *SetSpatialFilter()* vers 
le serveur. Il fera également sont possible pour les filtres attributaires définie 
avec *SetAttributeFilter()* (traduire le langage SQL d'OGR en description du filtre 
OGC). Quand cela n'est pas possible, il sera par défaut un filtre côté client, ce 
qui peut être une opération lente parce qu'impliquant la récupération de toutes 
les features du serveur.

Gestion de l'écriture / WFS-T
=============================

Le protocol WFS-T permette à l'utilisateur d'opérer au niveau de la feature. 
Aucune création de source de données, couche ou champs n'est pas possible.

La gestion de l'écriture est seulement activé lorsque la source de données est 
ouverte en mode update.

Les correspondances entre les opération du service e transaction WFS et les concepts 
OGR sont les suivantes :

* OGRFeature::CreateFeature() <==> opération d'insertion WFS
* OGRFeature::SetFeature() <==> opération de mise à jour WFS
* OGRFeature::DeleteFeature() <==> opération de suppression WFS

Les opérations de locks (service LockFeature) ne sont pas disponible pour le moment.

Il a quelques contraintes à garder à l'esprit. L'ID des features (FID) d'OGR est 
un entier, tandis que l'attribut gml:id du WFS/GML est une chaîne de caractères. 
Il n'est donc pas toujours possible de correspondre les deux valeurs. Le pilote 
WFS expose alors l'attribut gml:id d'une feature comme un champ 'gml_id'.

Lors de l'insertion d'un nouvelle feature avec *CreateFeature()*, et si la commande 
est réussie, OGR récupérera le gml:id et définira le champ 'gml_id' de la feature 
en conséquence. Il tentera également de définir le FID OGR si le gml:id est de 
la forme *layer_name.numeric_value*. Sinon le FID sera laissé à sa valeur par 
défaut.

Lors de la mise à jour d'une feature existante avec *SetFeature()*, le champ FID 
OGR sera ignoré. La requête renvoyée au pilote prendra seulement en compte la 
valeur du champ gml:id de la feature. La même chose s'applique pour *DeleteFeature()*.

Transaction OGR et gestion de l'écriture
========================================

Les opérations ci-dessus sont par défaut déclenchées vers le serveur en synchrone 
avec l'appel de l'API d'OGR. Cela peut cependant causer des problèmes de 
performances lorsque plusieurs commandes sont déclenchées dû à un grand nombre 
d'échanges client/serveur.

Il est possible de contourner ces opérations entre *OGRLayer::StartTransaction()* 
et *OGRLayer::CommitTransaction()*. Les opérations seront stockées en mémoire et 
seulement exécuté au moment où *CommitTransaction()* est appelé.

La contrainte de *CreateFeature()* est que l'utilisateur ne peut pas connaître 
quel gml:id a été assigné pour la feature insérée. Une requête spatiale SQL a été 
introduite dans le pilote WFS pour contourner ceci : en déclenchant la commande 
"``SELECT _LAST_INSERTED_FIDS_ FROM layer_name``" (où *layer_name* doit être 
remplacé par le *layer_name* réel) via *OGRDataSource::ExecuteSQL()*, une couche 
sera renvoyée avec autant de ligne avec un attribut unique gml_id que de features 
insérées pendant la dernière transaction commitée.

.. note:: pour le moment, seulement *CreateFeature()* utilise le mécanisme de 
    transaction d'OGR. *SetFeature()* et *DeleteFeature()* seront toujours 
    déclenché immédiatement.

Commandes SQL spéciales
========================

Les commandes SQL et pseudo-SQL suivantes envoyées à *OGRDataSource::ExecuteSQL()* 
sont spécifiques au pilote WFS :

* "DELETE FROM layer_name WHERE expression" : cela résultera en une opération WFS 
  de suppression. Cela peut être un moyen rapide de suppression d'une ou plusieurs 
  features. En particulier, cela peut être un remplaçant plus rapide pour 
  *OGRLayer::DeleteFeature()* quand gml:id est connu, mais la feature n'est pas 
  récupéré à partir du serveur.
* "SELECT _LAST_INSERTED_FIDS_ FROM layer_name" : voir le paragraphe au-dessus.

Pour le moment, toutes les autres commandes SQL sera réalisée par la couche 
générique, c'est à dire seulement réalisée côté client. Les filtres spatiaux et 
attributaires côté serveur doit être réalisé via les interfaces *SetSpatialFilter()* 
et *SetAttributeFilter()*.

Métadonnées des couches
========================

(OGR >= 1.9.0)

Une couche cachée appelée "WFSLayerMetadata" est rempli avec les enregistrements 
des métadonnées pour chaque couche WFS.

Chaque enregistrement contient un champ "layer_name", "title" et "abstract", à 
partir du document renvoyé par le GetCapabilities.

Cette couche est retournée via GetLayerByName("WFSLayerMetadata").

Exemples
=========

* Liste les types d'un serveur WFS :
  ::
    
    ogrinfo -ro WFS:http://www2.dmsolutions.ca/cgi-bin/mswfs_gmap

* Liste les types d'un serveur WFS dont la structure des couches sont en cache 
  dans un fichier XML :
  ::
    
    ogrinfo -ro mswfs_gmap.xml

* Liste les features d'une couche popplace, avec un filtre spatial :
  ::
    
    ogrinfo -ro WFS:http://www2.dmsolutions.ca/cgi-bin/mswfs_gmap popplace -spat 0 0 2961766.250000 3798856.750000

* Récupère les features de gml:id "world.2" et "world.3" à partir de la couche 
  tows:world :
  ::
    
    ogrinfo "WFS:http://www.tinyows.org/cgi-bin/tinyows" tows:world -ro -al -where "gml_id='world.2' or gml_id='world.3'"

* Affiche la couche metadata (OGR >= 1.9.0):
  ::
    
    ogrinfo -ro -al "WFS:http://v2.suite.opengeo.org/geoserver/ows" WFSLayerMetadata

Voir également
==============

* `Standard WFS de l'OGC <http://www.opengeospatial.org/standards/wfs>`_
* :ref:`gdal.ogr.formats.gml`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/04 (trunk 22202)