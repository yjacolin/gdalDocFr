==================================
Comprendre la syntaxe d'OpenLayers
==================================

Cette section a pour objectif de permettre aux utilisateur de bien comprendre la syntaxe utilisée dans le développement d'une application avec OpenLayers.

"Classes" OpenLayers
--------------------

OpenLayers est écrit dans un style "classique". Ça signifie que la librairie fournit des fonctions destinées à être utilisées avec le ``nouveau`` mot-clé qui retourne des objets. Ces fonctions commencent toutes avec une lettre majuscule.

.. code-block:: javascript

    var map = new OpenLayers.Map("map", options);
    
Le code ci-dessus créé un nouvel objet ``map`` avec toutes les propriétés du proptotype de la fonction ``OpenLayers.Map``. Les propriétés qui doivent être définie ou utilisées sont documentées dans la `documentation de l'API`_

.. _`documentation de l'API` : http://dev.openlayers.org/apidocs

L'argument ``options``
----------------------

La plupart des constructeurs des objets OpenLayers prennent un objet ``options`` comme un de leurs arguments. En général, vous pouvez définir la valeur de n'importe quelle propriété de l'API dans un argument option du constructeur.

Par exemple, pour les couches vecteur, en lisant la `documentation de l'API pour la couche vecteur`_, vous pouvez voir la propriété ``isBaseLayer``. Si vous définissez une valeur pour ``isBaseLayer`` dans l'argument option, cela sera définit pour la couche.

.. _`documentation de l'API pour la couche vecteur`: http://dev.openlayers.org/apidocs/files/OpenLayers/Layer/Vector-js.html

Par exemple :

.. code-block:: javascript

    var layer = new OpenLayers.Layer.Vector("Layer Name", {
        isBaseLayer: true
    });
    
    layer.isBaseLayer === true;  // cela est vrai

Vous pouvez également voir que la couche vecteur hérite de ``OpenLayers.Layer``. En suivant le lien vers la `documentation de l'API pour l'objet Layer`_, vous trouverez une référence à la propriété ``projection`` de la couche. Comme pour ``isBaseLayer``, si vous fournissez une propriété ``projection`` dans l'argument ``options``, cette valeur sera définie pour la couche.

.. _`documentation de l'API pour l'objet Layer` : http://dev.openlayers.org/apidocs/files/OpenLayers/Layer-js.html

.. code-block:: javascript

    var layer = new OpenLayers.Layer.Vector("Layer Name", {
        projection: new OpenLayers.Projection("EPSG:900913")
    });


