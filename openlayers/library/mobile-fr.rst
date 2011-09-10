Navigation mobile
++++++++++++++++++

La navigation mobile demande généralement une manière différente de naviguer. 
Les contrôles de Navigation et de Navigation tactile implémenté dans OpenLayers 
tentent de prendre en charge cela correctement par défaut, en utilisant quel que 
soit les événements disponibles dans le navigateur utilisé.

Ces contrôles ont été ajouté après OpenLayers 2.10.

Déplacement de carte
---------------------

Les navigateurs qui gère les événements tactiles (touchstart/touchmove/touchend) 
géreront le déplacement de la carte par le toucher, de la même manière que vous 
naviguer généralement sur les autres applications cartographiques sur ces 
plateformes.

À la fois le contrôle de la navigation et la navigation tactile gère cette 
méthode de déplacement.

Zoom par pincement
--------------------

Sur les matériels qui gèrent les événements tactiles multiples, il est possible 
de zoomer en pinçant vers le centre ou vers l'extérieur. Cela est possible par 
Control.PinchZoom, qui utilise en interne Handler.PinchZoom.

À la fois le contrôle de la navigation et la navigation tactile inclus cette 
méthode de zoome par défaut.

Le zoom par pincement fonctionne seulement si vous matériels délivre 
l'information sur les événements tactiles multilpes aux navigateurs. Cette 
gestion existe dans iOS 2.0+ et a été ajouté au moment de l'Android 2.2 mais pas 
tous les Android délivrent cette information au navigateur. Pour tester si votre 
matériel délivre bien cette information, vous pouvez visiter la 

.. _`Page de test Multitouch`: http://bit.ly/eDZrIw

Tap Panning
-----------
Dans le but de gérer les navigateurs tactile qui ne gère pas les événements 
tactiles, OpenLayers tente de gérer le 'tap panning', ou déplacement vers le 
centre d'une tape sur la carte. Combiné avec un ensemble de contrôle de zoom, 
cela permet à ces navigateurs de naviguer dans la carte.

Cette fonctionnalité est activée par défaut. Pour la désactiver explicitement 
vous pouvez définir ''{'clickOptions': {'tap': false}}'' dans les options du 
contrôle de navigation.

Il y a quelques matériels mobiles qui se comportent de manière similaire aux 
navigateurs pour la tape. : si vous avez un mécanisme de détection avancé pour 
trouver ces navigateurs et désirez activer explicitement la navigation par 
déplacement par tape, vous pouvez faire cela en passant true comme option du 
clic par tape.

En général, les matériels qui gèrent la tape mais pas le tactile zoomeront sur un 
double clic. Il n'y a généralement aucune manière d'empêcher ce comportement.

Gestion des navigateurs mobiles
---------------------------------

+----------------+---------------------+------------------+---------------+-------------+
| Navigateur     | Événements tactiles | Multiple touches | Accéléromètre | géolocation |
+================+=====================+==================+===============+=============+
| iOS (4.x)      | oui                 | oui              | oui           | oui         |
+----------------+---------------------+------------------+---------------+-------------+
| iOS (3.x)      | oui                 | oui              | non           | oui         |
+----------------+---------------------+------------------+---------------+-------------+
| iOS (2.x)      | oui                 | oui              | non           | ?           |
+----------------+---------------------+------------------+---------------+-------------+
| iOS (1.x)      | oui                 | non              | non           | ?           |
+----------------+---------------------+------------------+---------------+-------------+
| Android        | oui                 | non              | non           | oui         |
+----------------+---------------------+------------------+---------------+-------------+
| Opera Mobile   | non                 | non              | non           | oui         |
+----------------+---------------------+------------------+---------------+-------------+
| Symbian        | non                 | non              | non           | non         |
+----------------+---------------------+------------------+---------------+-------------+
| IE7 (WP7)      | non                 | non              | non           | non         |
+----------------+---------------------+------------------+---------------+-------------+
| Firefox 4(1)   | non                 | non              | non           | oui         |
+----------------+---------------------+------------------+---------------+-------------+

1. Firefox 4 beta gère les événements tactiles sous Windows 7 via les événements
   MozTouchDown/MozTouchMove. Dû au manque de plateforme de test, le code OpenLayers 
   ne gère pas actuellement ce type d'événement "touche".
2. Le navigateur android possède aucune gestion pour les événements tactiles 
   multiples. Des utilisateurs ont remonté que cela fonctionnait sur des modèles 
   Samsung spécifique pour l'utilisation de zoom par pincement dans OpenLayers 
   et maps.google.com avec la 2.1, mais perd cette fonctionnalité après 
   plusieurs une mise à jour en 2.2. Il y a une `ticket de bug ouvert`_ sur 
   Android sur le support des événements tactiles multiples dans le DOM, mais 
   aucune planification n'a été prévue.

.. _`ticket de bug ouvert`: http://code.google.com/p/android/issues/detail?id=11909   
