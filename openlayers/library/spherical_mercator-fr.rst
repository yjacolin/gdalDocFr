.. _spherical-mercator:

==================
Spherical Mercator
==================

.. include:: spherical_mercator_intro-fr.inc 

|spherical-mercator-intro| 

Qu'entend-on par « Spherical Mercator » ?
-----------------------------------------
*Spherical Mercator* est le terme consacré utilisé par la communauté OpenLayers -- ainsi que par les autres communautés SIG Open Source existantes -- pour décrire la projection utilisée par Google Maps, Microsoft Virtual Earth, Yahoo Maps, et d'autres fournisseurs d'API commerciales.

Ce terme est employé en référence au fait que ces fournisseurs utilisent une projection Mercator qui considère la Terre comme une sphère, plutôt q'une projection qui considèrerait la Terre comme un ellipsoïde. Cela affecte les calculs basés sur la considération de la planéité de la carte, et est, de ce fait, important à prendre en compte lorsque l'on travaille avec ces fournisseurs de cartes.

Il est nécessaire d'utiliser cette projection pour superposer des données aux cartes diffusées par les fournisseurs d'API commerciales. Cette recommandation est valable, en premier lieu, pour l'affichage de tuiles au-dessus de couches d'API commerciales, telles les TMS, WMS et autres tuiles similaires.

Pour des raisons de bon fonctionnement avec les API commerciales, de nombreux utilisateurs, créateurs de contenus pour une utilisation dans Google Maps, utilisent préférentiellement cette projection. Un exemple parlant est le projet OpenStreetMap, dont les tuiles sont toutes projetées selon la projection *spherical mercator*. 

Les projections, dans les SIG, sont couramment référencées à l'aide de leur code « EPSG », identifiants gérés par le European Petroleum Survey Group. Un identifiant commun est « EPSG:4326 » qui décrit les cartes dans lesquelles la latitude et la longitude sont considérées comme des valeurs X et Y. La désignation officielle de la projection sphérique Mercator est « EPSG:3785 ». 
Cependant, avant l'établissement de cette norme, une large partie des logiciels utilisaient l'identifiant « EPSG:900913 ». Ce code n'est pas officiel mais toujours utilisé comme code usuel dans OpenLayers. Chaque fois que le code « EPSG:4326 » apparaît, vous pouvez considérer qu'il décrit des coordonnées en longitude/latitude. Chaque fois que le code « EPSG:900913 » apparaît, il décrira des coordonnées en mètre, en x/y. 

Première carte
--------------

La première étape pour utiliser la projection sphérique Mercator est la création d'une carte utilisant cette projection. Cette carte sera basée sur l'API de Microsoft Virtual Earth. Le patron HTML suivant sera utilisé pour la carte. 

.. code-block:: html
  
  <html>
  <head>
    <title>Exemple OpenLayers</title>
      <script src='http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6.1'></script>
      <script src="http://openlayers.org/api/OpenLayers.js"></script>
      </head>
      <body>
        <div style="width:100%; height:100%" id="map"></div>
        <script defer='defer' type='text/javascript'>
          // Le code se place ici
        </script>
      </body>
  </html>
    
**Ex. 1**: patron HTML   

L'étape suivante consiste à ajouter la couche Microsoft Virtual Earth par défaut en tant que couche de base pour la carte.

 
.. code-block:: javascript 
  
  var map = new OpenLayers.Map('map');
  var layer = new OpenLayers.Layer.VirtualEarth("Virtual Earth",
   { 
       sphericalMercator: true,  
       maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34) 
   });
  map.addLayer(layer);
  map.zoomToMaxExtent();

Ceci créé une carte. Une fois cette carte en mains, vous devez être conscient que les coordonnées utilisées par *setCenter* ne sont pas les longitude et latitude ! En effet, elles sont exprimées dans l'unité de projection : le mètre dans ce cas précis. Cette carte permet de naviguer, mais sans une compréhension plus approfondie de la projection sphérique Mercator, il sera difficile de lui demander plus. 

Cette carte a des caractéristiques influençant le paramètre maxExtent.
Typiquement, la plupart des cartes utilisant la projection sphérique Mercator adoptent les limites suivantes pour la représentation du Monde : de -180 ° à 180 ° en longitude et de -85,0511 ° à 85,0511 ° en latitude. Parce que la projection Mercator provoque un étirement infini à l'approche des pôles, une limite dans la direction nord-sud est requise ; la limite appliquée ici permet d'obtenir des carrés parfaits dans l'unité de projection. Comme vous l'indique le paramètre *maxExtent* envoyé au constructeur de la couche, les coordonnées prennent des valeurs de -20037508,34 à 20037508,34 dans chaque direction. 

Par défaut, la résolution maximale de la carte (paramètre *maxResolution*) est adaptée pour que l'étendue maximale s'affiche sur 256 pixels. Il en résulte un *maxResolution* de 156543,0339. La prise en charge est interne à la couche et ne nécessite pas de déclaration dans les options de cette couche.

Si vous utilisez une couche WMS ou TMS indépendante avec une projection sphérique Mercator, vous devrez spécifier la propriété *maxResolution* de la couche, en plus du paramètre *maxExtent* comme montré ici. 

Travailler avec des coordonnées projetées
-----------------------------------------

Heureusement, OpenLayers fournit maintenant des outils pour vous aider à la reprojection de données côté client. Ceci inclut, dans la liste de vos opérations courantes, la possibilité de transformer des coordonnées, exprimées en longitude/latitude, dans la projection sphérique Mercator.
Dans le premier exemple, nous transformerons des coordonnées pour un usage avec la fonction *setCenter* et d'autres appels. Ensuite, nous montrerons comment utiliser l'option *displayProjection* de la carte pour modifier l'affichage des coordonnées pour refléter la projection de la carte de base.

Reprojection de points et de limites
++++++++++++++++++++++++++++++++++++

Pour effectuer une reprojection, créez d'abord un objet projection pour la projection par défaut.
Le code standard pour la projection en longitude/latitude est « EPSG:4326 ». Ce sont les longitude/latitude basées sur l'ellipsoïde WGS84. (Si vos données s'alignent bien dans Google Maps, c'est probablement la projection que vous avez.)

Le code suivant permet de créer l'objet qui gèrera vos coordonnées et permettra leur transformation.

.. code-block:: javascript
   
  var proj = new OpenLayers.Projection("EPSG:4326");
  var point = new OpenLayers.LonLat(-71, 42);
  point.transform(proj, map.getProjectionObject());

Ce point est maintenant projeté selon la projection sphérique Mercator et peut être envoyé à la méthode *setCenter* de la carte.

.. code-block:: javascript
  
  map.setCenter(point);

La transformation peut-être effectuée directement dans l'appel de la méthode *setCenter* :

.. code-block:: javascript
   
  var proj = new OpenLayers.Projection("EPSG:4326");
  var point = new OpenLayers.LonLat(-71, 42);
  map.setCenter(point.transform(proj, map.getProjectionObject()));

De cette façon, vous pouvez utiliser des coordonnées en longitude/latitude pour spécifier le centre de la carte.

La même technique peut être utilisée pour reprojeter les objets *OpenLayers.Bounds* : appelez simplement la méthode transform sur votre objet limite.

.. code-block:: javascript

  var bounds = new OpenLayers.Bounds(-74.047185, 40.679648, -73.907005, 40.882078)
  bounds.transform(proj, map.getProjectionObject()); 

Les transformations affectent les objets existants, de sorte qu'il n'y a pas besoin d'assigner une nouvelle variable. 

Reprojection de géométries
++++++++++++++++++++++++++

Les objets *geometry* ont la même méthode de transformation que les objets points et limites.
Ceci implique que chaque objet *geometry* créé dans le code d'application doit être transformé en appelant la méthode *transform* préalablement à son incorporation dans une couche, et que chaque objet *geometry* extrait d'une couche devra être transformé avant de pouvoir être manipulé.

Comme les transformations se font sur-place, elles ne devraient pas être effectuées sur des objets *geometry* déjà ajoutés à une couche. La bonne méthode consisterait à transformer un clone de la géométrie :

.. code-block:: javascript

   var feature = vector_layer.features[0];
   var geometry = feature.geometry.clone();
   geometry.transform(layerProj, targetProj);

Reprojection de données vectorielles
------------------------------------
La création de cartes projetées permet de reprojeter des données vectorielles sur un fond de carte. Il faut, pour cela, simplement spécifier le système de projection des données vectorielles correctement et s'assurer que la projection de la carte est également correcte.

.. code-block:: javascript
  
  var map = new OpenLayers.Map("map", { 
    projection: new OpenLayers.Projection("EPSG:900913")
  });
  var myBaseLayer = new OpenLayers.Layer.Google("Google", 
                {'sphericalMercator': true,
                 'maxExtent': new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34) 
                });
  map.addLayer(myBaseLayer);
  var myGML = new OpenLayers.Layer.GML("GML", "mygml.gml", { 
    projection: new OpenLayers.Projection("EPSG:4326")
  });
  map.addLayer(myGML);

Notez que vous pouvez employer cette procédure pour charger n'importe quel format supporté par OpenLayers, notamment WKT, GeoJSON, KML, etc. Spécifiez simplement l'option *format* de la couche GML.

.. code-block:: javascript
  
  var geojson = new OpenLayers.Layer.GML("GeoJSON", "geo.json", { 
    projection: new OpenLayers.Projection("EPSG:4326"),
    format: OpenLayers.Format.GeoJSON
  });
  map.addLayer(geojson);

Notez que si vous spécifiez un objet projection pour une couche, l'ajout manuel d'objets (via *layer.addFeatures*) nécessite leur transformation préalable. OpenLayers transformera uniquement la projection des géométries qui sont créées par la bibliothèque pour éviter la duplication du travail de projection.

Exportation de données projetées
--------------------------------
La méthode pour exporter des données vectorielles depuis OpenLayers consiste à extraire une collection de données d'une couche vectorielle et à la transmettre à une classe *Format* pour écrire le fichier de sortie. De cette manière, dans le cas d'une carte projetée, les données obtenues en sortie seront également projetées. Pour reprojeter des données au moment de la conversion, les projections source et de destination doivent être spécifiées dans la classe *Format* qui sera utilisée pour exporter les données.

.. code-block:: javascript
  
  var format = new OpenLayers.Format.GeoJSON({
    'internalProjection': new OpenLayers.Projection("EPSG:900913"),
    'externalProjection': new OpenLayers.Projection("EPSG:4326")
  });
  var jsonstring = format.write(vector_layer.features);

Projection spécifique à l'affichage dans les contrôles
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Plusieurs contrôles affichent les coordonnées à l'intention de l'utilisateur, soit directement, soit intégrés dans les liens. Les contrôles MousePosition et Permalink (ainsi que le contrôle associé ArgPars) utilisent, tout deux, les coordonnées correspondant au système de projection interne de la carte. Pour éviter les confusions chez l'utilisateur, OpenLayers permet de spécifier une projection spécifique à l'affichage. Quand les précédents contrôles sont utilisés, la transformation est effectuée depuis le système de projection de la carte vers le système de projection spécifique à l'affichage. 

Pour utiliser cette option, les options *projection* et *displayProjection* doivent être spécifiées lors de la création de la carte. Ceci effectué, les contrôles tiendront compte de cette option automatiquement pour cette carte. 

.. code-block:: javascript
  
  var map = new OpenLayers.Map("map", {
    projection: new OpenLayers.Projection("EPSG:900913"),
    displayProjection: new OpenLayers.Projection("EPSG:4326")
  });
  map.addControl(new OpenLayers.Control.Permalink());
  map.addControl(new OpenLayers.Control.MousePosition());

Vous pouvez alors ajouter des couches normalement. 
  
Création d'images raster dans la projection sphérique Mercator
--------------------------------------------------------------
L'une des raisons pour laquelle la projection sphérique Mercator est si importante est qu'elle est l'unique projection qui permette la superposition correcte d'images sur les couches commerciales telle Google Maps. Lorsqu'on utilise des images raster, dans le navigateur, il n'est pas possible de les reprojeter de la même façon que le ferait un client SIG plus complet. De ce fait, toutes les images doivent partager la même projection. 

La manière de créer des tuiles utilisant la projection sphérique Mercator dépend du logiciel utilisé pour générer les images. Ce document aborde l'exemple de MapServer.

MapServer
+++++++++

MapServer utilise proj.4 comme support pour les reprojections. Pour permettre la reprojection vers la projection sphérique Mercator, il faut ajouter la définition de cette projection dans le répertoire de données de proj.4.

Sur les systèmes Linux, éditez le fichier /usr/share/proj/epsg. A la fin du fichier, ajoutez la ligne suivante :
 
    <900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs

Après quoi, vous devez ajouter la projection après wms_srs, au sein du mot-clé METADATA de l'objet WEB de votre mapfile :

::
  
  map 
    web 
      metadata
        wms_srs "EPSG:4326 EPSG:900913" 
      end
    end  
    # Layers go here
  end 

Ceci vous permettra de requérir des tuiles auprès du serveur WMS MapServer dans la projection sphérique Mercator, lesquelles s'aligneront avec les données des fournisseurs commerciaux dans OpenLayers.

.. code-block:: javascript

            var options = {
                projection: new OpenLayers.Projection("EPSG:900913"),
                units: "m",
                maxResolution: 156543.0339,
                maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,
                                                 20037508.34, 20037508.34)
            };
            
            map = new OpenLayers.Map('map', options);

            // création des couches Google Mercator
            var gmap = new OpenLayers.Layer.Google(
                "Rues Google",
                {'sphericalMercator': true,
                 'maxExtent': new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34) 
                }
            );
            
            // création d'une couche WMS
            var wms = new OpenLayers.Layer.WMS(
                "carte du Monde",
                "http://labs.metacarta.com/wms/vmap0",
                {'layers': 'basic', 'transparent': true}
            );
            
            map.addLayers(gmap, wms);

Les couches WMS héritent automatiquement de la projection de la couche de base, de sorte qu'il n'est pas nécessaire de leur en spécifier une.

GeoServer
+++++++++

Les versions courantes de GeoServer incorporent le support de EPSG:900913 nativement. Il n'y a, donc pas lieu de l'ajouter dans les définitions de projection. Ajoutez simplement la couche GeoServer en tant que WMS puis ajoutez-le à la carte.

tuiles personnalisées
+++++++++++++++++++++

L'utilisation de la projection sphérique Mercator prend aussi tout son intérêt pour le chargement de tuiles personnalisées.
Beaucoup de ces tuiles sont créées en utilisant la même projection que Google Maps, en utilisant aussi, habituellement, le même modèle z/x/y pour y accéder. 


Si vous avez des tuiles qui sont paramétrées selon le modèle "Google", c'est-à-dire basées sur x, y, z et dont l'origine se trouve dans le coin supérieur gauche du monde, vous pouvez les charger dans une couche TMS, grâce à une fonction *get_url* légèrement modifiée. (Notez que cette approche remplace l'ancienne couche "LikeGoogle" du SVN.)

Définissez d'abord la fonction *get_url* utile. Elle devrait prendre en argument les limites englobantes et ressembler au code suivant :

.. code-block:: javascript
    
    function get_my_url (bounds) {
        var res = this.map.getResolution();
        var x = Math.round ((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
        var y = Math.round ((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
        var z = this.map.getZoom();

        var path = z + "/" + x + "/" + y + "." + this.type; 
        var url = this.url;
        if (url instanceof Array) {
            url = this.selectUrl(path, url);
        }
        return url + path;
        
    }

A la création de la couche TMS, vous spécifiez alors, en option, cette fonction personnalisée qui chargera les tuiles :
 
.. code-block:: javascript
  
    new OpenLayers.Layer.TMS("Name", 
                           "http://exemple.com/", 
                           { 'type':'png', 'getURL':get_my_url });

Ceci implique que la fonction *getURL* standard sera court-circuitée par votre fonction, permettant de charger vos tuiles à la mode Google plutôt que des tuiles TMS standard.

Quand vous procédez ainsi, votre carte devrait appliquer les mêmes *maxExtent* et *maxResolution* que les cartes Google Maps :

.. code-block:: javascript
  
   new OpenLayers.Map("map", {
       maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34), 
       numZoomLevels:18, 
       maxResolution:156543.0339, 
       units:'m', 
       projection: "EPSG:900913",
       displayProjection: new OpenLayers.Projection("EPSG:4326")
   });

Comme décrit précédemment, l'utilisation de cette couche implique que la manipulation de la carte se fait en coordonnées projetées.
