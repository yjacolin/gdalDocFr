.. _control.snapping-detail:

OpenLayers.Control.Snapping
===========================

Permet de contrôler la fonction de saisie par magnétisme (snapping) depuis les sommets des éléments d'une couche vers les noeuds, sommets ou arêtes des éléments d'autres couches. La saisie par magnétisme est possible lorsque le contrôle est actif, alors que lorsqu'il est désactivé, l'édition se fait selon le comportement habituel. Le contrôle peut être configuré pour permettre la saisie par magnétisme sur les noeuds, sommets et/ou arêtes d'un nombre indéterminé de couches (les éléments de ces couches étant chargés côté client). La tolérance, le type de saisie par magnétisme, et un filtre optionnel peuvent être configurés pour chaque couche-cible.

Voir la `Documentation de l'API saisie par magnétisme`_ pour une liste complète des options de configuration. L'`Exemple en ligne`_ est une démonstration complète de l'utilisation des contrôles. Les échantillons présentés ci-dessous, s'ils ne constituent pas des exemples complètement fonctionnels, permettent de présenter les différents aspects du comportement du contrôle.

.. _`Documentation de l'API saisie par magnétisme`: http://dev.openlayers.org/apidocs/files/OpenLayers/Control/Snapping-js.html
.. _`Exemple en ligne`: http://openlayers.org/dev/examples/snapping.html

Exemple d'utilisation :

1. Active la saisie par magnétisme à partir des éléments d'une couche vers des éléments de la même couche, avec la configuration par défaut.

.. code-block:: javascript

// La couche est nommée "roads"
    var snap = new OpenLayers.Control.Snapping(roads);

2. Active la saisie par magnétisme à partir des éléments d'une couche vers des éléments de la même couche, avec une configuration personnalisée.

.. code-block:: javascript

    // Magnétisme depuis les sommets vers les sommets des autres routes uniquement (pas les arêtes)
    // Tolérance de 30 pixels, et sans activer le magnétisme pour les "dirt roads"
    var snap = new OpenLayers.Control.Snapping(roads, {
        targets: [{
            layer: roads,
            tolerance: 30,
            edge: false,
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.NOT_EQUAL_TO,
                property: "surface",
                value: "dirt"
            })
        }]
    });


3. Active la saisie par magnétisme à partir des éléments d'une couche vers des éléments de plusieurs couches additionelles, toutes configurées de la même manière. Effectue une recherche de l'objet le plus proche dans toutes les couches, au lieu d'activer le magnétisme sur l'objet le plus proche dans la première couche concernée (configurer "greedy" à "false").

.. code-block:: javascript

    // La couche éditable est nommée "editable" et les trois couches cibles sont nommées "roads", parcels" et "buildings"
    // "parcels", and "buildings".
    var snap = new OpenLayers.Control.Snapping(editable, {
        defaults: {
            tolerance: 15,
            edge: false
        }
        targets: [roads, parcels, buildings],
        greedy: false
    });
