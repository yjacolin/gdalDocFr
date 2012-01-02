.. _`gdal.gdal.formats.rasdaman`:

Pilote GDAL Rasdaman
=====================

Rasdaman est un middleware de bases de données raster offrant un langage de 
requête de style SQL sur des tableaux multi-dimensionnels de taille illimitée, 
stockée dans une base de données relationnelle. Voir `www.rasdaman.org 
<http://www.rasdaman.org>`_ pour le code open-source, la documentation, etc. 
Actuellement rasdaman est en considération pour incubation à l'OSGeo.

Dans notre implémentation du pilote, GDAL se connecte à rasdaman en définissant 
un modèle de requête qui est instancié avec la boîte concrète de sous-ensembles 
lors de chaque accès. Cela permet de livrer des découpes 2-D à partir de données 
n-D définie (tel que les série temporelle de données satellites hyperspectraux, 
des données de simulation climatique multi-variable, des données de modélisation 
océaniques, etc.). En particulier, l'imagerie virtuelle peut être proposés qui 
est dérivée à la demande des données de réelle du terrain. Des détails techniques 
supplémentaires sont donnés ci-dessous.

La syntaxe de la chaîne de connexion suit le motif WKT du raster et se pratique 
comme cela :

::
    
    rasdaman: 
        query='select a[$x_lo:$x_hi,$y_lo:$y_hi] from MyImages as a' 
        [tileXSize=1024] [tileYSize=1024] 
        [host='localhost'] [port=7001] [database='RASBASE'] 
        [user='rasguest'] [password='rasguest'] 

La chaîne de langage des requêtes rasdaman (rasql) dans ce cas s'effectue seulement 
en sous ensemble. Sur l'accès aux images par GDAL, le paramètre $ est substitués
par la bounding box concrète calculé à partir des coordonnées des tuiles en entrée.

Toutefois, la requête fournis peut inclure tout type de traitement, tant qu'il 
renvoie quelque chose en 2-D. Par exemple, ceci détermine la moyenne des
pixels rouges et le proche infrarouge de la série chronologique la plus ancienne 
image :
::
    
        query='select ( a.red+a.nir ) /2 [$x_lo:$x_hi,$y_lo:$y_hi, 0 ] from SatStack as a'

Pour le moment il n'y a pas de gestion de lecture et d'écriture d'informations 
géoréférencement.

Voir également
---------------

* `Project Rasdaman <http://www.rasdaman.org/>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/19 (trunk 21243)