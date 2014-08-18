.. _`gdal.gdal.gdalsrsinfo`:

gdalsrsinfo
============

Liste des informations sur les SRS données dans de nombreux formats (WKT, PROJ.4, etc.)

**Usage :**

::
	
	gdalsrsinfo [options] srs_def

*srs_def* peut être le nom du fichier d'un jeu de données géré par GDAL/OGR à partir duquel 
extraire les informations du SRS ou n'importe quelles formes habituelles de GDAL/OGR
(WKT complet, PROJ.4, EPSG:n ou un fichier contenant le SRS)

Options :

* **--help-general ou -h :** Affiche l'aide et quitte. 
* **-p :** Affichage lisible lorsque cela est possible (e.g. WKT)
* **-V :** Valide les SRS
* **-o out_type :** Type de sortie { default, all, wkt_all, proj4, wkt, wkt_simple, 
  wkt_noct, wkt_esri, mapinfo, xml }

Description
*************

La commande *gdalsrsinfo* renvoie des informations sur les SRS données à partir d'un des formats suviants :

* Le nom du fichier d'un jeu de données géré par GDAL/OGR qui contient des informations de SRS 
* N'importe quelles formes habituells de GDAL/OGR forms (WKT complet, PROJ.4, EPSG:n ou nu fichier contenant le SRS).

Types en sortie :

* *default* : proj4 et wkt (option par défaut)
* *all* : toutes les options disponibles
* *wkt_all* : toutes les options wkt disponible
* *proj4* : chaîne PROJ.4
* *wkt* : format WKT de l'OGC (complet)
* *wkt_simple* : WKT de l'OGC (simplifié)
* *wkt_noct* : WKT de l'OGC (sans les paramètres CT de l'OGC)
* *wkt_esri* : format WKT d'ESRI
* *mapinfo* : format CoordSys dans le style Mapinfo
* *xml* : format XML (basé sur GML)


Exemple
*********

::
	
	$  gdalsrsinfo   "EPSG:4326"

	PROJ.4 : '+proj=longlat +datum=WGS84 +no_defs '

	OGC WKT :
	0GEOGCS["WGS 84",
	    DATUM["WGS_1984",
	        SPHEROID["WGS 84",6378137,298.257223563,
	            AUTHORITY["EPSG","7030"]],
	        AUTHORITY["EPSG","6326"]],
	    PRIMEM["Greenwich",0,
	        AUTHORITY["EPSG","8901"]],
	    UNIT["degree",0.0174532925199433,
	        AUTHORITY["EPSG","9122"]],
	    AUTHORITY["EPSG","4326"]]

::
	
	$ gdalsrsinfo -o proj4 osr/data/lcc_esri.prj
	'+proj=lcc +lat_1=34.33333333333334 +lat_2=36.16666666666666 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +datum=NAD83 +units=m +no_defs '

::

	$ gdalsrsinfo -o proj4 landsat.tif
	PROJ.4 : '+proj=utm +zone=19 +south +datum=WGS84 +units=m +no_defs '

::
	
	$ gdalsrsinfo  -o wkt -p  "EPSG:32722"

	PROJCS["WGS 84 / UTM zone 22S",
	    GEOGCS["WGS 84",
	        DATUM["WGS_1984",
	            SPHEROID["WGS 84",6378137,298.257223563,
	                AUTHORITY["EPSG","7030"]],
	            AUTHORITY["EPSG","6326"]],
	        PRIMEM["Greenwich",0,
	            AUTHORITY["EPSG","8901"]],
	        UNIT["degree",0.0174532925199433,
	            AUTHORITY["EPSG","9122"]],
	        AUTHORITY["EPSG","4326"]],
	    PROJECTION["Transverse_Mercator"],
	    PARAMETER["latitude_of_origin",0],
	    PARAMETER["central_meridian",-51],
	    PARAMETER["scale_factor",0.9996],
	    PARAMETER["false_easting",500000],
	    PARAMETER["false_northing",10000000],
	    UNIT["metre",1,
	        AUTHORITY["EPSG","9001"]],
	    AXIS["Easting",EAST],
	    AXIS["Northing",NORTH],
	    AUTHORITY["EPSG","32722"]]
::
	
	$ gdalsrsinfo  -o wkt_all  "EPSG:4618"

	OGC WKT :
	GEOGCS["SAD69",
	    DATUM["South_American_Datum_1969",
	        SPHEROID["GRS 1967 Modified",6378160,298.25,
	            AUTHORITY["EPSG","7050"]],
	        TOWGS84[-57,1,-41,0,0,0,0],
	        AUTHORITY["EPSG","6618"]],
	    PRIMEM["Greenwich",0,
	        AUTHORITY["EPSG","8901"]],
	    UNIT["degree",0.0174532925199433,
	        AUTHORITY["EPSG","9122"]],
	    AUTHORITY["EPSG","4618"]]
	
	OGC WKT (simple) :
	GEOGCS["SAD69",
	    DATUM["South_American_Datum_1969",
	        SPHEROID["GRS 1967 Modified",6378160,298.25],
	        TOWGS84[-57,1,-41,0,0,0,0]],
	    PRIMEM["Greenwich",0],
	    UNIT["degree",0.0174532925199433]]
	
	OGC WKT (no CT) :
	GEOGCS["SAD69",
	    DATUM["South_American_Datum_1969",
	        SPHEROID["GRS 1967 Modified",6378160,298.25]],
	    PRIMEM["Greenwich",0],
	    UNIT["degree",0.0174532925199433]]
	
	ESRI WKT :
	GEOGCS["SAD69",
	    DATUM["D_South_American_1969",
	        SPHEROID["GRS_1967_Truncated",6378160,298.25]],
	    PRIMEM["Greenwich",0],
	    UNIT["Degree",0.017453292519943295]]


.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/gdal_merge.html Trunk r25410)
