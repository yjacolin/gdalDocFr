Documentation francophone pour GDAL / OGR
====

![Logo GDAL](/gdal/gdal/GDAL_logo.png)

Ce dépôt regroupe la traduction de la documentation et des examples de codes (recettes) pour les bibliothèques GDAL/OGR : [accéder au site](http://gdal.gloobe.org/)

Travail mis à disposition par l'[OSGeo France](http://osgeo.asso.fr/).

![Logo OSGeo France](http://osgeo.asso.fr/sites/default/files/color/osgeo2013-501f811b/logo.png)

## Site et projet

[GDAL/OGR](http://www.gdal.org/) est un couple de bibliothèques libres dédié à la lecture, l'écriture et au traitement des données à caractère géographique / spatial, géré par l'[OSGeo](http://www.osgeo.org/) :

* GDAL est le composant principal dédié aux fichiers raster, prenant en compte [133 formats](http://www.gdal.org/formats_list.html)
* OGR est son pendant pour les fichiers vectoriels ou assimilés, prenant en compte [79 formats](http://www.gdal.org/ogr_formats.html)

Consulter le [dépôt officiel de GDAL](https://github.com/OSGeo/gdal).

### Projets connus utilisant GDAL/OGR

Pour une liste complète, voir [Logiciels utilisant GDAL/OGR](http://gdal.gloobe.org/logicielutilisantgdal.html).

* [GeoDjango](https://code.djangoproject.com/wiki/GeoDjango) : cartouche spatial du framework web Python de référence Django, désormais intégré par défaut à ce dernier
* [Talend DI](https://github.com/talend-spatial/talend-spatial) : cartouche spatial de l'ETL (Extract Transform Load) libre Talend
* [GeoKettle](http://www.spatialytics.org/projects/geokettle/) : cartouche spatial de l'ETL (Extract Transform Load) libre Kettle
* [GeoServer](https://github.com/geoserver) : serveur cartographique
* [GRASS](http://grass.osgeo.org/) : logiciel SIG libre bureautique
* [gvSIG](http://www.gvsig.org) : logiciel SIG libre bureautique
* [MapNik](http://mapnik.org/) : boîte à outils de cartographie et webmapping en Python
* [MapServer](http://mapserver.org)
* [OpenEV](http://openev.sourceforge.net/)
* [QGIS](https://github.com/qgis/QGIS) : logiciel SIG libre bureautique et serveur

## Pour contribuer

Si vous utilisez GDAL et/ou OGR dans votre activité, n'hésitez pas à apporter vos contributions :
* soit, si vous êtes sensibilisés à git, directement sur le dépôt en faisant un fork puis des PR (Pull Requests) ;
* soit en soumettant une ressource (lien, tutoriel, snippet...) aux contributeurs.

## Pour installer GeoDocFr/GDAL/OGR

```bash
sudo apt-get install python-setuptools
python bootstrap
./buildout/bin/buildout
```
