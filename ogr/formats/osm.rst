.. _`gdal.ogr.formats.osm`:

OSM - OpenStreetMap XML and PBF
(GDAL/OGR >= 1.10.0)

This driver reads OpenStreetMap files, in .osm (XML based) and .pbf (optimized binary) formats.

The driver is available if GDAL is built with SQLite support and, for .osm XML files, with Expat support.

The filenames must end with .osm or .pbf extension.

The driver will categorize features into 5 layers :

    points : "node" features that have significant tags attached.
    lines : "way" features that are recognized as non-area.
    multilinestrings : "relation" features that form a multilinestring(type = 'multilinestring' or type = 'route').
    multipolygons : "relation" features that form a multipolygon (type = 'multipolygon' or type = 'boundary'), and "way" features that are recognized as area.
    other_relations : "relation" features that do not belong to the above 2 layers.

Configuration
In the data folder of the GDAL distribution, you can find a osmconf.ini file that can be customized to fit your needs. You can also define an alternate path with the OSM_CONFIG_FILE configuration option.

The customization is essentially which OSM attributes and keys should be translated into OGR layer fields.

Starting with GDAL 2.0, fields can be computed with SQL expressions (evaluated by SQLite engine) from other fields/tags. For example to compute the z_order attribute.

"other_tags" field
When keys are not strictly identified in the `osmconf.ini <http://svn.osgeo.org/gdal/trunk/gdal/data/osmconf.ini>`_ file, the key/value pair is appended in a "other_tags" field, with a syntax compatible with the PostgreSQL HSTORE type. See the COLUMN_TYPES layer creation option of the `PG driver <http://www.gdal.org/drv_pg.html>`_.

For example :

ogr2ogr -f PostgreSQL "PG:dbname=osm" test.pbf -lco COLUMN_TYPES=other_tags=hstore

"all_tags" field
(OGR >= 1.11)

Similar to "other_tags", except that it contains both keys specifically identified to be reported as dedicated fields, as well as other keys.

"all_tags" is disabled by default, and when enabled, it is exclusive with "other_tags".
Internal working and performance tweaking
The driver will use an internal SQLite database to resolve geometries. If that database remains under 100 MB it will reside in RAM. If it grows above, it will be written in a temporary file on disk. By default, this file will be written in the current directory, unless you define the CPL_TMPDIR configuration option. The 100 MB default threshold can be adjusted with the OSM_MAX_TMPFILE_SIZE configuration option (value in MB).

For indexation of nodes, a custom mechanism not relying on SQLite is used by default (indexation of ways to solve relations is still relying on SQLite). It can speed up operations significantly. However, in some situations (non increasing node ids, or node ids not in expected range), it might not work and the driver will output an error message suggesting to relaunch by defining the OSM_USE_CUSTOM_INDEXING configuration option to NO.

When custom indexing is used (default case), the OSM_COMPRESS_NODES configuration option can be set to YES (the default is NO). This option might be turned on to improve performances when I/O access is the limiting factor (typically the case of rotational disk), and will be mostly efficient for country-sized OSM extracts where compression rate can go up to a factor of 3 or 4, and help keep the node DB to a size that fit in the OS I/O caches. For whole planet file, the effect of this option will be less efficient. This option consumes addionnal 60 MB of RAM.

Interleaved reading
Due to the nature of OSM files and how the driver works internally, the default reading mode might not work correctly, because too many features will accumulate in the layers before being consummed by the user application. For large files, applications should set the OGR_INTERLEAVED_READING=YES configuration option to turn on a special reading mode where the following reading pattern must be used :

    int bHasLayersNonEmpty;
    do
    {
        bHasLayersNonEmpty = FALSE;

        for( int iLayer = 0; iLayer < poDS->GetLayerCount(); iLayer++ )
        {
            OGRLayer *poLayer = poDS->GetLayer(iLayer);

            OGRFeature* poFeature;
            while( (poFeature = poLayer->GetNextFeature()) != NULL )
            {
                bHasLayersNonEmpty = TRUE;
                OGRFeature::DestroyFeature(poFeature);
            }
        }
    }
    while( bHasLayersNonEmpty );

Note : the ogr2ogr application has been modified to use that OGR_INTERLEAVED_READING mode without any particular user action.

Reading .osm.bz2 files and/or online files
.osm.bz2 are not natively recognized, however you can process them (on Unix), with the following command :

bzcat my.osm.bz2 | ogr2ogr -f SQLite my.sqlite /vsistdin/

You can convert a .osm or .pbf file without downloading it :

wget -O - http://www.example.com/some.pbf | ogr2ogr -f SQLite my.sqlite /vsistdin/

or

ogr2ogr -f SQLite my.sqlite /vsicurl_streaming/http://www.example.com/some.pbf -progress

And to combine the above steps :

wget -O - http://www.example.com/some.osm.bz2 | bzcat | ogr2ogr -f SQLite my.sqlite /vsistdin/

.. seealso::

* `OpenStreetMap home page <http://www.openstreetmap.org/>`_
* `OSM XML Format description <http://wiki.openstreetmap.org/wiki/OSM_XML>`_
* `OSM PBF Format description <http://wiki.openstreetmap.org/wiki/PBF_Format>`_

.. yjacolin at free.fr, Yves Jacolin 2014/11/08 (Trunk 27932)