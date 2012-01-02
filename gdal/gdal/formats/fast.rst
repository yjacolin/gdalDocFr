.. _`gdal.gdal.formats.fast`:

FAST -- EOSAT FAST Format
==========================

Lecture gérée à partir des formats FAST-L7A (Landsat TM data) et EOSAT Fast 
Format Rev. C (IRS-1C/1D data).  Si vous voulez lire d'autre jeu de de données 
dans ce format (SPOT), écrivez-moi (Andrey Kiselev, dron@ak4719.spb.edu). Vous 
pouvez partager des échantillons de données avec moi.

Les jeux de données au format FAST sont représentés par plusieurs fichiers : un 
ou plusieurs en-têtes administratifs et un ou plusieurs fichiers avec les 
véritables données des images dans un format brute. Les fichiers administratifs 
contiennent différentes informations sur les paramètres de scène incluant les 
noms des fichiers des images. Vous pouvez lire les fichiers avec les en-têtes 
administratifs avec n'importe quel éditeur de texte, ce sont juste des fichiers 
textes ASCII.

Ce pilote recherche les fichiers administratifs pour les fichiers en entrée. 
Les noms des fichiers des images seront extraits et les données seront importés, 
chaque fichier sera interprété comme une bande.

Les données
-----------

FAST-L7A
********

FAST-L7A consiste en plusieurs fichiers : un gros avec les données de l'image et 
trois petits fichiers avec des informations d'administration. Vous devez donner 
au pilote un des fichiers d'administration :

* **L7fppprrr_rrrYYYYMMDD_HPN.FST :** ficher d'en-tête des bandes panchromatique 
  avec 1 bande
* **L7fppprrr_rrrYYYYMMDD_HRF.FST :** fichier d'en-tête des bandes VNIR/ SWIR 
  avec 6 bandes 
* **L7fppprrr_rrrYYYYMMDD_HTM.FST :** fichier d'en-tête des bandes thermal avec 
  2 bandes

Toutes les images brutes et leur fichiers administratif correspondants seront 
importés comme des bandes GDAL.

À partir du document «  Level 1 Product Output Files Data Format Control Book » 
(http://ltpwww.gsfc.nasa.gov/IAS/pdfs/DFCB_V5_B2_R4.pdf) :
::
    
    The file naming convention for the FAST-L7A product files is 
    L7fppprrr_rrrYYYYMMDD_AAA.FST

    where
    L7 = Landsat 7 mission
    f = ETM+ format (1 or 2) (data not pertaining to a specific format defaults to 1)
    ppp = starting path of the product
    rrr_rrr = starting and ending rows of the product
    YYYYMMDD = acquisition date of the image
    AAA = file type:
    HPN = panchromatic band header file
    HRF = VNIR/ SWIR bands header file
    HTM = thermal bands header file
    B10 = band 1
    B20 = band 2
    B30 = band 3
    B40 = band 4
    B50 = band 5
    B61 = band 6L
    B62 = band 6H
    B70 = band 7
    B80 = band 8
    FST = FAST file extension

Vous devez donc donner au pilote un des fichiers parmi 
L7fppprrr_rrrYYYYMMDD_HPN.FST, L7fppprrr_rrrYYYYMMDD_HRF.FST ou 
L7fppprrr_rrrYYYYMMDD_HTM.FST. 

IRS-1C/1D
**********

Le format Fast Rev. C ne contient pas les noms des fichiers des bandes dans les 
en-têtes administratifs. Nous devons donc deviner les noms des fichiers des 
bandes, parce que les différents distributeurs nomment leurs fichiers 
différemment. Plusieurs schémas de nommage sont codé dans le pilote FAST de 
GDAL. Ceux-ci sont :
::
    
    <header>.<ext>
    <header>.1.<ext>
    <header>.2.<ext>
    ...

ou

::
    
    <header>.<ext>
    band1.<ext>
    band2.<ext>
    ...

ou

::
    
    <header>.<ext>
    band1.dat
    band2.dat
    ...

ou

::
    
    <header>.<ext>
    imagery1.<ext>
    imagery2.<ext>
    ...

ou

::
    
    <header>.<ext>
    imagery1.dat
    imagery2.dat
    ...

en majuscule ou minuscule. Le fichiers d'en-tête peut être nommé arbitrairement. 
Cela devrait couvrir la fantaisie de nommage des fichiers de la majorité des 
distributeurs. mais si vous n'avez pas de chance et votre jeu de données est 
nommé différemment vous devez les renommer manuellement avant l'importation des 
données avec GDAL.

Géoréférencement
----------------

Toutes les projections USGS doivent être gérées (pour ne pas les nommer UTM, 
LCC, PS, PC, TM, OM, SOM). Contactez-moi si vous avez des problèmes avec 
l'extraction de la projection appropriée.

Méta-données
*************

Les coefficients de calibration pour chaque bande signalée comme des objets de 
méta-données.

* ACQUISITION_DATE : date d'acquisition de la première scène au format yyyyddmm.
* SATELLITE : nom du satellite de la première scène.
* SENSOR : nom du capteur de la première scène.
* BIASn : valeur du biais pour le canal n.
* GAINn : valeur du gain pour le canal n.

**Voir aussi :**

* Implémenté dans *gdal/frmts/fast/fastdataset.cpp*.
* Description du format Landsat FAST L7A est disponible sur 
  http://ltpwww.gsfc.nasa.gov/IAS/htmls/l7_review.html (Lisez ESDIS Level 1 
  Product Generation System (LPGS) Output Files DFCB, Vol. 5, Book 2 disponible sur http://ltpwww.gsfc.nasa.gov/IAS/pdfs/DFCB_V5_B2_R4.pdf)
* Description du format EOSAT Fast Format REV. C disponible sur 
  http://www.euromap.de/docs/doc_001.html

.. yjacolin at free.fr, Yves Jacolin - 2009/02/22 19:43 (trunk 14483)