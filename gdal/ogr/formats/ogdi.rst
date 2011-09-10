.. _`gdal.ogr.formats.ogdi`:

=============
OGDI Vectors
=============

La gestion des vecteurs OGDI est optionnel dans OGR, et est normalement 
seulement configuré si OGDI est installé sur le système de compilation. S'il est 
disponible les vecteurs OGDI sont gérés pour l'accès en lecture pour les types 
de familles suivantes :

  * *Point*
  * *Line*
  * *Area*
  * *Text* (pour l'instant renvoie des points avec le texte dans l'attribut "texte")

OGDI peut (en autre formats) lire les produits VPF, tels que DCW et VMAP.

Si une URL GLTP d'OGDI est ouverte directement les possibilités OGDI 3.1 pour le 
pilote/serveur sont nécessaire pour obtenir une liste des couches. Une couche 
OGR est crée pour chaque famille OGDI disponible pour chaque couche dans le 
stockage de données. Pour les pilotes tel que VRF cela peut entrainer de 
nombreuses couches. Chacune des couches possède un nom sous OGR basé sur le nom 
sous OGDI plus un underscore et le nom de la famille. Par exemple une couche 
peut être appelée **watrcrsl@hydro(*)_line** si elle provient du pilote VRF.

À partir de GDAL/OGR 1.8.0, définir l'option de configuration 
*OGR_OGDI_LAUNDER_LAYER_NAMES* (ou la variable d'environnement) à YES entraînera 
la simplification des noms de couche. Par exemple : *watrcrsl_hydro* au lieu de 
'watrcrsl@hydro(*)_line'.

Autrement pour accéder à toutes les couches du stockage de données,  il est 
possible d'ouvrir une couche particulière en utilisant un nom de fichier 
personnalisé consistant à une URL GLTP correcte à laquelle vous ajoutez le nom 
de la couche suivit du type de la famille (séparé par une virgule). Ce mécanisme 
doit être utilisé pour accéder aux couches des pilotes Pre-OGDI 3.1 puisque 
avant OGDI 3.1 il n'y avait pas de manière correcte de découvrir les couches 
disponibles dans OGDI.

   gltp:[//<hostname>]/<driver_name>/<dataset_name>:<layer_name>:<family>

où <layer_name> est le nom de la couche OGDI, et <family> est choisit parmi : 
"line", "area", "point", ou "text".

Les informations du système de coordonnées sont gérées pour la plupart des 
systèmes de coordonnées. Un message sera produit quand une couche est ouverte et 
si le système de coordonnées ne peut être traduite.

Il n'y a pas de gestion de création ou de mise à jour dans le pilote OGDI.

Les couches Raster ne peuvent pas être lu avec ce pilote mais peut être récupéré 
avec le pilote Raster OGDI de GDAL.

Exemples
=========

Exemple d'usage d'``ogrinfo`` :
::
    
    ogrinfo gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'watrcrsl@hydro(*)_line'

Dans le nom du jeu de données *gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia* la 
partie *gltp:/vrf* n'est pas réellement dans le système de fichier, mais doit 
être ajouté. Les données VPF était à */usr4/mpp1/v0eur*/. Le répertoire 
*eurnasia* doit être au même niveau que les fichiers dht. et lat.. La référence 
*hydro* est un sous-répertoire de *eurnasia*/ où *watrcrsl.** est trouvé.

Exemple d'utilisation de conversion VMAP0 en SHAPE avec ''ogr2ogr'' :

::
    
    ogr2ogr watrcrsl.shp gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'watrcrsl@hydro(*)_line'
    ogr2ogr polbnda.shp  gltp:/vrf/usr4/mpp1/v0eur/vmaplv0/eurnasia 'polbnda@bnd(*)_area'

Une requête SQL d'OGR sur un jeu de données VMAP. Là encore, notez soigneusement 
les guillemets du nom de la couche :
::
    
    ogrinfo -ro gltp:/vrf/usr4/mpp1/v0noa/vmaplv0/noamer \
           -sql 'select * from "polbndl@bnd(*)_line" where use=26'

Voir également
===============

* `OGDI.SourceForge.Net <http://ogdi.sourceforge.net/>`_
* `Couvertures VMap0 <http://www.terragear.org/docs/vmap0/coverage.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 21654)