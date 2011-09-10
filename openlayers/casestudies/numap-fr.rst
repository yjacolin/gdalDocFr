.. _`NuMaps`: http://www.numaps.com.au/

.. _numaps_study:

NuMaps
======

`NuMaps`_ est une startup australienne qui publie les données australiennes du recensement (ABS, Bureau Australien des Statistiques) sous forme de DemographicDrapes (TM), soit une simple superposition de cartes thématiques semi-transparentes. Ces cartes sont fournies sous forme de service WMS pour ceux qui utilisent des applications permettant d'accéder aux services OGC (Open Geospatial Consortium). À l'origine, Numaps pensait utiliser l'API Google Maps mais son choix se porta finalement sur OpenLayers, autant pour la possibilité offerte par ce dernier d'accéder à plusieurs fournisseurs de cartes que pour l'interface robuste aux services OGC qu'elle constitue.

.. image:: _static/numaps_interface.jpg
   :align: right

Un des éléments-clés du choix d'utiliser OpenLayers fut la compatibilité avec les services web de l'OGC. Cette dernière était et reste stratégiquement très importante. Elle permet à NuMaps d'être compatible avec une gamme extrêmement large (et toujours croissante) d'applications clientes. Ce support des services web OGC par OpenLayer contribua largement au choix de celle-ci comme base de l'application de NuMaps.

En plus d'utiliser des sources de données OGC et des fonds de carte Google, NuMaps, en tant que client Google Ads, intègre également sans problèmes d'autres services gratuits de Google dans ses applications OpenLayers, à l'instar du géocodage ou des Google Charts. Cette possibilité d'utiliser et de combiner différents services est l'une des principales forces apportées par l'utilisation d'OpenLayers comme framework de webmapping.

NuMaps utilise en arrière-plan un WMS CubeWerx. CubeWerx est l'environnement serveur le plus adapté aux services OGC sur le marché. La combinaison de CubeWerx en arrière-plan et d'OpenLayers comme environnement privilégié d'applications a permis à NuMaps d'obtenir l'interopérabilité recherchée, avec l'extensibilité du support d'un nombre croissant de clients. À l'aide de technologies comme les Styled Layer Descriptors (SLD), NuMaps peut communiquer des informations de style au serveur WMS CubeWerx à la volée. L'utilisation que Numaps fait des SLD (décrire les règles et les filtres relatifs au style des données) permet aux internautes inscrits de modifier les filtres DemographicDrape externes [SLD], de créer des thèmes et des styles de carte personnalisés pour répondre aux besoins de leurs applications, en plus de tous les DemographicDrapes standards pré-configurés déjà disponibles.

.. image:: _static/numaps_styler.jpg
   :align: left 

Au-delà des DemographicDrapes fournies aux inscrits, certaines sont proposées gratuitement à l'aide d'un visualiseur basé sur OpenLayers. Les utilisateurs visés par ce service sont multiples, depuis les simples curieux d'un survol de données démographiques sur un fond Google Maps jusqu'aux démographes ayant besoin d'accéder aux DemographicDrapes comme couches intégrées à des processus d'analyse géo-démographique plus complexes.

Armé avec les outils fournis par OpenLayers et CubeWerx, NuMaps développe également une activité de fournisseur d'applications OpenLayers spécifiques, qui accèdent aux DemographicDrapes hébergées par NuMaps. À l'aide de nombreuses couches DemographicDrapes, une application a été développée pour assiter une agence gouvernementale à déterminer où implanter des services de santé à destination des peuples indigènes. Cette application permettait l'agrégation interactive de statistiques basées sur des polygones. OpenLayers a permis à NuMaps de développer des contrôles personnalisés, afin de créer des flux de travail faciles à suivre. Ces contrôles personnalisés ont permis à une application personnalisée de répondre aux besoins complexes des utilisateurs, tout en maintenant une simplicité de l'interface utilisateur peu fréquente avec d'autres outils de geoprocessing plus complexes.

NuMaps est un utilisateur avide d'OpenLayers, et continue à développer son usage d'OpenLayers au fil du temps.

.. _`Brad Spencer`: brad@numaps.com.au

Pour plus d'informations contacter :

|  `Brad Spencer`_
|  NuMaps
|  Australia

