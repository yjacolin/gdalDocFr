.. _`gdal.gdal.formats.hfa`:

==========================
HFA -- Erdas Imagine .img
==========================

GDAL gère le format Erdas Imagine .img en lecture et écriture. Le pilote gère 
la lecture des aperçues, les palettes et le géoréférencement. Il gère les types 
de bandes erdas u8, s8, u16, u32, f32, f64, c64 et c128.

Les tuiles compressées et manquante dans les fichiers erdas devraient être 
prises en charge proprement pendant la lecture. Les fichiers entre 2Go et 4 Go 
devrait fonctionner sous Windows NT et peuvent fonctionner sous certaines 
plateformes Unix. Les fichiers avec des fichiers étendues externes (nécessaire 
pour les jeux de données plus grands que 2 Go) sont aussi géré en lecture et 
écriture.

La lecture et l'écriture des méta-données est gérée au niveau du jeu de données 
et pour les bandes mais ce sont des méta-données spécifiques à GDAL – pas des 
méta-données sous une forme reconnus par Imagine. Les méta-données sont stockés 
dans une table appelée GDAL_MetaData avec une colonne pour une méta-donnée. Le 
titre est la clé et la valeur de la ligne 1 est la valeur.

Problème lors de la création
=============================

Les fichiers Erdas Imagine peuvent être crées avec n'importe quel type de bande 
définis par GDAL, les types complexes compris. les fichiers crées peuvent avoir 
n'importe quel nombre de bandes. les tables pseudo-couleur seront écrites si la 
méthodologie de *GDALDriver::CreateCopy()* est utilisée. La plupart des 
projections doivent être gérées bien que la traduction des datums inhabituels 
(autre que WGS84, WGS72, NAD83 et NAD27) peuvent être problématiques.

**Options de création :**

* **BLOCKSIZE=blocksize :** Tile width/height (32-2048). Défaut=64
* **USE_SPILL=YES :** force la génération de fichier de débordement (par défaut 
  un fichier de débordement est créé pour des images supérieures à 2 Go 
  seulement).  Défaut à *NO*
* **COMPRESSED=YES :** crée un fichier compressé. L'utilisation de fichier de 
  débordement désactive la compression.  Défaut à *NO*
* **NBITS=1/2/4 :** crée un fichier avec des types de données avec un sous-bytes 
  spécial.
* **PIXELTYPE=[DEFAULT/SIGNEDBYTE] :** en définissant ce paramètre à 
  *SIGNEDBYTE*, un nouveau fichier Byte peut être créé obligatoirement comme 
  byte signé.
* **AUX=YES :** pour créer un fichier .aux. Défaut à *NO*
* **IGNOREUTM=YES :** ignore UTM lors de la sélection du système de coordonnées 
  - utilisera Transverse Mercator. Utilisé seulement pour la méthode *Create()*. 
  Défaut à *NO*.
* **STATISTICS=YES :** pour générer des statistiques et un histogramme. Défaut 
  à *NO*.
* **DEPENDENT_FILE=filename :** nom du fichier dépendant (ne doit pas avoir de 
  chemin absolu), optionnel.
* **FORCETOPESTRING=YES :** force l'utilisation d chaîne ArcGIS PE dans le 
  fichier au lieu de format de système de coordonées Imagine. Dans certains 
  cas cela améliore la compatibilité du système de coordonnées d'ArcGIS.

Erdas Imagine gère la création externe des aperçus (avec ``gdaladdo`` par
exemple). Pour forcer leur création dans un fichier .rrd (plutôt qu'à 
l'intérieure du fichier .img originel) définissez l'option de configuration 
globale HFA_USE_RRD=YES.

Les noms des couches peuvent être définis et récupérés avec l'appel de 
*GDALSetDescription/GDALGetDescription* sur les objets bandes du Raster.

.. seealso::

* Implémenté dans *gdal/frmts/hfa/hfadataset.cpp*.
* Plus d'information, et d'autres outils sont disponibles sur la page du lecteur 
  d'Imagine (img) : http://home.gdal.org/projects/imagine/hfa_index.html
* Site officiel d'Erdas : http://www.erdas.com/

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 17162)