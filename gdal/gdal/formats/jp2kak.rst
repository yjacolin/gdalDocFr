.. _`gdal.gdal.formats.jp2kak`:

=======================================
JP2KAK -- JPEG-2000 (basé sur Kakadu)
=======================================

La plupart des formes des images compressées  JPEG2000 JP2 et JPC (ISO/IEC 
15444-1) peuvent être lu avec GDAL utilisant le pilote basé sur la bibliothèque 
Kakadu. De même, de nouvelles images peuvent être écrites. Les images existantes 
ne peuvent pas être mises à jour.

Le format de fichier JPEG2000 gère les compressions avec et sans perte d'image 
8 et 16 bits avec une ou plusieurs bandes (composants). Via le mécanisme GeoJP2 
(http://www.mappingscience.com/msi.html), le système de coordonnées et les 
informations de géoréférencement style GeoTIFF peuvent être inclus dans le 
fichier JP2. Les fichiers JPEG2000 utilisent un format et un mécanisme de 
compression substantiellement différent de la compression JPEG traditionnelle 
et du format JPEG JFIF. Il y a des mécanismes de compressions distincts produit 
par le même groupe. JPEG2000 est basé sur la compression par ondelette.

Le pilote JPEG200 documenté sur cette page (le pilote JP2KAK) est implémenté 
par-dessus de la bibliothèque commerciale Kakadu (http://www.kakadusoftware.com/). 
C'est une bibliothèque JPEG200 de grande qualité et hautement performante, 
largement utilisée dans la communauté géomatique et dans l'imagerie générale. 
Cependant, elle n'est pas libre et donc une compilation normale de GDAL à partir 
des sources n'inclura pas un support pour ce pilote à moins que le compilateur 
achète une licence pour la bibliothèque et configure en conséquence. GDAL inclut 
un autre pilote JPEG200 basé sur la bibliothèque libre JasPer 
(http://www.gdal.org/frmt_jpeg2000.html).

Lors de la lecture d'une image ce pilote représentera les bandes en byte (8 bits 
non signés), 16 bite signé ou 16 bits non signé. Les informations du système de 
coordonnées et de géoréférencement seront disponibles si le fichier est un fichier 
GeoJP2 (tm). Les fichiers couleurs encodés dans l'espace de couleur YCbCr seront 
automatiquement traduit en RVB. Les images avec une palette sont également gérées.

À partir de GDAL 1.9.0, les métadonnées XMP peuvent être extraite des fichiers 
JPEG2000, et seront stockées comme contenu brute XML dans le domaine de métadonnées 
xml:XMP.

Problèmes de création
=======================

Les fichiers JPEG2000 peuvent seulement être crée en utilisant le mécanisme 
*CreateCopy* pour les copier dans un jeu de donnée existant.

Les aperçues JPEG2000 sont maintenu comme partie de la description mathématique 
de l'image. Les aperçues ne peuvent pas être construit comme un traitement 
séparé, mais en lecture l'image sera généralement représenté comme ayant des 
niveaux d'aperçus à différentes puissances de deux facteurs.

**Options de création :**

* **QUALITY=n** : Définie le taux de la taille compressée comme un pourcentage 
  de la taille de l'image non compressée. Par défaut elle est de 20 et indique 
  que l'image doit avoir une taille de 20 % de celle de l'image non compressée. 
  La taille de l'image finale réelle peut ne pas correspondre exactement celle 
  demandée en fonction de différents facteurs. Une valeur de 100 entraînera 
  l'utilisation d'un algorithme de compression sans perte. Sur les données images 
  typique, si vous définissez une valeur plus grande que 65, il peut être 
  intéressant de tester avec *QUALITY=100* puisque la compression sans perte peut 
  produire une meilleure compression qu'une compression sans perte.
* **BLOCKXSIZE=n** : Définie la largeur de la tuile à utiliser. Par défaut elle 
  est de 20000. 
* **BLOCKYSIZE=n** : Définie la hauteur de la tuile à utiliser. Par défaut elle 
  est de la hauteur de l'image.
* **GMLJP2=YES/NO** : Indique si une boîte GML conforme au GML de l'OGC dans les 
  spécification JPEG2000 doit être inclus dans le fichier. Oui par défaut.
* **GeoJP2=YES/NO** : Indique si une boîte GML conforme aux spécifications GeoJP2 
  (GeoTIFF dans JPEG2000) doit être inclus dans le fichier. Oui par défaut.
* **LAYERS=n** : Contrôle le nombre de couche produite. C'est une sorte de 
  résolution de couches, mais pas tout à fait. La valeur par défaut est de 12 
  et cela fonctionne bine dans la plupart des cas.
  ROI=xoff,yoff,xsize,ysize : Sélectionne une région pour être une région 
  d'intérêt pour faire des traitements avec des données de meilleurs qualités. 
  Les différents options « R » ci-dessous peuvent être utilisé pour mieux 
  contrôler le taux. Par exemple, les définitions "ROI=0,0,100,100", "Rweight=7" 
  encoderaient la zone de 100x100 en haut à gauche de l'image avec une qualité 
  considérablement plus élevée comparée au reste de l'image.
  Les options de création suivantes sont hautement lié à la bibliothèque Kakadu, 
  et sont donnée pour une utilisation avancée seulement. Consultez la 
  documentation de Kakadu pour une meilleur compréhension de leur signification.
* **Corder** : Défaut à "PRCL". 
* **Cprecincts** : défaut à "{512,512},{256,512},{128,512},{64,512},{32,512},
  {16,512},{8,512},{4,512},{2,512}". 
* **ORGgen_plt** : défaut à "yes". 
* **Cmodes** : défaut de la bibliothèque Kakadu utilisé.
* **Clevels** : défaut de la bibliothèque Kakadu utilisé.
* **Rshift** : défaut de la bibliothèque Kakadu utilisé. 
* **Rlevels** : défaut de la bibliothèque Kakadu utilisé.
* **Rweight** : défaut de la bibliothèque Kakadu utilisé. 

.. seealso::

* Implémenté dans *gdal/frmts/jp2kak/jp2kakdataset.cpp*.
* JPEG2000 pour la pag Applications Geospatial, inclus la discussion GeoJP2(tm) 
  : http://www.remotesensing.org/jpeg2000/.
* Pilote JPEG200 alternatif : http://www.gdal.org/frmt_jpeg2000.html.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 22678)