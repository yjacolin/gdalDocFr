.. _`gdal.gdal.formats.sde`:

===================
ESRI ArcSDE Raster
===================

ArcSDE d'ESRI fournit une couche d'abstraction pour de nombreuses bases de 
données qui permettent le stockage de données raster. ArcSDE gère l'imagerie à 
n-bandes avec plusieurs bit de profondeur, et l'implémentation en cours du 
pilote de GDAL doit gérer autant de bande que vous pouvez lui fournir. ArcSDE 
gère le stockage des données LZW, JP2K, et non compressées, et les présente 
d'une manière transparente à travers son SDK de son API en C.

Fonctionnalités du pilote GDAL du Raster d'ArcSDE
==================================================

Le pilote aujourd'hui gère les fonctionnalités suivantes :

* Gestion de la lecture seulement.
* Information de transformation spatiale pour les rasters qui l'ont définie.
* Information des références des coordonnées.
* Interprétation des couleurs (palette pour les jeux de données avec une carte 
  des couleurs, en échelle de gris autrement).
* Statistique des bandes si ArcSDE les a mis en cache, autrement GDAL les 
  calculera.
* Gestion des aperçues (pyramide) d'ArcSDE.
* Données sur 1 bit, 4 bit, 8 bit, 16 bit, et 32 bit.
* Gestion de IReadBlock qui correspond à la représentation par ArcSDE de la 
  données dans la base de données.
* SDK de ArcSDE 9.1 et 9.2. Les versions plus anciennes peuvent aussi fonctionner, 
  mais n'ont pas été testées.

Le pilote ne gère pas aujourd'hui les fonctionnalités suivantes :

* L'écriture de jeux de données GDAL dans la base de données.
* Lecture importante, rapide, et en un seul passage de la base de données.
* lecture à partir du "Catalogues Raster d'ArcSDE d'ESRI ".
* masque NODATA.

Considérations des performances
================================

Le pilote raster d'ArcSDE gère actuellement seulement les méthodes de lecture 
de block. Chaque appel à cette méthode résulte en un requête pour un block de 
données raster pour chaque bandes de données dans le raster, et les requêtes en 
un seul passage pour toutes les bandes pour un block ou une zone donnée n'est 
pas réalisé actuellement. Par conséquence cette approche résulte en une 
sur-utilisation du réseau. On espère que le pilote sera amélioré pour gérer les 
lectures en un seul passage dans un futur proche.

Le pilote raster d'ArcSDE ne devrait consommer seulement une connexion ArcSDE 
tout au long de l'existence du jeu de données. Chaque connexion à la base de 
données a une surcharge d'approximativement de 2 secondes,  avec une 
surcharge additionnelle utilisée pour calculer les informations du jeu de 
données. Ainsi, l'utilisation du pilote dans des situations où il y a plusieurs 
ouverture et fermeture  de jeux de données n'est pas censé être très performants.
Bien que le SDK en C d'ArcSDE gère les threading et les fermetures (locking), 
le pilote raster d'ArcSDE pour GDAL n'utilise pas ces fonctionnalités. Ainsi, 
ce pilote doit être considéré  threadsafe, et partager des jeux de données 
entre threads engendrera des résultats indéfinies (et souvent désastreux).

Spécification du jeu de données
================================

Les jeux de données SDE sont définies avec les informations suivantes :
::
    
    SDE:sdemachine.iastate.edu,5151,database,username,password,fully.specified.tablename,RASTER

* **SDE:** – ceci est le préfixe qui indique à GDAL d'utiliser ou non le pilote 
  SDE 
* **sdemachine.iastate.edu** – le nom du DNS ou adresse IP du serveur auquel on 
  se connecte.
* **5151** – le numéro du port (5151 ou port:5151) ou l'entrée du service 
  (typiquement esri_sde). 
* **database** – la base de données à se connecter. Cela peut aussi être vide 
  et définie comme ...
* **username** – nom utilisateur.
* **password** – mot de passe.
* **fully.specified.tablename** – il est prudent d'utiliser un nom de table 
  définie entièrement autant que possible, bien que cela ne soit absolument pas 
  obligatoire.
* **RASTER** – nom optionnel de la colonne raster.


.. yjacolin at free.fr, Yves Jacolin - 2009/03/09 21:37 (trunk 14166)