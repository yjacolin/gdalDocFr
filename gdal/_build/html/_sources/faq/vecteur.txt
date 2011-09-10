.. _`gdal.faq.ogr`:

=============
FAQ vecteur
=============

Comment puis je fusionner des 100e de shapefiles ?
===================================================

Voici un script bash pour charger en masse un répertoire de shapefile qui ont 
le même schéma dans postgis. Il peut évidemment être amélioré, mais il fonctionne.

::
    
    #!/bin/bash

    # let OGR create a table from one of the files
    ogr2ogr -f Postgresql PG:"host=smoke.hobu.net" -a_srs "EPSG:26915" -nln outputlayer first_input_shape.shp -overwrite -nlt POLYGON

    # delete all the data in the table we just created (but don't delete the table)
    ogrinfo PG:"host=smoke.hobu.net" -sql "delete  from outputlayer"

    # loop through all of the shapefiles in the directory and load them
    for i in $(ls *.shp); do
    ogr2ogr -f Postgresql PG:"host=smoke.hobu.net" -a_srs " EPSG:26915" -nln outputlayer $i -update -append -skipfailures
    done 


.. note::
    si vous avez une erreur d'import de PostGIS similaire à "*ERROR: new row for 
    relation "layer1" violates check constraint*"  vous devez essayer de 
    substituer "*-nlt GEOMETRY*" par votre type de géométrie (dans l'exemple 
    ci-dessus ce sont des POLYGON). Cela évitera des erreurs si votre shapefiles 
    inclues des géométries de types polygones et des multipolygones, par exemple.
    Lisez ce message pour plus d'information : 
    http://postgis.refractions.net/pipermail/postgis-users/2006-June/012495.html


Ces étapes de consoles Unix illustre comment batcher une fusion multiple de 
shapefiles en un seul shapefil en utilisant OGR. Cela suppose que vous avez 
téléchargé un groupe de shapefile dans un fichier .zip qui sont tous de même 
type de données mais nécessite juste d'être combiné. Cela fonctionne sous Mac 
mais n'a pas été testé sous d'autres versions d'Unix :

::
    
    #Make a new directory called "tmp" and a sub directory called "merged"
    mkdir tmp
    mkdir tmp/merged

    #copy all zipped files to the "tmp" directory and then "cd" into it
    cp *.zip tmp
    cd tmp

    #unzip all the .zip archives
    find . -name "*.zip" -exec unzip '{}' \;

    #delete all .zip archives
    rm *.zip

    #move a single shapefile (and the cooresponded .shx, .dbf, etc files) to the "merged" directory 
    #(exchange 'myshape*' for the name of one of your shapefiles keeping the '*' at the end of the name)
    find . -name 'myshape*' -exec mv '{}' merged \;
    
    #Batch merge all the remaining shapefiles from the tmp dir into the copied file in the merge dir 
    #(exchange 'myshape' for the name of the copied shapefile)
    for i in $(ls *.shp); do ogr2ogr -f 'ESRI Shapefile' -update -append merged $i -nln myshape
    done

Cet exemple de console ``cmd`` Windows fusionne de multiple shapefile *wetlands* 
dans le répertoire actuel à un seule fichier *merged\wetlands.shp* (doublez les 
% pour mettre dans une script , %f --> %%f) :

::
    
    mkdir merged
    for %f in (*wetland*.shp) do (
    if not exist merged\wetlands.shp (
        ogr2ogr -f "esri shapefile" merged\wetlands.shp %f) else (
        ogr2ogr -f "esri shapefile" -update -append merged\wetlands.shp %f -nln Wetlands )
    )

Le truc est d'utiliser la première entré pour créer un nouveau shapefile puis 
seulement de mettre à jour. Voyez la fin de :ref:`gdal.ogr.formats.shapefile`.

si vous n'avez pas besoin de définir un nom lisible par un humain via *-nln*, 
en utilisant *-append* est plus simple :

::
    
    for %f in (dir1\*.shp dir2\*.shp) do (ogr2ogr -f "esri shapefile" -append merged %f)

Comment traduire un fichier de géométrie mélangée vers le format shapfile ?
============================================================================

Certains formats (tel que les Shapefiles d'ESRI) permet seulement un type de 
géométrie dans une couche, tandis que d'autres (comme les formats DGN, MapInfo, 
GML) permettent de mélanger des types de géométries dans une seule couche. Les 
tentatives de transformation résultera en des erreurs comme cela :

::
    
    % ogr2ogr out.shp mixed.dgn 
    ERROR 1: Attempt to write non-linestring (POLYGON) geometry to ARC type shapefile.
    ERROR 1: Terminating translation prematurely after failed
    translation of layer elements

La première étape dans la prise en charge de tel problème est de découvrir 
quels types de géométries existent dans le fichier source. Pour une fichier DGN 
appelé *mixed.dgn*, avec une couche appelé *elements* cela peut être accomplie 
en utilisant la commande SQL d'OGR (voyez [[ogr_sql]] pour les détails).

::
    
    % ogrinfo -ro mixed.dgn -sql 'select distinct ogr_geometry from elements'
    INFO: Open of `mixed.dgn'
        using driver `DGN' successful.

    Layer name: elements
    Geometry: Unknown (any)
    Feature Count: 1
    Layer SRS WKT:
    (unknown)
    ogr_geometry: String (0.0)
    OGRFeature(elements):0
    ogr_geometry (String) = LINESTRING

    OGRFeature(elements):1
    ogr_geometry (String) = POLYGON

    OGRFeature(elements):2
    ogr_geometry (String) = POINT

Ce fichier a des géométries points, lignes et polygones. Chacun doit être 
transmis dans un fichier séparé.

::
    
    % ogr2ogr out_point.shp mixed.dgn -where 'ogr_geometry = "POINT"'
    % ogr2ogr out_line.shp mixed.dgn -where 'ogr_geometry = "LINESTRING"'
    % ogr2ogr out_poly.shp mixed.dgn -where 'ogr_geometry = "POLYGON"'

Comment protéger les paramètres des commandes GDAL/OGR sous la console Microsoft Windows ?
============================================================================================

Lorsque vous travaillez avec une console Windows, il est utile de se souvenir 
que les règles de protection sont différent de ceux utilisé sous unix. Voici un 
exemple de protection correcte de requête SQL passé à ogrinfo (ou ogr2ogr) avec 
l'option *-sql* :

::
    
    ogrinfo . -sql "SELECT * FROM 'B_Major Cities 1' WHERE FID = 49"

La requête SQL complète est entouré de guillemets doubles, mais pas de 
guillemets simples. Le nom de la table (ici il fonctionne pour des shapefiles 
ESRI dans le répertoire courant, notez le point) inclues les espaces, il doit 
donc être entouré avec des guillemets simples.

Par exemple, ces deux variantes présentent des commandes incorrectes :

::
    
    ogrinfo . -sql 'SELECT * FROM 'B_Major Cities 1' WHERE FID = 49'
    ogrinfo . -sql 'SELECT * FROM "B_Major Cities 1" WHERE FID = 49'



Comment récupérer les formats gérés par ogr ?
==============================================

    Comme pour gdal, il suffit d'utiliser le paramètre --formats (avec un s ;-) :
    ::
        
        ogrinfo --formats

    renverra :

    ::
        
        $ ogrinfo --formats
        Supported Formats:
            -> "GRASS" (readonly)
            -> "ESRI Shapefile" (read/write)
            -> "MapInfo File" (read/write)
            -> "UK .NTF" (readonly)
            -> "SDTS" (readonly)
            -> "TIGER" (read/write)
            -> "S57" (read/write)
            -> "DGN" (read/write)
            -> "VRT" (readonly)
            -> "AVCBin" (readonly)
            -> "REC" (readonly)
            -> "Memory" (read/write)
            -> "CSV" (read/write)
            -> "GML" (read/write)
            -> "KML" (read/write)
            -> "ODBC" (read/write)
            -> "PGeo" (readonly)
            -> "OGDI" (readonly)
            -> "PostgreSQL" (read/write)

Comment récupérer des informations sur la couche vectorielle ?
================================================================

La commande ogrinfo permet de récupérer un grand nombre d'information d'une 
couche. Dans une première étape on récupère les informations contenu dans le 
jeu de données :
::
    
    $ ogrinfo clc00_fr.shp
    INFO: Open of `clc00_fr.shp'
            using driver `ESRI Shapefile' successful.
    1: clc00_fr (Polygon)

Les fichiers shp possèdent toujours une couche dont le nom est le même que le 
nom du fichier. Certains fichiers possèdent plusieurs couches qu'il est 
possible de différencier par ce moyen.

Pour obtenir des informations sur une couche du jeu de données, lancez la 
commande suivante :

::
    
    $ ogrinfo -so clc00_fr.shp clc00_fr
    INFO: Open of `clc00_fr.shp'
            using driver `ESRI Shapefile' successful.
    
    Layer name: clc00_fr
    Geometry: Polygon
    Feature Count: 270465
    Extent: (37256.000205, 1607395.375873) - (1207902.000605, 2687734.936295)
    Layer SRS WKT:
    PROJCS["NTF_Lambert_II_étendu",
        GEOGCS["GCS_NTF",
            DATUM["Nouvelle_Triangulation_Francaise",
                SPHEROID["Clarke_1880_IGN",6378249.2,293.46602]],
            PRIMEM["Greenwich",0.0],
            UNIT["Degree",0.0174532925199433]],
        PROJECTION["Lambert_Conformal_Conic_1SP"],
        PARAMETER["False_Easting",600000.0],
        PARAMETER["False_Northing",2200000.0],
        PARAMETER["Central_Meridian",2.3372291667],
        PARAMETER["Standard_Parallel_1",45.8989188889],
        PARAMETER["Standard_Parallel_2",47.6960144444],
        PARAMETER["Scale_Factor",1.0],
        PARAMETER["Latitude_Of_Origin",46.8],
        UNIT["Meter",1.0]]
    CODE_00: String (3.0)

Notez le paramètre ``-so`` qui permet de récupérer un **résumé** des 
informations de la couche. En absence de ce paramètre, ``ogrinfo`` renverra 
le contenu du fichier, c'est à dire les objets géographiques et la table 
attributaire !

Comment écrire dans une base de données POSTGIS ?
==================================================

Pour écrire dans une base de données PostGIS à partir de fichier shapefile :
::
    
    ogr2ogr -f “PostgreSQL” PG:”host=myhost user=myloginname dbname=mydbname password=mypassword” myshapefile.shp

Comment lire une base de données au format VMAP0 ?
===================================================

* Pour lire un fichier vmap0
  ::
    
    ogrinfo -ro -summary gltp:/vrf/mnt/data/v0eur/vmaplv0/eurnasia ‘polbnda@bnd(*)_area’

En cas de problème (format non reconnue), pensez à vérifier que le format OGDI 
est bien listé dans la liste des formats supportés. Si tel est le cas, vérifiez 
qu'il n'y ait pas de casse différente dans le nom du fichier (Document/Sig/ 
par exemple ne passera pas).

* Pour créer un fichier shp à partir d’une fichier VMAP0 :
  ::
    
    ogr2ogr watrcrsl.shp gltp:/vrf/mnt/data/v0eur/vmaplv0/eurnasia ‘watrcrsl@hydro(*)_line’

* Autre exemple, celui-ci permet de créer un fichier Shape en Lambert 2 étendue :
  ::
    
    ogr2ogr -t_srs ‘EPSG:27582’ contourl.shp gltp:/vrf/mnt/data/v0eur/vmaplv0/eurnasia “contourl@elev(*)_line”

Comment récupérer une zone géographique précise dans une jeu de données ?
==========================================================================

FIXME

Le paramètre ``-spat`` permet de définir une bbox :
::
    
    ogr2ogr -spat xmin ymin xmax ymax

Par exemple, en France :
::
    
    ogr2ogr -spat 


.. yjacolin at free.fr, Yves Jacolin - 2008/07/12 19:16