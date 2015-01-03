`gdal.gdal.formats.geopackage` 

http://www.gdal.org/drv_geopackage_raster.html

====================
GeoPackage raster
====================

Starting with GDAL 2.0, this driver implements full read/creation/update of tables containing raster tiles in the OGC GeoPackage format standard. The GeoPackage standard uses a SQLite database file as a generic container, and the standard defines:

    Expected metadata tables (gpkg_contents, gpkg_spatial_ref_sys, gpkg_tile_matrix, gpkg_tile_matrix_set, ...)
    Tile format encoding (PNG and JPEG for base specification, WebP as extension) and tiling conventions
    Naming and conventions for extensions

This driver reads and writes SQLite files from the file system, so it must be run by a user with read/write access to the files it is working with.

The driver can also handle GeoPackage vectors. See GeoPackage vector documentation page

Various kind of input datasets can be converted to GeoPackage raster :

    Single band grey level
    Single band with R,G,B or R,G,B,A color table
    Two bands: first band with grey level, second band with alpha channel
    Three bands: Red, Green, Blue
    Four band: Red, Green, Blue, Alpha

GeoPackage rasters only support Byte data type.

All raster extensions standardized by the GeoPackage specification are supported in read and creation :

    gpkg_webp: when storing WebP tiles, provided that GDAL is compiled against libwebp.
    gpkg_zoom_other: when resolution of consecutive zoom levels does not vary with a factor of 2.

Opening options

By default, the driver will expose a GeoPackage dataset as a four band (Red,Green, Blue,Alpha) dataset, which gives the maximum compatibility with the various encodings of tiles that can be stored. It is possible to specify an explicit number of bands with the BAND_COUNT opening option.

The driver will use the geographic/projected extent indicated in the gpkg_contents table, and do necessary clipping, if needed, to respect that extent. However that information being optional, if omitted, the driver will use the extent provided by the gpkg_tile_matrix_set, which covers the extent at all zoom levels. The user can also specify the USE_TILE_EXTENT=YES open option to use the actual extent of tiles at the maximum zoom level. Or it can specify any of MINX/MINY/MAXX/MAXY to have a custom extent.

The following open options are available:

    TABLE=table_name: Name of the table containing the tiles (called "Tile Pyramid User Data Table" in the GeoPackage specification language). If the GeoPackage dataset only contains one table, this option is not necessary. Otherwise, it is required.
    ZOOM_LEVEL=value: Integer value between 0 and the maximum filled in the gpkg_tile_matrix table. By default, the driver will select the maximum zoom level, such as at least one tile at that zoom level is found in the raster table.
    BAND_COUNT=1/2/3/4: Number of bands of the dataset exposed after opening. Some conversions will be done when possible and implemented, but this might fail in some cases, depending on the BAND_COUNT value and the number of bands of the tile. Defaults to 4 (which is the always safe value).
    MINX=value: Minimum longitude/easting of the area of interest.
    MINY=value: Minimum latitude/northing of the area of interest.
    MAXX=value: Maximum longitude/easting of the area of interest.
    MAXY=value: Maximum latitude/northing of the area of interest.
    USE_TILE_EXTENT=YES/NO: Whether to use the extent of actual existing tiles at the zoom level of the full resolution dataset. Defaults to NO.
    TILE_FORMAT=PNG_JPEG/PNG/PNG8/JPEG/WEBP: Format used to store tiles. See Tile format section. Only used in update mode. Defaults to PNG_JPEG.
    QUALITY=1-100: Quality setting for JPEG and WEBP compression. Only used in update mode. Default to 75.
    ZLEVEL=1-9: DEFLATE compression level for PNG tiles. Only used in update mode. Default to 6.
    DITHER=YES/NO: Whether to use Floyd-Steinberg dithering (for TILE_FORMAT=PNG8). Only used in update mode. Defaults to NO.

Note: open options are typically specified with "-oo name=value" syntax in most GDAL utilities, or with the GDALOpenEx() API call.
Creation issues

Depending of the number of bands of the input dataset and the tile format selected, the driver will do the necessary conversions to be compatible with the tile format.

To add several tile tables to a GeoPackage dataset (seen as GDAL subdatasets), or to add a tile table to an existing vector-only GeoPackage, the generic APPEND_SUBDATASET=YES creation option must be provided.

Fully transparent tiles will not be written to the database, as allowed by the format.

The driver implements the Create() and IWriteBlock() methods, so that arbitrary writing of raster blocks is possible, enabling the direct use of GeoPackage as the output dataset of utilities such as gdalwarp.

On creation, raster blocks can be written only if the geotransformation matrix has been set with SetGeoTransform() This is effectively needed to determine the zoom level of the full resolution dataset based on the pixel resolution, dataset and tile dimensions.

Technical/implementation note: when a dataset is opened with a non-default area of interest (i.e. use of MINX,MINY,MAXX,MAXY or USE_TILE_EXTENT open option), or when creating/ opening a dataset with a non-custom tiling scheme, it is possible that GDAL blocks do not exactly match a single GeoPackage tile. In which case, each GDAL block will overlap four GeoPackage tiles. This is easily handled on the read side, but on creation/update side, such configuration could cause numerous decompression/ recompression of tiles to be done, which might cause unnecessary quality loss when using lossy compression (JPEG, WebP). To avoid that, the driver will create a temporary database next to the main GeoPackage file to store partial GeoPackage tiles in a lossless (and uncompressed) way. Once a tile has received data for its four quadrants and for all the bands (or the dataset is closed or explicitely flushed with FlushCache()), those uncompressed tiles are definitely transfered to the GeoPackage file with the appropriate compression. All of this is transparent to the user of GDAL API/utilities
Tile formats

GeoPackage can store tiles in different formats, PNG and/or JPEG for the baseline specification, and WebP for extended GeoPackage. Support for those tile formats depend if the underlying drivers are available in GDAL, which is generally the case for PNG and JPEG, but not necessarily for WebP since it requires GDAL to be compiled against the optional libwebp.

By default, GDAL will use a mix of PNG and JPEG tiles. PNG tiles will be used to store tiles that are not completely opaque, either because input dataset has an alpha channel with non fully opaque content, or because tiles are partial due to clipping at the right or bottom edges of the raster, or when a dataset is opened with a non-default area of interest, or with a non-custom tiling scheme. On the contrary, for fully opaque tiles, JPEG format will be used.

It is possible to select one unique tile format by setting the creation/open option TILE_FORMAT to one of PNG, JPEG or WEBP. When using JPEG, the alpha channel will not be stored. When using WebP, the gpkg_webp extension will be registered. The lossy compression of WebP is used. Note that a recent enough libwebp (>=0.1.4) must be used to support alpha channel in WebP tiles.

PNG8 can be selected to use 8-bit PNG with a color table up to 256 colors. On creation, an optimized color table is computed for each tile. The DITHER option can be set to YES to use Floyd/Steinberg dithering algorithm, which spreads the quantization error on neighbouring pixels for better rendering (note however than when zooming in, this can cause non desirable visual artifacts). Setting it to YES will generally cause less effective compression. Note that at that time, such an 8-bit PNG formulation is only used for fully opaque tiles, as the median-cut algorithm currently implemented to compute the optimal color table does not support alpha channel (even if PNG8 format would potentially allow color table with transparency). So when selecting PNG8, non fully opaque tiles will be stored as 32-bit PNG.
Tiling schemes

By default, conversion to GeoPackage will create a custom tiling scheme, such that the input dataset can be losslessly converted, both at the pixel and georeferencing level (if using a lossless tile format such as PNG). That tiling scheme is such that its origin (min_x, max_y) in the gpkg_tile_matrix_set table perfectly matches the top left corner of the dataset, and the selected resolution (pixel_x_size, pixel_y_size) at the computed maximum zoom_level of the gpkg_tile_matrix table will match the pixel width and height of the raster.

However to ease interoperability with other implementations, and enable use of GeoPackage with tile servicing software, it is possible to select a predefined tiling scheme that has world coverage. The available tiling schemes are :

    GoogleCRS84Quad, as described in OGC 07-057r7 WMTS 1.0 specification, Annex E.3. That tiling schemes consists of a single 256x256 tile at its zoom level 0, in EPSG:4326 CRS, with extent in longitude and latitude in the range [-180,180]. Consequently, at zoom level 0, 64 lines are unused at the top and bottom of that tile. This may cause issues with some implementations of the specification, and there are some ambiguities about the exact definition of this tiling scheme. Using InspireCRS84Quad/PseudoTMS_GlobalGeodetic instead is therefore recommended.
    GoogleMapsCompatible, as described in WMTS 1.0 specification, Annex E.4. That tiling schemes consists of a single 256x256 tile at its zoom level 0, in EPSG:3857 CRS, with extent in easting and northing in the range [-20037508.34,20037508.34].
    InspireCRS84Quad, as described in Inspire View Services. That tiling schemes consists of two 256x256 tiles at its zoom level 0, in EPSG:4326 CRS, with extent in longitude in the range [-180,180] and in latitude in the range [-90,90].
    PseudoTMS_GlobalGeodetic, based on the global-geodetic profile of OSGeo TMS (Tile Map Service) specification. This has exactly the same definition as InspireCRS84Quad tiling scheme. Note however that full interoperability with TMS is not possible due to the origin of numbering of tiles being the top left corner in GeoPackage (consistently with WMTS convention), whereas TMS uses the bottom left corner as origin.
    PseudoTMS_GlobalMercator, based on the global-mercator profile of OSGeo TMS (Tile Map Service) specification. That tiling schemes consists of four 256x256 tiles at its zoom level 0, in EPSG:3857 CRS, with extent extent in easting and northing in the range [-20037508.34,20037508.34]. The same remark as with PseudoTMS_GlobalGeodetic applies regarding interoperability with TMS.

In all the above tiling schemes, consecutive zoom levels defer by a resolution of a factor of two.
Creation options

The following creation options are available:

    RASTER_TABLE=string. Name of tile user table. By default, based on the filename (i.e. if filename is foo.gpkg, the table will be called "foo").
    APPEND_SUBDATASET=YES/NO: If set to YES, an existing GeoPackage will not be priorly destroyed, such as to be able to add new content to it. Defaults to NO.
    RASTER_IDENTIFIER=string. Human-readable identifier (e.g. short name), put in the identifier column of the gpkg_contents table.
    RASTER_DESCRIPTION=string. Human-readable description, put in the description column of the gpkg_contents table.
    BLOCKSIZE=integer. Block size in width and height in pixels. Defaults to 256. Maximum supported is 4096. Should not be set when using a non-custom TILING_SCHEME.
    BLOCKXSIZE=integer. Block width in pixels. Defaults to 256. Maximum supported is 4096.
    BLOCKYSIZE=integer. Block height in pixels. Defaults to 256. Maximum supported is 4096.
    TILE_FORMAT=PNG_JPEG/PNG/PNG8/JPEG/WEBP: Format used to store tiles. See Tile formats section. Defaults to PNG_JPEG.
    QUALITY=1-100: Quality setting for JPEG and WEBP compression. Default to 75.
    ZLEVEL=1-9: DEFLATE compression level for PNG tiles. Default to 6.
    DITHER=YES/NO: Whether to use Floyd-Steinberg dithering (for TILE_FORMAT=PNG8). Defaults to NO.
    TILING_SCHEME=CUSTOM/GoogleCRS84Quad/GoogleMapsCompatible/InspireCRS84Quad/PseudoTMS_GlobalGeodetic/PseudoTMS_GlobalMercator. See Tiling schemes section. Defaults to CUSTOM.
    ZOOM_LEVEL_STRATEGY=AUTO/LOWER/UPPER. Strategy to determine zoom level. Only used for TILING_SCHEME is different from CUSTOM. LOWER will select the zoom level immediately below the theoretical computed non-integral zoom level, leading to subsampling. On the contrary, UPPER will select the immedately above zoom level, leading to oversampling. Defaults to AUTO which selects the closest zoom level.
    RESAMPLING=NEAREST/BILINEAR/CUBIC/CUBICSPLINE/LANCZOS/MODE/AVERAGE. Resampling algorithm. Only used for TILING_SCHEME is different from CUSTOM. Defaults to BILINEAR.

Overviews

gdaladdo / BuildOverviews() can be used to compute overviews. Power-of-two overview factors (2,4,8,16,...) should be favored to be conformant with the baseline GeoPackage specification. Use of other overview factors will work with the GDAL driver, and cause the gpkg_zoom_other extension to be registered, but that could potentially cause interoperability problems with other implementations that do not support that extension.

Overviews can also be cleared with the -clean option of gdaladdo (or BuildOverviews() with nOverviews=0)
Metadata

GDAL uses the standardized gpkg_metadata and gpkg_metadata_reference tables to read and write metadata.

GDAL metadata, from the default metadata domain and possibly other metadata domains, is serialized in a single XML document, conformant with the format used in GDAL PAM (Persistent Auxiliary Metadata) .aux.xml files, and registered with md_scope=dataset and md_standard_uri=http://gdal.org in gpkg_metadata. In gpkg_metadata_reference, this entry is referenced with a reference_scope=table and table_name={name of the raster table}

It is possible to read and write metadata that applies to the global GeoPackage, and not only to the raster table, by using the GEOPACKAGE metadata domain.

Metadata not originating from GDAL can be read by the driver and will be exposed as metadata items with keys of the form GPKG_METADATA_ITEM_XXX and values the content of the metadata columns of the gpkg_metadata table. Update of such metadata is not currently supported through GDAL interfaces ( although it can be through direct SQL commands).

The specific DESCRIPTION and IDENTIFIER metadata item of the default metadata domain can be used in read/write to read from/update the corresponding columns of the gpkg_contents table.
Examples

    Simple translation of a GeoTIFF into GeoPackage. The table 'byte' will be created with the tiles.

    % gdal_translate -of GPKG byte.tif byte.gpkg

    Translation of a GeoTIFF into GeoPackage using WebP tiles

    % gdal_translate -of GPKG byte.tif byte.gpkg -co TILE_FORMAT=WEBP

    Translation of a GeoTIFF into GeoPackage using GoogleMapsCompatible tiling scheme (with reprojection and resampling if needed)

    % gdal_translate -of GPKG byte.tif byte.gpkg -co TILING_SCHEME=GoogleMapsCompatible

    Building of overviews of an existing GeoPackage

    % gdaladdo -r cubic my.gpkg 2 4 8 16 32 64

    Addition of a new subdataset to an existing GeoPackage, and choose a non default name for the raster table.

    % gdal_translate -of GPKG new.tif existing.gpkg -co APPEND_SUBDATASET=YES -co RASTER_TABLE=new_table

    Reprojection of an input dataset to GeoPackage

    % gdalwarp -of GPKG in.tif out.gpkg -t_srs EPSG:3857

    Open a specific raster table in a GeoPackage

    % gdalinfo my.gpkg -oo TABLE=a_table

.. seealso::

    SQLite
    GeoPackage vector documentation page
    PNG driver documentation page
    JPEG driver documentation page
    WEBP driver documentation page
    OGC 07-057r7 WMTS 1.0 specification
    OSGeo TMS (Tile Map Service) specification

Other notes
===========

Development of raster support in the GeoPackage driver was financially supported by Safe Software.