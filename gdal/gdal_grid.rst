.. _`gdal.gdal.gdal_grid`:

gdal_grid
==========

Créer une grille régulière à partir de données éparses.

Usage
-------


Usage :

::
    
    gdal_grid [-ot {Byte/Int16/UInt16/UInt32/Int32/Float32/Float64/
            CInt16/CInt32/CFloat32/CFloat64}]
            [-of format] [-co "NAME=VALUE"]
            [-zfield field_name]
            [-a_srs srs_def] [-spat xmin ymin xmax ymax]
            [-clipsrc <xmin ymin xmax ymax>|WKT|datasource|spat_extent]
            [-clipsrcsql sql_statement] [-clipsrclayer layer]
            [-clipsrcwhere expression]
            [-l layername]* [-where expression] [-sql select_statement]
            [-txe xmin xmax] [-tye ymin ymax] [-outsize xsize ysize]
            [-a algorithm[:parameter1=value1]*] [-q]
            <src_datasource> <dst_filename>


Description
------------

Ce programme créé une grille régulière (raster) à partir des données 
éparpillées à partir d'une source de données OGR. Les données en entrées seront 
interpolées pour remplir les nœuds de la grille avec des valeurs, vous pouvez 
choisir diverses méthodes d'interpolations.

À partir de GDAL 1.10, il est possible de définir l'option de configurtion 
*GDAL_NUM_THREADS* pour paralléliser les processus. La valeur à spécifier est 
le nombre de threads de travail ou *ALL_CPUS* pour utiliser tout le CPU/core 
de l'ordinateur.

* **-ot type :** pour définir les types des données des bandes en sortie.
* **-of format :** sélectionne le format de sortie. GeoTIFF par défaut (GTiff). 
  Utiliser le nom du format court.
* **-txe xmin xmax :** définie les étendues X géoréférencées du fichier en sortie à 
  créer.
* **-tye ymin ymax :** définie les étendues Y géoréférencées du fichier en 
  sortie à créer.
* **-outsize xsize ysize :** définie la taille du fichier en sortie en pixel et 
  lignes.
* **-a_srs srs_def :** écrase la projection pour le fichier en sortie. Le 
  *srs_def* peut être de n'importe quel format que ceux habituelle dans GDAL/OGR, 
  WKT complet, PROJ.4, EPSG:n ou un fichier contenant une projection au format WKT.
* **-zfield field_name :** identifie un champ attributaire sur l'objet à utiliser 
  pour obtenir la valeur du z. Cette valeur écrase la valeur du Z lu dans la 
  géométrie (naturellement, si vous avez une valeur Z dans la géométrie, sinon 
  vous n'avez pas le choix et devez définir un nom de champ contenant la valeur 
  du Z).
* **-a [algorithm[:parameter1=value1][:parameter2=value2]...] :** définie 
  l'algorithme d'interpolation ou le nom de la métrique de données et (en option) 
  leurs paramètres. Lisez la section :ref:`gdal.gdal.gdal_grid.algo` et 
  :ref:`gdal.gdal.gdal_grid.metriques` pour plus d'information sur les 
  options disponibles.
* **-spat xmin ymin xmax ymax :** ajoute un filtre spatial pour sélectionner 
  seulement les géométries intersectant la boîte englobante décrite par (xmin, 
  ymin) - (xmax, ymax).
* **-clipsrc [xmin ymin xmax ymax]|WKT|datasource|spat_extent :** ajoute un 
  filtre spatial pour sélectionner seulement les features contenus dans une 
  bouding box définie (exprimé dans le SRS source), une géométrie WKT (POLYGON 
  ou MULTIPOLYGON), à partir d'une source de données ou bien de l'étendue 
  spatiale de l'option *-spat* si vous utilisez le mot-clé *spat_extent*. 
  Lorsque vous spécifiez une source de données, vous voudrez généralement 
  l'utiliser en combinaison de l'option *-clipsrclayer*, *-clipsrcwhere* ou 
  *-clipsrcsql*.
* **-clipsrcsql sql_statement :** sélectionne les géométries désirées en 
  utilisant une requête SQL à la place.
* **-clipsrclayer layername :** sélectionne la couche nommée à partir de la 
  source de données pour la découpe.
* **-clipsrcwhere expression :** restreint les géométries désirées basé sur une 
  requête attributaire.
* **-l layername :** indique la couche de la source de données qui sera utilisée 
  pour les objets en entrée. peut être définie de multiples fois, mais au moins 
  une couche ou une option *-sql* doit être définie.
* **-where expression :** une expression SQL optionnelle de requête de style 
  WHERE à appliquer aux objets sélectionnés à traiter à partir de la couche en 
  entrée.
* **-sql select_statement :** une requête SQL à évaluer en fonction de la source 
  de données pour produire une couche virtuelle d'objet à traiter.
* **-co "NAME=VALUE":** envoie une option de création au pilote de format de 
  sortie. Des options *-co* multiple peuvent être listés. Lisez la documentation 
  spécifique au format pour les options correctes de création pour chaque format.
* **-q :** supprime la visualisation de la progression et autres sorties qui ne 
  sont pas des erreurs.
* **src_datasource :** n'importe quelle source de données lisibles gérées par OGR.
* **dst_filename :** le fichier de sortie géré par GDAL.

.. _`gdal.gdal.gdal_grid.algo`:

Algorithmes d'interpolation
---------------------------

Il y a plusieurs algorithmes d'interpolation disponible.

invdist
********

Inverse de la distance à la puissance. C'est l'algorithme par défaut. Il possède 
les paramètres suivants :

* **power :** poids de la puissance (2.0 par défaut) ;
* **smoothing :** paramètre de douceur" (0.0 par défaut) ;
* **radius1 :** le premier rayon (axe des X si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **radius2 :** le second rayon (axe des Y si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **angle :** angle de rotation de l'ellipse de recherche en degré (sens des 
  aiguilles d'une montre, 0.0 par défaut).
* **max_points :** nombre maximal de points de données à utiliser. Ne cherche 
  pas un nombre de points au-dessus de ce nombre. Il est utilisé seulement si 
  l'ellipse de recherche est définie (les deux rayons ne sont pas nul). Zéro 
  signifie que tous les points trouvés doivent être utilisés. 0 est la valeur 
  par défaut.
* **min_points :** nombre minimal de points de données à utiliser. Si un nombre 
  de points inférieur est trouvé le noeud de la grille est considéré comme 
  vide et sera rempli de valeur *nodata*. Il est utilisé seulement si la 
  recherche de l'ellipse est définie (les deux rayons ne sont pas nuls). 0 est 
  la valeur par défaut.
* **nodata :** valeur *NODATA* pour remplir les points vides (0.0 par défaut).

average
********

Algorithme de la moyenne mobile. Il possède les paramètres suivants :

* **radius1 :** le premier rayon (axe des X si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **radius2 :** le second rayon (axe des Y si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **angle :** angle de rotation de l'ellipse de recherche en degré (sens des 
  aiguilles d'une montre, 0.0 par défaut).
* **min_points :** nombre minimal de points de données à utiliser. Si un nombre 
  de points inférieur est trouvé le noeud de la grille est considéré comme vide 
  et sera rempli de valeur *nodata*. 0 est la valeur par défaut.
* **nodata :** valeur *NODATA* pour remplir les points vides (0.0 par défaut).

Notez qu'il est essentiel de définir l'ellipse de recherche pour la méthode de 
la moyenne mobile. C'est une fenêtre qui sera moyennée lors du calcul des 
valeurs des nœuds de la grille.

nearest
********

Algorithme du plus proche voisin. Il possède les paramètres suivants :

* **radius1 :** le premier rayon (axe des X si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **radius2 :** le second rayon (axe des Y si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **angle :** angle de rotation de l'ellipse de recherche en degré (sens des 
  aiguilles d'une montre, 0.0 par défaut).
* **nodata :** valeur *NODATA* pour remplir les points vides (0.0 par défaut).

.. _`gdal.gdal.gdal_grid.metriques`:

Métriques des données
----------------------

Outre les fonctionnalités d'interpolation ``gdal_grid can`` peut être utilisé 
pour calculer certaines données métriques en utilisant la fenêtre définie et la 
géométrie grille en sortie. Ces métriques sont :

* **minimum :** valeur minimale trouvée dans l'ellipse de recherche du nœud de 
  la grille.
* **maximum :** valeur maximale trouvée dans l'ellipse de recherche du nœud de 
  la grille.
* **range :** une différence entre les valeurs minimales et maximales trouvées 
  dans l'ellipse de recherche du nœud de la grille.
* **count :** un nombre de point trouvé dans l'ellipse de recherche de noeud de 
  la grille.
* **average_distance :** une distance moyenne entre les noeuds de la grille 
  (centre de l'ellipse de recherche) et toutes les données ponctuelles trouvé 
  dans l'ellipse de recherche de noeud de la grille.
* **average_distance_pts :**  une distance moyenne entre les données ponctuelles 
  dans l'ellipse de recherche de noeud de la grille. La distance entre chaque 
  pair de points dans l'ellipse est calculé et la moyenne de toutes les distances 
  est définie comme valeur du noeud de la grille.
    
Tous les métriques ont les mêmes ensembles d'options :

* **radius1 :** le premier rayon (axe des X si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble .
  du tableau de point. 0.0 par défaut.
* **radius2 :** le second rayon (axe des Y si l'angle de rotation est 0) de 
  l'ellipse de recherche. Définissez ce paramètre à 0 pour utiliser l'ensemble 
  du tableau de point. 0.0 par défaut.
* **angle :** angle de rotation de l'ellipse de recherche en degré (sens des 
  aiguilles d'une montre, 0.0 par défaut).
* **min_points :** nombre minimal de points de données à utiliser. Si un nombre 
  de points inférieur est trouvé le noeud de la grille est considéré comme vide 
  et sera rempli de valeur *nodata*. Il est utilisé seulement si la recherche 
  de l'ellipse est définie (les deux rayons ne sont pas nuls). 0 est la valeur 
  par défaut.
* **nodata :** valeur *NODATA* pour remplir les points vides (0.0 par défaut).

.. _`gdal.gdal.gdal_grid.csv`:

Lire des valeurs séparées par des virgules
-------------------------------------------

Souvent vous avez un fichier texte avec une liste de valeurs XYZ séparées par 
des virgules à utiliser (appelé fichier CSV). Vous pouvez facilement utiliser 
ce type de source de données dans *gdal_grid*. Tout ce que vous devez faire est 
de créer un en-tête de jeu de données virtuel (VRT) pour votre fichier CSV et 
l'utiliser comme jeu de données en entré pour *gdal_grid*. Vous pouvez trouver 
des détails supplémentaires sur la page de description du :ref:`gdal.ogr.formats.vrt`.

Voici un petit exemple. Nous avons un fichier CSV appelé *dem.csv* contenant :

::
    
    Easting,Northing,Elevation
    86943.4,891957,139.13
    87124.3,892075,135.01
    86962.4,892321,182.04
    87077.6,891995,135.01
    ...

Pour les données ci-dessus nous créons un en-tête dem.vrt avec le contenu 
suivant :

::
    
    <OGRVRTDataSource>
        <OGRVRTLayer name="dem">
            <SrcDataSource>dem.csv</SrcDataSource> 
    <GeometryType>wkbPoint</GeometryType> 
    <GeometryField encoding="PointFromColumns" x="Easting" y="Northing" z="Elevation"/> 
        </OGRVRTLayer>
    </OGRVRTDataSource>

Cette description définie une géométrie appelée 2.5D avec trois coordonnées X,Y 
et Z. La valeur Z sera utilisée pour l'interpolation. Maintenant vous pouvez 
utiliser le fichier *dem.vrt* avec tous les programmes OGR (démarrez avec 
``ogrinfo`` pour tester que tout fonctionne correctement). La source de données 
contiendra une seule couche appelée "dem" rempli d'objet point construit à 
partir des valeurs contenu dans le fichier CSV. En utilisant cette technique, 
vous pouvez prendre en charge les fichiers CSV avec plus de trois colonnes, 
inverser des colonnes, etc.

Si votre fichier CSV ne contient pas d'en-tête de colonne alors il peut être 
pris en charge comme suit :

::
    
    <GeometryField encoding="PointFromColumns" x="field_1" y="field_2" z="field_3"/>

La page de description des fichiers :ref:`gdal.ogr.formats.csv` contient 
des détails sur le format CSV géré par GDAL/OGR.

Exemple
--------

Les exemples suivants pourraient créer un fichier raster TIFF à partir d'une 
source de données VRT décrit dans la section :ref:`gdal.gdal.gdal_grid.csv` en 
utilisant la distance inverse à la puissance. Les valeurs à interpoler seront 
lues partir de la valeur Z de l'enregistrement de la géométrie.

::
    
    gdal_grid -a invdist:power=2.0:smoothing=1.0 -txe 85000 89000 -tye 894000 
      890000 -outsize 400 400 -of GTiff -ot Float64 -l dem dem.vrt dem.tiff

La commande suivante fait la même chose que la précédente, mais lit les valeurs 
pour interpoler à partir du champ attributaire défini avec l'option *-zfield* à 
la place de l'enregistrement des géométries. Dans ce cas donc, les coordonnées 
X et Y sont récupérées dans la géométrie et le Z du champ *Elevation*.

::
    
    gdal_grid -zfield "Elevation" -a invdist:power=2.0:smoothing=1.0 -txe 85000 89000 -tye 894000 890000 *
      -outsize 400 400 -of GTiff -ot Float64 -l dem dem.vrt dem.tiff

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/gdal_grid.html Trunk r25410)
