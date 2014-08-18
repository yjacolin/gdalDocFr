.. _`gdal.ogr.formats.sqlite`:

SQLite/SpatiaLite RDBMS
=========================

OGR gère en option les tables spatiales et non-spatiale stocké dans les fichiers 
de base de données SQLite. SQLIte est un moteur RDBMS basé sur des fichiers 
simples et légers avec des commandes SQL assez complètes et avec des 
performances respectables.

Le pilote recherche une table *geometry_columns* énoncés tels que définis par 
le standard *Simple Features* de l'OGC, plus particulièrement comme définie 
dans la `RFC 16 de FDO <http://trac.osgeo.org/fdo/wiki/FDORfc16>`_. Si trouvé, 
elle est utilisé pour mappé les tables et les couches.

Si *geometry_columns* est trouvée, chaque table est traitée comme une couche. 
Les couches avec un champ *WKT_GEOMETRY* seront traitées comme des tables 
spatiales, et la colonne *WKT_GEOMETRY* sera lu comme une géométrie Well Known 
Text

Si *geometry_columns* est trouvée, elle sera utilisée pour rechercher le système 
de référence spatiale dans la table *spatial_ref_sys*.

Les bases de données SQLite sont essentiellement sans type, mais le pilote 
SQLite tentera de classifier les champs attributaires comme texte, entier ou 
virgule flottante basé sur le contenu de la première ligne de la table. Aucun 
type de champ attributaire n'existant dans SQLite.

Les bases de données SQLite fonctionne souvent mal sur un NFS, ou d'autres 
protocoles de systèmes de fichiers par réseau dû à une faible gestion des 
cadenas. Il est plus sure d'opérer seulement avec des fichiers SQLite sur un 
disque système du système local.

SQLite est un pilote compilé en option. Il n'est pas compilé par défaut.

Bien que le pilote SQLite gère la lecture des données spatiales à partir des 
enregistrements, il n'y a pas de gestion pour l'indexation spatiale, donc les 
requêtes spatiales tendent à être longue. Les requêtes attributaires peuvent 
être rapide, spécialement si des indexes sont construits pour les colonnes 
attributaires appropriées en utilisant la commande SQL "CREATE INDEX ON ( )".

Par défaut, les requêtes SQL sont passées directement au moteur de base de 
données SQLite. Il est également possible de demander au pilote de prendre 
en charge les commandes SQL avec le :ref:`gdal.ogr.sql`, en passant la chaine 
"OGRSQL" à la méthode *ExecuteSQL()*, comme nom du dialecte SQL.

À partir de OGR 1.8.0, l'option de configuration *OGR_SQLITE_SYNCHRONOUS* a été 
ajoutée. Quand définie à OFF, cela déclenche une commande 'PRAGMA synchronous = OFF' 
à la base de données SQLite.
Cela a l'avantage d’accélérer certaines opérations d'écriture (par exemple les 
systèmes de fichier EXT4), mais au dépend de la sécurité des données ; crash du 
système/OS. Utilisez le donc avec soin dans des environnements en production et 
lisez la 
`documentation de SQLite qui en parle <http://www.sqlite.org/pragma.html#pragma_synchronous>`_.

Utiliser la bibliothèque SpatiaLite (extension spatiale pour SQLite)
----------------------------------------------------------------------

(À partir de GDAL 1.7.0)

Le pilote SQLite peut lire et écrire des bases de données SpatiaLite sans nécessité 
le chargement de la bibliothèque SpatiaLite. Mais si vous configurez GDAL/OGR avec 
un lien explicite à la bibliothèque  SpatiaLite (version >= 2.3), vous aurez les 
avantages de toutes les extensions fournie par cette bibliothèque, comme les indexes 
spatiaux, les fonctions spatiales, etc.

Quelques exemples :
::
    
    # Duplique la base de données échantillon fournie avec SpatiaLite (ne nécessite 
    # pas un lien explicite avec SpatiaLite)
    ogr2ogr -f SQLite testspatialite.sqlite test-2.3.sqlite  -dsco SPATIALITE=YES

    # Ajouter un index spatial sur la colonne géométrique de la table Towns 
    # (nécessite un lien explicite avec SpatiaLite)
    ogrinfo testspatialite.sqlite -sql "SELECT CreateSpatialIndex('Towns', 'geometry')"

    # Faire une requête avec un filtre spatial (nécessite un lien explicite avec SpatiaLite)
    ogrinfo testspatialite.sqlite \
        -sql "SELECT Name, asText(geometry) FROM Towns WHERE MBRIntersects(geometry, BuildMBR(754000, 4692000, 770000, 4924000))"

ou

::
    
    # fonctionnera plus rapidement avec des filtres spatiaux et des liens 
    # explicites avec SpatiaLite
    ogrinfo testspatialite.sqlite Towns -spat 754000 4692000 770000 4924000

Problèmes de création
----------------------

Le pilote SQLite gère la création de fichiers de base de données SQLite ou 
l'ajout de tables à une base existante. Remarquez qu'un nouveau fichier de base 
de données ne peut pas être crée sur un fichier existant.

Options de création de la base de données
******************************************

* **METADATA=yes/no :** cela permet d'éviter la création des tables 
  *geometry_columns* et *spatial_ref_sys* dans une nouvelle base de données. 
  Par défaut les tables de méta-données sont créées lorsqu'une nouvelle base de 
  données est crée.
* **SPATIALITE=yes/no :** (à partir de GDAL 1.7.0) créé le mode SpatiaLite des 
  tables de métadonnées, qui sont un peu différente des métadonnées utilisées par 
  ce pilote OGR et des spécifications OGC. Implique **METADATA=yes**.
* **INIT_WITH_EPSG=yes/no :** (à partir de GDAL 1.8.0) insère le contenu du fichier 
  CSV EPSG dans la table *spatial_ref_sys*. no par défaut.

Options de création de couche
******************************

* **FORMAT=WKB/WKT/SPATIALITE :** contrôle le format utilisé pour la colonne géométrique. 
  Par défaut WKB (Well Known Binary) est utilisé. Cela est généralement plus 
  efficace lors du traitement et de l'espace utilisé, mais plus complexe à 
  comprendre ou utiliser dans des application simples que le WKT (Well Known Text).
  L'extension SpatiaLite utilise son propre format binaire pour stocker les 
  géométries et vous pouvez le choisir également. Il sera automatiquement 
  sélectionné lorsque la base de données SpatiaLite est ouverte ou créé avec l'option 
  **SPATIALITE=yes**. La valeur SPATIALITE est disponible à partir de GDAL 1.7.0
* **LAUNDER=yes/no :** contrôle si les noms de la couche et des champs seront 
  nettoyer pour une utilisation plus facile dans SQLite. Les noms nettoyés seront 
  converties en minuscule et certains caractères spéciaux seront changés en 
  'underscores'. 
* **SPATIAL_INDEX=yes/no :** (À partir de GDAL 1.7.0) si la base de données est 
  de type SpatiaLite, et si OGR est lié à libspatialite, cette option peut être 
  utilisé pour contrôler si un index spatiale doit être créé. Yes par défaut.

Autres informations
--------------------

* Le développement du pilote SQLite pour OGR a été financé par 
  `le groupe DM Solutions <http://www.dmsolutions.ca/>`_ et `GoMOOS <http://www.gomoos.org/>`_.
* `Page principale pour SQLite <http://www.sqlite.org>`_.
* `Extension spatiaLite de SQLite <http://www.gaia-gis.it/spatialite/>`_.
* `FDO RFC 16 <http://trac.osgeo.org/fdo/wiki/FDORfc16>`_ : Fournisseur FDO pour SQLite

.. yjacolin at free.fr, Yves Jacolin - 2011/08/04 (trunk 21002)