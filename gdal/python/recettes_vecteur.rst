.. _`gdal.python.vecteur.recettes`:

Recettes OGR
=============

Obtenir la liste alphabétique des pilotes disponibles
-----------------------------------------------

    Une fois GDAL/OGR correctement installés avec Python, il est toujours utile de pouvoir vérifier les pilotes disponibles avec le système et la version installés.  
   
.. code-block:: python

    # importer OGR
    try:
        from osgeo import ogr
    except:
        import ogr

    # compter le nombre de pilotes disponibles
    cnt = ogr.GetDriverCount()

    # créer une liste vide
    formatsList = []

    # lister les formats
    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()   # récupérer le nom du pilote
        if not driverName in formatsList:
            formatsList.append(driverName)
        else:
            pass

    # ranger par ordre alphabétique
    formatsList.sort() # Sorting the messy list of ogr drivers 

    # afficher la list
    for i in formatsList:
        print i



Récupérer la liste des couches dans une Esri File GeoDataBase
--------------------------------------------------
    
    Permet d'obtenir la liste alphabétique des couches d'une GDB, format propriétaire de base de données fichiers.Requiert la version 1.11.0 et ultérieures de GDAL/OGR mais aucune dépendance Esri. C'est l'avantage du nouveau pilote `OpenFileGDB développé par Ewen Rouault <http://www.gdal.org/drv_openfilegdb.html>`_ par rapport au pilote `FileGDB <http://www.gdal.org/drv_filegdb.html>`_.
    
.. code-block:: python

    # import
    import sys

    # importer OGR
    from osgeo import ogr

    # gérer les exceptions spécifiques à OGR
    ogr.UseExceptions()

    # charger le pilote
    driver = ogr.GetDriverByName("OpenFileGDB")

    # ouvrir la FileGDB
    try:
        gdb = driver.Open(gdb_path, 0)
    except Exception, e:
        print e
        sys.exit()

    # créer la liste vide
    featsClassList = []

    # parcourir les couches selon leur index
    for featsClass_idx in range(gdb.GetLayerCount()):
        featsClass = gdb.GetLayerByIndex(featsClass_idx)
        featsClassList.append(featsClass.GetName())

    # trier par ordre alphabétique
    featsClassList.sort()

    # afficher le résultat
    for featsClass in featsClassList:
        print featsClass
        
    # fermer proprement
    del gdb

.. auteurs : Jared Erickson, Julien Moura