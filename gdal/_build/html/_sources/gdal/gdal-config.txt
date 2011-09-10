.. _`gdal.gdal.gdal-config`:

============
gdal-config
============

Détermine diverses informations sur l'installation de GDAL.

**Usage :**
::
    
    gdal-config [OPTIONS]
    Options :
        [--prefix[=DIR]]
        [--libs]
        [--cflags]
        [--version]
        [--ogr-enabled]
        [--formats]

Ce script (disponible seulement sur les systèmes Unix) peut être utilisé pour 
déterminer les diverses informations sur l'installation de GDAL. Il est 
normalement juste utilisé par les scripts de configuration des applications 
utilisant GDAL mais il peut être invoqué par l'utilisateur final.

* **--prefix :** le niveau le plus haut pour le répertoire d'installation de GDAL.
* **--libs :** bibliothèques et liens nécessaires pour GDAL.
* **--cflags :** définitions d'include et de macro nécessaire pour compiler des 
  modules en utilisant GDAL.
* **--version :** renvoi la version de GDAL.
* **--ogr-enabled :** renvoi "yes" ou "no" vers la sortie standard selon que OGG 
  a compilé avec GDAL ou non.
* **--formats :** renvoi quels formats sont configurés dans GDAL vers la sortie.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/15 20:03 (http://gdal.org/gdal-config.html Page originale)
