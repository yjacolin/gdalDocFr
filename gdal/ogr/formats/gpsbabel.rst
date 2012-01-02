.. _`gdal.ogr.formats.gpsbabel`:

GPSBabel
=========

(GDAL/OGR >= 1.8.0)

Le pilote GPSBabel repose sur la commande `GPSBabel <http://www.gpsbabel.org>`_ 
pour accéder aux différents formats de fichier GPS.

L'exécutable GPSBabel doit être accessible à travers le PATH.

Gestion de la lecture
----------------------

Le pilote nécessite le pilote :ref:`gdal.ogr.formats.gpx` pour gérer entièrement 
la lecture (via la bibliothèque Expat) et être capable de parser la sortie de 
GPSBabel, puisque GPX est utilisé comme format intermédiaire.

Les couches renvoyées peuvent être des waypoints, routes, route_points, tracks, 
track_points en fonction des données en entrée.

La synthaxe pour définir une source de données en entrée est : 
*GPSBabel:gpsbabel_file_format[,gpsbabel_format_option]*:[features=[waypoints,][tracks,][routes]:]filename*
où :

* *gpsbabel_file_format* est un des `formats de fichier <http://www.gpsbabel.org/capabilities.shtml>`_ 
  pris en charge par GPSBabel.
* *gpsbabel_format_option* est n'importe quelles options pris en charge par le 
  format spécifié par GPSBabel (référez vous au document de chaque format de 
  GPSBabel)
* *features=* peut être utilisé pour modifier le type de feature que GPSBabel 
  importera. waypoints correspond à l'option -w de la ligne de commande de 
  gpsbabel, tracks correspond à -t et routes correspond à -r. Cette option peut 
  être utilisé pour nécessité un import de donnée complet à partir du recepteur 
  GPS qui sont lent et pour lesquels GPSBabel pourrait ne récupérer que les 
  waypoints par défaut. Voyez la documentation sur 
  `Route and Track modes <http://www.gpsbabel.org/htmldoc-1.3.6/Route_And_Track_Modes.html>`_ 
  pour plus de détails.
* *filename* peut être un fichier réel sur disque, un fichier via l'API des 
  fichiers virtuels de GDAL, ou un matériel spécial pris en charge par GPSBabel 
  tel que "usb:", "/dev/ttyS0", "COM1:", etc.. Ce qui est réellement géré dépend 
  du format de GPSBabel utilisé.

Alternativement, pour quelques formats de GPSBabel sélectionné, spécifier simplement 
le nom du fichier peut être suffisant. La liste pour l'instant est :

* garmin_txt
* gdb
* magellan
* mapsend
* mapsource
* nmea
* osm
* ozi

L'option de configuration *USE_TEMPFILE=YES* peut être utilisé pour créer un fichier 
GPX temporaire sur disque au lieu d'un en mémoire, lors de la lecture d'un gros 
volume de données.

Gestion de l'écriture
----------------------

Le pilote repose sur le pilote GPX pour créer un fichier intermédiaire qui sera 
finalement traduit par GPSBabel vers le format de GPSBabel désiré (le pilote GPX 
ne nécessite pas d'être configuré pour la gestion de la lecture pour la gestion 
de l'écriture de GPSBabel).

Les géométries gérées, options et autres problèmes de création sont ceux du pilote 
GPX. Référez vous à la page :ref:`gdal.ogr.formats.gpx` pour plus de détails.

La syntaxe pour définir une source de données en sortie est :
*GPSBabel:gpsbabel_file_format[,gpsbabel_format_option]\*:filename* où :

* *gpsbabel_file_format* est un des 
  `formats de fichier <http://www.gpsbabel.org/capabilities.shtml>`_ pris en 
  charge par GPSBabel.
* *gpsbabel_format_option* est une des options pris en charge par le format de 
  GPSBabel définie (référez vous à la documentation des formats de GPSBabel)

Alternativement, vous pouvez juste passer un nom de fichier comme nom de source 
de données en sortie et définir l'option de création du jeu de données 
GPSBABEL_DRIVER=gpsbabel_file_format[,gpsbabel_format_option]*

L'option de configuration *USE_TEMPFILE=YES* peut être utilisé pour créer un fichier 
GPX temporaire sur disque au lieu d'un en mémoire, lors de l'écriture d'un gros 
volume de données.

Exemples
*********

* Lire les waypoints à partir d'un récepteur USB Garmin :
  ::
    
    ogrinfo -ro -al GPSBabel:garmin:usb:


* Convertir un shapefile vers un format Magellan Mapsend :
  ::
    
    ogr2ogr -f GPSBabel GPSBabel:mapsend:out.mapsend in.shp

Voir également
---------------

* `Home page de GPSBabel <http://www.gpsbabel.org>`_
* `Formats de fichier de GPSBabel <http://www.gpsbabel.org/capabilities.shtml>`_
* :ref:`gdal.ogr.formats.gpx`

.. yjacolin at free.fr, Yves Jacolin - 2011/07/21 (trunk 19796)
