.. _`gdal.gdal.presentation`:

Utilitaires GDAL
==================

Les programmes suivants sont distribués avec GDAL :

* :ref:`gdal.gdal.gdalinfo` - renvoi des informations sur un fichier.
* :ref:`gdal.gdal.gdal_translate` - Copie un fichier raster, avec la possibilité de 
  contrôler son format de sortie.
* :ref:`gdal.gdal.gdaladdo` - Ajoute une pré-visualisation à un fichier.
* :ref:`gdal.gdal.gdalwarp` - Déforme une image dans un nouveau système de coordonnées.
* :ref:`gdal.gdal.gdaltindex` - Construit un index de tuile raster pour MapServer.
* :ref:`gdal.gdal.gdalbuildvrt` - Construire un VRT à partir d'une liste de jeu de 
  données.
* :ref:`gdal.gdal.gdal_contour` - Contour à partir d'un Modèle Numérique de Terrain.
* :ref:`gdal.gdal.gdaldem` - Outils pour analiser et visualiser les MNT. 
* :ref:`gdal.gdal.rgb2pct` - Convertit une image en RVB 24bit vers une palette 8bit.
* :ref:`gdal.gdal.pct2rgb` - Convertit une image d'une palette 8bit en 
  une image RVB 24bit.
* :ref:`gdal.gdal.gdal_merge` - Construit une mosaïque à partir d'une série 
  d'images.
* :ref:`gdal.gdal.gdal2tiles` - Créer une structure de tuile TMS, un KML et un simple 
  visualiseur web.
* :ref:`gdal.gdal.gdal_rasterize` - Transforme des couches vecteurs en couche raster.
* :ref:`gdal.gdal.gdaltransform` - Transforme des coordonnées.
* :ref:`gdal.gdal.nearblack` - Convertie des bords proches du noir/blanc à leurs 
  valeurs exactes.
* :ref:`gdal.gdal.gdal_retile` - "Retiles" un ensemble de tuiles et/ou construit 
  des niveaux de pyramide tuilée.
* :ref:`gdal.gdal.gdal_grid` - Créer un raster à partir de données découpées.
* :ref:`gdal.gdal.gdal_proximity` - Calcul une carte de proximité en raster.
* :ref:`gdal.gdal.gdal_polygonize` - Génère des polygones à partir d'un raster.
* :ref:`gdal.gdal.gdal_sieve` - Filtre sieve de raster.
* :ref:`gdal.gdal.gdal_fillnodata` - Interpole dans les régions *nodata*.
* :ref:`gdal.gdal.gdallocationinfo` - Interroger un raster pour une localisation donnée.
* :ref:`gdal.gdal.gdalsrsinfo` - Renvoie un SRS données en différents formats (GDAL >= 1.9.0).
* :ref:`gdal.gdal.gdalmove` - Transforme le système de coordonnés d'un fichier (GDAL >= 1.10).
* :ref:`gdal.gdal.gdal-config` - Obtient des informations pour compiler des logiciels 
  qui utilisent GDAL.

Créer de nouveaux fichiers
----------------------------

Accéder à un fichier existant est assez facile. Il suffit d'indiquer le nom du 
fichier ou du jeu de données en paramètre dans la ligne de commande. Par contre, 
créer un fichier est plus compliqué. Il peut être nécessaire d'indiquer le 
format à générer, diverses options de création affectant la manière dont il sera 
créé et éventuellement un système de coordonnées à définir. Plusieurs de ces 
options sont prises en charge par les différents modules GDAL et sont 
introduites ici.

* ``-of format`` : Sélectionne le format du fichier à créer. Les formats sont 
  précisés par leur nom court tel que GTiff (pour GeoTIFF) ou HFA (pour Herdas 
  Imagine). La liste des codes des formats peut être listée par le drapeau 
  ``--formats``. Seuls les formats décrits comme “rw” (Lecture-écriture) peuvent 
  être créés.

  Plusieurs utilitaires créent par défaut des fichiers GéoTiff, si aucun format 
  n'est spécifié. Les extensions des fichiers ne sont pas utilisées pour 
  déterminer le format de sortie, ni ajoutées par GDAL si l'utilisateur les a omis.

* ``-co NAME=VALUE`` : Plusieurs formats ont une ou plusieurs options 
  spécifiques de création qui peuvent être utilisées pour contrôler la création 
  du fichier. Par exemple, le pilote GéoTiff supporte des options de créations 
  pour préciser la compression, ou si le fichier doit être tuilé.

  Ces options de création disponibles varient en fonction du pilote et certains 
  formats en n'ont pas du tout. La liste des options supportées pour chaque format 
  peut être affichée avec le drapeau ``--format <format>`` en ligne de commande, 
  mais la documentation Web du format est certainement l'endroit le plus 
  approprié pour obtenir tous les détails nécessaires.

* ``-a_srs SRS`` : Plusieurs utilitaires (dont ``gdal_translate`` et 
  ``gdalwarp``) incluent la possibilité de définir les systèmes de coordonnées 
  dans la ligne de commande avec les options ``-a_srs`` (définit le SRS à la 
  sortie), ``-s_srs`` (le SRS source) et ``-t_srs`` (le SRS cible).

  Ces options permettent de définir le système de coordonnées (*SRS* signifie 
  *Spatial Reference System*, système de référence spatial) de nombreuses façons :

  * **NAD27/NAD83/WGS84/WGS72 :** Ces systèmes de coordonnées géographiques 
    (lat/lon) communs sont précisés directement avec ces termes.
  * **EPSG:n :** les Systèmes de coordonnées (projetés ou géographiques) sont 
    indiqués en se basant sur leur code EPSG, par exemple EPSG:2154 correspond au 
    Lambert 93 en France. Une liste des systèmes de coordonnées est disponible 
    dans les fichiers gcs.csv et pcs.csv de GDAL.
  * **PROJ.4 Définitions :** Une chaîne de définition PROJ.4 est utilisée comme 
    système de coordonnées. Par exemple, "+proj=utm +zone=11 +datum=WGS84". 
    Prenez soin de garder la chaîne proj.4 en un morceau, sous la forme d'un seul 
    argument, en utilisant des guillemets doubles.
  * **OpenGIS Well Known Text :** L'Open GIS Consortium a défini un format 
    textuel pour décrire les systèmes de coordonnées comme une partie des 
    spécifications Simple Features. Ce format est celui que GDAL utilise comme 
    système de coordonnées. Le nom du fichier contenant une définition du système 
    de coordonnées WKT, peut être utilisé comme argument du système de 
    coordonnées, ou le système de coordonnées complet peut être utilisé dans la 
    ligne de commande (bien que gérer tous les guillemets puisse être un défi).
  * **ESRI Well Known Text :** ESRI utilise une légère variation du format WKT de 
    l'OGC dans leur produit ArcGIS (fichiers .prj), et ceux-ci peuvent être 
    utilisés de la même manière que les fichiers WKT, mais le nom du fichier doit 
    être précédé de *ESRI::*. Par exemple "ESRI::NAD 1927 StatePlane Wyoming West 
    FIPS 4904.prj".
  * **Références spatiales à partir d'URL :** par exemple 
    http://spatialreference.org/ref/user/north-pacific-albers-conic-equal-area/.
  * **Un nom de fichier :** Le nom d'un fichier contenant des définitions de 
    système de coordonnées en WKT, chaînes PROJ.4, ou XML/GML peut être fourni.

Options de la ligne de commande
--------------------------------

Tous les programmes en ligne de commande de GDAL supportent les options 
générales suivantes :

* ``--version`` : affiche la version de GDAL et termine.
* ``--formats`` : liste tous les formats raster supportés par cette compilation 
  de GDAL (en lecture seule et en lecture écriture) et se termine. La gestion 
  du format est indiquée comme suit :

  * 'ro' et un pilote en lecture seule ; 
  * 'rw' est lu ou écrit (c'est à dire géré par *CreateCopy*);
  * 'rw+' est lu, écrit et mis à jour (c'est à dire géré par *Create*). Le 
    caractère 'v' est ajouté pour les formats gérant l'IO virtuel (/vsimem, 
    /vsigzip, /vsizip, etc). Note : Les formats valides pour la sortie de 
    ``gdalwarp`` sont les formats qui gèrent la méthode *Create()* (marqué rw+), a 
    seulement la méthode *CreateCopy()*.

* ``--format format`` : liste des informations détaillées sur le pilote du 
  format. Le format doit être le nom court affiché par l'option --formats, tels 
  que GTiff.
* ``--optfile file`` : lit le nom du fichier et substitut son contenu dans la 
  liste des options de la ligne de commande. Les lignes débutantes par # sont 
  ignorées. Des arguments de plusieurs mots peuvent être réunis en les 
  entourant de guillemets.
* ``--config key value`` : définit la valeur de `la clé dans la configuration <http://trac.osgeo.org/gdal/wiki/ConfigOptions>`_, 
  par opposition à la déclaration des variables d'environnements. Il existe des 
  mots-clés de configuration communs tels que GDAL_CACHEMAX (mémoire utilisé en 
  interne pour mettre en cache en mégaoctets) et GDAL_DATA (chemin du répertoire 
  des "données" de GDAL). Des pilotes individuels peuvent être influencés par 
  d'autres options de configuration.
* ``--debug value`` : contrôle quel message de débogage sera affiché. Une 
  valeur à ON permettra l'affichage des messages de débogage. Une valeur à OFF 
  n'affichera pas les messages de débogage. Une autre valeur sélectionnera 
  seulement les messages de débogages contenant cette chaîne dans le code le 
  précédent.
* ``--help-general`` : donne un bref message des usages des options en ligne de 
  commande et termine.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01* (gdal/apps/gdal_utilities.dox Trunk 25410)
