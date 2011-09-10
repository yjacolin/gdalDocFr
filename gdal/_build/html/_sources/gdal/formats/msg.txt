.. _`gdal.gdal.formats.msg`:

===================================
MSG -- Météosat Seconde Génération
===================================

Ce pilote implémente la gestion de la lecture pour les fichiers  Meteosat 
Second Generation. Le nom de ces fichiers sont du type 
*H-000-MSG1__-MSG1________-HRV______-000007___-200405311115-C_*, distribué 
habituellement dans une structure arborescente avec des dates (par exemple 
2004/05/31 pour le fichier mentionné).

Les fichiers MSG sont compressé par ondelette. Une bibliothèque sous licence 
`Eumetsat <http://www.eumetsat.int/>`_ est nécessaire 
(« Wavelet Transform Software » - http://www.eumetsat.int/en/dps/helpdesk/tools.html#wavelet). 
Le logiciel est compatible sous les systèmes Microsoft Windows, Linux et 
Solaris, et il fonctionne sous 32 bits et 64 bits ainsi que les architectures 
mélangées. Elle est sous licence logiciel et est disponible après acceptation 
de la licence logiciel WaveLet Transform lors d'une procédure électronique.

Une partie des sources du fichier *xrithdr_extr.c* provenant  XRIT2PIC est 
utilisé pour parser les en-têtes MSG. Ces sources sont sous licence GNU General 
Public Licence publié par la Fondation Free Software.

Ce pilote n'est pas activé par défaut. Lisez la partie « `instructions de compilation <http://www.gdal.org/frmt_msg.html#MSG_Build_Instructions>`_ » pour la manière 
d'inclure ce pilote dans votre bibliothèque GDAL.

Instructions de compilation
============================

Téléchargez la bibliothèque Eumestat pour la décompression par ondelette. C'est 
un fichier nommé PublicDecompWt.zip. Décompressez son contenu dans un 
sous-répertoire avec le même nom (dans frmts/msg). 

Si vous compilez avec Visual Studio 6.0, décompressez le makefiles .vc pour 
*PublicDecompWT* à partir du fichier  *PublicDecompWTMakefiles.zip*.

Si vous compilez en utilisant GNUMakefile, utilisez l'option ``--with-msg`` pour 
activer le pilote MSG :

::
    
    ./configure --with-msg

S'il se trouve que certain ajustement soit nécessaire dans le makefile et/ou 
les fichiers sources, s'il vous plaît commitez" les. La bibliothèque Eumetsat 
promet d'être indépendant de la plateforme, mais puisque nous travaillons sous 
Microsfot Windows et Visual Studio 6.0, nous n'avons pas la possibilité de 
vérifier si l'ensemble du pilote msg l'est. De plus, appliquez les étapes 4 à 7 
du `tutorial d'Implémentation du pilote de GDAL <http://www.gdal.org/gdal_drivertut.html>`_, 
section "Ajouter un pilote à l'arbre de GDAL".

Le wiki de MSG est disponible sur http://trac.osgeo.org/gdal/wiki/MSG. Il est 
dédié à la documentation de la compilation et astuce d'usage.

Spécification des sources des jeux de données
================================================

Il est possible de sélectionner des fichiers individuels pour l'ouverture. Dans 
ce cas, le pilote collectera les fichiers qui correspondent aux autres bandes 
de la même image, et composera correctement l'image.

**Exemple avec gdal_translate.exe :**
::
    
    gdal_translate C:\hrit_a\2004\05\31\H-000-MSG1__-MSG1________-HRV______-000008___-200405311115-C_ c:\output\myimage.tif

Il est également possible d'utiliser la syntaxe suivantes pour l'ouverture des 
fichiers MSG :
::
    
    MSG(source_folder,timestamp,(canal,canal,...,canal),use_root_folder,data_conversion,nr_cycles,step)


* ``source_folder`` : un chemin vers la structure arborescente qui contient 
  les fichiers.
* ``timestamp`` : 12 digits représentant une date/heure qui identifie les 114 
  fichiers des 12 images de cette heure, par exemple 200501181200 
* ``canal`` : un nombre compris entre 1 et 12, représentant chacun des 12 canaux 
  disponibles. Lorsqu'un seul canal est disponible, les crochets sont optionnels.

use_root_folder : Y pour indiquer que les fichiers résident directement à la 
racine du répertoire source_folder définie. N pour indiquer que les fichiers 
résident dans les répertoires structurés en date : source_folder/YYYY/MM/DD 

* ``data_conversion`` : 

  * ``N`` pour garder les valeurs DN originelles de 10 bits. Le résultat est 
    UInt16. 
  * ``B`` pour convertir en 8 bits (commode pour les images GIF et JPEG). Le 
    résultat est en Byte. 
  * ``R`` pour réaliser des calibration radio-métrique et obtenir le résultat 
    en mW/m2/sr/(cm-1)-1. Le résultat est Float32. 
  * ``L`` pour réaliser des calibrations radio-métrique et obtenir les résultat 
    en W/m2/sr/um. Le résultat est Float32. 
  * ``T`` pour obtenir la réflectivité pour les bandes visible (1, 2, 3 et 12) 
    et la température en degré Kelvin pour les bandes infrarouges (toutes les 
    autres bandes). Le résultat est Float32.

* ``nr_cycles`` : un nombre qui indique le nombre de cycles consécutifs pour 
  être inclus dans le même fichier (séries temporelle). Ceux-ci sont ajouté aux 
  bandes additionnelles.
* ``step`` : un nombre qui indique quelle est la taille de l'étape quand des 
  cycles multiples sont choisit. Par exemple : toutes les 15 minutes : step = 1, 
  toutes les 30 minutes : step = 2 etc. Notez que les cycles sont des multiple 
  de 15, vous ne pouvez donc pas avoir des images entre ces moments (step est 
  un entier). 

**Exemples avec gdal_translate.exe :**

Exemple d'appel pour récupérer une image MSG 200501181200 avec des bandes 1, 2 
et 3 au format IMG :
::
    
    gdal_translate -of HFA MSG(\\pc2133-24002\RawData\,200501181200,(1,2,3),N,N,1,1) d:\output\outfile.img

Au format JPG, et convertir des images e 10 bites en image 8 bits en divisant 
toutes les valeurs par 4 :
::
    
    gdal_translate -of JPEG MSG(\\pc2133-24002\RawData\,200501181200,(1,2,3),N,B,1,1) d:\output\outfile.jpg

Même chose, mais en réordonnant les bandes dans l'image JPEG pour ressembler à 
une image RVB :
::
    
    gdal_translate -of JPEG MSG(\\pc2133-24002\RawData\,200501181200,(3,2,1),N,B,1,1) d:\output\outfile.jpg

Sortie Geotiff, seule la bande 2, valeurs originales en 10 bits :
::
    
    gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,2,N,N,1,1) d:\output\outfile.tif

Bande 12 :
::
    
    gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,12,N,N,1,1) d:\output\outfile.tif

La même bande 12 avec une calibration radiométrique en mW/m2/sr/(cm-1)-1 :
::
    
    gdal_translate -of GTiff MSG(\\pc2133-24002\RawData\,200501181200,12,N,R,1,1) d:\output\outfile.tif

Récupérer les données de c:\hrit-data\2005\01\18 au lieu de 
\\pc2133-24002\RawData\... :
::
    
    gdal_translate -of GTiff MSG(c:\hrit-data\2005\01\18,200501181200,12,Y,R,1,1) d:\output\outfile.tif

Autre option pour faire la même chose (notez la différence dans le Y et le N 
pour l'utilisation du paramètre “use_root_folder” :
::
    
    gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,R,1,1) d:\output\outfile.tif

Sans calibration radiométrique, mais pour 10 cycles consécutifs (donc de 1200 à 
1415) :
::
    
    gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,N,10,1) d:\output\outfile.tif

10 cycles,mais toutes les heures (donc de 1200 à 2100) :
::
    
    gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,12,N,N,10,4) d:\output\outfile.tif

10 cycles, toutes les heures, et les bandes 3, 2 et 1 :
::
    
    gdal_translate -of GTiff MSG(c:\hrit-data\,200501181200,(3,2,1),N,N,10,4) d:\output\outfile.tif

Géoréférencement et projection
===============================

Les images utilisent la projection de vue satellites géo-stationnaires. La 
plupart des logiciels SIG ne reconnaissent pas cette projection (nous savons 
seulement que le logiciel ILWIS possède cette projection), mais ``gdalwarp.exe`` 
peut être utilisé pour reprojeter les images.

**Lisez également :**

* Implémenté dans *gdal/frmts/msg/msgdataset.cpp*.
* http://www.eumetsat.int - Organisation Européenne pour l'Exploitation  des Satellites Météorologique


.. yjacolin at free.fr, Yves Jacolin - 2009/03/16 21:36 (trunk 15065)