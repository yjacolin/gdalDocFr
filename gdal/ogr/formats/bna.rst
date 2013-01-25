.. _`gdal.ogr.formats.bna`:

================
BNA - Atlas BNA
================

Le format BNA est un format d'échange ASCII pour les données vecteurs 2D géré 
par plusieurs applications. Il contient seulement les géométries et quelques 
identifiants par enregistrement. Les attributs doivent être stockés dans des 
fichiers externes. Il ne gère pas les informations du système de coordonnées.

OGR gère la lecture et l'écriture au format BNA.

Le pilote OGR gère la lecture et l'écriture de tous les types de géométrie du 
format BNA :

* points
* polygones
* lignes
* ellipses/cercles

Comme le format BNA n'a pas de spécification formelle, il peut y avoir plusieurs 
formes de fichiers de données BNA. Le pilote OGR fait de son mieux pour lire les 
jeux de données BNA et gérer les formats d'enregistrements en simple ou 
multi-ligne, les enregistrements avec 2, 3 ou 4 identifiants, etc. Si vous avez 
un fichier de données BNA qui ne peut être lu correctement par le pilote BNA, 
s'il vous plait créer un rapport de bug sur le système de suivi de GDAL.

Pour être reconnue comme BNA, l'extension du fichier doit être ".bna". Lors de 
la lecture d'un fichier BNA, le pilote le scannera entièrement pour retrouver 
quelles couches sont disponibles. Si le nom du fichier est foo.bna, les couches 
seront nommées *foo_points*, *foo_polygons*, *foo_lines* et *foo_ellipses*.

Le pilote BNA gère la lecture des polygones avec des trous ou des iles. Il 
détermine ce qui est un trou ou une île seulement par analyse géométrique (tests 
d'inclusion, de non-intersection) et ignore complètement la notion de polygone 
"sinueux" (polygon winding) (si les bords d'un polygone sont décrits dans le 
sens des aiguilles d'une montre ou à l'inverse). GDAL doit être compilé avec 
GEOS pour permettre ces tests. Les polygones sont présentés comme des 
multipolygones dans le modèle Simple Feature d'OGR.

Les ellipses et cercles sont transformés en polygone avec 360 points.

Problèmes lors de la création
==============================

Lors de l'export, toutes les couches sont écrites dans un seul fichier BNA. La 
mise à jour de fichiers existants n'est pas gérée pour l'instant.

Si le fichier en sortie existe déjà, l'écriture n'aura pas lieu. Vous devez 
supprimer le fichier existant d'abord.

Le créateur BNA gère les options de création suivantes (options de jeu de 
données) :

* **LINEFORMAT :** par défaut, lors de la création de nouveaux fichiers ceux-ci 
  sont créés avec la convention de fin de ligne de la plate-forme local (CR/LF 
  sur win32 ou LF on sur tous les autres systèmes). Cela peut être écrasée par 
  l'utilisation de l'option de création de couche *LINEFORMAT* qui peut avoir 
  une valeur CRLF (format DOS) ou LF (format Unix).
* **MULTILINE :** par défaut, les fichier BNA sont créés au format multiligne 
  (pour chaque enregistrement, la première ligne contient les identifiants et 
  le type/nombre de coordonnées à suivre. Les lignes suivantes contiennent une 
  paire de coordonnées). Cela peut être écrasée à travers l'utilisation de 
  *MULTILINE=NO*.
* **NB_IDS :** les enregistrements BNA peuvent contenir de 2 à 4 identifiants 
  par enregistrement. Certaines applications gère seulement un nombre 
  d'identifiants précis. Vous pouvez écraser la valeur par défaut (2) par une 
  valeur précise : 2,3 ou 4, ou *NB_SOURCE_FIELDS*. *NB_SOURCE_FIELDS* signifie 
  que le fichier en sortie contiendra le même nombre d'identifiants que les 
  objets écrits (fixé entre 2 et 4).
* **ELLIPSES_AS_ELLIPSES :** Le *writer* BNA tentera de reconnaitre les 
  ellipses et les cercles lors de l'écriture des polygones. Cela fonctionnera 
  seulement si l'objet a été précédemment lu à partir d'un fichier BNA. Comme 
  certaine application ne gère pas les cercles/ellipses dans un fichier de 
  données BNA, il peut être utile de demander au *writer* en spécifiant 
  *ELLIPSES_AS_ELLIPSES=NO* de ne pas les exporter tel quel, mais de les 
  laisser sous forme de polygones.
* **NB_PAIRS_PER_LINE :** cette option peut être utilisée pour limiter le 
  nombre de paires de coordonnées par ligne dans le format multiligne.
* **COORDINATE_PRECISION :** cette option peut être utilisée pour définir le 
  nombre de décimal pour les coordonnés. 10 par défaut.

Gestion de l'API du système de fichier Virtuel VSI
====================================================

(Certaines fonctions ci-dessous peuvent nécessiter OGR >= 1.9.0).
 
Le pilote gère la lecture et l'écriture vers les fichiers gérés par l'API 
du Système de Fichier Virtual VSI, ce qui inclus les fichiers "normaux" 
ainsi que les fichiers dans les domaines /vsizip/ (lecture-écriture), 
/vsigzip/ (lecture-écriture), /vsicurl/ (lecture seule).

L'écriture vers /dev/stdout ou /vsistdout/ est également géré.

Exemples
=========

La commande ''ogrinfo'' peut être utilisée pour faire un dump du contenu des 
fichiers de données BNA :

::
    
    ogrinfo -ro -al a_bna_file.bna

La commande ''ogr2ogr'' peut être utilisée pour réaliser une traduction du 
format BNA vers le format BNA :

::
    
    ogr2ogr -f BNA -dsco "NB_IDS=2" -dsco "ELLIPSES_AS_ELLIPSES=NO" output.bna input.bna

.. seealso::

 * `Description du format de fichier BNA <http://www.softwright.com/faq/support/boundary_file_bna_format.html>`_
 * `Une autre description du format de fichier BNA  <http://64.145.236.125/forum/topic.asp?topic_id=1930&forum_id=1&Topic_Title=how+to+edit+*.bna+files%3F&forum_title=Surfer+Support&M=False>`_
 *  `Archive des produits lié à Census (ACRP) <http://sedac.ciesin.org/plue/cenguide.html>`_ 
    : téléchargement de jeu de données BNA de fichier de limite basé sur des 
    fichiers TIGER 1992 contenant les géographies des États-Unis

.. yjacolin at free.fr, Yves Jacolin - 2013/01/23 (trunk 23022)
