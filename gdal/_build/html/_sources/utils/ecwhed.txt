.. _`gdal.utils.ecwhed`:

========
ecwhed
========

ECW header viewer and editor
SYNOPSIS

Usage:

ecwhed [--help]
       [--version]
       [-a_ullr ulx uly lrx lry]
       [-co "DATUM=VALUE"]
       [-co "PROJ=VALUE"]
       file

DESCRIPTION

The ecwhed utility is a viewer and editor for ECW files headers. The program can change the datum, projection and corner coordinates without decompressing and recompressing the image.

-a_ullr ulx uly lrx lry:
    Assign/override the georeferenced bounds of the output file. This assigns georeferenced bounds to the output file, ignoring what would have been derived from the source file.

-co "DATUM=VALUE":
    Assign/override the datum

-co "PROJ=VALUE":
    Assign/override the projection 

EXAMPLES

For instance, the georeferencing information contained in an ECW file can be displayed with a command like this:

ecwhed FRA-0100.ecw

Datum = NTF
Projection = LM2FRANC
Origin = (223000.000000, 2152500.000000)
Pixel Size = (100.000000, -100.000000)
Corner Coordinates:
Upper Left = (223000.000000, 2152500.000000)
Upper Right = (547500.000000, 2152500.000000)
Lower Left = (223000.000000, 1690000.000000)
Lower Right = (547500.000000, 1690000.000000)

For instance, an ECW file can be georeferenced with a command like this:

ecwhed -co "DATUM=NTF" -co "PROJ=LM2FRANC" -a_ullr 970000 1860000 980000 1850000 map.ecw

DOWNLOAD

The source code is available here : ecwhed-0.1.tar.gz . It is released under the GPL license version 2. To compile it, you will need the ECW SDK from ErMapper, that can be downloaded from the ErMapper web site.

Source : http://jrepetto.free.fr/ecwhed/

Last Revision : 02/07/2008
