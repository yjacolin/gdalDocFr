.. _`gdal.gdal.gdal2tiles`:

gdal2tiles.py
==============

génère un répertoire avec des tuiles TMS, un KML et des visualisateurs web simples.

Usage
------

::
    
    gdal2tiles.py [-title "Title"] [-publishurl http:*yourserver/dir/]
                [-nogooglemaps] [-noopenlayers] [-nokml]
                [-googlemapskey KEY] [-forcekml] [-v]
                input_file [output_dir]

Description
------------

La commande génère un répertoire avec de petites tuiles et métadonnées, suivant 
la spécification du Service de Tuilage de carte de l'OSGeo. Des pages web 
simples avec des visualiseurs basés sur Google Map et OpenLayers sont générés 
également - tout le monde peut confortablement explorer vos cartes en ligne et 
vous n'avez pas besoin d'installer ou de configurer un logiciel spécial (comme 
Mapserver) et la carte s'affiche très rapidement dans le navigateur web. Vous 
avez seulement besoin de télécharger votre répertoire généré dans un serveur web.

``GDAL2Tiles`` créé également les métadonnées nécessaires pour Google Earth 
(*SuperOverlay* KML), dans le cas où la carte fournie utilise une projection 
*EPSG:4326*.

Les fichiers world et les références spatiales incluses sont utilisés durant la 
génération des tuiles, mais vous pouvez publier également une image sans le 
géoréférencement.

* **-title "Title" :** titre utilisé pour les métadonnées générées, les 
  visualisateurs web et les fichiers KML.
* **-publishurl http:*yourserver/dir/ :** adresse du répertoire dans lequel 
  vous allez télécharger le résultat. Il doit se terminer par un slash.
* **-nogooglemaps :** ne génère pas de page HTML de base pour Google Maps. 
* **-noopenlayers :** ne génère pas de page HTML de base pour OpenLayers. 
* **-nokml :** ne génère pas de fichier KML pour Google Earth. 
* **-googlemapskey KEY :** clé pour votre domaine généré sur la page web de 
  l'API de Google Maps (http://www.google.com/apis/maps/signup.html). 
* **-forcekml :** force la régénération des fichiers KML. Le fichier en entrée 
  doit utiliser des coordonnées *EPSG:4326* !
* **-v :** génère une sortie verbeuse lors de la génération des tuiles.

.. warning::
    gdal2tiles.py est un script Python qui nécessite la compilation avec la 
    liaison python de nouvelle génération.

.. yves at georezo.net, Yves Jacolin - 2010/12/29 15:10 (http://gdal.org/gdal2tiles.html Trunk r21324)
