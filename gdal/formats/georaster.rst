.. _`gdal.gdal.formats.georaster`:

===========================
GeoRaster d'Oracle Spatial
===========================

Ce pilote gère la lecture et l'écriture de données raster au format GeoRaster 
d'Oracle Spatial (10g ou supérieur). Le pilote GeoRaster d'Oracle Spatial est 
compilé en option comme plugin GDAL mais il nécessite les bibliothèques clientes 
d'Oracle.

Lors de l'ouverture du GeoRaster, son nom doit être définie sous la forme :
::
    
    georaster:<user>{,/}<pwd>{,@}[db],[schema.][table],[column],[where]
    georaster:<user>{,/}<pwd>{,@}[db],<rdt>,<rid>

où :

* *user*   = login du nom d'utilisateur du serveur Oracle ;
* *pwd*    = mot de passe utilisateur ;
* *db*     = identification du serveur Oracle (nom de la base de données) ;
* *schema* = nom du schéma ;
* *table*  = nom d'une table GeoRaster (table qui contient des colonnes 
  GeoRaster) ;
* *column* = nom de la colonne données de type *MDSYS.SDO_GEORASTER* ;
* *where*  = un clause WHERE simple pour identifier un ou plusieurs GeoRaster ;
* *rdt*    = nom d'une table de données raster ;
* *rid*    = identification numérique d'un GeoRaster.

Exemples :

::
    
    geor:scott,tiger,demodb,table,column,id=1
    geor:scott,tiger,demodb,table,column,"id = 1"
    "georaster:scott/tiger@demodb,table,column,gain>10"
    "georaster:scott/tiger@demodb,table,column,city='Brasilia'"
    georaster:scott,tiger,,rdt_10$,10
    geor:scott/tiger,,rdt_10$,10

.. note::
    N'utilisez pas d'espace autour des valeurs du champ et la virgule.

.. note::
    Comme dans les deux exemples précédents, le champs du nom de la base de 
    données peut être laissé vide (",,") et le TNSNAME sera utilisé.

.. note::
    Si la requête résulte en plus d'un GeoRaster elle sera traitée comme une liste 
    de métadonnées de sous-jeu de données (voir plus bas).

Naviguer dans la base de données des GeoRasters
==================================================

En fournissant certaine information basique le pilote GeoRaster est capable de 
lister les rasters existant stockés sur le serveur :

Pour lister toutes les tables sur le serveur qui appartiennent à un utilisateur 
et à une base de données :
::
    
    % gdalinfo georaster:scott/tiger@db1

Pour lister toutes les colonnes de types GeoRaster qui existent dans cette table :
::
    
    % gdalinfo georaster:scott/tiger@db1,table_name

Ceci listera tous les objets GeoRaster stocké dans cette table :
::
    
    % gdalinfo georaster:scott/tiger@db1,table_name,georaster_column

Ceci listera tous les GeoRaster existant sur cette table selon la clause QHERE :
::
    
    % gdalinfo georaster:scott/tiger@db1,table_name,georaster_column,city='Brasilia'

Notez que le résultat de ces requêtes est renvoyé à GDAL comme méta-données 
d'un sous jeu de données, par exemple :

::
    
    % gdalinfo georaster:scott/tiger
    Driver: GeoRaster/Oracle Spatial GeoRaster
    Subdatasets:
    SUBDATASET_1_NAME=georaster:scott,tiger,,LANDSAT
    SUBDATASET_1_DESC=Table:LANDSAT
    SUBDATASET_2_NAME=georaster:scott,tiger,,GDAL_IMPORT
    SUBDATASET_2_DESC=Table:GDAL_IMPORT

Options de création
=====================

* **BLOCKXSIZE :** le nombre de colonne de pixel dans un bloc raster.
* **BLOCKYSIZE :** le nombre de ligne de pixel dans un bloc raster.
* **BLOCKBSIZE :** le nombre de bandes dans un bloc raster.
* **SRID :** assigne une identification de projection/système de référence EPSG 
  à un GeoRaster.
* **INTERLEAVE :** mode d'entrelacement de bande, BAND, LINE, PIXEL (ou BSQ, 
  BIP, BIL) pour les entrelacements de bandes séquentielles, Ligne ou Pixel.
* **DESCRIPTION :** une description simple d'une nouvelle table dans la syntaxe 
  SQL. Si la table existe déjà, cette option de création sera ignorée, par 
  exemple :
  ::
    
    % gdal_translate -of georaster landsat_823.tif geor:scott/tiger@orcl,landsat,raster \
    -co DESCRIPTION="(ID NUMBER, NAME VARCHAR2(40), RASTER MDSYS.SDO_GEORASTER)" \
    -co INSERT="VALUES (1,'Scene 823',SDO_GEOR.INIT())"

* **INSERT :** une clause SQL simple d'insert/values pour informer le pilote 
  des valeurs qu'il doit insérer dans une nouvelle ligne de la table, par exemple :
  ::
    
    % gdal_translate -of georaster landsat_825.tif geor:scott/tiger@orcl,landsat,raster \
    -co INSERT="(ID, RASTER) VALUES (2,SDO_GEOR.INIT())"

* **COMPRESS :** options de compression, JPEG-F, les pixels originaux sont 
  modifiés.
  
* **GENPYRAMID :** génère une pyramide après qu'un objet GeoRaster a été importé 
  dans la base de données. Le contenu de ce paramètre doit être une méthode de 
  réechentillonage parmi NN (nearest neighbor), BILINEAR, BIQUADRATIC, CUBIC, 
  AVERAGE4 ou AVERAGE16. Si GENPYRLEVELS n'est pas informée la fonction PL/SQL 
  *sdo_geor.generatePyramid* calculera le nombre de niveau à générer.
* **GENPYRLEVELS :** définie le nombre de niveau de pyramide à générer. Si 
  *GENPYRAMID* n'est pas définie la méthode de réechentillonage NN (nearest 
  neighbor) s'appliquera.
* **QUALITY :** option de la qualité de la compression pour le format JPEG de 0 
  à 100. 75 par défaut.
* **NBITS :** type de données sous byte, options : 1, 2 ou 4.
* **SPATIALEXTENT :** génère les étendus spatiales. La valeur par défaut est TRUE ce qui 
  signifie que cette option doit être informée pour forcer l'étendue spatiale à rester 
  NULL. Si EXTENTSRID n'est pas définie la géométrie de l'étendue spatiale sera générée 
  avec le même SRID que l'objet GeoGeoraster.
* **EXTENTSRID :** code SRID à utilisé la géoémtrie de l'étendue spatiale. Si la 
  table/colonne a déjà une étendue spatiale, la valeur définie doit être du même 
  SRID que pour l'étendue spatiale des autres GeoRaster existants.
* **OBJECTTABLE :** pour créer RDT en tant qu'objet SDO_RASTER mettez TRUE, la 
  valeur par défaut est FALSE et le RDT sera créé comme des tables relationnels 
  régulières. Cela ne s'applique pas au version d'Oracle inférieure à 11.

Importer des GeoRaster
=======================

Pendant le processus d'import de raster dans un objet GeoRaster il est possible 
de donner au pilote une simple définition de table SQL et également une clause 
de valeurs/insert SQL pour informer le pilote de la table à créer et les valeurs 
à ajouter aux nouvelles lignes. L'exemple suivant réalise cela :
::
    
    % gdal_translate -of georaster Newpor.tif georaster:scott/tiger,,landsat,scene \
    -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE MDSYS.SDO_GEORASTER)" \
    -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())" \
    -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" -co "BLOCKBSIZE=3" \
    -co "INTERLEAVE=PIXEL" -co "COMPRESS=JPEG-F"

Notez que l'option de création *DESCRIPTION* nécessite de donner le nom de la 
table (landsat). Le nom de la colonne (scene) doit correspondre à la description :
::
    
    % gdal_translate -of georaster landsat_1.tif georaster:scott/tiger,,landsat,scene \
    -co "DESCRIPTION=(ID NUMBER, SITE VARCHAR2(45), SCENE MDSYS.SDO_GEORASTER)" \
    -co "INSERT=VALUES(1,'West fields', SDO_GEOR.INIT())"

Si la table *landsat* existe, l'option *DESCRIPTION* est ignorée. Le pilote peut 
seulement mette à jour une colonne GeoRaster par commande ``gdal_translate``. 
Oracle créé des noms et valeurs par défauts pour RDT et RID pendant 
l'initialisation des objet *SDO_GEORASTER* mais les utilisateurs peuvent aussi 
définir un nom et une valeur de leur choix.
::
    
    % gdal_translate -of georaster landsat_1.tif georaster:scott/tiger,,landsat,scene \
    -co "INSERT=VALUES(10,'Main building', SDO_GEOR.INIT("RDT", 10))"

Si aucune information n'est données sur l'endroit où stocker le raster, le 
pilote créera (s'il n'existe pas déjà) une table par défaut nommée *GDAL_IMPORT* 
avec juste une colonne GeoRaster nommée *RASTER*, par exemple :
::
    
    % gdal_translate -of georaster input.tif “geor:scott/tiger@dbdemo”

Exporter des GeoRaster
=========================

Un GeoRaster peut être identifié par une clause Where ou par une pair de RDT & 
RID :
::
    
    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54 output.tif
    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,st_rdt_1,130 output.tif

Utilisation générale de GeoRaster
===================================

Les GeoRaster peuvent être utilisé dans n'importe quel ligne de commande GDAL 
avec toutes les options disponibles. Comme  une extraction d'une reprojection 
d'un sous jeu de données d'image :
::
    
    % gdal_translate -of gtiff geor:scott/tiger@dbdemo,landsat,scene,id=54 output.tif \
    -srcwin 0 0 800 600
    
    % gdalwarp -of png geor:scott/tiger@dbdemo,st_rdt_1,130 output.png -t_srs EPSG:9000913

Deux GeoRaster différents peuvent être utilisé comme entré et sortie lors de la 
même opération :
::
    
    % gdal_translate -of georaster geor:scott/tiger@dbdemo,landsat,scene,id=54 geor:scott/tiger@proj1,projview,image -co \
    INSERT="VALUES (102, SDO_GEOR.INIT())"

Les applications qui utilisent GDAL peuvent théoriquement lire et écrire du 
GeoRaster comme tout autre format mais la plupart d'entre eux sont plus enclins 
à tenter d'accéder aux fichiers sur le système de fichier donc une alternative 
est de créer un VRT pour représenter la description du GeoRaster, par exemple :
::
    
    % gdal_translate -of VRT geor:scott/tiger@dbdemo,landsat,scene,id=54 view_54.vrt
    % openenv view_54.vrt

.. yjacolin at free.fr, Yves Jacolin - 2014/09/02 (trunk 27629)
