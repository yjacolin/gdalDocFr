.. _`gdal.ogr.formats.pg_advanced`:

Informations avancées du pilote PostgreSQL / PostGIS
====================================================

L'information collectée dans cette page traite de sujet avancé, non trouvé dans 
la page :ref:`gdal.ogr.formats.pg`.

Options de connexion relié aux schémas et tables
--------------------------------------------------

À partir de GDAL 1.8.0, l'ouverture de la base de données doit être significativement 
plus rapide que dans les versions précédentes, l'utilisation des options *tables=* 
ou *schemas=* ne devraient pas accélérer les choses.

À partir de GDAL 1.6.0, l'ensemble des tables à scanner peut être écrasé en 
spécifiant *tables=[schema.]table[(geom_column_name)][,[schema2.]table2[(geom_column_name2)],...]* dans la chaîne de 
connexion. Si le paramètre est trouvé, le pilote saute l'énumération des tables 
comme décrite dans le paragraphe suivant.

À partir de GDAL 1.7.0, il est possible de restreindre les schémas qui seront 
scannés lors de l'établissement de la liste des tables. Cela peut être réalisé 
en spécifiant *schemas=schema_name[,schema_name2]* dans la chaîne de connections. 
Cela peut aussi être un moyen d'accélérer la connexion à la base de données 
PostgreSQL s'il y a beaucoup de schémas. Remarquez que si seulement un schéma 
est listé, il sera aussi défini comme le schéma actif (et le nom du schéma ne 
sera pas en préfixe des noms des couches). Autrement, le schéma actif sera 
encore 'public', à moins que cela soit spécifié par l'option *active_schema=*.

À partir de GDAL 1.7.0, le schéma actif ('public' par défaut) peut être écrasé 
en définissant *active_schema=schema_name* dans la chaîne de connexion. Le 
schéma actif est le schéma où les tables sont créées ou recherchées lorsque leur 
nom n'est pas défini en préfixe explicitement dans les noms des couches. Notez 
que cela ne restreint pas les tables qui seront listées (voir l'option * schemas=* 
ci-dessus). Lors de l'obtention de la liste des tables, le nom des tables dans 
le schéma actif ne sera pas préfixé par le nom du schéma. Par exemple, si vous 
avez la table 'foo' dans le schéma public, et une table 'foo' dans le schéma 
'bar_schema' et que vous définissez *'active_schema=bar_schema*, deux couches 
seront listées : 'foo' (implicitement dans 'bar_schema') et 'public.foo'.

Colonnes géométrique multiples
-------------------------------

À partir de GDAL 1.6.0, le pilote PostgreSQL gère l'accès aux tables avec 
plusieurs colonnes géométriques PostGIS. Pour de telles tables, il y aura autant 
de couches reportées que de nombre de colonnes géométriques listées pour cette 
table dans la table *geometry_columns*. Par exemple, si une table 'foo' a deux 
colonnes géométriques 'bar' et 'baz', deux couches seront reportées : 'foo(bar)' 
et 'foo(baz)'. Pour une compatibilité arrière, si une table possède une seule 
colonne géométrique, le nom de la couche est le nom de la table. Aussi si une 
table 'foo' possède plusieurs colonnes géométriques, avec une appelée 
'wkb_geometry', la couche correspondante à cette colonne géométrique sera 
simplement reportée comme 'foo'. Soyez attentif - le comportement lors de la 
création, mise à jour ou suppression de couches qui sont basées sur des tables 
avec de multiples colonnes géométriques PostGIS est connue pour avoir des effets 
secondaires (mal connu) sur les autres couches puisqu'elles sont intimement liées. 
Par conséquent, cette possibilité doit être utilisée essentiellement en lecture 
seule.

Couches
--------

À partir de GDAL 1.6.0, même quand PostGIS est activé, si l'utilisateur définit 
la variable d'environnement 
::
    
    PG_LIST_ALL_TABLES=YES

(et ne définie pas ''tables=''), toutes les tables attributaires des 
utilisateurs et les vues nommées seront traitées comme des couches. Cependant, 
les tables avec des colonnes de géométrie multiple seront seulement rapportées 
une fois dans ce mode. Ainsi, cette variable est essentiellement utile lorsque 
PostGIS est activé pour retrouver les tables sans données spatiales, ou les 
vues sans entrée dans la table *geometry_columns*.

Dans tous les cas, tous les utilisateurs peuvent réaliser des requêtes 
explicitement avec *GetLayerByName()*.

Les tables attributaires (non spatiale) peuvent être accédée, et retourneront 
les objets avec leurs attributs, mais sans géométrie. Si la table possède un 
champ *wkb_geometry*, elle sera traitée comme une table spatiale. Le type du 
champ est inspecté pour déterminer comment il doit être lu. Cela peut être un 
champ géométrique PostGIS, qui est supposé être au format WKT de l'OGC, ou de 
type BYTEA ou OID auquel cas il est utilisé comme une source de géométrie WKB 
de l'OGC.

À partir de GDAL 1.6.0, les tables héritées de tables spatiales sont gérées.

S'il y a un champ *ogc_fid*, il sera utilisé pour définir l'id de l'objet des 
géométries, et ne sera pas traité comme un champ régulier.

Le nom de la couche peut être de la forme *schema.table*. Le schéma doit 
exister, et l'utilisateur doit avoir les droits d'écriture pour la cible et le 
schéma public.

À partir de GDAL 1.7.0, i l'utilisateur définie la variable d'environnement 
*PG_SKIP_VIEWS=YES* (et ne spécifie pas *tables=*), seul les tables de 
l'utilisateur seront traité comme couche. L'action par défaut est d'inclure les 
vues. Cette variable est particulièrement utile lorsque vous devez copier les 
données dans un autre format tout en évitant la redondance des données à partir 
des vues.

Vues nommées
-------------

Quand PostGIS est activé pour la base de données accédée, les vues nommées sont 
gérées, si et seulement si une entré dans la table *geometry_columns* existe. 
Mais, notez que la fonction SQL *AddGeometryColumn()* n'accepte pas l'ajout 
d'une entrée pour une vue (seulement pour les tables attributaires). Il faut 
donc le réaliser à la main avec une requête comme :

::
    
    "INSERT INTO geometry_columns VALUES ('', 'public', 'name_of_my_view', 'name_of_geometry_column', 2, 4326, 'POINT');"

À partir de GDAL 1.6.0, il est également possible d'utiliser des vues nommées 
sans insertion dans la table *geometry_columns*. Pour cela, vous devez définir 
explicitement le nom de la vue dans l'option *table=* de la chaîne de 
connections. Voyez au-dessus. La contrainte est qu'OGR ne sera pas capable de 
rapporter un SRS valide et de retrouver le bon type de la géométrie.

Récupérer le FID d'une feature nouvellement insérée
----------------------------------------------------

À partir d'OGR 1.8.0 et des bases de données PostgreSQL >= 8.2, le FID d'une 
feature (i.e. habtiduellement la valeur de la colonne *OGC_FID* pour une feature) 
insérée dans une table avec *CreateFeature()*, en mode non copie, sera récupéré 
à partir de la base et peut être obtenu avec *GetFID()*. Un effet de bord de ce 
nouveau comportement est que vous devez faire attention si vous réutiliser le 
même objet feature dans une loupe qui réalise des intersections. Après la première 
itération, le FID sera définie à une valeur non null, à la deuxième itération donc, 
*CreateFeature()* tentera d'insérer la nouvelle feature avec le FID de l'ancienne 
feature, ce qui échouera puique vous ne pouvez pas insérer deux features avec le 
même FID. Dans ce cas vous devez explicitement reseter le FID avant l'appel de 
*CreateFeature()*, ou utiliser un objet feature tout neuf.

Court exemple en Python :
::
    
    feat = ogr.Feature(lyr.GetLayerDefn())
    for i in range(100):
        feat.SetFID(-1)  # Reset FID to null value
        lyr.CreateFeature(feat)
        print('The feature has been assigned FID %d' % feat.GetFID())

ou :
::
    
    for i in range(100):
        feat = ogr.Feature(lyr.GetLayerDefn())
        lyr.CreateFeature(feat)
        print('The feature has been assigned FID %d' % feat.GetFID())


Le comportement d'OGR < 1.8.0 peut être obtenu en définissant l'option de 
configuration *OGR_PG_RETRIEVE_FID* à FALSE.

Avertissements
---------------

* La logique de reconnaissance des types est pour l'instant assez pauvre. Les 
  types *INT** et *NUMERIC(width,0)* sont mappé en *integer*, les types *FLOAT* 
  et *NUMERIC(width,precision>0)* sont mappé en *real*, date, time, timestamp 
  et datetime sont gérés comme des types *date* et tous les autres types sont 
  simplement traités comme des *strings*.
* Un objet séquence appelé *<tablename>_ogc_fid_seq* est créé pour les nouvelles tables 
  (couche).
* La lecture séquentielle est réalisée dans une seule transaction. Toutes 
  tentatives d'écriture dans une couche lors d'une lecture séquentielle 
  entraîneront probablement un *BEGIN* alors qu'il est déjà dans une 
  transaction et renverra un message d'erreur.

Exemples avancés
******************

* Cet exemple montre l'utilisation de ``ogrinfo`` pour lister seulement les 
  couches définies par l'option *tables=* (à partir de GDAL 1.6.0).
  ::
    
    ogrinfo -ro PG:'dbname=warmerda tables=table1,table2'

* Cet exemple montre l'utilisation de ``ogrinfo`` pour requêter une table 'foo' 
  avec des colonnes à géométrie multiple ('geom1' et 'geom2') (à partir de GDAL 
  1.6.0) :
  ::
    
    ogrinfo -ro -al PG:dbname=warmerda 'foo(geom2)'


* Cet exemple montre comment lister seulement les couches dans les schémas 
  *apt200810* et *apt200812*. Les noms des couches seront préfixés par le nom 
  du schéma auquel ils appartiennent (à partir de GDAL 1.7.0) :
  ::
    
    ogrinfo -ro PG:'dbname=warmerda schemas=apt200810,apt200812'

* Cet exemple montre l'utilisation de ``ogrinfo`` pour lister seulement les 
  couches dans le schéma nommé *apt200810*. Notez que les noms des couches ne 
  seront pas préfixés par *apt200810* puisque seul un schéma est listé (à partir 
  de GDAL 1.7.0) :
  ::
    
    ogrinfo -ro PG:'dbname=warmerda schemas=apt200810'

* Cet exemple montre comment convertir un ensemble de shapefile dans le 
  répertoire *apt200810* dans un schéma *apt200810* existant de Postgres. Dans 
  cet exemple, nous pourrions utiliser l'option *the schemas=* à la place (à 
  partir de GDAL 1.7.0) :
  ::
    
    ogr2ogr -f PostgreSQL "PG:dbname=warmerda active_schema=apt200810" apt200810

* Cet exemple montre comment convertir toutes les tables dans le schéma 
  *apt200810* comme un ensemble de shapefile dans le répertoire *apt200810*. 
  Notez que les noms des couches ne seront pas préfixés par *apt200810* puisque 
  seul un schéma est listé (à partir de GDAL 1.7.0) :
  ::
    
    ogr2ogr apt200810 PG:'dbname=warmerda schemas=apt200810'

* Cet exemple montre comment écraser une table existante dans un schéma existant. 
  Notez que l'utilisation de l'option ''-nln'' pour définir le nom de la couche 
  qualifiée :
  ::
    
    ogr2ogr -overwrite -f PostgreSQL "PG:dbname=warmerda" mytable.shp mytable -nln myschema.mytable

Notez que l'utilisation de *-lco SCHEMA=mytable* à la place de *-nln* n'aurait 
pas fonctionner dans ce cas (voir bug 
`#2821 <http://trac.osgeo.org/gdal/ticket/2821>`_ pour plus de détails).

Si vous désirez écraser plusieurs tables à la fois localisées dans un schéma, 
l'option *-nln* n'est pas plus appropriée, il peut être donc plus facile 
d'utiliser la chaîne de connexions *active_schema* (à partir de GDAL 1.7.0). 
L'exemple suivant écrasera, si nécessaire, toutes les tables PostgreSQL 
correspondantes à un ensemble de shapefile dans un répertoire *apt200810* :
::
    
    ogr2ogr -overwrite -f PostgreSQL "PG:dbname=warmerda active_schema=apt200810" apt200810

Voir également
---------------

* :ref:`gdal.ogr.formats.pg`

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 21040)