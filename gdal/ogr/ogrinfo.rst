.. _`gdal.ogr.ogrinfo`:

ogrinfo
========

Listes des informations sur une source de données géré par OGR.

Usage
------

::
    
    ogrinfo [--help-general] [-ro] [-q] [-where restricted_where]
          [-spat xmin ymin xmax ymax] [-fid fid]
          [-sql statement] [-dialect dialect] [-al] [-so] [-fields={YES/NO}]
          [-geom={YES/NO/SUMMARY}][--formats]
          datasource_name [layer [layer ...]]

Le programme ``ogrinfo`` liste diverses informations sur la source de données 
gérée par OGR vers la sortie standard (le terminal).

* **-ro :** ouvre la source de données en lecture seule. 
* **-al :** liste tous les objets de toutes les couches (utilisé à la place de 
  fournir des noms de couche comme arguments). 
* **-so`` / ``Summary Only :** supprime la liste des objets, affiche seulement 
  les informations comme la projection, le schéma, le nombre d'objets et l'étendue.
* **-q :** Rapport d'informations diverses en mode silence, incluant le système 
  de coordonnées, le schéma de la couche, l'étendue et le nombre d'objets.
* **-where restricted_where :** un requête attributaire dans une forme 
  restreinte sous la forme de requête SQL WHERE. Seulement les objets 
  correspondant à la requête attributaire seront renvoyés.
* **-sql statement :** exécute la requête SQL indiquée et retourne le résultat.
* **-spat xmin ymin xmax ymax :** la zone d'intérêt. Seulement les objets à 
  l'intérieur du rectangle seront renvoyés.
* **-fid fid :** si fournit, seulement les objets avec cet identifiant seront 
  renvoyés. Fonctionnement exclusif aux requêtes attributaire ou SQL.
   
  .. note::
    si vous voulez sélectionner plusieurs features basées sur leur feature_id, 
    vous pouvez également utilisé le fait que le 'fid' est un champ spécial 
    reconnu par .  le SQL d'OGR. Donc, '-where "fid in (1,3,5)"' sélectionnera 
    les features 1, 3 et 5.
* **-fields={YES/NO} :** (à partir de GDAL 1.6.0) Si définie à *NO*, le dump 
  des feature n'affichera pas les valeurs des champs. La valeur par défaut est 
  *YES*.
* **-geom={YES/NO/SUMMARY} :** (à partir de GDAL 1.6.0) Si définie à *NO*, le 
  dump des feature n'affichera pas les géométries. Si définie à *SUMMARY*, seul 
  le résumé des géométries sera affiché. Si définie à *YES*, la géométrie sera 
  rapporté au format WKT complet de l'OGC. La valeur par défaut est *YES*.
* **--formats :** liste les pilotes des formats qui sont activés.
* **datasource_name :** La source de données à ouvrir. Peut être un nom de 
  fichier, un répertoire ou un autre nom virtuel. Regardez la liste des formats 
  vecteurs OGR pour les sources de données gérées.
* **layer :** une ou plusieurs noms de couches peuvent être reportés.

Si aucun nom de couches n'est passé, alors ``ogrinfo`` renverra une liste de 
couches disponibles (et leur type géométrique). Si le(s) nom(s) des couches est 
passé alors leurs étendues, système de coordonnées, le nombre d'objet ; le type 
géométrique, le schéma et toutes les géométries correspondant aux requêtes des 
paramètres seront renvoyés vers le terminal. Si aucun paramètre de requête n'est 
fourni, toutes les géométries seront renvoyées.

Les géométries sont renvoyées au format WKT de l'OGC.

Exemple retournant toutes les couches d'un fichier NTF :
::
    
    % ogrinfo wrk/SHETLAND_ISLANDS.NTF
    INFO: Open of `wrk/SHETLAND_ISLANDS.NTF'
    using driver `UK .NTF' successful.
    1: BL2000_LINK (Line String)
    2: BL2000_POLY (None)
    3: BL2000_COLLECTIONS (None)
    4: FEATURE_CLASSES (None)

Exemple en utilisant une requête pour restreindre la sortie des objets d'une 
couche :
::
    
    % ogrinfo -ro -where 'GLOBAL_LINK_ID=185878' wrk/SHETLAND_ISLANDS.NTF BL2000_LINK
    INFO: Open of `wrk/SHETLAND_ISLANDS.NTF'
    using driver `UK .NTF' successful.
    
    Layer name: BL2000_LINK
    Geometry: Line String
    Feature Count: 1
    Extent: (419794.100000, 1069031.000000) - (419927.900000, 1069153.500000)
    Layer SRS WKT:
    PROJCS["OSGB 1936 / British National Grid",
        GEOGCS["OSGB 1936",
            DATUM["OSGB_1936",
                SPHEROID["Airy 1830",6377563.396,299.3249646]],
            PRIMEM["Greenwich",0],
            UNIT["degree",0.0174532925199433]],
        PROJECTION["Transverse_Mercator"],
        PARAMETER["latitude_of_origin",49],
        PARAMETER["central_meridian",-2],
        PARAMETER["scale_factor",0.999601272],
        PARAMETER["false_easting",400000],
        PARAMETER["false_northing",-100000],
        UNIT["metre",1]]
    LINE_ID: Integer (6.0)
    GEOM_ID: Integer (6.0)
    FEAT_CODE: String (4.0)
    GLOBAL_LINK_ID: Integer (10.0)
    TILE_REF: String (10.0)
    OGRFeature(BL2000_LINK):2
        LINE_ID (Integer) = 2
        GEOM_ID (Integer) = 2
        FEAT_CODE (String) = (null)
        GLOBAL_LINK_ID (Integer) = 185878
        TILE_REF (String) = SHETLAND I
        LINESTRING (419832.100 1069046.300,419820.100 1069043.800,419808.300
        1069048.800,419805.100 1069046.000,419805.000 1069040.600,419809.400
        1069037.400,419827.400 1069035.600,419842 1069031,419859.000
        1069032.800,419879.500 1069049.500,419886.700 1069061.400,419890.100
        1069070.500,419890.900 1069081.800,419896.500 1069086.800,419898.400
        1069092.900,419896.700 1069094.800,419892.500 1069094.300,419878.100
        1069085.600,419875.400 1069087.300,419875.100 1069091.100,419872.200
        1069094.600,419890.400 1069106.400,419907.600 1069112.800,419924.600
        1069133.800,419927.900 1069146.300,419927.600 1069152.400,419922.600
        1069153.500,419917.100 1069153.500,419911.500 1069153.000,419908.700
        1069152.500,419903.400 1069150.800,419898.800 1069149.400,419894.800
        1069149.300,419890.700 1069149.400,419890.600 1069149.400,419880.800
        1069149.800,419876.900 1069148.900,419873.100 1069147.500,419870.200
        1069146.400,419862.100 1069143.000,419860 1069142,419854.900
        1069138.600,419850 1069135,419848.800 1069134.100,419843
        1069130,419836.200 1069127.600,419824.600 1069123.800,419820.200
        1069126.900,419815.500 1069126.900,419808.200 1069116.500,419798.700
        1069117.600,419794.100 1069115.100,419796.300 1069109.100,419801.800
        1069106.800,419805.000  1069107.300)

.. yjacolin at free.fr, Yves Jacolin - 2010/12/30 14:25 (http://www.gdal.org/ogrinfo.html Trunk 21366)
