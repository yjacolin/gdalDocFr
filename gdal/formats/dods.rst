.. _`gdal.gdal.formats.dods`:

=============================
DODS -- OPeNDAP Grid Client
=============================

GDAL inclut en option la gestion en lecture des grilles 2D et des tableaux via 
le protocole OPeNDAP (DODS).

Dénomination des jeux de données
==================================

La spécification complète du nom des jeux de données consiste en une URL du jeu 
de données OPeNDAP, le chemin complet vers le tableau désiré ou la variable 
grille, et un indicateur des indices du tableau à accéder.

Par exemple, si l'url http://maps.gdal.org/daac-bin/nph-hdf/3B42.HDF.dds renvoie 
une définition DDS comme celle-ci :
::
    
    Dataset {
    Structure {
        Structure {
        Float64 percipitate[scan = 5][longitude = 360][latitude = 80];
        Float64 relError[scan = 5][longitude = 360][latitude = 80];
        } PlanetaryGrid;
    } DATA_GRANULE;
    } 3B42.HDF;

alors la grille peut être accéder en utilisant le nom du jeu de données suivant 
dans GDAL :

http://maps.gdal.org/daac-bin/nph-hdf/3B42.HDF?DATA_GRANULE.PlanetaryGrid.percipitate[0][x][y]

Le chemin complet vers la grille ou le tableau à accéder nécessite d'être 
définie (sans compter le nom du jeu de données extérieur). GDAL doit savoir 
quels indices du tableau correspond au x (longitude ou coordonnées à l'est). 
Toutes les autres dimensions nécessite d'être limité à une valeur seule.

Dans le cas de serveurs de données avec seulement des tableaux 2D et des grilles 
comme enfant immédiat du jeu de données il peut ne pas être nécessaire de nommer 
grille ou la variable tableau.

Dans les cas où il y a un grand nombre de tableaux 2D ou de grilles au niveau du 
jeu de données, ils peuvent être chacun automatiquement traité comme bandes 
séparées.


Méta-données spécialisées AIS/DAS
====================================

Diverses informations seront transportées via le DAS décrivant le jeu de données. 
Certains pilotes DODS (tels que celui basé sur GDAL) retourne déjà les 
informations DAS suivantes mais dans d'autres cas il peut être fournie localement 
en utilisant le mécanisme AIX. Lisez la documentation sur DODS pour les détails 
du fonctionnement du mécanisme AIS.
::
    
    Attributes {

        GLOBAL { 
            Float64 Northernmost_Northing 71.1722;
            Float64 Southernmost_Northing  4.8278;
            Float64	Easternmost_Easting  -27.8897;
            Float64	Westernmost_Easting -112.11;
            Float64 GeoTransform "71.1722 0.001 0.0 -112.11 0.0 -0.001";
            String spatial_ref "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433]]";
            Metadata { 
            String TIFFTAG_XRESOLUTION "400";
            String TIFFTAG_YRESOLUTION "400";
            String TIFFTAG_RESOLUTIONUNIT "2 (pixels/inch)";
            }
        }

        band_1 {
            String Description "...";
            String 
        }
    }


Jeu de données
***************

Il y aura un objet dans le DAS nommé GLOBAL contenant les attributs du jeu de 
données dans l'ensemble.

Il possède les sous-items suivants :

* **Northernmost_Northing :** La latitude ou la valeur la plus au nord du bord 
  au nord de l'image.
* **Southernmost_Northing :** La latitude ou la valeur la plus au nord du bord 
  au sud de l'image.
* **Easternmost_Easting :** La longitude ou la valeur la plus à l'est du bord à 
  l'ouest de l'image.
* **Westernmost_Easting :** La longitude ou la valeur la plus à l'est du bord à 
  l'est de l'image.
* **GeoTransform :** Les six paramètres définissant la transformation affine 
  entre les pixels/l'espacement des lignes et l'espace géoréférencé si 
  applicable. Stocké comme un chaîne de caractère simple avec des valeurs 
  séparées par des espaces. Notez que cela permet des images en rotation ou 
  inclinées (optionnel)
* **SpatialRef :** La descriptions OpenGIS WKT du système de coordonnées. Si 
  absente, il sera supposé que le système de coordonnées est le WGS84. 
  (optionnel)
* **Metadata :** un conteneur avec une liste d'attributs de chaînes de 
  caractères pour chaque item de méta-données disponible. Le nom du mot-clé de 
  l'item de la méta-données sera utilisé comme nom d'attribut. Les valeurs des 
  méta-données seront toujours nue chaîne. (optionnel)
* address GCPs

Notez que les valeurs des bords nord et est peuvent être calculé à partir de la 
taille de la grille et de la transformation géométrique. Ils sont d'abord inclus 
comme documentation supplémentaire qui est plus facile à interpréter par 
l'utilisateur que la transformation géométrique. Ils seront également utilisé 
pour calculer une transformation géométrique interne si l'une d'elle n'est pas 
fournit, mais si les deux sont fournit la transformation géométrique prendra le dessus.

Bande
******

Il y aura un objet dans le DAS nommé après chaque bande contenant des attributs 
d'une bande spécifique.

Il aura les sous-items suivants :

* **Metadata :** un conteneur avec une liste d'attributs de chaîne pour chaque 
  item de méta-données disponilbe. Le nom du mot-clés de l'item de la 
  méta-données sera utilisé comme nom d'attribut. Les valeurs des méta-données 
  seront toujours des chaînes. (optionnel)
* **PhotometricInterpretation :** aura une valeur parmi "Undefined", 
  "GrayIndex", "PaletteIndex", "Red", "Green", "Blue", "Alpha", "Hue", 
  "Saturation", "Lightness", "Cyan", "Magenta", "Yellow" ou "Black". (optionnel)
* **units :** nom des unités (parmi "ft" ou "m" pour les données d'élévation). 
  (optionnel)
* **add_offset :** déplacement à appliquer aux valeur des pixels. (après 
  scale_factor) pour calculer une valeur de pixel "réelle". Par défaut à 0.0. 
  (optionnel)
* **scale_factor :** Redimensionnement à appliquer aux valeur du pixel (avant 
  add_offset) pour calculer une valeur de pixel "réelle". Par défauts à 1.0. 
  (optionnel)
* **Description :** Texte descriptif sur la bande. (optionnel)
* **missing_value :** La valeur *nodata* pour le raster. (optionnel)
* **Colormap :** Un conteneur avec un sous-conteneur pour chaque couleur dans 
  la table de couleur, ressemblant au suivant. le composant alpha est optionnel 
  et supposé à 255 (opaque) s'il est absent.

::
    
          Colormap { 
            Color_0 { 
              Byte red 0;
              Byte green 0;
              Byte blue 0;
              Byte alpha 255;
            }
            Color_1 { 
              Byte red 255;
              Byte green 255;
              Byte blue 255;
              Byte alpha 255;
            }
            ...
          }


.. seealso::

* `Site OPeNDAP <http://www.opendap.org/>`_

.. yjacolin at free.fr, Yves Jacolin - 2009/02/22 19:32 (Trunk 7509)