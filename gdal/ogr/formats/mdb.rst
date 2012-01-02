.. _`gdal.ogr.formats.mdb`:

Access MDB databases
====================

GDAL/OGR >= 1.9.0

OGR gère en option l'accès en lecture les fichiers .mdb en utilisant la 
bibliothèque Java `Jackcess <http://jackcess.sourceforge.net/>`_.

Ce pilote a d'abord comme objectif d'être utilisé sur les plateformes Unix pour 
contourner les problèmes avec la bibliothèque MDBTools qui agit comme le pilote 
ODBC pour les bases de données MDB.

Le pilote peut détecter les bases de données MDB de Geomedia et les géodatabases 
personnels d'ESRI et les utilisera exactement comme les pilotes 
:ref:`gdal.ogr.formats.pgeo` et :ref:`gdal.ogr.formats.geomedia` le font. Pour 
les autres bases de données MDB, toutes les tables seront présentées comme couches 
OGR.

Comment compiler le pilote MDB (sur Linux)
-------------------------------------------

Vous avez besoin d'un JDK (JRE n'est pas suffisant) pour compiler le pilote.

Sur Ubuntu 10.04 avec le packaqe *openjdk-6-jdk* installé, 

::
    
    ./configure --with-java=yes --with-mdb=yes

Il est possible d'ajouter l'option *--with-jvm-lib-add-rpath* pour inclure le 
chemin dans la *libjvm.so* dans la bibliothèque GDAL.

Sur les autres version de Linux, vous pouvez devoir spécifier :

::
    
    ./configure --with-java=/path/to/jdk/root/path --with-jvm-lib=/path/to/libjvm/directory --with-mdb=yes

où */path/to/libjvm/directory* est par exemple */usr/lib/jvm/java-6-openjdk/jre/lib/amd64*.

Comment lancer le pilote MDB (sur Linux)
-----------------------------------------

Vous avez besoin de JRE et 3 JAR externe pour lancer le pilote.

1. si vous n'avez pas spécifié *--with-jvm-lib-add-rpath* au moment du *configure*, 
   définissez le chemin du répertoire qui contient *libjvm.so* dans *LD_LIBRARY_PATH* 
   ou dans /etc/ld.so.conf.
2. Télécharger *jackcess-1.2.2.jar*, *commons-lang-2.4.jar* et 
   *commons-logging-1.1.1.jar* (les autres versions peuvent fonctionner).
3. placer les 3 JARs soit dans le répertoire *lib/ext* du JRE (par exemple 
   */usr/lib/jvm/java-6-openjdk/jre/lib/ext*) ou dans un autre répertoire et 
   pointer explicitement avec la variable d'environnement *CLASSPATH*.

Ressources
-----------

* Page principale de la bibliothèque `Jackcess <http://jackcess.sourceforge.net/>`_.
* Utilitaire qui contient les `dépendances JARs <http://mdb-sqlite.googlecode.com/files/mdb-sqlite-1.0.2.tar.bz2>`_ nécessaires.

Voir également
--------------

* La page du pilote :ref:`gdal.ogr.formats.pgeo`.
* La page du pilote :ref:`gdal.ogr.formats.geomedia`


.. yjacolin at free.fr, Yves Jacolin  2011/08/02 (trunk 21564)