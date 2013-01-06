.. fichier dans le répertoire raw"

.. _`gdal.gdal.formats.lcp`:

===========================================
Pilote GDAL pour le format FARSITE v.4 LCP
===========================================

Les fichiers FARSITE v. 4 landscape (LCP) est un format raster multi-bande 
utilisé par modélisations de simulation de comportement des incendies et des 
effets du feu tels que FARSITE, FLAMMAP et FBAT (www.fire.org). Les bandes d'un 
fichier LCP stocke des données décrivant le terrain, la canopée des arbres, et 
la surface du pétrole. L'`USGS National Map for LANDFIRE <http://landfire.cr.usgs.gov/viewer>`_ 
distribue des données au format LCP, et des programmes tels que FARSITE et 
`LFDAT <http://www.landfire.gov/datatool.php>`_ peuvent créer des fichiers LCP 
à partir de raster en entré. Le pilote GDAL pour LCP gère la lecteur seule.

Un fichier LCP (.lcp) est essentiellement un format brute avec un en-tête de 
7,316-byte décrit ci-dessous. Le type de données pour toutes les bandes est un 
entier de 16 bit signé. Les bandes sont entrelacées par pixel. Cinq bandes sont 
nécessaire : élévation, pente, aspect, modèle de pétrole, et couverture de la 
canopée des végétaux. Les bandes de *crown fuel* (hauteur de la canopée, la 
hauteur du couvert de base, la densité du couvert), et de la surface des bandes 
de pétrole (humus, les débris ligneux grossiers) sont optionnels.

Le pilote LCP lit les unités linéaire, la taille de la cellule, et l'étendue 
mais le fichier LCP ne définie pas la projection. Les projections UTM sont 
typique mais d'autres projections sont possible.

Le pilote LCP de GDAL renvoie des informations sur les méta-données des jeux de 
données et les niveaux de bandes :

**Jeu de données**

::
    
    LATITUDE: Latitude of the dataset, negative for southern hemisphere
    LINEAR_UNIT: Feet or meters
    DESCRIPTION: LCP file description

**Bande**

::
    
    <band>_UNIT or <band>_OPTION: units or options code for the band
    <band>_UNIT_NAME or <band>_OPTION_DESC: descriptive name of units/options
    <band>_MIN: minimum value
    <band>_MAX: maximum value
    <band>_NUM_CLASSES: number of classes, -1 if > 100
    <band>_VALUES: comma-delimited list of class values (fuel model band only)
    <band>_FILE: original input raster file name for the band

.. note::
    Le pilote LCP dérive de la classe helper *RawDataset* déclarée dans 
    *gdal/frmts/raw*. Il doit être implémenté dans *gdal/frmts/raw/lcpdataset.cpp*.

**Format d'en-tête LCP :**

+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+ byte de début + N°. de bytes  + Format    + Nom               + Description                                           +
+===============+===============+===========+===================+=======================================================+
+ 0             + 4             +  long     + crown fuels       + 20 if no crown fuels, 21 if crown fuels exist         +
+               +               +           +                   + (crown fuels = canopy height, canopy base height,     +
+               +               +           +                   + canopy bulk density)                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4            +  4            +  long     + ground fuels      + 20 if no ground fuels, 21 if ground fuels exist       +
+               +               +           +                   + (ground fuels = duff loading, coarse woody)           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  8            +  4            +  long     +  latitude         + latitude (négative pour l'hémisphère sud)             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  12           +  8            +  double   +  loeast           + offset to preserve coordinate precision (legacy       +
+               +               +           +                   + from 16-bit OS days)                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  20           +  8            +  double   +  hieast           + offset to preserve coordinate precision (legacy       +
+               +               +           +                   + from 16-bit OS days)                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  28           +  8            +  double   +  lonorth          + offset to preserve coordinate precision (legacy       +
+               +               +           +                   + from 16-bit OS days)                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  36           +  8            +  double   +  hinorth          + offset to preserve coordinate precision (legacy from  +
+               +               +           +                   + 16-bit OS days)                                       +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  44           +  4            +  long     +  loelev           + élévation minimale                                    +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  48           +  4            +  long     +  hielev           + élévation maximale                                    +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  52           +  4            +  long     +  numelev          + nombre de classes d'élévation, -1 si > 100            +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  56           +  400          +  long     + elevation values  + liste de valeurs d'élévation de type longs            + 
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  456          +  4            +  long     + loslope           + pente minimale                                        +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  460          +  4            +  long     + hislope           + pente maximale                                        +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  464          +  4            +  long     + numslope          + nombre de classes de pente, -1 si > 100               +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  468          +  400          +  long     + slope values      +liste de valeurs de pente de type longs                +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  868          +  4            +  long     + loaspect          + orientation minimale                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  872          +  4            +  long     + hiaspect          + orientation maximale                                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  876          +  4            +  long     + numaspects        + nombre de classes d'orientation, -1 si > 100          +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  880          +  400          +  long     + aspect values     + liste de valeurs d'orientation de type longs          +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1280         +  4            +  long     + lofuel            + modèle de la valeur du fuel minimale                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1284         +  4            +  long     + hifuel            + modèle de la valeur du fuel maximale                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1288         +  4            +  long     + numfuel           + nombre de modèle de fuel -1 si > 100                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1292         +  400          +  long     + fuel values       + liste de modèle de la valeur de fuel de type longs    +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1692         +  4            +  long     + locover           + couverture de la canopée minimale                     +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1696         +  4            +  long     + hicover           + couverture de la canopée maximale                     +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1700         +  4            +  long     + numcover          + nombre de classes de couverture de la canopée, -1 si  +
+               +               +           +                   + > 100                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  1704         +  400          +  long     + cover values      + liste des valeurs de couverture de la canopée de type +
+               +               +           +                   + longs                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2104         +  4            +  long     + loheight          + hauteur minimale de la canopée                        +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2108         +  4            +  long     + hiheight          + hauteur maximale de la canopée                        +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2112         +  4            +  long     + numheight         + nombre de classes de la hauteur de la canopée, -1 si  +
+               +               +           +                   + > 100                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2116         +  400          +  long     + height values     + liste de valeurs de la hauteur de la canopée de type  +
+               +               +           +                   + longs                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2516         +  4            +  long     + lobase            + hauteur minimale de la base de la canopée             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2520         +  4            +  long     + hibase            + hauteur maximale de la base de la canopée             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2524         +  4            +  long     + numbase           + nombre de classes de hauteur de la base de la canopée,+
+               +               +           +                   + -1 si > 100                                           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2528         +  400          +  long     + base values       +liste de valeurs de la hauteur de la base de la canopée+
+               +               +           +                   + de type longs                                         +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2928         +  4            +  long     + lodensity         + minimum de la densité du couvert                      +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2932         +  4            +  long     + hidensity         + maximum  de la densité du couvert                     +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2936         +  4            +  long     + numdensity        + nombre de classes de la densité du couvert, -1 si >100+
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  2940         +  400          +  long     +density values     +liste de valeur de la densité du couvert de type longs +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3340         +  4            +  long     + loduff            + minimum de poussière (duff)                           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3344         +  4            +  long     + hiduff            + maximum de poussière (duff)                           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3348         +  4            +  long     + numduff           + nombre de classes de poussière, -1 si > 100           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3352         +  400          +  long     + duff values       + liste de valeur de poussière de type longs            +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3752         +  4            +  long     + lowoody           + ligneux grossiers minimal                             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3756         +  4            +  long     + hiwoody           + ligneux grossiers maximal                             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3760         +  4            +  long     + numwoodies        + nombre de classes de ligneux grossiers, -1 si > 100   +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  3764         +  400          +  long     + woody values      + liste de valeurs de ligneux grossiers de type longs   +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4164         +  4            +  long     + numeast           + nombre de colonnes raster                             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4168         +  4            +  long     + numnorth          + nombre de ligne de raster                             +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4172         +  8            +  double   + EastUtm           + X max                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4180         +  8            +  double   + WestUtm           + X min                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4188         +  8            +  double   + NorthUtm          + Y max                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4196         +  8            +  double   + SouthUtm          + Y min                                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4204         +  4            +  long     + GridUnits         + unité linéaire : 0 = meters, 1 = feet, 2 = kilometers +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4208         +  8            +  double   + XResol            + largeur de la taille de la cellule en GridUnits       +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4216         +  8            +  double   + YResol            + hauteur de la taille de la cellule en GridUnits       +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4224         +  2            +  short    + EUnits            + unité d'élévation : 0 = meters, 1 = feet              +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4226         +  2            +  short    + SUnits            + unité de la pente : 0 = degrees, 1 = percent          +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4228         +  2            +  short    + AUnits            + unité de l'orientation : 0 = Grass categories, 1 =    +
+               +               +           +                   + Grass degrees, 2 = azimuth degrees                    +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4230         +  2            +  short    +  FOptions         + options du modèle de fuel : 0 = pas de modèle         +
+               +               +           +                   + personnalisé ET pas de fichier de conversion, 1 =     +
+               +               +           +                   + modèle personnalisé MAIS pas de fichier de conversion,+
+               +               +           +                   + 2 = pas de modèle personnalisé MAIS fichier de        +
+               +               +           +                   + conversion, 3 = modèle de personnalisé ET fichier de  +
+               +               +           +                   + conversion nécessaire                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4232         +  2            +  short    + CUnits            + unité de couverture de la canopée : 0 = categories    +
+               +               +           +                   + (0-4), 1 = percent                                    +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4234         +  2            +  short    + HUnits            + unité de hauteur de canopée :                         +
+               +               +           +                   + 1 = meters, 2 = feet, 3 = m x 10, 4 = ft x 10         +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4236         +  2            +  short    + BUnits            + unité de hauteur de la base de la canopée :           +
+               +               +           +                   + 1 = meters, 2 = feet, 3 = m x 10, 4 = ft x 10         +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4238         +  2            +  short    + PUnits            + unité de la densité du couvert : 1 = kg/m<sup>3</sup>,+
+               +               +           +                   + 2 = lb/ft<sup>3</sup>, 3 = kg/m<sup>3</sup> x 100,    +
+               +               +           +                   + 4 = lb/ft<sup>3</sup> x 1000                          +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4240         +  2            +  short    + DUnits            + unité de la poussière : 1 = Mg/ha x 10, 2 = t/ac x 10 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4242         +  2            +  short    + WOptions          + options du ligneux grossiers (1 si la bande ligneux   +
+               +               +           +                   + grossier est présent)                                 +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4244         +  256          +  char[]   + ElevFile          + nom du fichier d'élévation                            +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4500         +  256          +  char[]   + SlopeFile         + nom du fichier de pente                               +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  4756         +  256          +  char[]   + AspectFile        + nom du fichier de l'orientation                       +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  5012         +  256          +  char[]   + FuelFile          + nom du fichier du modèle de fuel                      +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  5268         +  256          +  char[]   + CoverFile         + nom du fichier de la couverture de la canopée         +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  5524         +  256          +  char[]   + HeightFile        + nom du fichier de la hauteur de la canopée            +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  5780         +  256          +  char[]   + BaseFile          + nom du fichier de la base de la canopée               +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  6036         +  256          +  char[]   + DensityFile       + nom du fichier de la densité du couvert               +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  6292         +  256          +  char[]   + DuffFile          + nom du fichier de poussière                           +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  6548         +  256          +  char[]   + WoodyFile         + nom du fichier des ligneux grossiers                  +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+
+  6804         +  512          +  char[]   + Description       + fichier de description LCP                            +
+---------------+---------------+-----------+-------------------+-------------------------------------------------------+

*Chris Toney, 2009-02-14* 


.. yjacolin at free.fr, Yves Jacolin - 2009/04/06 19:54 (trunk 16356)