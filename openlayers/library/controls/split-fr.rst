.. _control.split-detail:

OpenLayers.Control.Split
========================

Permet de découper les éléments linéaires d'une couche vecteur en fonction des modifications/éditions d'éléments linéaires de n'importe quelle autre couche vecteur, ou d'une couche dessin temporaire. Le contrôle fonctionne selon deux modes. Par défaut, le contrôle permet de dessiner les éléments temporaires sur une couche dessin temporaire (gérée par le contrôle), cette dernière étant ensuite utilisée pour découper les éléments choisis de la couche-cible. En mode auto-split, Le contrôle suit les éditions de la couche modifiable (ajouts de nouveaux éléments ou modification des éléments existants) et découpe les éléments choisis sur la couche-cible.

Comme tous les contrôles, celui-ci peut être ajouté à une carte. Il n'a pas de représentation visuelle distincte mais peut être connecté à un bouton, ou à tout autre outil, pour permettre son activation en cliquant. Aucune interface graphique n'est fournie pour la configuration du contrôle. La collecte des instructions de l'utilisateur pour la configuration des contrôles est une tâche spécifique de l'application.

Voir la `documentation de l'API Split`_ pour une liste complète des options de configuration. L'`exemple de base` présente l'utilisation du contrôle dans un exemple complet, et l'`exemple découpe/magnétisme` présente le contrôle de découpe en conjonction avec le :ref:`Contrôle de saisie par magnétisme <control.snapping-detail>`. Les échantillons présentés ci-dessous, s'ils ne sont pas complets, visent néanmoins à introduire différents aspects du comportement du contrôle.

.. _`documentation de l'API Split`: http://dev.openlayers.org/apidocs/files/OpenLayers/Control/Split-js.html
.. _`exemple de base`: http://openlayers.org/dev/examples/split-feature.html
.. _`exemple découpe/magnétisme`: http://openlayers.org/dev/examples/split-feature.html

Exemple d'usage :

1. Création d'un contrôle de découpe permettant de dessiner des éléments temporaires servant à découper des roads.

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({layer: roads});

2. Création d'un contrôle qui surveille les éditions de la couche "roads", et qui découpe les roads existantes avec n'importe quelle route nouvellement créée ou modifiée sur la même couche.

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({layer: roads, source: roads});

3. Création d'un contrôle ne permettant que la découpe des "chemins" (surface = dirt).

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({
        layer: roads,
        targetFilter: new OpenLayers.Filter.Comparison({
            type: OpenLayers.Filter.Comparison.EQUAL_TO,
            property: "surface",
            value: "dirt"
        })
    });

4. Pas de segments créés en-dessous d'une tolérance donnée : pour les intersections ayant lieu à moins de cette distance d'un sommet existant, ce dernier sera utilisé pour découper la ligne au lieu du point d'intersection calculé.

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({
        layer: roads, 
        source: roads,
        tolerance: 0.01 // mêmes unités que la couche roads
    });

5. Création d'un guetteur pour les découpes modifiant les attributs des éléments.

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({
        layer: roads, 
        eventListeners: {
            "split": function(event) {
                var road;
                for(var i=0; i<event.features.length; ++i) {
                    road = event.features[i];
                    // attributes are cloned from original
                    road.attributes["length"] = road.getLength();
                }
            }
        }
    });

6. Diffère la suppression des éléments découpés. À la condition qu'une stratégie séparée de sauvegarde des éditions et qu'un protocole de gestion de la communication aient été mis en place, le contrôle peut être configuré pour déterminer l'état des éléments au lieu de les détruire effectivement. Les éléments découpés verront leur état déterminé à DELETE à moins qu'un état INSERT soit en attente (auquel cas ils seront détruits immédiatement). Tous les nouveaux éléments obtiennent l'état INSERT (sans prise en compte de la valeur deferDelete).

.. code-block:: javascript

    // La couche vecteur est nommée "roads"
    var split = new OpenLayers.Control.Split({
        layer: roads,
        deferDelete: true,
        tolerance: 0.001
    });
