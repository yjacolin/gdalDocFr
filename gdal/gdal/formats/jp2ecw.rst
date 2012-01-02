.. _`gdal.gdal.formats.jp2ecw`:

JP2ECW -- ERMapper JPEG2000 (.jp2)
===================================

GDAL gère la lecture et l'écriture des fichiers JPEG2000 en utilisant le SKD 
ECW d'ERDAS.

Le système de coordonnées et de transformation du géoréférencement sont lu, et 
un certain degré de gestion est inclus pour GeoJP2 (tm) (GeoTIFF-in-JPEG2000), 
ERDAS GML-in-JPEG2000, et la nouvelle spécification GML-in-JPEG2000 développé 
par l'OGC.
La gestion du pilote JP2ECW dans GDAL est optionnelle et nécessite la liaison 
vers la bibliothèque SDK ECW externe fournit par ERDAS.

Problèmes de création
----------------------

Le SDK ECW 4.x d'ERDAS est seulement gratuit pour la décompression d'image. Pour 
compresser des images il est nécessaire de compiler le SDK en lecture/écriture et 
de fournir une clé de licence OEM à son lancement qui peut être acheté chez ERDAS.

Pour ceux utilisant encore le SDK ECW 3.3, les images inférieures à 500 Mo peuvent 
être compressées grauitement, bien que les images plus grandes nécessite une 
licence de ERDAS. Voir l'agrément de la licence et l'option LARGE_OK.

**Options de création :**

* **TARGET=percent :** définie la taille cible de la réduction exprimé en 
  pourcentage de l'originale. Si elle n'est pas fournit, la valeur par défaut 
  est de 75 pour une réduction de 75 %. TARGET=0 utilise une compression sans 
  perte.
* **PROJ=name :** nom de la projection ECW à utiliser. Des exemples employés  sont 
  NUTM11, ou GEODETIC.
* **DATUM=name :** nom du datum d'ECW à utiliser à utiliser. Des exemples employés 
  sont WGS84 ou NAD83.
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
* **GMLJP2=YES/NO :** indique si une boîte GML conforme à OGC GML des 
  spécifications du JPEG2000 doit être incluse dans le fichier. YES par défaut.
* **GeoJP2=YES/NO :** indique si une boîte GML conforme aux spécifications 
  GeoJP2 (GeoTIFF dans JPEG2000) doit être incluse dans le fichier. YES par 
  défaut.
* **PROFILE=profile :** Un profile parmi BASELINE_0, BASELINE_1, BASELINE_2, 
  NPJE ou EPJE. Lisez la documentation du SDK d'ECW pour les détails sur la 
  signification des profiles.
* **PROGRESSION=LRCP/RLCP/RPCL :** définie l'ordre de la progression avec quel 
  codestream JPEG2000 il a été écrit.
* **CODESTREAM_ONLY=YES/NO :** si définie à YES, seulement le code stream de 
  l'image compressée sera écrit. S'il est définie à NO (par défaut) un paquet 
  JP2 sera écrit autour du code stream incluant divers meté information.
* **LEVELS=n** : Lire le SDK ECW pour les détails.
* **LAYERS=n** : Lire le SDK ECW pour les détails.
* **PRECINCT_WIDTH=n** : Lire le SDK ECW pour les détails.
* **PRECINCT_HEIGHT=n** : Lire le SDK ECW pour les détails.
* **TILE_WIDTH=n** : Lire le SDK ECW pour les détails.
* **TILE_HEIGHT=n** : Lire le SDK ECW pour les détails.
* **INCLUDE_SOP=YES/NO** : Lire le SDK ECW pour les détails.
* **INCLUDE_EPH=YES/NO** : Lire le SDK ECW pour les détails.
* **DECOMPRESS_LAYERS=n** : Lire le SDK ECW pour les détails.
* **DECOMPRESS_RECONSTRUCTION_PARAMETER=n** : Lire le SDK ECW pour les détails.

Le format JPEG2000 ne gère pas la création des aperçues puisque le format est 
déjà considéré comme suffisamment optimisé pour les « aperçues arbitraires ».

Options de configuration
-------------------------
 
Le SDK ECW d'ERDAS gère une grande variété d'`options de configuration 
<http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_ pour contrôler différentes 
fonctionnalités. La plupart de celles-ci sont exposée par les options de 
configuration de GDAL. Voyez la documentation du SDK ECW pour plus de détails 
sur la signification de ces options. 

* **ECW_CACHE_MAXMEM=bytes :** octets maximal de RAM utilisé pour la mise en cache 
  mémoire. S'il n'est pas définie, jusqu'à 1/4 de la RAM physique sera utilisé par 
  le SDK pour la mise en cache en mémoire.
* **ECW_TEXTURE_DITHER=TRUE/FALSE :** cela peut être définie à FALSE pour 
  désactiver le tramage lors de la décompression des fichiers ECW. TRUE par défaut.
* **ECW_FORCE_FILE_REOPEN=TRUE/FALSE :** cela peut être définie à TRUE pour forcer 
  à ouvrir un fichier pris en charge pour chaque fichier pour chaque connexion 
  réalisée. FALSE par défaut.
* **ECW_CACHE_MAXOPEN=number :** le nombre maximal de fichier à garder ouvert 
  pour que le fichier ECW prenne en charge la mise en cache. Illimité par défaut.
* **ECW_AUTOGEN_J2I=TRUE/FALSE :** Contrôle si les fichiers d'index .j2i doivent 
  être créés lors de l'ouverture des fichiers jpeg2000. TRUE par édfaut.
* **ECW_RESILIENT_DECODING=TRUE/FALSE :** contrôle si le lecteur doit oublier les 
  erreurs dans un fichier et essayer de renvoyer autant de données que possible. 
  TRUE par défaut. Si définie à FALSE un fichier invalide résultera en une erreur.
* **ECW_ENCODE_KEY, ECW_ENCODE_COMPANY :** ces valeurs, comme décrite dans les 
  options de création, peuvent aussi être définir comme options de configuration. 
  voir plus haut.

Voir également
--------------

* Implémenté dans *gdal/frmts/ecw/ecwdataset.cpp*.
* SDK ECW disponible sur `Erdas.com <http://www.erdas.com/products/ERDASECWJPEG2000SDK/Details.aspx>`_
* `Astuces de compilation de l'ECW pour GDAL <http://trac.osgeo.org/gdal/wiki/ECW>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 21403)