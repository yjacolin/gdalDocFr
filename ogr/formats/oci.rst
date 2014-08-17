.. _`gdal.ogr.formats.oci`:

Oracle Spatial
==============

Ce pilote gère la lecture et l'écriture de données dans le format 
objet-relationnel d'Oracle Spatial (8.1.7 et plus récent). Le pilote d'Oracle 
Spatial n'est pas compilé par défaut dans OGR, mais peut l'être sur les 
plateformes où les bibliothèques cliente d'Oracle sont disponible. 

Lors de l'ouverture d'une base de données, son nom doit être définie sous la 
forme <<*OCI:userid/password@database_instance:table,table*>>. La liste des 
tables est optionnelle. La partie *database_instance* peut être omise lors de 
l'accès à l'instance de base de données local par défaut.

Si la liste des tables n'est pas fournie, alors toutes les tables apparaissant 
dans la table *ALL_SDO_GEOM_METADATA* seront traité par OGR comme des couches 
avec les noms de table comme nom de couche. Les tables non-spatiales ou les 
tables spatiales non listé dans la table *ALL_SDO_GEOM_METADATA* ne sont pas 
accessible à moins de les lister dans le nom de la source de données. Même dans 
des bases de donnés où toutes les couches désirées sont dans la table 
*ALL_SDO_GEOM_METADATA*, il peut être préférable de lister seulement les tables 
à utiliser puisque cela peut réduire substantiellement le temps d'initialisation 
dans les bases de données avec beaucoup de tables.

Si la table à une colonne de type entier appelée *OGR_FID* il sera utilisé comme 
identifiant d'objet par OGR (et il n'apparait pas comme un attribut normal). 
Lors du chargement des données dans Oracle Spatial, OGR créera toujours le champ 
*OGR_FID*.

Problèmes avec SQL
-------------------

Par défaut le pilote d'Oracle envoie une requête SQL directement au moteur 
Oracle plutôt que de l'évaluer en interne lors de l'utilisation de l'appel 
*ExecuteSQL()* sur *OGRDataSource*, ou l'option de commande *-sql* à ``ogr2ogr``. 
Les expressions de requête d'attributs sont également envoyé à Oracle.

De même deux commandes spéciales sont gérées via l'interface *ExecuteSQL()*. Ce 
sont "*DELLAYER:<table_name>*" pour supprimer une couche et 
"*VALLAYER:<table_name>*" pour appliquer une vérification 
*SDO_GEOM.VALIDATE_GEOMETRY()* sur la couche. En interne, ces pseudo-commandes 
sont traduit en commandes plus complexe pour Oracle.

Il est également possible de demander au pilote de prendre en charge les 
commandes SQL avec le :ref:`gdal.ogr.sql`, en envoyant la chaine 
"*OGRSQL*" à la méthode *ExecuteSQL()* comme nom du dialecte SQL.

Avertissements
---------------

* La logique de reconnaissance de type est actuellement assez pauvre. Aucun 
  effort n'est fait pour préserver la longueur réelles pour les champs de type 
  entier et réel.
* Différents types tels que les objets et les BLOBs dans Oracle seront 
  complètement ignorés par OGR.
* Actuellement les sémantiques de transaction d'OGR ne sont pas proprement 
  liées aux sémantiques de transaction dans Oracle.
* Si un attribut appelée *OGR_FID* existe dans le schéma pour les tables lues, 
  il sera utilisé comme FID. Les lectures aléatoires (basé sur le FID) sur des 
  tables sans champ FID identifié (et indexé) peut être très lente. Pour forcer 
  l'utilisation d'un nom de champ particulier la variable de configuration 
  *OCI_FID* (c'est à dire une variable d'environnement) peut être définie par 
  le nom du champ cible.
* Les types de géométries courbes sont convertie en *linestrings* ou en *anneau 
  linéaire* en segments de 6 degrés lors de la lecture. Le pilote ne gère pas 
  l'écriture de géométries courbes.
* Il n'y a pas de gestion pour les nuages de point(SDO_PC), TIN (SDO_TIN) et les 
  types de données de texte d'annotation dans Oracle Spatial.

Problèmes de création
---------------------

Le pilote Oracle Spatial ne gère pas la création de nouveaux jeux de données 
(instances de bases de données), mais il doit permettre la création de nouvelles 
couches dans une base de données existantes.

Dès la fermeture de *OGRDataSource* les nouvelles couches créées auront un 
index spatial automatiquement créé. À ce moment la table *USER_SDO_GEOM_METADATA* 
sera également mise à jour avec les limites pour la table basé sur les objets 
qui ont été réellement écris. Une conséquence de cela est qu'une fois que une 
couche a été chargée il n'est généralement pas possible de charger des objets 
additionnel en dehors de l'étendue originel sans modifier manuellement 
l'information *DIMINFO* dans *USER_SDO_GEOM_METADATA* et reconstruire l'index spatial.

Options de création de couche
******************************

* **OVERWRITE :** peut être *YES* pour forcer une couche existante au nom 
  désiré d'être détruite avant la création de la couche demandée.
* **TRUNCATE :** peut être à "YES" pour forcer la table existante pour être 
  réutilisée, mais en vidant la table, préservant les indexes ou les dépendances.
* **LAUNDER :** peut être *YES* pour forcer les nouveaux champs créés sur 
  cette couche à avoir leurs noms de champ "nettoyer" dans une forme plus 
  compatible avec Oracle. Cela convertit les lettres en minuscule et certains 
  caractères spéciaux comme *-* et *#* en *_*. La valeur par défaut est *NO*.
* **PRECISION :** peut être *YES* pour forcer de nouveaux champs à créer sur 
  cette couche pour essayer et représenter l'information de la largeur et de la 
  précision, en utilisant les types *NUMBER(largeur,précision)* ou 
  *VARCHAR2(largeur)* si disponible. Si *NO* alors les les types *NUMBER*, 
  *INTEGER* et *VARCHAR2* seront utilisés à la place. La valeur par défaut est 
  *YES*.
* **DIM :** peut être définie à 2 ou 3 pour forcer la dimension de la couche 
  créée. S'il n'est pas définie, 3 est utilisé par défaut.
* **INDEX :** peut être définie à *OFF* pour désactiver la création d'un 
  index spatial quand une couche est chargé complètement. Par défaut un index 
  est créé si n'importe quel objet d'une couche possède des géométries valides.
* **INDEX_PARAMETERS :** peut être utilisé pour passer des paramètres de 
  création lorsque l'index spatial est créé. Par exemple définir 
  *INDEX_PARAMETERS* à *SDO_LEVEL=5* entrainera l'utilisation d'un index à 
  tuile de 5 niveaux. Par défaut aucun paramètre n'est passé entrainant la 
  création d'un index spatial R-Tree.
* **DIMINFO_X :** peut être définie aux valeurs xmin,xmax,xres pour contrôler 
  l'information de la dimension X écrite dans la table *USER_SDO_GEOM_METADATA*. 
  Par défaut les étendues sont collectées à partir des données écrites réelles.
* **DIMINFO_Y :** peut être définie aux valeurs ymin,ymax,yres pour contrôler 
  l'information de la dimension Y écrite dans la table *USER_SDO_GEOM_METADATA*. 
  Par défaut les étendues sont collectées à partir des données écrites réelles.
* **DIMINFO_Z :** peut être définie aux valeurs zmin,zmax,zres pour contrôler 
  l'information de la dimension Z écrite dans la table *USER_SDO_GEOM_METADATA*. 
  Par défaut les valeurs fixées de -100000,100000,0.002 sont utilisées pour les 
  couches avec une 3e dimension.
* **SRID :** Par défaut, ce pilote tentera de trouver une ligne existante dans 
  la table *MDSYS.CS_SRS* avec un système de coordonnées au format Well known 
  Text correspondant exactement à celui du jeu de données. Si aucun n'est trouvé, 
  une nouvelle ligne sera ajoutée à cette table. L'option de création de SRID 
  permet aux utilisateurs de forcer l'utilisation d'un SRID Oracle existant 
  même s'il ne correspond pas exactement au WKT auquel le pilote s'attend.
* **MULTI_LOAD :** Si activé les nouveaux objets seront créés en groupe de 100 
  par commande INSERT SQL, au lieu que chaque objet soit une commande INSERT 
  séparée. En ayant cela activé est le moyen le plus rapide de charger des 
  données rapidement. Le mode multi-load est activé par défaut, et peut être 
  forcé pour ne pas l'être pour les couches existantes ou pour les nouvelles 
  couches en la définissant à *NO*.
* **LOADER_FILE :** Si cette option est définie, toutes les informations des 
  objets seront écrites dans un fichier utilisable avec le chargeur SQL au lieu 
  d'être insérées directement dans la base de données. La couche en elle-même 
  est toujours créée dans la base de données immédiatement. La gestion du 
  chargeur SQL est encore expérimentale, et généralement le mode *MULTI_LOAd* 
  activé doit être utilisé à la place lors des essaies pour des performances 
  optimales des chargements.
* **GEOMETRY_NAME :** Par défaut OGR créé de nouvelles tables avec une colonne 
  géométrique nommé *ORA_GEOMETRY*. Si vous préférez utiliser un nom différent, 
  il peut être fournit avec l'option de création de couche *GEOMETRY_NAME*.

Exemple
*******

Simple traduction d'un shapefile vers Oracle. La table 'ABC' sera créée avec 
les objets provenant du fichier *abc.shp* et les attributs du fichier *abc.dbf*.
::
    
    % ogr2ogr -f OCI OCI:warmerda/password@gdal800.dreadfest.com abc.shp

Ce second exemple charge une couche des frontières politique à partir d'un VPF 
(avec le [[ogr_ogdi|pilote OGDI]]), et renomme la couche à partir de la couche 
mystérieuse d'OGDI en quelque chose de plus compréhensible. Si une table 
existante au nom désiré existe elle sera écrasée.
::
    
    % ogr2ogr  -f OCI OCI:warmerda/password \
        gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia \
        -lco OVERWRITE=yes -nln polbndl_bnd 'polbndl@bnd(*)_line'

Cet exemple montre l'utilisation d'``ogrinfo`` pour évaluer une commande de 
requête SQL dans Oracle. Des requêtes spécifique sophistiquées d'Oracle Spatial 
peuvent également être utilisé via l'option en ligne de commande *-sql* d'``ogrinfo``.
::
    
    ogrinfo -ro OCI:warmerda/password -sql "SELECT pop_1994 from canada where province_name = 'Alberta'"

Crédits
--------

Le développeur voudrait remercier la société `SRC, LLC <http://www.extendthereach.com/>`_ 
pour son apport financier au développement de pilote.

.. yjacolin at free.fr, Yves Jacolin 2011/08/03 (Trunk 22601)