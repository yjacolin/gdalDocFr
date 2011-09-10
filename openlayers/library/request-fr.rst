.. _request:

Requête de Données Distantes
============================

Il existe différentes façons d'obtenir des données du serveur à partir du client. Spécifier des sources d'images, de scripts et de feuilles de style peut être fait à tout moment pour demander des nouvelles données sans rafraichir un document entier. Ces types de requête s'appliquent pour toute origine. Un autre moyen de retrouver des données du serveur consiste à mettre à jour l'adresse d'un document dans un frame (iframe ou autre). Ces types de requête s'appliquent également pour n'importe quelle origine. Cependant, le code s'exécutant dans le document original est restreint à la lecture de données provenant de documents de la même origine. Cela signifie que si votre application provient de http://example.com, votre code peut charger dans un frame un document provenant de n'importe quelle autre origine (disons http://example.net), mais votre code peut uniquement accéder dans le document principal à des données servies par le même protocole (http), le même domaine (example.com), et le même port (probablement 80 dans ce cas).

Les types de requêtes ci-dessus sont utiles car elles sont asynchrones. Autrement dit, l'utilisateur peut continuer à voir la page originale et interagir avec elle alors que des données supplémentaires sont chargées. Une façon plus commune de charger des données de manière asynchrone est d'utiliser `l'objet XMLHttpRequest <http://www.w3.org/TR/XMLHttpRequest/>`_. Avec un objet XMLHttpRequest, vous pouvez ouvrir une connexion vers un serveur et envoyer ou recevoir des données via HTTP (ou HTTPS). Les objets XMLHttpRequest sont un peu délicats à utiliser et ne sont malheureusement pas supportés par tous les navigateurs. OpenLayers fournit une fonction inter-navigateur `XMLHttpRequest <http://code.google.com/p/xmlhttprequest/>`_ et l'enveloppe dans des méthodes commodes ``OpenLayers.Request``.

En général, toute communication initiée par des méthodes ``OpenLayers.Request`` est limitée à la règle de la même origine : les requêtes peuvent être réalisées uniquement avec le même protocole, le même domaine et le même port que le document dans lequel s'exécute le code. Les méthodes ``OpenLayers.Request`` vous permettent d'accéder aux données de manière asynchrone ou synchrone (les requêtes synchrones vont bloquer l'interface utilisateur tant que la requête est en cours).


.. note::
    Bien que le "cross-domain Ajax" existe, à moins qu'un utilisateur ait spécifiquement configuré les paramètres de sécurité de son navigateur, la règle de la même origine sera appliquée aux requêtes de type XMLHttpRequest. La fonctionnalité "cross-domain" est typiquement réalisée par la mise en place d'un proxy (sur la même origine) qui transmet toutes les communications à un serveur distant ou qui effectue les requêtes sans l'objet XMLHttpRequest (dans une balise script par exemple). Une nuance de la règle de la même origine est que le code s'exécutant dans la page d'un domaine peut définir la propriété ``document.domain`` à un suffixe du domaine original. Cela signifie que le code s'exécutant dans un document de sub.example.com peut demander des données de example.com en mettant le ``document.domain`` à example.com. Un document de example.com, cependant, ne peut pas préfixer la propriété de domaine pour demander des données d'un sous-domaine.

Les méthodes ``OpenLayers.Request`` correspondent aux verbes HTTP courants: GET, POST, PUT, DELETE, HEAD, et OPTIONS. Voir la `Request API documentation`_ pour une description de chacune de ces méthodes. Les courts exemples ci-dessous illustrent l'usage de ces méthodes sous une variété de conditions.

.. _`Request API documentation`: http://dev.openlayers.org/apidocs/files/OpenLayers/Request-js.html

Exemples d'utilisation
----------------------

1. Envoi d'une requête GET et traitement de la réponse.

.. code-block:: javascript

    function handler(request) {
        // if the response was XML, try the parsed doc
        alert(request.responseXML);
        // otherwise, you've got the response text
        alert(request.responseText);
        // and don't forget you've got status codes
        alert(request.status);
        // and of course you can get headers
        alert(request.getAllResponseHeaders());
        // etc.
    }

    var request = OpenLayers.Request.GET({
        url: "http://host/path",
        callback: handler
    });

2. Envoi d'une requête GET avec des paires clé:valeur.

.. code-block:: javascript

    function handler(request) {
        // do something with the response
        alert(request.responseXML);
    }

    var request = OpenLayers.Request.GET({
        url: "http://host/path",
        params: {somekey: "some value & this will be encoded properly"},
        callback: handler
    });

3. Envoi d'une requête GET où le handler est une méthode publique d'un certain objet.

.. code-block:: javascript

    // assuming obj was constructed earlier
    obj.handler = function(request) {
        this.doSomething(request);
    }
    
    var request = OpenLayers.Request.GET({
        url: "http://host/path",
        callback: obj.handler,
        scope: obj
    });

4. Envoi d'une requête GET synchrone. 

.. code-block:: javascript

    var request = OpenLayers.Request.GET({
        url: "http://host/path",
        async: false
    });
    // do something with the response
    alert(request.responseXML);

5. Envoi d'une requête POST avec certaines données.

.. code-block:: javascript

    // assuming you already know how to create your handler
    var request = OpenLayers.Request.POST({
        url: "http://host/path",
        data: "my data to post",
        callback: handler
    });

6. Envoi d'une requête POST avec un type de contenu spécifique (application/xml apr défaut).

.. code-block:: javascript

    // again assuming you have a handler
    var request = OpenLayers.Request.POST({
        url: "http://host/path",
        data: "this is text not xml!",
        headers: {
            "Content-Type": "text/plain"
        },
        callback: handler
    });

7. Envoi d'une requête POST avec des données "form-encoded".

.. code-block:: javascript

    var request = OpenLayers.Request.POST({
        url: "http://host/path",
        data: OpenLayers.Util.getParameterString({foo: "bar"}),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        callback: handler
    })

8. Envoi d'une requête GET puis abandon de celle-ci.

.. code-block:: javascript

    var request = OpenLayers.Request.GET(); // dumb, but possible
    request.abort();

9. Traitement des nombreuses façons dont une requête peut échouer.

.. code-block:: javascript

    function handler(request) {
        // the server could report an error
        if(request.status == 500) {
            // do something to calm the user
        }
        // the server could say you sent too much stuff
        if(request.status == 413) {
            // tell the user to trim their request a bit
        }
        // the browser's parser may have failed
        if(!request.responseXML) {
            // get ready for parsing by hand
        }
        // etc.
    }
    // issue a request as above

10. Envoi de requêtes DELETE, PUT, HEAD, et OPTIONS.

.. code-block:: javascript

    // handlers defined elsewhere
    
    var deleteRequest = OpenLayers.Request.DELETE({
        url: "http://host/path",
        callback: deleteHandler
    });
    
    var putRequest = OpenLayers.Request.PUT({
        url: "http://host/path",
        callback: putHandler
    });
    
    var headRequest = OpenLayers.Request.HEAD({
        url: "http://host/path",
        callback: headHandler
    });
    
    var optionsRequest = OpenLayers.Request.OPTIONS({
        url: "http://host/path",
        callback: optionsHandler
    });

11. (Rare) Envoi d'une requête GET en utilisant un proxy autre que celui spécifié dans OpenLayers.ProxyHost (la même règle d'origine s'applique).

.. code-block:: javascript

    // handler defined elsewhere
    var request == OpenLayers.Request.GET({
        url: "http://host/path",
        params: {somekey: "some value"},
        proxy: "http://sameorigin/proxy?url=" // defaults to OpenLayers.ProxyHost
    });

