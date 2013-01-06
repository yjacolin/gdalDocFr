.. _`gdal.gdal.formats.ogdi`:

===================
OGDI -- Pont OGDI
===================

.. warning::
    À partir de GDAL >= 1.5.0, il y a très peu de raison d'utiliser le pont 
    vers le pilote OGDI raster puisque les formats 
    :ref:`gdal.gdal.formats.divers_formats.adrgarc`, :ref:`gdal.gdal.formats.dted` 
    et :ref:`gdal.gdal.formats.divers_formats.rpftoc` (CADRG/CIB) sont gérés 
    nativement par GDAL.

Les sources de données raster OGDI sont géré par GDAL en lecture. À la fois les 
matrices et les familles devraient être géré, ainsi que la lecture des cartes de 
couleurs et les méta-données des projections. Le lecteur GDAL a pour but d'être 
utilisé avec le pilote OGDI 3.1, mais les pilotes OGDI 3.0 devrait aussi 
fonctionner.

Les jeux de données OGDI sont ouvert dans GDAL par la sélection de l'url GLTP. 
Par exemple, *gltp://gdal.velocet.ca/adrg/usr4/mpp1/adrg/TPSUS0101* ouvrira le 
jeu de données ADRG stocké dans /usr4/mpp1/adrg/TPSUS0101 sur la machine 
gdal.velocet.ca (en assumant qu'il y ait un serveur OGDI en fonctionnement) en 
utilisant le pilote 'adrg'. Cet accès par défaut à l'ensemble du serveur de 
données tentera de représenter toutes les couches (et tous les types de famille) 
comme des bandes, toutes à la résolution et à la région rapporté par le serveur 
de données lors de l'accès initial.

Il est également possible desélectionner une couche particulière et d'accéder à 
la famille d'un serveur de données OGDI en indiquant le nom de la couche dans le 
nom. Le nom du jeu de données GDAL 
``gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0102.IMG"`` : la matrice sélectionnera 
la couche nommée TPUS0102.IMG du jeu de données /usr4/mpp1/adrg/TPUS0101 sur le 
système local en utilisant le pilote ADRG, et accèdera à la famille de la 
matrice. Quand on accède à une couche spécifique decette manière, GDAL tentera 
de déterminer la région et la résolution à partir du document capabilities OGDI 
3.1. Notez que les serveurs de données OGDI 3.0 doivent avoir la couche et la 
famille définie dans le nom du jeu de données puisqu'ils ne peuvent pas être 
déterminer automatiquement.

Par exemple :

::
    
    gltp://gdal.velocet.ca/adrg/usr4/mpp1/adrg/TPUS0101
    gltp:/adrg/usr4/mpp1/adrg/TPUS0101
    gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0102.IMG":Matrix

Les couches de famille Matrix OGDI (couches d'entier pseudo-couleur) sont 
représentées comme une simple bande de raster avec une table de couleur. Bien 
que les couches Matrix contiennent des valeurs entières de 32 bits, elles sont 
représentées dans GDAL comme 8 couches. Toutes les valeurs au-dessus de 255 sont 
tronqué à 255, et seulement les 256 entrées de la table de couleur sont 
capturées. Puisque cela fonctionne bien pour les couches Matrix, il est espéré 
que les couches Matrix avec un domaine plus dynamique soient représenté dans un 
futur proche sous forme d'un autre type de données.

Les couches de famille d'Image OGDI peuvent en interne avoir un type RVB (1) qui 
est représenté sous forme de trois bandes dans GDAL, ou en Byte (2), UInt16 (3), 
Int16 (4) ou Int32 (5). Il n'y a pas de gestion pour les bandes de virgules 
flottantes dans OGDI 3.1.

Le pilote OGDI de GDAL représentera les sources de données OGDI comme ayant des 
aperçues *arbitraires*. N'importe quel raster de GDAL lu par des requêtes à 
une résolution réduite sera passé au pilote OGDI avec cette résolution réduite ; 
permettant potentiellement une efficacité dans la lecture des informations des 
aperçues à partir d'un serveur de données OGDI.

Si un serveur de données OGDI est ouvert sans avoir sélectionner le nom d'une 
couche dans le nom du jeu de données, et si le serveur de données a les 
capacités des styles OGDI 3.1, la liste des couches sera rendu disponible comme 
des méta-données de sous-jeu de données. Par exemple, la commande ``gdalinfo`` 
pourra renvoyer ce qui suit. Ces informations peuvent être utilisé pour établir 
les couches disponibles pour un accès direct.
::
    
    Subdatasets:
        SUBDATASET_1_NAME=gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0101.IMG":Matrix
        SUBDATASET_1_DESC=TPUS0101.IMG as Matrix
        SUBDATASET_2_NAME=gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0102.IMG":Matrix
        SUBDATASET_2_DESC=TPUS0102.IMG as Matrix
        SUBDATASET_3_NAME=gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0101.IMG":Image
        SUBDATASET_3_DESC=TPUS0101.IMG as Image
        SUBDATASET_4_NAME=gltp:/adrg/usr4/mpp1/adrg/TPUS0101:"TPUS0102.IMG":Image
        SUBDATASET_4_DESC=TPUS0102.IMG as Image

.. seealso::

* `ogdi.sourceforge.net <http://ogdi.sourceforge.net/>`_

.. yjacolin at free.fr, Yves Jacolin - 2009/03/14 16:00 (trunk 14660)