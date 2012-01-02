.. _`gdal.ogr.formats.avcbin`:

Arc/Info Binary Coverage
=========================

Les couvertures Arc/Info Binary (par exemple Arc/Info V7 et plus récente) sont 
gérées par OGR en lecture.

Les sections *label*, *arc*, *polygone*, *centroide*, *région* et *texte* d'une 
couverture sont toutes gérées comme couches. Les attributs provenant d'INFO sont 
ajoutés aux *labels*, *arc*, *polygones* ou *région* aux endroits appropriés. 
Lorsqu'elles sont disponibles, les informations de projections sont lu et 
traduit. Les géométries polygonales sont collectées pour les couches polygones 
et région à partir des arcs les composants.

Les sections textes sont représentées comme des couches ponctuelles. La hauteur 
d'affichage est préservée dans le champ attributaire *HEIGHT* ; cependant, 
d'autre information sur l'orientation du texte est ignorée.

Les tables attributaires associées avec une couverture, mais pas nommément 
désignés, qui doit être attachée à l'une des couches géométriques n'est pas 
accessible par OGR. Notez que les tables attributaires sont stockées dans un 
répertoire *info*/ au même niveau que le répertoire de couverture. Si cela est 
inaccessible ou corrompue aucune information d'attributs ne sera ajoutée aux 
couches de couverture, mais la géométrie doit être encore accessible.

Si le répertoire contient des fichiers avec des noms comme w001001.adf alors la 
couverture est une :ref:`gdal.gdal.divers_formats.aig` qui peut être lu par GDAL, 
et n'est pas une couche vecteur gérée par OGR.

Les couches sont nommées comme suit :

- une couche label (label de polygone, ou des points libres) est nommée *LAB* 
  si présente.
- une couche centroide (centroide de polygone) est nommée *CNT* si présente.
- une couche arc (ligne) est nommée *ARC* si présente.
- une couche polygone est nommée *PAL* si présente.
- une section texte est nommé selon la sous-classe de la section.
- une sous-classe de région est nommé selon le nom de la sous-classe.

Le pilote des couvertures binaire d'Arc/Info tente d'optimiser les requêtes 
spatiales mais dû à l'absence d'index spatial cela est juste réalisé en 
minimisant les traitements pour les objets en dehors de la fenêtre spatiale.

La lecture aléatoire (par FID) des arcs, et des polygones est gérée, il peut ne 
pas être géré pour les autres types d'objets.

Voir également
--------------

* `Page de la bibliothèque AVCE00 <http://avce00.maptools.org/>`_
* `Pilote d'OGR pour AVCE00 (.E00) <http://gdal.org/ogr/ogr_avce00.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/06/30 (trunk 17338)