.. _`gdal.gdal.gdallocationinfo`:

==================
gdallocationinfo
==================

Outil de requête raster

Usage
=====

Usage :
::
    
    gdallocationinfo [--help-general] [-xml] [-lifonly] [-valonly]
                   [-b band]* [-l_srs srs_def] [-geoloc] [-wgs84]
                   srcfile [x y]

Description
=============

La commande ``gdallocationinfo`` fournie un mécanisme pour demander des 
informations sur un pixel pour une localisation donnée dans l'un des différents 
systèmes de coordonnées gérés. Plusieurs options de rapport sont proposés.

* **-xml :** le rapport en sortie sera formaté en XML pour facilité le 
  post-traitement.
* **-lifonly :** le seul retour est la production des noms de fichier à partir 
  de la demande de LocationInfo en fonction de la base de données (ie pour 
  identifier le fichier impacté à partir des VRT).
* **-valonly :** le seul retour sont les valeurs du pixel sélectionné sur 
  chaque bandes sélectionnées.
* **-b band :** sélectionne une bande à interroger. Plusieurs bandes peuvent 
  être listées. Par défaut toutes les bandes sont interrogées.
* **-l_srs srs def :** Le système de coordonnées de la localisation x et y en 
  entrée.
* **-geoloc :** indique que les points x et y en entrée sont dans le système de 
  géoréférencement de l'image.
* **-wgs84 :** indique que les points x et y  en entrée sont en lat, long WGS84.
* **srcfile :** le nom de la source de données raster GDAL.
* **x :** localisation X du pixel cible. Par défaut le système de coordonnées 
  est pixel/ligne sauf si *-l_srs*, *-wgs84* ou *-geoloc* sont fournie.
* **y :** localisation Y du pixel cible. Par défaut le système de coordonnées 
  est pixel/ligne sauf si *-l_srs*, *-wgs84* ou *-geoloc* sont fournie.

Cette commande a pour objectif de fournir diverses informations d'un pixel. Pour 
l'instant il rapporte trois choses :

* la localisation du pixel dans l'espace pixel/ligne.
* le résultat d'une requête de méta-données LocationInfo en fonction de la 
  source de données - pour l'instant cela est seulement implémenté pour les 
  fichiers VRT qui rapportera le(s) fichier(s) utilisé(s) pour satisfaire les 
  requêtes pour ce pixel.
* la valeur du pixel du raster pour ce pixel pour toutes ou un sous-ensemble de 
  bande(s).
* la valeur du pixel non ajusté si une échelle et/ou un décalage est appliqué à 
  la bande.

Le pixel sélectionné est interrogé par les coordonnées x/y sur la ligne de 
commande, ou lu par l'entrée standard (stdin). Plus d'une paire de coordonnées 
peut être fournies lors de la lecture des coordonnées par l'entrée standard. Par 
défaut, les coordonnées pixel/ligne sont attendue. Cependant lors de 
l'utilisation des options *-geoloc*, *-wgs84*, ou *-l_srs* il est possible de 
définir la localisation dans d'autres système de coordonnées.

Le rapport par défaut est au format texte lisible. Il est possible de récupérer 
une sortie en xml avec l'option *-xml*.

Afin de pouvoir utiliser des scripts, les options *-valonly* et *-lifonly* sont 
fournie pour restreindre la sortie aux valeurs de pixels réels, ou les fichiers 
LocationInfo identifiés pour le pixel.

Il est prévue que des possibilités de rapport supplémentaire seront ajouté à 
``gdallocationinfo`` dans le futur.

Exemple
========

Exemple simple reportant un pixel (256,256) sur le fichier *utm.tif*.
::
    
    $ gdallocationinfo utm.tif 256 256
    Report:
        Location: (256P,256L)
        Band 1:
        Value: 115

Requêter un fichier VRT fournissant la localisation en WGS84 et récupérant le 
résultat en xml :
::
    
    $ gdallocationinfo -xml -wgs84 utm.vrt -117.5 33.75
    <Report pixel="217" line="282">
        <BandReport band="1">
        <LocationInfo>
            <File>utm.tif</File>
        </LocationInfo>
        <Value>16</Value>
        </BandReport>
    </Report>


.. yjacolin at free.fr, Yves Jacolin - 2010/12/29 15:44 (http://gdal.org/gdallocationinfo.html Trunk r21324)