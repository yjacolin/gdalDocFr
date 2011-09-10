.. _`gdal.faq.divers`:

===========
FAQ divers
===========

Est ce que la bibliothèque GDAL est thread-safe ? 
===================================================

Non, GDAL n'est pas complètement *thread safe*.

Cependant pour GDAL 1.3.0 beaucoup de travail a été réalisé pour réaliser des 
scénarios thread safe. En particulier pour des situations où plusieurs threads 
sont lu à partir de jeux de données GDAL en même temps cela devrait fonctionner 
tant que deux threads n'accèdent pas le même objet *GDALDataset* en même temps. 
Cependant, dans ce scénario, aucun thread ne peut être écrit vers GDAL tant que 
les autres sont lu où cela entrainera un jolie chaos.

Aussi, bien que l'infrastructure cœur de GDAL est maintenant trhead-safe pour 
ce cas spécifique, seulement quelques pilotes ont été examiner pour être 
*thread safe*.

Il est convenue de travailler encore sur l'amélioration de la protection des 
thread de GDAL dans les futures versions.

Est ce que GDAL fonctionne avec différents locales internationales pour les chiffres numérique ?
=================================================================================================

Non, GDAL se sert d'une manière intensive de *sprintf()* et de *atof()* pour 
traduire les valeurs numériques. Si une locale affecte le formatage des nombres, 
altérant le rôle de la virgule et des périodes dans les chiffres, alors PROJ.4 
ne fonctionnera pas. Ce problème est commun dans certaines locales européennes.

Sur les plateformes de type-Unix, ce problème peut être évité en forçant 
l'utilisation de la locale des chiffres par défaut en définissant la variable 
d'environnement *LC_NUMERIC* à *C*, par exemple :

::
    
    $ export LC_NUMERIC=C
    $ gdalinfo abc.tif

Comment débuguer GDAL ?
========================

Différente information de débugage utile sera produit par GDAL et OGR si la 
variable d'environnement *CPL_DEBUG* est définie à la valeur *ON*. Lisez la 
documentation pour la fonction *CPLDebug()* pour plus d'information sur les 
messages de débugages interne.

Pour les versions plus vielles que GDAL 1.5, sur les systèmes Unix GDAL peut 
être compilé avec la variable d'environnement *CFG* définie pour activer la 
gestion du débugage avec l'option de compilation *-g*. Pour GDAL supérieur à 
la version 1.5, vous pouvez activer les symboles de débugages avec l'option de 
configuration *--enable-debug*.

Sous Windows éditez le fichier *make.opt* et assurez vous que /ZI apparaisse 
dans la variable OPTFLAGS.

Comment dois je supprimer les ressources découvertes à partir de GDAL sous windows ? 
=====================================================================================

La manière la plus saine pour libérer les ressources réservées et renvoyées 
(avec le propriétaire transféré à l'appel) à partir de la bibliothèque GDAL est 
d'utiliser la fonction dédiée de suppression. La suppression permet de libérer 
les ressources sur le bon module, sans traverser les limites des modules ce qui 
cause des erreurs de violation d'accès à la mémoire.

  * Exemple correct de suppression de ressource :

  ::
    
    OGRDataSource\* poDS = NULL;

    // OGRDataSource aquisition made on side of the GDAL module
    poDS = OGRSFDriverRegistrar::Open( "point.shp", FALSE );

    // ...

    // Properly resource release using deallocator function
    OGRDataSource::DestroyDataSource( poDS );

* Exemple incorrect de suppression de ressource :
  ::
    
    OGRDataSource\* poDS = NULL;

    // OGRDataSource aquisition made on side of the GDAL module
    poDS = OGRSFDriverRegistrar::Open( "point.shp", FALSE );

    // ...

    // Deallocation across modules boundaries.
    // Here, the deallocation crosses GDAL DLL library and client's module (ie. executable module)
    delete poDS;


Des explications plus détaillées du problème peuvent être trouvé dans les 
articles suivants :

* `1ère cause possible <http://vcfaq.mvps.org/lang/9.htm>`_ d'erreur 
  *segmentation fault* dans une dll
* `Utiliser et libérer des la mémoire à travers des limites de modules <http://blogs.msdn.com/oldnewthing/archive/2006/09/15/755966.aspx>`_

.. yjacolin at free.fr, Yves Jacolin - 2009/03/10 21:31