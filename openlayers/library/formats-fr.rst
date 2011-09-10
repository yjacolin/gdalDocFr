=======
Formats
=======

Les Formats sont des classes qui analysent différentes sources de données et les convertissent en objets internes d'OpenLayers. La plupart des formats sont centrés sur la lecture des données à partir d'un XML DOM ou d'une chaîne de caractères et sur la conversion de celles-ci en objets OpenLayers.Feature.Vector.

Formats intégrés
++++++++++++++++

.. _format.kml:

KML
---

Le format KML lit des données KML et renvoie un tableau d'objets OpenLayers.Feature.Vector.

L'analyseur KML supporte l'analyse de styles locaux et distants.

L'analyseur KML supporte les liens réseaux.

Pour récupérer des données distantes, l'option maxDepth doit être supérieure à 0. Cette option indique à l'analyseur KML les niveaux à parcourir avant d'abandonner.

.. #1796, #1877

*Note*: Avant la version 2.8 d'OpenLayers, l'option maxDepth ne fonctionnait pas. Si aucun paramètre n'était spécifié, le format KML parcourait les liens réseau et les styles distants.

Création de Formats
+++++++++++++++++++

Créer des formats spécifiques, particulièrement pour une utilisation avec les OpenLayers Protocols, est relativement facile: créez simplement une sous-classe de Format ayant une méthode 'read' qui prenne en entrée une chaîne de caractères et qui renvoie un tableau d'éléments.

.. code-block:: javascript

  var MyFormatClass = OpenLayers.Class(OpenLayers.Format.XML, {
      read: function(data) {
          // We're going to read XML
          if(typeof data == "string") {
              data = OpenLayers.Format.XML.prototype.read.apply(this, [data]);
          }
          var elems = data.getElementByTagName("line");
          var features = [];
          var wkt = new OpenLayers.Format.WKT();
          for (var i = 0; i < elems.length; i++) {
              var node = elems[i];
              var wktString = this.concatChildValues(node);
              features.push(wkt.read(wktString));
          }
          return features;
      }
  });    

Ceci va lire un document XML contenant une série d'éléments XML 'line' avec du WKT encapsulé dans chacun d'eux. On peut l'utiliser avec une ligne 'format: MyFormatClass' dans un Layer.GML, ou 'format: new MyFormatClass()' dans des Protocols qui supportent ce paramètre.
