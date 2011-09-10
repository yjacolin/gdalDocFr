.. _`gdal.ogr.formats.sde`:

================
ESRI ArcSDE
================

OGR gère en option la lecture des instances de bases de données ArcSDE d'ESRI. 
ArcSDE est une solution spatiale de type middleware pour le stockage de données 
spatiales pour diverses bases de données relationnelles en arrière. Le pilote 
ArcSDE d'OGR dépend de sa compilation avec les bibliothèques cliente d'ArcSDE 
fournit par ESRI.

Les instances ArcSDE sont accédées avec un nom de source de données de la forme 
suivante. Les champs serveur, instance, nom d'utilisateur et mot de passe sont 
nécessaire. L'instance est le numéro de port du serveur SDE, qui est par défaut 
à 5151. Si le paramètre couche est définie alors le pilote SDE est capable de 
sauter la lecture des méta-données pour chaque couche ; échapper cette étape 
est un moyen d'aller plus vite.

.. note::
    Seulement GDAL 1.6+ gère la requête d'opération d'écriture et de version. 
    Les versions plus anciennes ne gère que les requêtes sur la version de la 
    base (*SDE.DEFAULT*) et aucune opération d'écriture.

::
    
    SDE:server,instance,database,username,password[,layer]

Pour définir une version sur laquelle réaliser une requête , vous **devez** 
définir une couche. La version *SDE.DEFAULT* sera utilisé lorsqu'aucune nom de 
version n'est définie.
::
    
    SDE:server,instance,database,username,password,layer,[version]

Vous pouvez également faire une requête pour créer une nouvelle version si elle 
n'existe pas déjà. Si la version enfant existe déjà, elle sera utilisé à moins 
que la variable d'environnement *SDE_VERSIONOVERWRITE* est définie à *TRUE*. 
Dans ce cas, la version sera supprimée et recrée.
::
    
    SDE:server,instance,database,username,password,layer,[parentversion],[childversion]

Le pilote ArcSDE d'OGR ne gère pas la lecture des données CAD (traité comme 
attribut BLOB), les propriétés annotation, les valeurs de mesure au sommet, ou 
les données raster. La méthode *ExecuteSQL()* n'est pas passé à la base de 
données sous-jacente. Pour l'instant il est interprété par le parseur SQL 
limité d'OGR. Les indexes spatiaux sont utilisés pour accélérer les requêtes 
spatiales.

Le pilote a été testé avec ArcSDE 9.x, et devrait fonctionner avec les versions 
plus récentes, ainsi que les version ArcSDE 8.2 ou 8.3. À la fois les géométries 
2D et 3D sont gérées. Les géométries Courbe sont approximées comme des lignes 
(en réalité encore à faire).

ArcSDE est généralement sensible à la casse, et les noms de tables entièrement 
qualifiés. Bien que vous pouvez utiliser les noms courts pour certaines 
opérations, d'autres (notamment la suppression) nécessitera un nom entièrement 
qualifié. À cause de cela, il est généralement préférable de toujours utiliser 
des noms entièrement qualifiés.

Options de création de couches
==============================

* **OVERWRITE :** peut être définie pour permettre l'écrasement d'une 
  couche existante pendant le processus de création de couche. Si définie, et 
  que la valeur n'est pas *NO*, la couche sera d'abord effacée avant d'être 
  créé avec le même nom que celle existante. Définie à *NO* explicitement, ou 
  ne pas inclure l'option pour traiter les tentatives de créer de nouvelles 
  couches qui entrent en collision avec une couche existante de même nom comme 
  une erreur. *Off* par défaut.
* **GEOMETRY_NAME :** par défaut OGR crée de nouvelles couches avec la 
  colonne géométrique (*feature*) nommé 'SHAPE'. si vous désirez utiliser un 
  nom différent, celui-ci peut être fournit par l'option de création d couche 
  *GEOMETRY_NAME*.
* **SDE_FID :** peut être définie pour écraser le nom par défaut de la colonne 
  ID des objets. *OBJECTID* par défaut.
* **SDE_KEYWORD :** le mot-clé *DBTUNE* avec lequel créer la couche. Par 
  défaut à *DEFAULTS*.
* **SDE_DESCRIPTION :** La description textuelle de la couche. Par défaut à 
  <<Created by GDAL/OGR 1.6>> (également utilisé comme la description de la 
  version lors de la création d'une nouvelle création de version enfant à 
  partir d'une version parent).
* **SDE_MULTIVERSION :** si cette option de création est définie à *FALSE*, 
  le multi-versioning sera désactivé pour la couche au moment de la création. 
  Par défaut, les tables multi-version sont créées quand des couches sont 
  créées dans une source de données SDE.
* **USE_NSTRING :** si cette option est définie à "TRUE" alors les champs 
  chaînes seront créé sous le type NSTRING. Cette option a été ajouté pour 
  GDAL/OGR 1.9.0.

Variables d'environnement
=========================

* **OGR_SDE_GETLAYERTYPE :** peut être à *TRUE* pour déterminer le type 
  de géométrie à partir de la base de données. Autrement, le pilote SDE 
  retournera toujours un type de géométrie *Unknown*.
* **OGR_SDE_SEARCHORDER :** peut être à *ATTRIBUTE_FIRST* pour informer 
  ArcSDE de filtrer sur un attribut **avant** d'utiliser un filtre spatial ou 
  *SPATIAL_FIRST* pour utiliser un filtre spatial. Par défaut, il utilise un 
  filtre spatial d'abord.
* **SDE_VERSIONOVERWRITE :** si définie à *TRUE*, la version enfant 
  définie sera supprimée avant d'être recréée. Notez que cette action ne fait 
  rien pour concilier n'importe quelle édition qui existait sur cette version 
  avant de faire cela et les rejette essentiellement.
* **GR_SDE_USE_NSTRING :** si cette option est définie à "TRUE" alors les champs 
  chaînes seront créé sous le type NSTRING. Cette option a été ajouté pour 
  GDAL/OGR 1.9.0.

Exemples
=========

Voyez le script test ``ogr_sde.py`` pour des exemples de chaîne de 
connections et des usages de ce pilote.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 19:46 (trunk 22293)