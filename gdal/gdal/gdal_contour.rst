.. _`gdal.gdal.gdal_contour`:

gdal_contour
=============

Construit les lignes de contours à partir d'un modèle d'élévation raster dans 
un fichier vecteur.

**Usage :**
::
    
    gdal_contour [-b <band>] [-a <attribute_name>] [-3d] [-inodata]
                    [-snodata n] [-f <formatname>] [-i <interval>]
                    [-off <offset>] [-fl <level> <level>...]
                    [-nln <outlayername>]
                    <src_filename> <dst_filename> 

Ce programme génère un fichier de contour en vecteur à partir d'un modèle 
d'élévation en raster (DEM).

.. versionadded:: 1.7.0 
   Les chaînes linéaire de contour seront orientées 
   systématiquement. Le côté haut sera vers la droite, c'est à dire qu'une ligne 
   aura pour sens le sens des aiguilles d'une montre.

* **-b band :** définie une bande particulière à utiliser à partir du DEM. Par 
  défaut la bande nº 1.
* **-a name :** fournie un nom pour l'attribut dans lequel placer l'élévation. 
  S'il n'est pas fourni, aucun attribut d'élévation n'est attaché.
* **-3d :** force la production de vecteurs 3D à la place e 2D. En incluant 
  l'élévation à chaque vertex.
* **-inodata :** ignore les valeurs nodata implicites dans l'ensemble de 
  données – traite toutes les valeurs comme valides.
* **-snodata value :** valeur des pixels en entrée à traiter en tant que « nodata ».
* **-f format :** créé une sortie dans un format particulier, en shapefile par 
  défaut.
* **-i interval :** intervalle des élévations entre les contours.
* **-off offset :** début du zéro relatif à partir duquel interpréter les 
  intervalles.
* **-fl level :** nomme un ou plusieurs « niveaux fixés » à extraire.
* **-nln outlayername :** fournie un nom pour la couche vectorielle en sortie. 
  *contour* par défaut.

**Exemple :**

Cela créera un contour de 10 m à partir des données d'un DEM dans le fichier 
*dem.tif* et produira un shapefile dans *contour.shp*, *contour.shx*, 
*contour.dbf* avec les élévations des contours dans l'attribut « elev ».
::
    
    gdal_contour -a elev dem.tif contour.shp 10.0

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.orggdal_contour.html Trunk r25410)
