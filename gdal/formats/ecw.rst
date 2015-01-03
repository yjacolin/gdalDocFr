.. _`gdal.gdal.formats.ecw`:

=========================================
Le format ECW - ERDAS Compress Wavelets
=========================================

GDAL supporte le format .ecw en lecture et en écriture. L'implémentation 
actuelle lit n'importe quel nombre de bande mais renvoi seulement des images 
en 8 bit. Les systèmes de coordonnées et les transformations du géo-référencement 
sont lu, mais dans certains cas les systèmes de coordonnées ne seront pas traduit.

Le support du pilote ECW dans GDAL est optionnel, et nécessite le lien avec la 
bibliothèque SDK ECW externe fournit par Intergraphe (anciennement ERDAS).

En plus des fichiers ECW, ce pilote gère aussi l'accès au service de réseau 
d'image en utilisant le protocole "ECWP". Utilisez l'url complète *ecwp://* du 
service comme nom de jeu de données. Lorsqu'il compilé avec le SDK 4.1 ou plus 
récent il est aussi possible de tirer avantage des accès asynchrone des services 
ECWP de la `RFC 24 <http://trac.osgeo.org/gdal/wiki/rfc24_progressive_data_support>`_.
 
À partir de GDAL 1.9.0, les métadonnées XMP peuvent être extraite à partir des 
fichiers JPEG2000, et seront stockés comme contenu brute XML dans le domaine de 
métadonnées xml:XMP.

Mise à jour de géoréférencement / domaine de Métadonnées ECW
===============================================================

.. versionadded:: à partir de GDAL 1.9.0

Les valeurs des paramètres UNITS, DATUM et PROJ trouvées dans l'en-tête ECW sont 
retournée par le domaine de méta-données ECW. Ils peuvent être définie avec la 
méthode SetMetadataItem() dans le but de modifier les informations d'en-tête d'un 
fichier ECW existant, ouvert en mode mise à jour, sans modifier l'image.

La projection et le géoréférencement peuvent aussi être modifié avec les méthodes 
SetGeoTransform() et SetProjection(). Si la projection est définie avec 
SetProjection() et PROJ, DATUM et UNITS avec SetMetadataItem(), les dernières 
valeurs écraseront les valeurs compilé avec la chaîne de projection.

Version 3 des fichiers ECW
============================

.. versionadded:: à partir de GDAL 1.10.0

Le SDK ECW 5.x fourni un fichier de format ammendé qui permet de stocker des 
données statistiques, des histogrammes, des métadonnées, des métadonnées rpc et 
gère le type de données de bande UInt16.
 
Pour le moment tout n'est pas implémenté : 

* **Statistics and Histograms** - implémentation complète pour l'écriture et la 
  lecture. Pas de clé ECW_OEM_KEY néccessaire.
* **File Metadata** - gestion en lecture seule. Des statistiques seront aussi 
  préservées/mises à jour durant la méthode CreateCopy.
* **RPC Metadata** - géré par le format de fichier, pas géré par le pilote. 
* **Header Metadata** - écrit par le SDK lui-même. Retournée par gdalinfo.

Clé des métadonnées de fichiers
*********************************

* FILE_METADATA_ACQUISITION_DATE
* FILE_METADATA_ACQUISITION_SENSOR_NAME
* FILE_METADATA_ADDRESS
* FILE_METADATA_AUTHOR
* FILE_METADATA_CLASSIFICATION
* FILE_METADATA_COMPANY - doit être définie à ECW_OEM_KEY
* FILE_METADATA_COMPRESSION_SOFTWARE - mis à jour pendant la recompression
* FILE_METADATA_COPYRIGHT
* FILE_METADATA_EMAIL
* FILE_METADATA_TELEPHONE

Les métadonnées suivant de l'en-tête seront retournées
*******************************************************

* CLOCKWISE_ROTATION_DEG
* COLORSPACE (reporté pour les fichiers en version 2 également)
* COMPRESSION_DATE
* COMPRESSION_RATE_ACTUAL
* COMPRESSION_RATE_TARGET (reporté pour les fichiers en version 2 également)
* VERSION (reporté pour les fichiers en version 2 également)

Problèmes de création
========================

Le SDK ECW 4.x d'ERDAS est seulement gratuire pour la décompression d'image. Pour 
compresser des images il est nécessaire de compiler le SDK en lecture / écriture 
et de fournir la clé de licence OEM lors du fonctionnement qui peut être acheté 
chez ERDAS.

Pour ceux utilisant toujours le SDK ECW 3.3, les images inférieures à 500 Mo 
peuvent être compressé gratuitement, tandis que les images plus grosses nécessitent 
une licence d'ERDAS. Voyez l'agréement de licence et l'option *LARGE_OK*.

Les fichiers à compresser au format ECW doivent également être d'au moins 128 × 128. 
Les sources qui ne sont pas en 8 bites seront re-échantillonnées par la 
bibliothèque SDK ECW d'une manière un peu incompréhensible. Le résultat est une 
image en 8 bites pour les fichiers ECW en version. Les fichiers ECW en version 3 
gère 16 bits par canal (comme type de données Uint16). Veuillez lire les options 
de création pour activer l'écriture de fichier ECW en version 3.

Lors de l'écriture des informations du système de coordonnées dans les fichiers 
ECW, la plupart des systèmes de coordonnées courants ne sont pas intégrés 
proprement. Si vous connaissez le nom du système de coordonnées au format 
ERMapper, vous pouvez l'obliger à le définir au moment de la création avec les 
options de création du PROJ et du DATUM.

**Options de création :**

* **TARGET=pourcentage :** définit la taille de réduction cible comme un 
  pourcentage de l'originale. S'il n'est pas définit, la valeur par défaut est 
  de 90 pour les images en nuances de gris et de 95 pour les images RVB.
* **PROJ=nom :** Nom au format ECW de la chaîne de projection à utiliser. 
  Des exemples courants sont NUTM11, ou GEODETIC.
* **DATUM=nom :** nom du datum au format d'ECW à utiliser. Des exemples 
  courants sont WGS84 ou NAD83.
* **UNITS=name :** (GDAL >= 1.9.0) nom des unités de projection ECW à utiliser : 
  METERS (par défaut) ou FEET (pied US).
* **LARGE_OK=YES :** lorsque compilé avec le SDK ECW 3.x cette option peut être 
  définie  pour autoriser la compression des fichiers supérieur à 500 Mo. Il est 
  de la responsabilité de l'utilisateur de s'assurer que les nécessités de licence 
  pour la compression des gros fichiers a été suivit.
* **ECW_ENCODE_KEY=key :** fournie la clé d'encodage OEM acheté chez Erdas qui 
  permet l'encodage des images. La clé a une longueur approximative de 129 hex. 
  Il peut aussi être fournie comme option de configuration.
* **ECW_ENCODE_COMPANY=name :** fournie le nom de la société qui possède la clé 
  d'encodage OEM d'ERDAS (voir ECW_ENCODE_KEY). Cela doit correspondre exactement 
  au nom utilisé par ERDAS lors de la fourniture de la clé OEM. Il peut aussi être 
  fournie comme option de configuration.
* **ECW_FORMAT_VERSION=2/3 :** (GDAL >= 1.10.0) lorsqu'il est compilé avec le 
  SDK 5.x du format ECW cette option peut être définie pour permettre la création 
  de fichier ECW en version 3. Cela permet d'écrire des rasters avec un type de 
  données UInt16 (nouvelle fonctionnalités des fichiers ECW en version 3). La 
  valeur par défaut est 2 ce qui créera des fichiers ECW en version 2.

Le format ECW ne supporte pas la création d'aperçu puisque le format ECW est 
déjà censé être optimisé pour les « aperçues arbitraires ».

Options de configuration
==========================
 
Le SDK ECW d'ERDAS gère une grande variété d'`options de configuration 
<http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ pour contrôler différentes 
fonctionnalités. La plupart de celles-ci sont exposée par les options de 
configuration de GDAL. Voyez la documentation du SDK ECW pour plus de détails 
sur la signification de ces options. 

* **ECW_CACHE_MAXMEM=bytes :** octets maximal de RAM utilisé pour la mise en cache 
  mémoire. S'il n'est pas définie, jusqu'à 1/4 de la RAM physique sera utilisé par 
  le SDK pour la mise en cache en mémoire.
* SDK ECW disponible sur `www.ermapper.com <http://www.ermapper.com/>`_.
* **ECWP_CACHE_LOCATION=path :** chemin vers le répertoire à utiliser pour la mise 
  en cache des résultats de ECWP. Si non définie, la mise en ache ECWP ne sera 
  pas activée.
* **ECWP_CACHE_SIZE_MB=number_of_megabytes :** le nombre maximal de Mo d'espace 
  dans ECWP_CACHE_LOCATION à utilisé pour la mise en cache des résultats ECWP.
* **ECWP_BLOCKING_TIME_MS :** temps de lecture qu'un ecwp:// bloquera avant de 
  revenir - 10 000 ms par défaut.
* **ECWP_REFRESH_TIME_MS :** délais entre l'arrivé des blocs et la prochaine 
  demande de rafraîchissement - 10 000 ms par défaut. Dans le cas de GDAL ceci 
  est le temps que le pilote attendra pour plus de données d'une connexion ecwp 
  pour laquelle le résultat finale n'a pas été renvoyé. Si définie trop petit 
  alors les requêtes *RasterIO()* produiront souvent des résultats de faibles 
 résolutions.
* **ECW_TEXTURE_DITHER=TRUE/FALSE :** cela peut être définie à FALSE pour 
  désactiver le tramage lors de la décompression des fichiers ECW. TRUE par défaut.
* **ECW_FORCE_FILE_REOPEN=TRUE/FALSE :** cela peut être définie à TRUE pour forcer 
  à ouvrir un fichier pris en charge pour chaque fichier pour chaque connexion 
  réalisée. FALSE par défaut.
* **ECW_CACHE_MAXOPEN=number :** le nombre maximal de fichier à garder ouvert 
  pour que le fichier ECW prenne en charge la mise en cache. Illimité par défaut.
* **ECW_RESILIENT_DECODING=TRUE/FALSE :** contrôle si le lecteur doit oublier les 
  erreurs dans un fichier et essayer de renvoyer autant de données que possible. 
  TRUE par défaut. Si définie à FALSE un fichier invalide résultera en une erreur.
* **ECW_ENCODE_KEY, ECW_ENCODE_COMPANY :** ces valeurs, comme décrite dans les 
  options de création, peuvent aussi être définir comme options de configuration. 
  voir plus haut.

.. seealso::

  * Implementé dans *gdal/frmts/ecw/*.
  * La page ECW (http://geospatial.intergraph.com/products/other/ecw/ERDASECWJPEG2000SDK/Details.aspx chez 
    http://www.geospatial.intergraph.com)
  * `Astuces de compilation de l'ECW pour GDAL <http://trac.osgeo.org/gdal/wiki/ECW>`_

.. yjacolin at free.fr, Yves Jacolin - 2013/04/05 (trunk 25864)
