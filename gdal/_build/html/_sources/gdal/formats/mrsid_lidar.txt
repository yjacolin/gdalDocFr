.. _`gdal.gdal.formats.mrsid_lidar`:

================================================================
Compression Lidar de MrSID/MG4 / Fichiers view de Cloud ponctuel
================================================================

Ce pilote fournie un moyen de visualiser un fichier LiDAR compressé en MrSID/MG4 
comme un MNT raster. Les spécificités de la conversion dépend de la taille de la 
cellule désirée, des critères de filtre, des méthodes d'agrégation et éventuellement 
d'autres paramètres. Pour cette raison, **le meilleur moyen de lire un fichier 
LiDAR compressé en MrSID/MG4 est en le référençant dans un fichier View (.view), 
qui paramétrise sa conversion en raster. Le pilote lira un fichier MG4 directement, 
cependant il utilise des paramètres de rasterisation par défaut qui peuvent ne pas 
produire un rendu correcte**. Le contenu d'un fichier View est décrit dans la spécification 
`documents de visualisation de MrSID/MG4 LiDAR`_.

MrSID/MG4 est une technologie de compression de cloud ponctuel à base d'ondelettes. 
Vous pouvez y penser comme un fichier LAS, seulement plus petit et avec un index 
spatial interne. Il a été développé et est distribué par LizardTech. Ce pilote 
gère la lecture de fichier LiDAR MG4 en utilisant le kit de développement de 
décodage (DSDK). **Ce DSDK est gratuitement distribué ; mais il n'est pas un 
logiciel open source. Vous devez contacter LizardTech pour l'obtenir (voyez le 
lien en bas de ce chapitre).**

Exemple de fichier View (à partir de la spécification des documents View)
==========================================================================

Fichier .view le plus simple possible
--------------------------------------

Le plus simple moyen pour afficher un fichier MG4 est de l'envelopper dans un 
fichier View (.view) comme cela. Ici, la référence relative au fichier MG4 
signifie que le fichier doit exister dans le même répertoire que le fichier .view. 
Puisque nous ne mappons pas les bandes de façon explicite, nous obtenons la 
valeur par défaut, qui est uniquement l'élévation. Par défaut, nous agrégeons 
basé sur la moyenne. Autrement dit, si deux points (ou plus) land sur une seule
cellule, nous allons exposer la moyenne des deux. Il n'y a aucun filtrage ici, 
donc nous aurons tous les points indépendamment du code de classification ou du 
numéro de retour. Puisque le type de données natif d'élévation est "Float64", 
qui est le type de données de la bande que nous allons exposer.

::
    
    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
    </PointCloudView>

Découpe des données
--------------------

Ceci est similaire à l'exemple ci-dessus, mais nous utilisons la balise 
optionnelle ClipBox pour sélectionner une étendue de 300 mètres nord-sud via le
cloud. Si nous voulions découper dans les directions Est-Ouest, nous aurions pu 
spécifier ceci explicitement au lieu d'utiliser NOFITLER pour ceux-ci. De même, 
nous pourrions aussi découper dans la direction Z.

::
    
    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
        <ClipBox>505500 505800 NOFILTER NOFILTER</ClipBox>
    </PointCloudView>


Expose as a bare earth (Max) DEM
---------------------------------

Ici, nous exposons une seule bande (élévation) mais désirons seulement les points 
qui ont été classifié comme "Ground". *ClassificationFitler* définie une valeur de 
2 - Le code ASPRS Point Class qui stipule les points "Ground". De plus, au lieu 
de la méthode d’agrégation "Moyen" par défaut, nous spécifiions "Max". Cela 
signifie que si deux points (ou plus) se situe dans une seule cellule, nous exposons 
la plus grande des deux valeurs d'élévation.

::
    
    <PointCloudView>
        <InputFile>E:\ESRIDevSummit2010\Tetons.sid</InputFile>
        <Band> <!-- Max Bare Earth-->
            <Channel>Z</Channel>
            <AggregationMethod>Max</AggregationMethod>
            <ClassificationFilter>2</ClassificationFilter>
        </Band>
    </PointCloudView>

Image d'intensité
------------------

Ici nous exposons une image d'intensité à partir du cloud ponctuel.

::
    
    <PointCloudView>
        <InputFile>Tetons.sid</InputFile>
        <Band>
            <!-- All intensities -->
            <Channel>Intensity</Channel>
        </Band>
    </PointCloudView>


Images RVB
-----------

Certaines images cloud ponctuelle inclut des données RVB. Si c'est le cas, vous 
pouvez utiliser un fichier .view comme celui-ci pour exposer ces données.

::
    
    <PointCloudView>
        <InputFile>Grass Lake Small.xyzRGB.sid</InputFile>
        <Band>
            <Channel>Red</Channel>
        </Band>
        <Band>
            <Channel>Green</Channel>
        </Band>
        <Band>
            <Channel>Blue</Channel>
        </Band>
    </PointCloudView> 


Gestion de l'écriture 
======================

Ce pilote ne gère pas l'écriture de fichiers MG4.

Limitations de l'implémentation actuelle
========================================

Seulement une balise *<InputFile>* est gérée. Elle doit référencer un fichier MG4.

La seule *<InterpolationMethod>* qui est gérée est *<None>* (défaut). Utilisez 
cela pour définir une valeur NODATA si la valeur par défaut (valeur maximale de 
ce type de données) n'est pas ce que vous souhaitez. Voyez la spécification 
"document View" pour plus de détails.

Il y a une insuffisance dans la vérification des erreurs pour les erreurs de format 
et les paramètres invalides. Plusieurs entrées invalides échoueront probablement 
silencieusement.

Voir également
===============

* Implémenté dans *gdal/frmts/mrsid_lidar/gdal_MG4Lidar.cpp*
* Spécification des `documents de visualisation de MrSID/MG4 LiDAR`_
* `Site web de LizardTech <http://www.lizardtech.com>`_

.. _`documents de visualisation de MrSID/MG4 LiDAR`: http://www.gdal.org/frmt_mrsid_lidar_view_point_cloud.html

.. yjacolin at free.fr, Yves Jacolin - 2011/08/14 (trunk 21644)