.. _`gdal.ogr.formats.memory`:

=======
Memory
=======

Le pilote implémente l'accès en lecture et en écriture des couches d'objet 
géométrique entièrement en mémoire. Ceci est d'abord utile pour augmenter les 
performances et est un espace de stockage grandement malléable. Toutes les 
options de mises à jour, types de géométries, et types de champ sont gérés.

Il n'y aucun moyen d'ouvrir un espace de stockage existante en mémoire. Il doit 
être crée avec *CreateDataSource()* et remplie puis utilisé en continuité. 
Lorsque l'espace de stockage est fermé, tout le contenu est libéré et détruit.

Le pilote n'implémente pas d'index attributaire ou spatial, les requêtes 
attributaires et spatiales sont encore évaluées pour toutes les géométries. 
Chercher les géométries par id des géométries devrait être rapide (juste un 
tableau à lire et les géométrie à copier).

Problèmes de création
=====================

N'importe quel nom peut être utilisé pour une source de données crée. Il n'y a 
pas d'options de création de source de données ou  de couche. Les noms des 
couches nécessitent d'être unique, mais n'a pas d'autres contraintes.

Les id des géométries envoyés à *CreateFeature()* sont préservé à moins qu'ils 
n'excèdent 10 000 000 auquel cas ils seront remis à zéro pour éviter un besoin 
d'un tableau excessivement large et des géométries clairsemées.

De nouveau champs peuvent être ajouté aux couches qui ont des déjà des 
géométries.

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 21:38 (trunk 11300)