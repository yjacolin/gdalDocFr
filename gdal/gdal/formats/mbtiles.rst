.. _`gdal.gdal.formats.mbtiles`:

=========
MBTiles
=========

.. versionadded:: 1.10 le pilote MBTiles permet de lire les rasters au format MBTiles, qui est 
   une spécification pour stocker des données cartographique tuilées dans des bases de données 
   SQLites.

GDAL/OGR doit être compilé avec la gestion du pilote SQLite, et des pilotes JPEG et PNG.

Le SRS esttoujours la projection Pseudo-Mercator (ie Google Mercator).

Le pilote peut récupéré les attributs des pixels encodés selon la spécification UTFGrid 
disponible dans certains fichiers MBTiles. Ils peuvent être obtenu avec la commande 
``gdallocationinfo`` ou avec l'appel *GetMetadataItem("Pixel_iCol_iLine", "LocationInfo")* 
sur un objet bande.

Exemples
=========

* Accéder à un raster MBTiles distant :

  ::
	
    $ gdalinfo /vsicurl/http://a.tiles.mapbox.com/v3/kkaefer.iceland.mbtiles

  Renvoie :

  ::
	
    Driver: MBTiles/MBTiles
    Files: /vsicurl/http://a.tiles.mapbox.com/v3/kkaefer.iceland.mbtiles
    Size is 16384, 16384
    Coordinate System is:
    PROJCS["WGS 84 / Pseudo-Mercator",
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
        PROJECTION["Mercator_1SP"],
        PARAMETER["central_meridian",0],
        PARAMETER["scale_factor",1],
        PARAMETER["false_easting",0],
        PARAMETER["false_northing",0],
        UNIT["metre",1,
            AUTHORITY["EPSG","9001"]],
        AXIS["X",EAST],
        AXIS["Y",NORTH],
        EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"],
        AUTHORITY["EPSG","3857"]]
    Origin = (-3757031.250000000000000,11271093.750000000000000)
    Pixel Size = (152.873992919921875,-152.873992919921875)
    Image Structure Metadata:
      INTERLEAVE=PIXEL
    Corner Coordinates:
    Upper Left  (-3757031.250,11271093.750) ( 33d44'59.95"W, 70d36'45.36"N)
    Lower Left  (-3757031.250, 8766406.250) ( 33d44'59.95"W, 61d36'22.97"N)
    Upper Right (-1252343.750,11271093.750) ( 11d14'59.98"W, 70d36'45.36"N)
    Lower Right (-1252343.750, 8766406.250) ( 11d14'59.98"W, 61d36'22.97"N)
    Center      (-2504687.500,10018750.000) ( 22d29'59.97"W, 66d30'47.68"N)
    Band 1 Block=256x256 Type=Byte, ColorInterp=Red
      Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Mask Flags: PER_DATASET ALPHA
      Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
    Band 2 Block=256x256 Type=Byte, ColorInterp=Green
      Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Mask Flags: PER_DATASET ALPHA
      Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
    Band 3 Block=256x256 Type=Byte, ColorInterp=Blue
      Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
      Mask Flags: PER_DATASET ALPHA
      Overviews of mask band: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512
    Band 4 Block=256x256 Type=Byte, ColorInterp=Alpha
      Overviews: 8192x8192, 4096x4096, 2048x2048, 1024x1024, 512x512

* Lire des attributs de pixel encodés selon la spécification UTFGrid :
  ::
	
    $ gdallocationinfo /vsicurl/http://a.tiles.mapbox.com/v3/mapbox.geography-class.mbtiles -wgs84 2 49 -b 1 -xml

  Renvoie :

  ::
	
	<Report pixel="33132" line="22506">
	      <BandReport band="1">
	        <LocationInfo>
	          <Key>74</Key>
	          <JSon>{"admin":"France","flag_png":"iVBORw0KGgoAAAANSUhEUgAAAGQAAABDEAIAAAC1uevOAAAACXBIWXMAAABIAAAASABGyWs+AAAABmJLR0T///////8JWPfcAAABPklEQVR42u3cMRLBQBSA4Zc9CgqcALXC4bThBA5gNFyFM+wBVNFqjYTszpfi1Sm++bOv2ETEdNK2pc/T9ny977rCn+fx8rjtc7dMmybnxXy9KncGWGCBBRZYYIEFFlhggQUWWGCBBRZYYIE1/GzSLB0CLLAUCyywwAILLLDAAgsssGyFlcAqnJRiKRZYYIEFFlhggQUWWGDZCsFSLLDAAgsssP4DazQowVIssMACy1ZYG6wP30qxwFIssMACCyywwOr/HAYWWIplKwQLLLDAAgssZyywwAILLLDAqh6We4VgKZatECywFAsssMACCyywwAILLLBshWCBpVhggQUWWGCBBRZYYIFlKwQLLMUCCyywwAILLLBG+T8ZsMBSLFshWIoFFlhg/fp8BhZYigUWWGB9C+t9ggUWWGD5FA44XxBz7mcwZM9VAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDExLTA5LTAyVDIzOjI5OjIxLTA0OjAwcQbBWgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxMS0wMi0yOFQyMTo0ODozMS0wNTowMJkeu+wAAABSdEVYdHN2ZzpiYXNlLXVyaQBmaWxlOi8vL2hvbWUvYWovQ29kZS90bS1tYXN0ZXIvZXhhbXBsZXMvZ2VvZ3JhcGh5LWNsYXNzL2ZsYWdzL0ZSQS5zdmen2JoeAAAAAElFTkSuQmCC"}</JSon>
	        </LocationInfo>
	        <Value>238</Value>
	      </BandReport>
	    </Report>

.. seealso::

   * `Spécification MBTiles <https://github.com/mapbox/mbtiles-spec>`_
   * `Spécification UTFGrid  <https://github.com/mapbox/utfgrid-spec/blob/master/1.0/utfgrid.md>`_

 
.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (Trunk r25229)
