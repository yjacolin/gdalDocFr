.. _`gdal.gdal.formats.nitf`:

=============================================
NITF -- National Imagery Transmission Format
=============================================

GDAL gère la lecture de plusieurs sous-types de fichiers images NITF, et 
l'écriture des fichiers NITF 2.1 simples. Les fichiers  NITF 1.1, NITF 2.0, 
NITF 2.1 et NSIF 1.0 avec des images non compressées, compressé en  ARIDPCM, 
JPEG, compression JPEG200 (avec le SDK Kakadu ou ECW) ou VQ devraient être 
lisible.

Le test de la gestion de la lecture a été réalisé sur différents produits, dont 
CIB et les frames CADRG des produits RPF, frames ECRG, produits HRE.

Les tables de couleurs pour les images en pseudo-couleur sont lu. Dans certains 
cas les valeurs *nodata* sont identifiées.

Les étendues Lat/Long sont lu à partir des informations IGEOLO dans l'en-tête 
de l'image si elle est disponible. Si une information de géoréférencement en 
lat/long en haute définition est disponible dans les données auxiliaires RPF, 
ceux-ci seront utilisé en préférence à l'information IGEOLO de faible précision. 
Au cas où une instance de BLOCKA est trouvée, les coordonnées de plus haute 
précision du BLOCKA sont utilisées si les données du bloc couvre l'image 
complète – c'est à dire si le champ L_LINES avec le nombre de ligne pour ce 
bloc est égal au nombre de ligne de l'image. De plus, toutes les instances du 
BLOCKA sont renvoyées comme méta-données. Si GeoSDE TRE est disponible, elle sera 
utilisé pour fournir des coordonnées de plus hautes précisions.

La plupart des fichiers d'en-tête et des champs d'en-tête de l'image sont 
renvoyé comme des méta-données de niveau du jeu de données.

Problèmes lors de la création
==============================

À l'export, les fichiers NITF sont toujours écrit en NITF 2.1 avec une image et 
aucune autre couche auxiliaire. Les images sont non compressées par défaut, mais 
les compressions JPEG et JPEG2000 sont également disponible. Le géoréférencement 
peut seulement être écrit pour les images utilisant le système de coordonnées 
géographique ou une projection WGS84 UTM. Les coordonnées sont implicitement 
traité comme WGS84 même s'ils sont en réalité dans un système de coordonnée 
géographique différent. Les tables de pseudo-couleur peuvent être écrites pour 
les images 8 bites.

En plus de l'export orienté par l'API *CreateCopy()*, il est également 
possible de créer un fichier NTIF vide en utilisant Create() et d'écrire l'image 
à la demande. Cependant, en utilisant cette méthodologie, l'écriture de tables 
pseudo-couleurs et le géoréférencement ne sont pas gérés à moins que des options 
IREP et ICORDS appropriées ne soient fournit. 

**Options  de création :**

La plupart des en-tête de fichier, des méta-données d'en-tête des images et des 
champs de sécurité peuvent être définie avec des **options de création** 
appropriées (bien qu'elles sont reportées comme item de métadonnées, mais ne doit 
pas être définir comme métadonnées). Par exemple définir "FTITLE=Image of 
abandoned missle silo south west of Karsk" dans la liste d'option de création 
entraînera la configuration du champ FTITLE dans l'en-tête du fichier NITF. 
Utilisez les noms des champs officiels à partir du document de spécification NITF ; 
de placer pas le préfixe "NITF_" qui est reporté lors de la demande de la liste 
de métadonnées.

* **IC=NC/C3/M3/C8 :** définie la méthode compression :

  * NC est la valeur par défaut, et signifie pas de compressions ;
  * C3 signifie compression JPEG et est seulement disponible pour la méthode 
    ``CreateCopy()``. Les options de création spécifique au format JPEG *QUALITY* 
    et *PROGRESSIVE* peuvent être utilisé. Voyez la documentation sur le 
    :ref:`gdal.gdal.formats.jpeg`. À partir de GDAL 1.7.0, les images multi-blocs 
    peuvent être écrite.
  * M3 est une variation de C3. la seule différence est qu'une carte de bloc est 
    écrite, ce qui permet la recherche rapide d'un bloc (à partir de GDAL 1.7.0).
  * C8 signifie compression JPEG2000 (un bloc) et est disponible pour les  
    méthodes ``CreateCopy()`` et/ou ``Create()``. La compression *JPEG2000* est 
    seulement disponible si les pilotes *JP2ECW*, JP2KAK ou Jasper sont 
    disponibles.
    
    * JP2ECW : les options de création spécifique au format JP2ECW *TARGET* et 
      *PROFILE* peuvent être utilisée. Voyez la documentation du 
      :ref:`gdal.gdal.formats.jp2ecw`. 
    * JP2KAK : les options de création généraux spécifique à JP2KAK peuvent être 
      utilisé ((QUALITY, BLOCKXSIZE, BLOCKYSIZE, GMLPJ2, GeoJP2, LAYERS, ROI). 
      seulement la méthode *CreateCopy()* est disponible. Voyez 
      :ref:`gdal.gdal.formats.jp2kak`. 
    * À partir de GDAL 1.7.0, si le pilote JP2ECW et JP2KAK ne sont pas 
      disponibles, le pilote JPEG2000 de Jasper peut être utilisé dans le cas 
      de ``CreateCopy()``.

* **NUMI=n :** (à partir de GDAL 1.7.0) Nombre d'images. 1 par défaut. Cette 
  option  est seulement compatible avec IC=NC (images non compressées).
* **ICORDS=G/D/N/S :** définir à "G" pour s'assurer que l'espace sera 
  réservé pour les coordonnées du coin géographique (en DMS) pour être définie 
  plus tard par ``SetGeoTransform()``, définie à "D" pour les coordonnées 
  géographiques en degré décimal, définie à "N" pour la projection UTM WGS84 
  dans l'hémisphère nord ou à "S" pour la projection UTM WGS84 dans l'hémisphère 
  sud (seulement nécessaire pour la méthode ``Create()``, pas pour 
  ``CreateCopy()``). Si vous créez un nouveau fichier NITF et avez définie "N" 
  ou "S" pour ICORDS, vous devez appeler plus tard la méthode *SetProjection* 
  avec un SRS UTM cohérent pour définir un numéro de zone UTM (autrement elle 
  sera à 0 par défaut).
* **FHDR :** la version du fichier peut être sélectionnée bien que les 
  deux seules possibilités gérées sont "NITF02.10" (celui par défaut), et 
  "NSIF01.00". 
* **IREP :** définir à "RGB/LUT" pour réserver l'espace pour une table de 
  couleur pour chaque bande en sortie (seulement nécessaire pour la méthode 
  ``Create()``, pas pour ``CreateCopy()``).
* **IREPBAND :** (GDAL >= 1.9.0) Liste séparé par des virgules de bandes 
  IREPBAND dans l'ordre des bandes.
* **ISUBCAT :** (GDAL >= 1.9.0) Liste spéré par des virgules des bandes 
  ISUBCAT dans l'ordre des bandes.
* **LUT_SIZE :** définie pour contrôler la taille des tables de 
  pseudo-couleurs pour les bandes RVB/LUT. Une valeur de 256 est assumé si 
  aucune est présente (seulement nécessaire pour la méthode ``Create()``, pas 
  pour ``CreateCopy()``).
* **TFW=YES :** force la génération d'un fichier world ESRI associé (.tfw).
* **BLOCKXSIZE=n :** définie la largeur du bloc.
* **BLOCKYSIZE=n :** définie la hauteur du bloc.
* **BLOCKA_*= :** si un ensemble d'option de BLOCKA est fournit avec la même 
  organisation que la méta-donnée NITF_BLOCKA rapporté lors de la lecture d'un 
  fichier NITF avec des arbres BLOCKA, alors un fichier sera créer avec des 
  arbres BLOCKA.
* **TRE=tre-name,tre-contents :** un ou plusieurs options de création 
  d'arbres peuvent être utilisées pour écrire des arbres définie par 
  l'utilisateur à l'en-tête de l'image. Le nom de l'arbre doit être de moins de 
  6 caractères, et le contenu de l'arbre doit être protégé par un \ s'il 
  contient des \ ou des bytes à 0. L'argument est le même format que celui 
  renvoyé dans le domaine méta-données de l'arbre lors de la lecture.
* **FILE_TRE=tre-name=tre-contents :** (GDAL >= 1.8.0) similaire aux options ci-
  dessus, sauf que TRE sont écrite dans l'en-tête du fichier, au lieu de l'en-tête 
  de l'image.
* **SDE_TRE=YES/NO :** (GDAL >= 1.8.0) écrite GEOLOB et GEOPSB TREs pour obtenir 
  un géoréférencement plus précis. Ceci est limité au SRS géographique, et pour 
  ``CreateCopy()`` pour le moment.

Liens 
======

* :ref:`gdal.gdal.formats.nitf_avancee`
* `Page publique du Bureau Technique du NITFS <http://www.gwg.nga.mil/ntb/>`_.
* `DIGEST Part 2 Annex D (describe encoding of NITF Spatial Data Extensions) <http://www.gwg.nga.mil/ntb/baseline/docs/digest/part2_annex_d.pdf>`_.
* :ref:`gdal.gdal.formats.divers_formats.rpftoc` : pour lire la Table Of Content des produits CIB et CADRG.
* `MIL-PRF-89038 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28080000+-+99999%29/MIL-PRF-89038_25371/>`_ : Spécification des produits RPF, CADRG, CIB.
* :ref:`gdal.gdal.formats.divers_formats.ecrgtoc` : pour lire la Table Of Contents des produits ECRG.
* `MIL-PRF-32283 <http://www.everyspec.com/MIL-PRF/MIL-PRF+%28030000+-+79999%29/MIL-PRF-32283_26022/>`_ : Spécification des produits ECRG.

Crédit
=======

L'auteur souhaite remercier AUG Signal (http://www.augsignals.com/) et le 
programme GeoConnections (http://geoconnections.org/) pour l'aide au 
développement de ce pilote ainsi que Steve Rawlinson (JPEG), Reiner Beck 
(BLOCKA) pour l'aide à l'ajout de fonctionnalités.


.. yjacolin at free.fr, Yves Jacolin - 2014/02/24 (trunk 26980)