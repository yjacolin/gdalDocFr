.. _`gdal.install`:

Installation
===============

.. Rajouter les liens http://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries

Binaires GDAL/OGR
-------------------

Le projet GDAL ne produit pas de binaire régulier téléchargeable (exécutable) pour 
chaque version. Cependant, des efforts sont réalisés pour produire des binaires prêt 
à l'emploi.

FWTools
********

Le `binaire FWTools <http://trac.osgeo.org/gdal/wiki/FWTools>`_ pour les systèmes Linux et Windows inclus l'ensemble des 
bibliothèques, commandes, la gestion de Python et la documentation de GDAL et  
d'autres choses encore (dont le visualiseur OpenEV). Des informations supplémentaires 
sont disponibles sur le site de `FWTools <http://fwtools.maptools.org/>`_

La dernière version de FWtools pour Windows, la version 2.4.7, date de la pre-version 
pre-1.6 de GDAL. Pour bénéficier de la dernière et meilleure version, vous pouvez 
vous référez aux autres builds binaire mentionnés dans la section Windows plus bas.

Les binaires FWTools pour Linux doivent fonctionner sur presque tous les systèmes 
Linux Intel moderne (leur production a débuté avec la série expérimentales de la 
série des 3.0.X).

Linux
*******

Fedora
````````

Fedora, depuis la version 7, inclus les binaires GDAL.

Entreprise Linux GIS (ELGIS)
````````````````````````````

L'effort `ELGIS <http://elgis.argeo.org/>`_ fournie des RPMs de différentes applications SIG pour Enterprise 
Linux et ses dérivés (RHEL, CentOS, Scientific Linux).

OpenSuSE
`````````

Les RPM de GDAL pour OpenSuSE avec d'autres outils géospatial sont publiés sur http://download.opensuse.org/repositories/Application:/Geo/

Debian
```````

L'équipe `SIG de Debian <http://wiki.debian.org/DebianGis>`_ maintient des 
`paquets GDAL <http://packages.debian.org/cgi-bin/search_packages.pl?keywords=gdal&searchon=names&subword=1&version=all&release=all>`_ 
pour `Debian GNU/Linux <http://en.wikipedia.org/wiki/Debian>`_.

Ubuntu
````````

Un nouveau UbuntuGIS est disponible sur `launchpad d'UbuntuGIS <https://launchpad.net/~ubuntugis>`_ 
et fournit des paquets à jour de GDAL pour Ubuntu Hardy, Karmic et Lucid. Pour 
plus d'informations, vous pouvez consulter la page `UbuntuGIS <https://wiki.ubuntu.com/UbuntuGIS>`_.

MacOS X
*********

William Kyngesburye maintien un ensemble de builds pour GDAL et d'autres logiciels 
SIG sur http://www.kyngchaos.com/software:frameworks

Windows
********

* Tamas Szekeres maintien un ensemble complet de paquetages binaires pour Win32 
  et Win64 (compilé avec VC2003/VC2005/VC2008/VC2010) disponible à l'endroit 
  suivant : http://www.gisinternals.com/sdk/

  Ces paquets sont basés sur le développement actuel et les branches stables compilées 
  à partir du SVN journalier de GDAL. Les paquets SDK correspondant sont également 
  disponibles pour téléchargement à partir de cet endroit. Les paquets -devel 
  sont basé sur la version en développement (1.9.0dev au moment de la rédaction), 
  et les paquets -stable sont basés sur la dernière branche de la version stable 
  (1.8 au moment de la rédaction).

* `MapServer pour Windows (MS4W) <http://www.maptools.org/ms4w/>`_ est un installeur populaire qui contient GDAL, 
  MapServer, et le serveur web Apache. Maintenu par `Gateway Geomatics <http://www.gatewaygeomatics.com/>`_. 
* Des binaires Windows via MinGW sont disponibles ici http://map.hut.fi/files/Geoinformatica/win32/
* Geoinformatica-yy-mm-dd.zip contient GDAL (habituellement une version de développement), Perl-GDAL, Perl, et beaucoup d'autres choses.
* Des exécuables minimalistes pour Windows sont disponibles ici : http://download.osgeo.org/gdal/win32/1.6/gdalwin32exe160.zip
* D'autres plugins seront ajoutés au même endroit (comme Oracle/OCI) : http://download.osgeo.org/gdal/win32/
* Des binaires avec plus de fonctionnalités pour Windows, dont python, proj et la 
  gestion C# sont disponibles comme part du paquetage `FWTools <http://fwtools.maptools.org/>`_ 
  (date d'avant la version pre-1.6 de GDAL).

OSGeo4W
********

`OSGeo4W <http://trac.osgeo.org/osgeo4w>`_ est une distribution de binaire d'un 
grand ensemble de logiciels open source geospatial pour les environnements Win32 
(Windows XP, Vista, etc). OSGeo4W inclus GDAL/OGR,  `GRASS <http://grass.itc.it/>`_, MapServer, 
`OpenEV <http://openev.sourceforge.net/>`_,  `uDig <http://udig.refractions.net/>`_, 
ainsi que d'autres paquetages (environ 70 à l'été 2008). 
