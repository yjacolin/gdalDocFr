.. _`gdal.gdal.formats.mrsid`:

===================================================
MrSID --- Multi-resolution Seamless Image Database
===================================================

MrSID est une technologie de compression d'image basée sur la transformée par 
ondelette qui peut être utilisé à la fois avec et sans perte. Cette technologie 
a été acquise sous sa forme originelle par les Laboratoires Nationaux de Los 
Alamos (LANL), où il a été développé sous l'égide du gouvernement U.S. pour le 
stockage des empreintes digitales pour le FBI. Maintenant elle est développée 
et distribuée  par la société LizardTech.

Ce pilote gère la lecture des fichiers images MrSID en utilisant le kit de 
développement de logiciel d'encodage de LizardTech (DSDK). Ce DSDK n'est pas un 
logiciel libre, vous devez contacter LizardTech pour l'obtenir (voyez le lien à 
la fin de cette section). Si vous utilisez GCC, s'il vous plaît, assurez-vous 
que vous avez le même compilateur qui a été utilisé pour la compilation de DSDK. 
C'est une bibliothèque en C++, vous pouvez donc avoir des incompatibilités dans 
le name mangling entre les différentes version de GCC (2.95.x et 3.x).

Les dernières versions de DSDK gère également le décodage du format de fichier 
JPEG2000, ce pilote peut aussi être utilisé pour le format JPEG2000.


Méta-données
===============

Les méta-données MrSID sont traduites de manière transparente dans les chaînes 
de méta-données de GDAL. Les fichiers au format MrSID contiennent un ensemble 
de balises de méta-données standards telles que : IMAGE__WIDTH (contient la 
largeur de l'image),  IMAGE__HEIGHT (contient la hauteur de l'image), 
IMAGE__XY_ORIGIN (contient les coordonnées x et y de l'origine), 
IMAGE__INPUT_NAME (contient le nom ou les noms des fichiers utilisés pour créer 
l'image MrSID) etc. Les clés des méta-données de GDAL ne peuvent pas contenir 
certains caractères ':' et '=', mais les balises MrSID standards contiennent 
toujours le symbole ':' dans les noms des balises. Ces caractères sont remplacés 
dans GDAL par '_' pendant la traduction. Si vous utilisez d'autres logiciels 
pour travailler sur les images MrSID attendez vous à ce que les noms des clés 
des méta-données soient affichés différemment.

.. versionadded:: 1.9.0 les métadonnées XMP peuvent être extraites des fichiers 
   JPEG2000, et seront stockées comme contenu brute XML dans le domaine de 
   métadonnées xml:XMP.

Géoréférencement
==================

Les images MrSID peuvent contenir des informations de géoréférencement et du 
système de coordonnées sous la forme de clé géographique (GeoKeys) GeoTiff, 
traduites dans les enregistrements des méta-données. Toutes ces GeoKeys sont 
extraites proprement et utilisées par le pilote. Malheureusement, il y a une 
contrainte : les anciens encodeurs MrSID avaient un bug qui entraînait des 
GeoKeys incorrectes, stocké dans les fichiers MrSID. Ce bug a été corrigé dans 
la version 1.5 du logiciel MrSID , mais si vous avez un vieil encodeur ou des 
fichiers crées avec un vieil encodeur, vous ne pouvez pas utiliser leurs 
informations de géoréférencement.

.. seealso::

  * Implementé dans *gdal/frmts/mrsid/mrsiddataset.cpp*.
  * Site Web de LizardTech

.. yjacolin at free.fr, Yves Jacolin 2013/01/01 (trunk 25207)
