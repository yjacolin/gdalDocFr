.. _`gdal.ogr.formats.gtm`:

=====================
GTM - GPS TrackMaker
=====================

(à partir de GDAL 1.7.0)

`GPSTrackMaker <http://www.gpstm.com/">`_ est nu programme qui est compatible avec 
plus de 160 modèles GPS. Il vous permet de créer vos propres cartes. Il gère les 
cartes vecteurs et images.

Le pilote OGR gère la lecture et l'écriture des fichiers GTM 211 (.gtm) ; cependant, 
dans cette implémentation nous ne gérons pas les images et les routes. Waypoints 
et traces sont gérés.

Bien que GTM gère plusieurs types de données, comme NAD 1967, SAD 1969, et 
d'autres, le fichier en sortie du pilote d'OGR utilisera WGS 1984. Le pilote GTM 
lira proprement seulement les fichiers GTM géoréférencés en WGS 1984 (si ce 
n'est pas le cas une alerte sera envoyée).

Le pilote OGR gère seulement les POINT, LINESTRING, et MULTILINESTRING.

Exemple
=========

* La commande ``ogrinfo`` peut être utilisée opur dumper le contenu d'un fichier 
  de données GTM :

  ::
    
    ogrinfo -ro -al input.gtm

* Utilisez l'option *-sql* pour mapper les noms des champs vers ceux autorisées par 
  le schéma GTM :
  ::
    
    ogr2ogr -f "GPSTrackMaker" output.gtm input.shp -sql "SELECT field1 AS name, field2 AS color, field3 AS type FROM input"

* Exemple de traduction à partir de PostGIS vers GTM :
  ::
    
    ogr2ogr -f "GPSTrackMaker" output.gtm PG:"host=hostaddress user=username dbname=db password=mypassword" -sql "select filed1 as name, field2 as color, field3 as type, wkb_geometry from input" -nlt MULTILINESTRING

  .. note:: vous devez définir le type de couche en tant que POINT, LINESTRING, 
    ou MULTILINESTRING.

Voir également
===============

* `Home page pour le Programme GPS TrackMaker <http://www.gpstm.com/>`_
* `Documentation du format GTM 211 <http://www.gpstm.com/download/GTM211_format.pdf>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/07/21 (trunk 17609)