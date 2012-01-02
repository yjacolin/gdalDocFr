.. _`gdal.gdal.formats.airsar`:

AIRSAR -- AIRSAR Polarimetric Format
=====================================

La plupart des variantes du format Polarimétrique d'AIRSAR produit par le 
Processeur Intégré d'AIRSAR sont gérés en lecture par GDAL. Les produits 
d'AIRSAR incluent normalement divers fichiers associés, mais seules les données 
d'image elles-mêmes sont gérées. Normalement celles-ci sont nommées 
*mission_l.dat* (Bande L) ou *mission_c.dat* (Bande C).

Le format AIRSAR contient une image polarimétrique sous forme de matrice de 
dispersion compressée. GDAL décompresse la donnée dans une matrice de stockage 
puis convertit cette forme dans une matrice de covariance. Les 6 bandes 
retournées sont les six valeurs nécessaire pour définir la matrice 3x3 de 
covariance d'Hermitian. La convention utilisée pour représenter la matrice de 
covariance en terme d'éléments de matrice de dispersion HH, HV (=VH) et VV est 
indiqué ci-dessous. Notez que les éléments non-diagonal de la matrice sont des 
valeurs complexes, tandis que les valeurs diagonales sont des réels (bien que 
représenté par des bandes complexes).

* Band 1 : Covariance_11 (Float32) = HH*conj(HH)
* Band 2 : Covariance_12 (CFloat32) = sqrt(2)*HH*conj(HV)
* Band 3 : Covariance_13 (CFloat32) = HH*conj(VV)
* Band 4 : Covariance_22 (Float32) = 2*HV*conj(HV)
* Band 5 : Covariance_23 (CFloat32) = sqrt(2)*HV*conj(VV)
* Band 6 : Covariance_33 (Float32) = VV*conj(VV)

L'identité des bandes sont également reflété dans les méta-données et les 
descriptions des bandes.

Le format du produit AIRSAR inclut (potentiellement) plusieurs en-tête 
d'information. Ces informations sont capturé et représenté comme des méta-données 
sur le fichier dans son ensemble. Les objets des informations à partir de 
l'en-tête principal sont préfixé de « MH\_ », les objets de l'en-tête du paramètre 
sont préfixé de « PH\_ » et les informations de l'en-tête de calibration sont 
préfixé de « CH\_ ». Les noms des objets des méta-données sont dérivé 
automatiquement du nom des champs de l'en-tête lui-même.

Aucun effort n'est fait pour lire les fichiers associés avec le produit d'AIRSAR 
tel que *mission_l.mocomp*, *mission_meta.airsar* ou *mission_meta.podaac*.

**Lisez également :**

* **AIRSAR Data Format :** http://airsar.jpl.nasa.gov/documents/dataformat.htm

.. yjacolin at free.fr, Yves Jacolin - 2009/02/15 19:52 (trunk 6766)