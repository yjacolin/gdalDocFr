.. _`gdal.python.vecteur.intro`:

=============
Vecteurs
=============

Lire un fichier vecteur
=======================

La lecture d'un fichier vecteur se fait en plusieurs étape :

* ouverture du fichier avec le pilote, on obtient l'objet initiale ;
* lecture de la couche de cet objet; on obtient l'objet layer ;
* lecture des objets (feature) de l'objet layer, on obtient l'objet feature.

Pour chaque objet on a un ensemble de méthodes liées à la classe à laquelle il 
appartient. Les méthodes peuvent être listées grâce à la méthode ``dir(objet)``. 
Exemple ``dir(ogr)`` mais vous pouvez aussi regarder la doc de l'API Python.

Un fichier vecteur est lu grâce à la méthode *Open()* de la classe 
*OGRSFDriverRegistrar*, exemple :
::
    
    ds_ref = ogr.Open("/url/to/file.shp", update = 0)

Nous obtenons un objet initial, quelles sont les méthodes que nous pouvons lui 
appliquer ? Facile : ``dir(ds_ref)`` ou http://wiki.gloobe.org/gdal/classosgeo_1_1ogr_1_1DataSource.html

Vous devez ensuite récupérer la ou les couche(s) grâce à *GetLayer()*, pour un 
shape, le nom de la couche est la même que le nom du fichier sans l'extension 
sinon vous devez utiliser le numéro de la couche :
::
    
    Layer_ref = ds_ref.GetLayer()

La variable *Layer_ref* contient maintenant l'objet *layer*. Si vous ne 
connaissez pas le numéro de la couche, vous pouvez utiliser la méthode 
*GetLayerByName()* pour récupérer l'objet layer.

Vous pouvez ainsi accéder aux informations de cette couche :

::
    
    Layer_ref.GetName() #Ne devrait pas être possible, GetName() n'existe pas pour l'objet OGRLayer !
    Layer_ref.GetFeatureCount()
    feature = Layer_ref.GetFeature(1) # Récupère l'objet (feature) numéro 1

Vous pouvez trouvez plus d'information dans la classe *OGRDataSource*.

Lorsque vous avez l'objet *feature*, vous pouvez gérer vos objets géométriques 
avec la classe *Feature*.
::
    
    import os, sys, string,  shutil
    from osgeo import ogr
    
    #Nom et géométrie d'un shapefile
    ds_ref = ogr.Open('D:/monShapeFile.shp', update = 0)
    Layer_ref = ds_ref.GetLayer()
    print "Layer name : " + Layer_ref.GetName()
    print "Number of features : " + str(Layer_ref.GetFeatureCount())
    
    #Sélection sur un shapefile
    query='SURFACE > 1000'
    Layer_ref.SetAttributeFilter(query)
    
    # Export de la sélection
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_dest=driver.CreateDataSource('D:/maSelection.shp')
    ds_dest.CopyLayer (Layer_ref ,  'maSelection')
    ds_dest.Destroy()
 
    ds_ref.Destroy()

Écrire un fichier vecteur
==========================
::
    
    # Create a Shapefile
    output="d:/temp/testogr.shp"
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(output):
        driver.DeleteDataSource(output)
    ds = driver.CreateDataSource(output)
    layer = ds.CreateLayer(output, geom_type=ogr.wkbPolygon)

Création de shapefile à partir de coordonnées
----------------------------------------------

Pour créer des objets géométriques à partir de coordonnées une possibilité est 
de passer par Wkt ([http://en.wikipedia.org/wiki/Well-known_text Well-known text]). 
Il s'agit d'une simple chaîne de caractère qui permet de définir le type d'objet 
et les coordonnées associées.

Exemple de Wkt :
::
    
    wkt_point = 'POINT(6 10)'
    wkt_ligne = 'LINESTRING(3 4,10 50,20 25)'
    wkt_polygone = 'POLYGON((1 1,5 1,5 5,1 5,1 1),(2 2, 3 2, 3 3, 2 3,2 2))'

Vous pouvez alors créer un objet *Geometry* en utilisant la méthode 
*CreateGeometryFromWkt*.

Exemple : création d'un shapefile de points à partir des coordonnées x y
::
    
    #Création d'un shapefile de points
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource('D:/monShapefile.shp')
    layer = ds.CreateLayer('monShapefile', geom_type=ogr.wkbPoint)
    
    #
    feature_def=layer.GetLayerDefn()
    f = ogr.Feature(feature_def)
    
    # Ajout du point
    x = 731065
    y = 2368493
    wkt = 'POINT(%f %f)' % (x, y)
    p = ogr.CreateGeometryFromWkt(wkt)
    f.SetGeometryDirectly(p)
    layer.CreateFeature(f)
    
    f.Destroy()

Projections
============

Exemple : définir une projection (Lambert 2 étendu) à un shapefile :
::
    
    # Crée le système de référence spatiale
    lambert2e = osr.SpatialReference()
    lambert2e.ImportFromEPSG(27572)
    
    #Crée le fichier .proj
    lambert2e.MorphToESRI()
    wkt_proj = lambert2e.ExportToWkt()
    prj_file = open('D:/monShapefile.prj', 'w')
    prj_file.write(wkt_proj)
    prj_file.close()

Les manipulations de systèmes de projections se font sur les objets *Geometry*. 
On peut soit utiliser la méthode *TransformTo* soit *Transform*.

* TransformTo suppose qu'un système de coordonnées a été défini pour l'objet 
  *Geometry* et qu'un objet *SpatialReference* a été défini comme système de 
  coordonnées d'arrivé.
* *Transform* suppose qu'un objet *CoordinateTransformation* ait été défini. 
  Il n'est pas indispensable d'avoir défini le système de coordonnées de l'objet 
  *Geometry* traité, il sera supposé que ce système correspond à celui de départ 
  de l'objet *CoordinateTransformation*.

Il est conseillé d'utiliser plutôt *Transform* et donc de définir au préalable un 
objet *CoordinateTransformation* pour des modifications sur un grand nombre d'objets.

Comment Reprojeter des données
-------------------------------

On créé deux objets Références Spatiales et pour chacun on importe les données 
de reprojection via un import à partir d'un code EPSG. Puis on créé un objet 
Géométrie à partir d'un WKT. On lui assigne un projection, puis on reprojète l'objet.
::
    
    to_srs = osr.SpatialReference()
    to_srs.ImportFromEPSG(4326)
    from_srs = osr.SpatialReference()
    from_srs.ImportFromEPSG(900913)
    
    wkt = 'POINT(%f %f)' % (x, y)
    
    pt = ogr.CreateGeometryFromWkt(wkt)
    pt.AssignSpatialReference(from_srs)
    pt.TransformTo(to_srs)
    geom = pt.GetX(),pt.GetY()
    return pt

Requêtes spatiales
===================

Par bbox
---------

Par objet géométrique
----------------------

Par requête SQL
----------------



.. auteurs : Yves Jacolin, Marie Silvestre