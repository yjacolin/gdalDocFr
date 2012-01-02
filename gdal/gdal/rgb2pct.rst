.. _`gdal.gdal.rgb2pct`:

rgb2pct.py
===========

Convertit une image RVB (24 bits) en une image en pseudo-couleurs (8 bits).

**Usage :**
::
    
    rgb2pct.py [-n colors | -pct palette_file] [-of format] source_file dest_file

Cette commande calculera une table pseudo-couleur optimale pour une image RVB 
donnée en utilisant un algorithme de coupe médian à partir d'un histogramme RVB 
ré-échantillonné. Puis il convertit l'image en image pseudo-couleur en utilisant 
la table de couleur. Cette conversion utilise l'erreur de diffusion 
Floyd-Steinberg pour optimiser la qualité visuelle de l'image en sortie.

* **-n colors :** sélectionne le nombre de couleurs dans la table de couleurs 
  générée. Par défaut il est défini à 256. Il doit être compris entre 2 et 256.
* **-pct palette_file :** extrait la table de couleur à partir de 
  *palette_file* au lieu de la calculer. Elle peut être utilisée pour obtenir 
  une table de couleur cohérente pour des fichiers multiples. *palette_file* doit 3
  être un fichier raster dans un format géré par GDAL avec une palette.
* **-of format :** format à générer (par défaut un GéoTIFF). Même sémantique 
  que l'option *-of* pour ''gdal_translate''. Seuls les formats de sortie 
  supportant les tables de pseudo-couleurs doivent être utilisés.
* **source_file :** le fichier RVB en entrée.
* **dest_file :** le fichier en pseudo-couleur en sortie qui sera créé.

.. note::
    **REMARQUE :** ''rbg2pct.py'' est un script Python, et fonctionnera 
    seulement si GDAL a été compilé avec le support de Python.

Exemple
--------

Si vous désirez créer la palette à la main, le format le plus simple est 
probablement le format VRT de GDAL. Dans l'exemple suivant un VRT a été créé 
dans un éditeur de texte avec une petite palette de 4 couleurs avec les couleurs 
RVB 238/238/238/255, 237/237/237/255, 236/236/236/255 et 229/229/229/255.

::
    
    % rgb2pct.py -pct palette.vrt rgb.tif pseudo-colored.tif
    % more < palette.vrt
    <VRTDataset rasterXSize="226" rasterYSize="271">
        <VRTRasterBand dataType="Byte" band="1">
        <ColorInterp>Palette</ColorInterp>
        <ColorTable>
            <Entry c1="238" c2="238" c3="238" c4="255"/>
            <Entry c1="237" c2="237" c3="237" c4="255"/>
            <Entry c1="236" c2="236" c3="236" c4="255"/>
            <Entry c1="229" c2="229" c3="229" c4="255"/>
        </ColorTable>
        </VRTRasterBand>
    </VRTDataset> 

.. _`gdal.gdal.pct2rgb`:


pct2rgb.py
===========

Convertit une image en pseudo-couleurs (8 bits) en une image RVB (24 bits)

**Usage :**
::
    
    pct2rgb.py [-of format] [-b band] [-rgba] source_file dest_file

Cette commande convertira une bande en pseudo-couleur d'un fichier en entrée en 
un fichier RVB en sortie au format désiré.

* **-of format :** format à générer (par défaut un GeoTIFF).
* **-b band :** bande à convertir en RVB, 1 par défaut.
* **-rgba :** générer un fichier RVBA (au lieu d'un fichier RVB par défaut).
* **source_file :** le fichier en entrée.
* **dest_file :** le fichier en RVB en sortie qui sera créé.

.. note::
    **REMARQUE :** ''rbg2pct.py'' est un script Python, et fonctionnera 
    seulement si GDAL a été compilé avec le support de Python.

.. warning::
    La nouvelle option '-expand rgb|rgba' de l'utilitaire ''gdal_translate'' 
    rend ce script obsolète.


.. yjacolin@free.fr, Yves Jacolin - 2009/02/15 20:10 (http://gdal.org/rgb2pct.html 
   rgb2pct Trunk 21324 et http://gdal.org/pct2rgb.htmlpct2rgb Trunk 21324)
