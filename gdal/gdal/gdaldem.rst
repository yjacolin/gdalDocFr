.. _`gdal.gdal.gdaldem`:

gdaldem
========

Outils pour analyser et visualiser des MNT, (à partir de GDAL 1.7.0)

Synopsis
---------

Usage :

* Pour générer une carte de reliefs ombragés à partir de n'importe quel raster 
  d'élévation géré par GDAL :
  ::
    
        gdaldem hillshade input_dem output_hillshade
                [-z ZFactor (défaut=1)] [-s scale* (défaut=1)]"
                [-az Azimuth (défaut=315)] [-alt Altitude (défaut=45)]
                [-alg ZevenbergenThorne]
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-co "NAME=VALUE"]* [-q]

* Pour générer une carte des pentes à partir de n'importe quel raster 
  d'élévation géré par GDAL :
  ::
    
        gdaldem slope input_dem output_slope_map"
                [-p use percent slope (défaut=degrees)] [-s scale* (défaut=1)]
                [-alg ZevenbergenThorne]
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-co "NAME=VALUE"]* [-q]

* Pour générer une carte d'aspect à partir de n'importe quel raster d'élévation 
  géré par GDAL. Créé en sortie un raster en float de 32 bit avec des valeurs de 
  pixels de 0 à 360 indiquant l'azymuth :
  ::
    
        gdaldem aspect input_dem output_aspect_map"
                [-trigonometric] [-zero_for_flat]
                [-alg ZevenbergenThorne]
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-co "NAME=VALUE"]* [-q]

* Pour générer une carte de relief en couleur à partir de n'importe quel raster 
  d'élévation géré par GDAL où *color_text_file* contient les lignes au format 
  "elevation_value rouge vert bleu" :
  ::
    
        gdaldem color-relief input_dem color_text_file output_color_relief_map
                [-alpha] [-exact_color_entry | -nearest_color_entry]
                [-b Band (défaut=1)] [-of format] [-co "NAME=VALUE"]* [-q]

* Pour générer une carte d'Index de Rugosité du Terrain (*Terrain Ruggedness 
  Index* (TRI)) à partir de n'importe quel raster d'élévation géré par GDAL :
  ::
    
        gdaldem TRI input_dem output_TRI_map
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-q]

* Pour générer une carte d'Index de Position Topographique (*Topographic 
  Position Index* (TPI)) à partir de n'importe quel raster d'élévation géré par 
  GDAL :
  ::
    
        gdaldem TPI input_dem output_TPI_map
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-q]

* Pour générer une carte de rugosité à partir de n'importe quel raster 
  d'élévation géré par GDAL :
  ::
    
        gdaldem roughness input_dem output_roughness_map
                [-compute_edges] [-b Band (défaut=1)] [-of format] [-q]

.. note::
    Scale est le rapport des unités verticales sur celles horizontales pour 
    *Feet:Latlong* utilisez *scale=370400*, pour *Meters:LatLong* utilisez 
    *scale=111120*

Cette commande possède 7 modes différents :

* **hillshade :** pour générer une carte de relief ombragé à partir de 
  n'importe quel raster d'élévation géré par GDAL.
* **slope :** pour générer une carte des pentes à partir de n'importe quel 
  raster d'élévation géré par GDAL. 
* **aspect :** pour générer une carte d'aspect à partir de n'importe quel 
  raster d'élévation géré par GDAL.
* **color-relief :** pour générer une carte des reliefs en couleur à partir de 
  n'importe quel raster d'élévation géré par GDAL.
* **TRI :** pour générer une carte d'Index de Rugosité du Terrain à partir de 
  n'importe quel raster d'élévation géré par GDAL. 
* **TPI :** pour générer une carte d'Index de Position Topographique à partir 
  de n'importe quel raster d'élévation géré par GDAL.
* **roughness :** pour générer une carte de rugosité à partir de n'importe quel 
  raster d'élévation géré par GDAL.

Les options générales suivantes sont disponibles :

* **input_dem :** le raster MNT en entrée à traiter.
* **output_xxx_map :** le raster en sortie produit.
* **-of format :** sélectionne le format de sortie. La valeur par défaut est 
  GeoTIFF (GTiff). Utiliser le nom court du format.
* **-compute_edges :** (GDAL >= 1.8.0) réalise le calcul au bord du raster et 
  proche des valeurs *nodata*
* **-alg ZevenbergenThorne :** (GDAL >= 1.8.0) utilise les formules de 
  Zevenbergen & Thorne au lieu de celle de Horn pour calculer les pentes et 
  les aspects. La littérature suggère que celle de Zevenbergen & Thorne est plus 
  adaptée aux paysages doux, tandis que celle de Horn a de meilleurs résultats 
  sur les terrains plus rudes.
* **-b band :** sélectionne une bande en entrée à traiter. Les bandes sont 
  numérotées à partir de 1.
* **-co "NAME=VALUE" :** passe une option de création au pilote du format de 
  sortie. Plusieurs options *-co* peuvent être listées. Voyez la documentation 
  spécifique du format pour les options de création légales pour chaque format.
* **-q :** supprime la barre de progression et les autres informations.

Pour tous les algorithme, sauf *color-relief*, une valeur *nodata* dans le jeu 
de données cible sera émise si au moins un pixel définie dans la valeur *nodata* 
est trouvé dans une fenêtre 3x3 centrée autour du pixel source. La conséquence 
de cela est qu'il y aura un bord d'un pixel autour de chaque image définie à la 
valeur *nodata*. À partir de GDAL 1.8.0, si l'option *-compute_edges* est 
définie, ''gdaldem'' calculera les valeurs au bord de l'image ou si une valeur 
*nodata* est trouvée dans la fenêtre 3x3, en interpolant les valeurs manquantes.

Modes
-------

hillshade
**********

Cette commande renvoie un raster de 8 bit avec un bel effet de relief ombragé. 
Cela est très utile pour visualiser le terrain. Vous pouvez en option définir 
l'azymuth et l'altitude la source de lumière, un facteur d'exagération vertical 
et un facteur d'échelle à tenir compte pour les différences entre les unités 
verticales et horizontales.

La valeur 0 est utilisée comme valeur *nodata* en sortie.

Les options spécifiques suivantes sont disponibles :

* **-z zFactor :** exagération verticale utilisé pour multiplier les élévations.
* **-s scale :** rapport des unités verticales et horizontale. Si l'unité 
  horizontale du MNT source est le degrés (par exemple la projection Lat/Long 
  WGS84), vous pouvez utiliser *scale=111120* si l'unité vertical sont les 
  mètres (ou *scale=370400* si elles sont en pied).
* **-az azimuth :** azymuth de la lumière, en degrés. 0 si elle arrive d'en haut 
  du raster, 90 de l'est, ... La valeur par défaut, 315, devrait rarement être 
  changée puisque c'est la valeur généralement utilisé pour générer des cartes 
  de relief.
* **-alt altitude :** altitude de la lumière, en degrés. 90 si la lumière 
  arrive au dessus du MNT. 0 si c'est une lumière rasante.

slope
******

Cette commande utilise un raster MNT et renvoie un raster en float 32 bit avec 
des valeurs de pente. Vous avez la possibilité de définir le type de pente que 
vous voulez : degrés ou pourcentage. Dans le cas où les unités horizontales 
diffèrent des unités verticales vous pouvez également fournie un facteur 
d'échelle.

La valeur -9999 est utilisé comme valeur *nodata* en sortie.

Les options spécifiques suivantes sont disponibles :

* **-p :** si définie, la pente sera exprimée en pourcent. Autrement, elle sera 
  exprimée en degrés. 
* **-s scale :** rapport des unités verticale et horizontale. Si l'unité 
  horizontal du MNT source est le degrés (par exemple une projection WGS84 
  Lat/Long), vous pouvez utiliser *scale=111120* si l'unité vertical est le 
  mètre (ou *scale=370400* si elles sont en pied).

aspect
*******

Cette commande renvoie un raster float 32 bit avec des valeurs entre 0° et 360° 
représentant l'azymuth dont les pentes font face. La définition de l'azymuth 
est : 0° signifie que la pente est face au Nord, 90° face à l'Est, 180° face au 
sud et 270° face à l'Ouest (en supposant que le haut du raster en entrée est 
orienté au Nord). La valeur -9999 de l'aspect est utilisé comme valeur *nodata* 
pour indiquer un aspect indéfinie dans les zones plates avec la pente = 0.

Les options spécifiques suivantes sont disponibles :

* **-trigonometric :** renvoie un angle trigonométrique au lieu de l'azymuth. 
  Donc 0° signifie l'Est, 90° le Nord, 180° l'Ouest et 270° le Sud.
* **-zero_for_flat :** renvoie 0 pour les zones plates avec *slope=0* au lieu 
  de -9999.

En utilisant ces deux options, l'aspect renvoyé par ''gdaldem aspect'' doit être 
identique à celui de la commande ''r.slope.aspect'' de GRASS. Autrement il est 
identique à celui de la commande *aspect.cpp* de Matthew Perry.

color-relief
*************

Cette commande renvoie un raster à 3 bande (RVB) ou à 4 bandes (RVBA) avec des 
valeurs calculées à partir de l'élévation et d'un fichier de configuration de 
couleur au format texte, contenant l'association entre les différentes valeurs 
d'élévation et la couleur désirée correspondante. Par défaut, les couleurs entre 
les valeurs d'élévation données sont mélangées en douceur et le résultat est un 
beau MNT coloré. Les options *-exact_color_entry* ou *-nearest_color_entry* 
peuvent être utilisées pour éviter cette interpolation linéaire pour les valeurs 
qui n'ont pas de correspondance avec un index de couleur du fichier de 
configuration.

Les options spécifiques suivantes sont disponibles :

* **color_text_file :** fichier de configuration des couleurs au format texte.
* **-alpha :** ajoute un canal alpha au raster en sortie.
* **-exact_color_entry :** utilise une stricte correspondance lors de la 
  recherche dans le fichier de configuration des couleurs. Si aucun couleur 
  correspondante n'est trouvée, le quadruplet RVBA "0,0,0,0"sera utilisé.
* **-nearest_color_entry :** utilise le quadruplet RVBA correspondant à l'entrée 
  le plus proche dans le fichier de configuration des couleurs.

Le mode *color-relief* est le seul mode gérant le format VRT en sortie. Dans ce 
cas, il traduira le fichier de configuration des couleurs en éléments <LUT> 
appropriés. Notez que les élévations définie en pourcentage seront traduit en 
valeur absolue, ce qui doit être pris en compte lorsque les statistiques du 
raster source diffère de celui qui a été utilisé lors de la construction du VRT.

Le fichier de configuration des couleurs au format texte contient généralement 
4 colonnes par ligne : la valeur de l'élévation et les composants correspondants 
de Rouge, Vert, Bleu (entre 0 et 255). La valeur de l'élévation peut être une 
valeur en virgule flottante, ou le mot-clé *nv* pour la valeur *nodata*. 
L'élévation peut aussi être exprimée en pourcentage : 0 % étant la valeur 
minimale trouvé dans le raster, 100 % la valeur maximale.

Une colonne supplémentaire peut être ajouté optionnellement pour le composant 
alpha. S'il n'est pas définie, l'opacité complète (255) est supposée.

Différents séparateurs de champs sont acceptés : virgule, tabulation, espaces, 
':'.

Les couleurs communes utilisées par GRASS peuvent également être spécifiées en 
utilisant leur nom, au lieu du triplet RVB. La liste des noms gérés est : 
*white*, *black*, *red*, *green*, *blue*, *yellow*, *magenta*, *cyan*, *aqua*, 
*grey/gray*, *orange*, *brown*, *purple/violet* et *indigo*.

Depuis GDAL 1.8.0, les fichiers de palette .cpt GMT sont également géré 
(COLOR_MODEL = RGB suelement).

.. note::
    La syntaxe du fichier de configuration de couleur est dérivé de celui géré par 
    la commande r.colors de GRASS. Les fichiers (.clr) de table de couleur HDR 
    d'ESRI correspondent également à cette syntaxe. Le composent alpha et la gestion 
    des tabulations et virgules comme séparateurs sont des extensions spécifiques 
    à GDAL.


Par exemple :
::
    
    3500   white
    2500   235:220:175
    50%   190 185 135
    700    240 250 150
    0      50  180  50
    nv     0   0   0   0 

TRI
*****

Cette commande renvoie un raster à une seule bande avec des valeurs calculées à 
partir de l'élévation. TRI signifie *Terrain Ruggedness Index*, qui est définie 
comme la différence moyenne entre un pixel central et ses cellules l'entourant 
(voir *Wilson et al 2007, Marine Geodesy 30:3-35*).

La valeur -9999 est utilisé comme valeur *nodata* en sortie.

Il n'y a pas d'options spécifiques.

TPI
****

Cette commande renvoie un raste à une seule bande avec des valeurs calculées à 
partir de l'élévation. TPI signifie *Topographic Position Index*, qui est 
définie comme la différence entre un pixel central et la moyenne des cellules 
l'entourant (voir *Wilson et al 2007, Marine Geodesy 30:3-35*).

La valeur -9999 est utilisé comme valeur *nodata* en sortie.

Il n'y a pas d'options spécifiques.

roughness
***********

Cette commande renvoie un raster à une seule bande calculé à partir de 
l'élévation. La rugosité est la plus grande différence inter-cellule d'un pixel 
central et ses cellules l'entourant, comme définie dans *Wilson et al (2007, 
Marine Geodesy 30:3-35)*.

La valeur -9999 est utilisé comme valeur *nodata* en sortie.

Il n'y a pas d'options spécifiques.

Auteurs
--------

Matthew Perry <perrygeo@gmail.com>, Even Rouault 
<even.rouault@mines-paris.org>, Howard Butler <hobu.inc@gmail.com>, 
Chris Yesson <chris.yesson@ioz.ac.uk>

Derived from code by Michael Shapiro, Olga Waupotitsch, Marjorie Larson, 
Jim Westervelt : U.S. Army CERL, 1993. GRASS 4.1 Reference Manual. U.S. Army 
Corps of Engineers, Construction Engineering Research Laboratories, Champaign, 
Illinois, 1-425.

Voir également
----------------

Documentation des commandes GRASS connexes :

* http://grass.osgeo.org/grass64/manuals/html64_user/r.slope.aspect.html
* http://grass.osgeo.org/grass64/manuals/html64_user/r.shaded.relief.html
* http://grass.osgeo.org/grass64/manuals/html64_user/r.colors.html 

.. yves at georezo.net, Yves Jacolin - 2010/12/29 15:36 ((http://gdal.org/gdaldem.html Trunk r21324)