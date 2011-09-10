=======
Couches
=======

Les couches sont les 'source de données' dans OpenLayers.

Couches de base et autres
---------------------------

OpenLayers a deux types de couches opérant au sein de votre application : les 
couches de base et les couches superposées. Cette différence détermine plusieurs aspects de 
la manière d'interagir avec une carte OpenLayers.

Couches de base
+++++++++++++++

Les couches de base sont mutuellement exclusive, ce qui signifie que seule 
une couche peut être activée. La couche de base active détermine la projection 
disponible (le système de coordonnées) et les niveaux de zoom disponible sur 
la carte.

Le fait qu'une couche soit une couche de base ou non est déterminé par la 
propriété isBaseLayer. Cela peut être modifié par les options de la couche.

Les couches de base s'affichent toujours en dessous des couches de superposition.

Couches de superposition
+++++++++++++++++++++++++

Les couches qui ne sont pas de base -- parfois appelées 'overlays' ou couches de 
superposition -- sont des couches alternatives aux couches de base. Plusieurs 
couches de superposition peuvent être activée à la fois. Ces couches ne 
contrôlent pas les niveaux de zoom de la carte, mais peuvent être activée ou 
désactivée à certaines échelles par les paramètres de résolution/d'échelle 
min/max.

Certains types de couches overlays gèrent la reprojection vers la projection de 
la couche de base au moment du chargement de la couche. La plupart des couches 
de superposition ne sont pas définies par défaut comme couches de base, comme le fait la 
classe Layer. Les couches qui ne sont pas de base s'affichent au dessus des 
couches de base.

couches raster
--------------

Les couches raster sont des couches d'images. Ces couches sont typiquement dans 
une projection fixée qui ne peut pas être changé côté client.

.. _layer.google:

Google
++++++

Cette couche permet d'utiliser les données Google Maps dans OpenLayers. Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche Google`_. Pour un exemple d'utilisation, voyez l'`exemple Spherical Mercator`_.

Si vous superposez d'autres données sur une couche de base de Google Maps, vous voudrez interagir avec la couche de Google Maps dans des coordonnées projetées (ceci est particulièrement important si vous travaillez avec des données d'imagerie). Vous pouvez lire plus d'information sur la 'projection sphérique Mercator que Google Maps - et d'autres fournisseurs commerciaux - utilise dans la documentation :ref:`spherical Mercator`.

La classe de la couche Google est conçue pour être seulement utilisée en tant que couche de base.

.. _`documentation de l'API sur la couche Google`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Google-js.html

.. _`exemple Spherical Mercator`: http://openlayers.org/dev/examples/spherical-mercator.html

.. _layer.image:

Image
+++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche image`_.

.. _`documentation de l'API sur la couche image`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Image-js.html

.. _layer.kamap:

KaMap
+++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche KaMap`_.

.. _`documentation de l'API sur la couche KaMap`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/KaMap-js.html

.. _layer.kamapcache:

KaMapCache
++++++++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche KaMapCache`_.

.. _`documentation de l'API sur la couche KaMapCache`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/KaMapCache-js.html

.. _layer.mapguide:

MapGuide
++++++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche MapGuide`_.

.. _`documentation de l'API sur la couche MapGuide`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/MapGuide-js.html

.. _layer.mapserver:

MapServer
+++++++++

Cette couche n'est pas nécessaire pour interagir avec MapServer. En général, la couche :ref:`layer.wms` est préférée à la couche MapServer. Puisque MapServer expose la plupart de ses fonctionnalités CGI également en mode WMS, la couche WMS est préférable. La couche MapServer peut souvent mener à des cartes qui semblent fonctionner, mais ne focntionent pas en raison de problèmes de projection ou d'autres erreurs de configuration similaire. Sauf si vous avez une bonne raison de ne pas le faire, vous devriez utiliser Layer.WMS au lieu de Layer.MapServer.

.. _`FAQ sur la configuration des différentes propriétés de projection` : http://faq.openlayers.org/map/how-do-i-set-a-different-projection-on-my-map/

Si vous utilisez Layer.MapServer, et que votre carte est répétée plusieurs fois, cela indique que vous n'avez pas configuré correctement votre carte pour être dans une projection différente. OpenLayers ne peut pas lire cette information à partir de votre mapfile, et il doit être configuré explicitement. La  `FAQ sur la configuration des différentes propriétés de projection`_ fournit des informations sur la manière de configurer différentes projection dans OepnLayers.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche MapServer`_.

.. _`documentation de l'API sur la couche MapServer`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/MapServer-js.html

.. _layer.multimap:

MultiMap
++++++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche MultiMap`_.

.. _`documentation de l'API sur la couche MultiMap`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/MultiMap-js.html

.. _layer.tms:

TMS
+++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche TMS`_.

.. _`documentation de l'API sur la couche TMS`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/TMS-js.html

.. _layer.tilecache:

TileCache
+++++++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche TileCache`_.

.. _`documentation de l'API sur la couche TileCache`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/TileCache-js.html

.. _layer.virtualearth:

VirtualEarth
++++++++++++
Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche VirtualEarth`_.

.. _`documentation de l'API sur la couche VirtualEarth`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/VirtualEarth-js.html

.. _layer.wms:

WMS
+++
Type de couche pour accéder des données servie selon le standard Web Mapping Service.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche WMS`_.

.. _`documentation de l'API sur la couche WMS`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/WMS-js.html

.. _layer.worldwind:

WorldWind
+++++++++

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche WorldWind`_.

.. _`Documentation de l'API sur la couche WorldWind`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/WorldWind-js.html

.. _layer.yahoo:

Yahoo
+++++

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche Yahoo`_.

.. _`documentation de l'API sur la couche Yahoo`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Yahoo-js.html


Couches de superposition
------------------------
Les couches de superposition peuvent être n'importe quelles couches ayant leur source de données dans un autre format que sous forme d'image. Cela inclut les sous-classes des couches :ref:`layer.markers` et :ref:`layer.vector`. Pour plus d'information sur les différences entre ces deux classes de base, lisez la documention sur :ref:`overlays`.

.. _layer.boxes:

Boxes
+++++
Basé sur une surclasse de markers. En général, il est plus intéressant d'implémenter cette fonctionnalité avec une couche vecteur et des géométries polygonales. Maintenu pour une compatibilité arrière.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche Boxes`_.

.. _`documentation de l'API sur la couche Boxes`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Boxes-js.html

.. _layer.gml:

GML
+++
La couche GML est une surclasse de la couche vecteur pour lire les données à partir d'un fichier et l'afficher. Elle est idéale pour travailler avec plusieurs formats, pas seulement avec GML, et peut peut être configuré pour lire d'autres formats via l'option 'format' de la couche.

Le cas d'utilisation le plus simple des couchesGML est simplement de charger un fichier GML. L'`exemple de couche GML`_ montre cela : ajoutez simplement :

.. code-block:: javascript
   
   var layer = new OpenLayers.Layer.GML("GML", "gml/polygon.xml")
   map.addLayer(layer);

Si vous voulez ajouter un type de format différent, vous pouvez changer l'option format de la couche au moment de l'initialisation. L'`exemple KML`_ montre cela :

.. code-block:: javascript
   
   var layer = new OpenLayers.Layer.GML("KML", "kml/lines.kml", {
      format: OpenLayers.Format.KML
   })
   map.addLayer(layer);

Vous pouvez aussi ajouter formatOption à la couche : ces options sont utilisées lors de la création de la classe format en interne à la couche :

.. code-block:: javascript
   
   var layer = new OpenLayers.Layer.GML("KML", "kml/lines.kml", {
      format: OpenLayers.Format.KML,
      formatOptions: {
        'extractStyles': true
      }
   });
   map.addLayer(layer);

Les options du format sont déterminées par la classe format.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur la couche GML`_.

.. _`exemple KML`: http://openlayers.org/dev/examples/kml-layer.html
.. _`exemple de couche GML`: http://openlayers.org/dev/examples/gml-layer.html
.. _`documentation de l'API sur la couche GML`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/GML-js.html

.. _layer.georss:

GeoRSS
++++++
La couche GeoRSS utilise le format GeoRSS et affiche les résultats comme 'markers' cliquable. C'est une surclasse de la couche Markers qui ne gère pas les lignes ni les polygones. Plusieurs de ses comportement sont codés en dur, et il est en général préférable d'utiliser une couche GML avec un contrôleur SelectFeature à la place de la couche GeosRSS si vous voulez pouvoir configurer le comportement de votre application (Pour plus d'information sur comment réaliser cette transition, lisez :ref:`transition-markers-to-vectors`.)

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches GeoRSS`_.

.. _`documentation de l'API sur les couches GeoRSS` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/GeoRSS-js.html

.. _layer.markers:

Markers
+++++++
La couche de base Markers est assez simple et permet d'utiliser la fonction addMarkers pour ajouter des markers à la couche. Elle gère seulement les points, pas les lignes et les polygones.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches Markers`_.

.. _`documentation de l'API sur les couches Markers` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Markers-js.html

.. _layer.pointtrack:

PointTrack
++++++++++

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches PointTrack`_.

.. _`documentation de l'API sur les couches PointTrack` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/PointTrack-js.html

.. _layer.text:

Texte
+++++
La couche Texte utilise le format Texte et affiche les résultats comme marqueurs cliquables. C'est une surclasse de la couche Markers qui ne gère pas les lignes ni les polygones. Plusieurs de ses comportements sont codés en dur, et il est en général préférable d'utiliser une couche GML avec un Contrôleur SelectFeature à la place de la couche Text si vous voulez pouvoir configurer le comportement de votre application (Pour plus d'information sur comment réaliser cette transition, lisez :ref:`transition-markers-to-vectors`.)

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches Texte`_.

.. _`documentation de l'API sur les couches Texte` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Text-js.html

.. _layer.vector:

Vecteur
+++++++
La couche Vecteur est la base de la gestion avancées des géométries dans OpenLayers. Les classes comme GML et WFS sont des surclasses de la couche Vecteur. Lors de la création d'objets dans le code JavaScript, la bonne pratique est généralement d'utiliser directement la couche Vecteur.

À partir d'OpenLayers 2.7, le développement de l'extension de la couche Vecteur a débuté pour avoir des fonctionnalités supplémentaires pour charger des données, remplacer le grand nombre de surclasse de couches. Ce travail sur les classe Strategy et Protocol est pensé pour faciliter l'interaction avec les données à partir de sources distantes. Pour plus d'information sur les stratégies et les protocoles, lisez la documentation de l'API d'OpenLayers.

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches Vecteur`_.

.. _`documentation de l'API sur les couches Vecteur` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Vector-js.html

.. _layer.wfs:

WFS
+++

Pour toutes informations sur l'API, lisez la `documentation de l'API sur les couches WFS`_.

.. _`documentation de l'API sur les couches WFS` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/WFS-js.html


Sur-classes génériques
-----------------------

* EventPane
* FixedZoomLevels
* Grid
* HTTPRequest
* SphericalMercator
