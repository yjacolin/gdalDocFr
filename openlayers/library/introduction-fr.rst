===============
Démarrer
===============

Créer votre première carte
--------------------------
L'API d'OpenLayers a deux concepts qui sont important à comprendre afin de 
construire votre première carte : 'Map' et'Layer'. Une Map d'OpenLayers stocke 
les informations sur la projection, l'étendue, les unités etc. par défaut de la 
carte. Dans l'objet Map, les données sont affichées via des objets 'Layer'. L'objet 
Layer représente la source de données, et comprend des informations sur la 
manière dont OpenLayers doit demander les données et les afficher.

Façonner le code HTML
+++++++++++++++++++++

Construire un visualisateur OpenLayers nécessite l'écriture de code HTML dans 
lequel votre visualisateur sera vu. OpenLayers gère la création de carte dans 
n'importe quel élément de type block -- cela signifie qu'elle peut être utilisée 
pour placer une carte dans n'importe quel élément HTML de votre page.

En plus d'un élément de type block, il est également nécessaire d'inclure 
une balise script qui inclut la bibliothèque OpenLayers à la page.

.. code-block:: html
  
  <html>
  <head>
    <title>OpenLayers Example</title>
      <script src="http://openlayers.org/api/OpenLayers.js"></script>
      </head>
      <body>
        <div style="width:100%; height:100%" id="map"></div>
      </body>
  </html>
    
**Ex. 1 :** Créer votre première page HTML 

Créer le visualisateur de la carte
+++++++++++++++++++++++++++++++++++

Dans le but de créer un visualisateur, vous devez d'abord créer une carte. Le 
constructeur OpenLayers.Map nécessite un argument : cet argument doit être soit 
un élément HTML soit un ID d'un élément HTML. C'est l'élément dans lequel la 
carte sera placée.

.. code-block:: javascript

  var map = new OpenLayers.Map('map');
  
**Ex. 2 :** Constructeur Map

L'étape suivante dans la création du visualiseur est d'ajouter une couche à 
cette carte. OpenLayers gère plusieurs sources de données différentes, des 
services WMS à Yahoo! Maps ou WorldWind. Dans cet exemple, nous utilisons une 
couche WMS. Celle-ci est un exemple fourni par MetaCarta.

.. code-block:: javascript

  var wms = new OpenLayers.Layer.WMS(
    "OpenLayers WMS",
    "http://labs.metacarta.com/wms/vmap0", 
    {'layers':'basic'} );
  map.addLayer(wms);

**Ex. 3 :** Constructeur Layer

Le premier paramètre dans ce constructeur est l'url du serveur WMS. Le second 
est un objet contenant les paramètres à ajouter aux requêtes WMS.

Enfin, pour afficher la carte, vous devez définir un centre et un 
niveau de zoom. Pour que le zoom correspond à la carte dans la fenêtre, vous 
pouvez utiliser la fonction zoomToMaxExtent, qui zoomera au plus proche 
tout en permettant d'inclure l'étendue maximale dans la fenêtre.

Rassembler l'ensemble
++++++++++++++++++++++

Le bloc de code suivant réunit toutes les pièces pour un créer un 
visualiseur OpenLayers.

.. code-block:: html

  <html>
  <head>
    <title>OpenLayers Example</title>
      <script src="http://openlayers.org/api/OpenLayers.js"></script>
      </head>
      <body>
        <div style="width:100%; height:100%" id="map"></div>
        <script defer="defer" type="text/javascript">
          var map = new OpenLayers.Map('map');
          var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
              "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
          map.addLayer(wms);
          map.zoomToMaxExtent();
        </script>
  
  </body>
  </html>

**Ex. 4 :** Code HTML et Javascript complet  pour un simple navigateur WMS

Ajouter un WMS en superposition
-------------------------------

Les couches WMS ont la possibilité d'être superposées (overlay) au dessus d'autres 
couches WMS de la même projection. Il y a plusieurs manières de définir une 
couche comme overlay, plutôt qu'une base layer. Avec un WMS, la meilleure 
manière pour réaliser cela est de définir le paramètre 'transparent' à 'true'. 
L'exemple ici utilise un WMS des frontières politiques pour présenter une 
superposition d'un WMS transparent.

.. code-block:: javascript

    var twms = new OpenLayers.Layer.WMS( "World Map", 
        "http://world.freemap.in/cgi-bin/mapserv?", 
        { map: '/www/freemap.in/world/map/factbooktrans.map', 
          transparent: 'true', layers: 'factbook'} 
        );
    map.addLayer(twms);

**Ex. 5 :** Comment ajouter une couche WMS transparente en overlay à votre carte

Le paramètre 'true' appliqué à la transparence définit automatiquement deux 
options :
 
 * le paramètre format. L'option format de la couche WMS est définie à image/png 
   si le navigateur supporte les images PNG transparentes (tous les navigateurs 
   sauf Internet Explorer 6). Dans Internet Explorer 6, cela sera plutôt changé 
   à image/gif.
   
 * l'option isBaseLayer. L'option isBaseLayer contrôle si la couche peut être 
   affichée en même temps que d'autres couches. Cette option est définie à false par 
   défaut pour les couches WMS, mais définir la transparence à true la modifie 
   à true par défaut.

Si nous réunissons ce code avec celui écrit un peu plus tôt, nous obtenons ceci :

.. code-block:: html

  <html>
  <head>
    <title>OpenLayers Example</title>
      <script src="http://openlayers.org/api/OpenLayers.js"></script>
      </head>
      <body>
        <div style="width:100%; height:100%" id="map"></div>
        <script defer="defer" type="text/javascript">
          var map = new OpenLayers.Map('map');
          var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS", 
              "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
          var twms = new OpenLayers.Layer.WMS( "World Map", 
              "http://world.freemap.in/cgi-bin/mapserv?", 
              { map: '/www/freemap.in/world/map/factbooktrans.map', 
                transparent: 'true', layers: 'factbook'} 
              );
          map.addLayers([wms, twms]);
          map.zoomToMaxExtent();
        </script>
  
  </body>
  </html>

**Ex. 6 :** Comment ajouter une couche WMS transparence en superposition à 
votre carte

Une dernière chose à noter ici est que nous devons utiliser addLayers sur 
l'objet Map pour ajouter les deux couches en même temps. Cela nous permet 
d'économiser une ligne de code dans ce cas, et peut être utile dans d'autres 
cas quand nous devons ajouter en même temps plusieurs couches à une carte.
