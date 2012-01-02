.. _`gdal.gdal.gdal_retile`:

gdal_retile.py
===============

``gdal_retile`` - ``gdal_retile.py`` recréé un ensemble de tuiles et/ou 
construit les niveaux de la pyramide tuilée.

Usage
------

Usage :
::
    
    gdal_retile.py [-v] [-co NAME=VALUE]* [-of out_format] [-ps pixelWidth pixelHeight]
               [-ot  {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
                      CInt16/CInt32/CFloat32/CFloat64}]'
               [ -tileIndex tileIndexName [-tileIndexField tileIndexFieldName]]
               [ -csv fileName [-csvDelim delimiter]]
               [-s_srs srs_def]  [-pyramidOnly]
               [-r {near/bilinear/cubic/cubicspline/lanczos}]
               -levels numberoflevels
               [-useDirForEachRow] 
               -targetDir TileDirectory input_files

Description
-------------

La commande recréera les tuiles d'un ensemble de tuiles en entrée. Toutes les 
tuiles en entrée doivent être géoréférencées dans le même système de coordonnées 
et avoir un nombre de bandes correspondant. En option les niveaux de pyramide 
sont générés. Il est possible de générer des fichiers shape pour la sortie 
tuilés.

Si votre nombre de fichiers d'entrée dépasse le buffer de la ligne de commande, 
utilise l'option générale ``--optfile``.

* **-targetDir directory :** le répertoire dans lequel les tuiles résultantes 
  seront créées. Les pyramides sont rangées dans des sous-répertoires numérotés 
  à partir de 1. Les tuiles créées ont un schéma de numérotation et contienne 
  le nom de(s) tuile(s) source ;
* **-of format :** format de sortie, GeoTIFF par défaut (GTiff). 
* **-co NAME=VALUE :** option de création pour le fichier de sortie. Des options 
  multiples peuvent être définies.
* **-ot datatype :** force les bandes d'images en sortie à un type spécifique. 
  Utilisez le nom du type (c'est-à-dire Byte, Int16...) 
* **-ps pixelsize_x pixelsize_y :** taille du pixel à utiliser pour le fichier 
  de sortie. S'il n'est pas défini, un pixel de 256 x 256 est choisi par défaut ;
* **-levels numberOfLevels :** nombre de niveaux de pyramide à construire ; 
* **-v :** génère une sortie verbeuse des opérations de tuilage lors de leur 
  génération ; 
* **-pyramidOnly :** pas de retuilage, construire seulement les pyramides ;
* **-r algorithm :** algorithme d'échantillonnage, *near* par défaut ;
* **-s_srs srs_def :** référence spatiale source à utiliser. Le système de 
  coordonnées qui doit être envoyé peut avoir n'importe quel format géré par 
  l'appel de *OGRSpatialReference.SetFro‐mUserInput()*, ce qui inclut les 
  EPSG PCS et GCSes (par exemple  EPSG:4296),, les déclarations PROJ4 (comme 
  ci-dessus), ou le nom d'un fichier .prj contenant une projection au format 
  Well Known Text. Si aucun *srs_def* n'est donné, le *srs_def* des tuiles 
  sources est utilisé (s'il en a un). Le *srs_def* sera propagé pour créer les 
  tuiles (si possible) et au(x) fichier(s) optionnel(s) ;
* **-tileIndex tileIndexName :** le nom du fichier shape contenant l'index des 
  tuiles résultantes ;
* **-tileIndexField tileIndexFieldName :** le nom de l'attribut contenant le 
  nom des tuiles ;
* **-csv csvFileName :** le nom du fichier csv contenant les informations de 
  géoréférencement des tuiles. Le fichier contient 5 colonnes : *tilename,minx,maxx,miny,maxy* 
* **-csvDelim column delimiter :** le délimiteur de colonne utilisé dans le 
  fichier csv, la valeur par défaut est le point-virgule ";".
* **-useDirForEachRow :** normalement les tuiles de l'image de base sont 
  stockées comme décrites dans l'option *-targetDir*. Pour de grandes images, 
  certains systèmes de fichier ont des problèmes de performances si le nombre de 
  fichier dans un répertoire est trop important, ne permettant pas à 
  ``gdal_retile.py`` de finir dans un temps raisonnable. Utiliser ce paramètre 
  permet de créer une structure différente en sortie. Les tuiles de l'image de 
  base sont stockées dans un sous-répertoire nommé 0, les pyramides dans les 
  sous-répertoires sont numérotés 1,2,... Dans chacun des ces répertoires un 
  autre niveau de sous-répertoire est créé, numéroté de 0 à n, en fonction du 
  nombre de ligne de tuile qui sont nécessaire pour chaque niveau. Enfin, un 
  répertoire contient seulement les tuiles pour une ligne d'un niveau 
  spécifique. Pour les grandes images une amélioration de la performance d'un 
  facteur N est réalisée.

.. warning::
    ``gdal_merge.py`` est un script Python, et ne fonctionnera seulement si 
    GDAL a été compilé avec la gestion de Python.

.. yves at free.fr, Yves Jacolin - 2010/12/29 15:12 (http://gdal.org/gdal_retile.html Trunk r21324)
