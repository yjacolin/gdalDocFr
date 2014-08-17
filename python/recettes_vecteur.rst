.. _`gdal.python.vecteur.recettes`:

Recettes OGR
=============

Obtenir la liste alphabétique des pilotes disponibles
-----------------------------------------------

    Une fois GDAL/OGR correctement installés avec Python, il est toujours utile de pouvoir vérifier les pilotes disponibles selons le système et la version installés.  
   
.. code-block:: python

    # importer OGR
    try:
        from osgeo import ogr
    except:
        import ogr

    # compter le nombre de pilotes disponibles
    nbr_pilotes = ogr.GetDriverCount()

    # créer une liste vide
    listeFormats = []

    # lister les formats
    for i in range(nbr_pilotes):
        pilote = ogr.GetDriver(i)
        nomPilote = pilote.GetName()   # récupérer le nom du pilote
        if not nomPilote in listeFormats:
            listeFormats.append(nomPilote)
        else:
            pass

    # ranger par ordre alphabétique
    listeFormats.sort()

    # afficher la list
    for format in listeFormats:
        print format



Récupérer la liste des couches dans une Esri File GeoDataBase
--------------------------------------------------
    
    Permet d'obtenir la liste alphabétique des couches d'une GDB, format propriétaire de base de données fichiers.Requiert la version 1.11.0 et ultérieures de GDAL/OGR mais aucune dépendance Esri. C'est l'avantage du nouveau pilote `OpenFileGDB développé par Ewen Rouault <http://www.gdal.org/drv_openfilegdb.html>`_ par rapport au pilote `FileGDB <http://www.gdal.org/drv_filegdb.html>`_.
    
.. code-block:: python

    # import depuis la librairie standard
    import sys

    # importer OGR
    from osgeo import ogr

    # gérer les exceptions spécifiques à OGR
    ogr.UseExceptions()

    # charger le pilote
    pilote = ogr.GetDriverByName("OpenFileGDB")

    # ouvrir la FileGDB
    try:
        gdb = pilote.Open(gdb_path, 0)
    except Exception, e:
        print e
        sys.exit()

    # créer la liste vide
    listClassesObjets = []

    # parcourir les couches selon leur index
    for featsClass_idx in range(gdb.GetLayerCount()):
        featsClass = gdb.GetLayerByIndex(featsClass_idx)
        listClassesObjets.append(featsClass.GetName())

    # trier par ordre alphabétique
    listClassesObjets.sort()

    # afficher le résultat
    for featsClass in listClassesObjets:
        print featsClass
        
    # fermer proprement
    del gdb

.. auteurs : Jared Erickson, Julien Moura