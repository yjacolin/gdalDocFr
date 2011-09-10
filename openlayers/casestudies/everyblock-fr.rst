.. _everyblock_study:

EveryBlock
==========

.. include:: everyblock_about-fr.inc

|everyblock-intro|

EveryBlock a étudié différentes APIs Javascript pour son site, comme l'API Javascript de Google Maps. Toutefois, EveryBlock souhaitait que ses cartes ressemblent au reste du site, avec la même charte graphique, le même style, etc. Paul Smith, co-fondateur d'EveryBlock, explique la décision de sa société en rappelant qu'avec Google Maps, "le composant principal - la carte elle-même - est hors de vos mains".

.. image:: _static/everyblock_sm.png
   :align: right 

De l'autre côté, avec OpenLayers, EveryBlock a le contrôle complet : sur le style, les données, les restrictions d'usage, et plus encore. En utilisant OpenLayers, EveryBlock est apte à créer pour son site Internet des cartes qui soient en leur contrôle, plutôt que dépendantes de l'API d'un fournisseur.

En commençant avec le jeu de données TIGER du Bureau états-unien du recensement, EveryBlock a utilisé Mapnik pour créer des tuiles attractives -- en s'aidant au début de TileCache, puis en utilisant une routine personnelle de génération et de distribution de tuiles. OpenLayers a été en mesure de répondre à ces deux besoins, en fournissant la possibilité de créer des classes de couches personnalisées pour charger les tuiles d'EveryBlock "sur commande".

Un autre avantage de l'utilisation de la librairie OpenLayers est la possibilité de créer rapidement et facilement des contrôles personnalisés, adaptés à l'application en termes de fonctionnalité. A l'aide du CSS et d'options de création de cartes simples d'usage, EveryBlock a été en mesure de créer un set minimal de contrôles utilisateurs, permettant une navigation facile et rapide sur la carte, avec des éléments graphiques harmonisés au reste du site.

.. image:: _static/eb-charlotte.png
   :align: left

En plus de l'utilisation de fonctionnalités inclues par défaut dans OpenLayers, EveryBlock a été en mesure d'étendre OpenLayers pour permettre l'affichage de grandes quantités de données, utilisant des outils serveur personnalisés pour créer des clusters de données. A l'aide des paramètres de style des vecteurs, ils sont en mesure de créer des éléments qui se redimensionnent automatiquement -- grâce aux fonctions de vectorisation dans le navigateur -- pour représenter différents éléments -- nouvelles histoires, photos, et plus encore. Cette fonctionnalité permet à EveryBlock de créer d'impressionnantes cartes riches en signification, à l'intérieur même de l'environnement limité du navigateur.

Au fur et à mesure de la croissance d'EveryBlock, son usage d'OpenLayers a changé. Paul Smith continue d'encourager l'utilisation d'OpenLayers pour EveryBlock, et rappelle qu'"OpenLayers est par défaut suffisamment sophistiqué pour beaucoup d'applications, mais sa puissance véritable est dans son design, qui permet de construire facilement des solutions personnalisées ; il ne lutte pas contre, ni ne cache la nature de Javascript -- un langage sous-estimé mais très puissant -- et permet ainsi de coder de nouvelles fonctionnalités avec une grande économie".

L'utilisation d'OpenLayers a offert à EveryBlock la fonctionnalité qui lui a permis de mettre son site Internet sur pied, et plutôt que d'utiliser Google Maps, comme tant d'autres sites, EveryBlock a été capable d'allier des composants Open Source comme OpenLayers et Mapnik à des données ouvertes du gouvernement des États-Unis pour construire une couche élémentaire de cartographie. La possibilité d'étendre OpenLayers au support de nouvelles sources de données, et d'utiliser les fonctionnalités avancées d'OpenLayers comme la vectorisation en ligne pour sauvegarder la génération d'image côté serveur et plus, est un aspect clé de l'utilisabilité de l'interface cartographique d'EveryBlock.

Pour plus d'informations, contactez :

  Paul Smith

.. _`Paul Smith`: http://www.pauladamsmith.com/
.. _`Election Day Advent Calendar`: http://www.electiondayadventcalendar.com/
.. _`Friends of the Bloomingdale Trail`: http://www.bloomingdaletrail.org/
  
  `Paul Smith`_ est cofondateur et développeur à EveryBlock. Il crée des sites 
  internet et des application sur le Web depuis 1994. Il est également co-créateur
  du `Election Day Advent Calendar`_, et membre fondateur de `Friends of the 
  Bloomingdale Trail`_. Il vit à Chicago.
