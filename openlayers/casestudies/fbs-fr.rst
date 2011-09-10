FBS
---

.. _`FBS`: http://www.mlslistingonlinesoftware.com/
.. _`flexmls Web`: http://www.flexmls.com/

`FBS`_ est une entreprise coopérative basée à Fargo, Dakota du Nord, qui crée des logiciels et des services pour l'industrie immobilière, dont son produit phare `flexmls Web`_. FBS utilise OpenLayers pour ajouter de la valeur à son produit en ligne, en offrant des cartes hautement interactives et riches en données.

.. image:: _static/fbs1.png
  :align: right

Quand FBS a décidé de réinventer sa plate-forme de cartographie, toutes les options étaient sur la table. Au final, les autres produits de cartographie les plus populaires se montrèrent trop peu flexibles pour les besoins de la plate-forme. Dans l'industrie immobilière, plusieurs fonctions sont requises pour une plate-forme cartographique : FBS cherchait à pouvoir afficher des photographies aériennes, des plans de rues, des cartes parcellaires, des zones inondables, et plus encore - autant de besoins nécessitant une librairie logicielle capable de fonctionner avec beaucoup de sources et d'API différentes. De plus, FBS avait besoin d'afficher une trop grande quantité de données pour les objets d'une API Javascript. La solution idéale devait également être suffisamment flexible pour permettre de mettre en place des fonctions de cartographies supplémentaires, tout en laissant la porte ouverte à des changements futurs de direction si nécessaire. OpenLayers permettait tout cela.

FBS a commencé sa transformation cartographique en créant une infrastruction de tuilage destinée à alimenter OpenLayers. À l'aide de Mapserver, ils furent en mesure de générer un cache de tuiles personnalisé permettant d'afficher des informations plus détaillées comme les limites de parcelles fiscales, les régions de Service de Listing Multiple (Multiple Listing Service), des informations liées à des zones spécifiques à chaque client et plus. Si les clients de FBS possèdent des données géospatiales, il est possible de générer des cartes pour les afficher et OpenLayers sera plus qu'heureux de les fournir.

Beaucoup des API de cartographie disponibles sont l'équivalent d'une interface extrêmement rigide. OpenLayers offre un contrôle sans pareil sur l'interface cartographique, tant pour l'apparence que pour les fonctionnalités. L'interface cartographique de FBS possède un style unique qui la distingue de la majorité des cartes en lignes. De plus, il est possible d'étendre OpenLayers pour fournir des outils d'interface personnalisés si nécessaire.

.. _`DM Solutions Group`: http://www.dmsolutions.ca/

Avec leur partenaire `DM Solutions Group`_, FBS a pu capitaliser sur les outils existants comme l'édition vecteur, la gestion des couches, les pop-ups et les outils de mesure de distances. Avec un contrôle total sur les outils, FBS peut changer leur comportement et les connecter à des services personnalisés, adaptables à leurs spécifications. En combinant plusieurs de ces outils côté client et les services coté serveur, FBS a créé quelques outils qui offrent des fonctionnalités-clés spécifiques aux applications, sans même avoir à hacker une API fermée et confuse. Le résultat est une application de cartographie qui fonctionne comme elle doit fonctionner, au lieu d'être une demande d'amélioration supplémentaire sur la liste déjà interminable d'une entreprise géante...

.. image:: _static/fbs2.png
  :align: left

Avec le grand nombre de propriétés incluses dans le système web de flexmls, la solution cartographique de FBS avait besoin de permettre aux clients de visualiser tous les éléments présents dans leur secteur, pas uniquement les McNuggets. A l'aide d'un peu de codage côté serveur et de Mapserver, une superposition personnalisée affichant toutes les données d'un secteur donné peut être générée et affichée rapidement et efficacement par OpenLayers. Ce dernier acceptant énormément de formats de données différents, le ciel est la seule limite à la résolution de problèmes de données denses et touffues comme on en rencontre parfois ! Cela se traduit par une manipulation de la carte (zoom, panorama...) pour une mise à jour rapide de la carte, impossible avec des API Javascript qui doivent généralement gérer tout un ensemble de points d'intérêt dans le navigateur de l'utilisateur final. 

Un autre grand atout d'OpenLayers est la flexibilité qu'il fournit face à un avenir incertain. Comme OpenLayers repose sur des protocoles ouverts, il peut être configuré pour récolter des données cartographiques d'une grande variété de sources. Dans les secteurs où il est hors de question d'acheter une imagerie aérienne de grande qualité, il est possible de configurer OpenLayers pour afficher les cartes satellites de Google. Il s'agit là d'une alternative économique pour les clients n'ayant accès qu'à de l'imagerie particulièrement chère à l'achat, ou qui vivent dans des secteurs ruraux où une couverture excellente n'est tout simplement pas disponible. Cela aide également différents clients internationaux pour les endroits où la fiabilité des données géographiques peut être limitée. Si les autres fournisseurs de cartographie offrent un service cartographique que FBS n'a pas, la nature d'OpenLayers lui permet de l'intégrer sans avoir à retourner sur la table de dessin.

Pour plus d'informations, contacter :

.. _`Brandon Medenwald`: brandon@fbsdata.com
  
  `Brandon Medenwald`_
  Développeur Web, employé et membre de la coopérative FBS

