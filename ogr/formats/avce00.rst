.. _`gdal.ogr.formats.avce00`:

Couverture Arc/Info E00 (ASCII)
================================

Les couvertures Arc/Info E00 (par exemple Arc/Info V7 et plus récent) sont 
gérées par OGR en lecture.

Les sections label, arc, polygone, centroïde, région et texte d'une couverture 
sont toutes gérées comme couches. Les attributs d'INFO sont ajoutés aux labels, 
arcs, polygones ou régions à l'endroit approprié. Lorsque cela est disponible 
les informations de projection sont lu et traduite. Les géométries polygonales 
sont collectées pour les couches polygonales et régions à partir des arcs de 
compositions.

Les sections textes sont représentées comme des couches de points. La hauteur 
d'affichage est préservée dans le champ attributaire HEIGHT ; cependant, les 
autres informations sur l'orientation du texte sont ignorées.

Les tables info associées à une couverture mais pas spécialement nommé pour être 
reliée à une des couches géométriques existantes n'est pas actuellement 
accessible par OGR. Notez que les tables info sont stockées dans un répertoire 
'info' au même niveau que le répertoire de couverture. Si cela est inaccessible 
ou corrompue aucun attribut info ne seront ajoutés aux couches de couverture, 
mais la géométrie devrait toujours être accessible.

Les couches sont nommé comme suit :

- une couche label (labels polygonaux, ou points libres) est nommée LAB si 
  présente.
- une couche centroïde (centroïde de polygone) est nommée CNT si présente.
- une couche arc (ligne) est nommée ARC si présente.
- une couche polygone est nommée "PAL" si présente.
- une section texte est nommée en fonction de la sous-classe de la section.
- une sous-classe d'une région est nommée en fonction du nom de la sous-classe.

La lecture aléatoire (par FID) d'arcs ou de polygone est gérée, elle peut ne pas 
être gérée pour d'autres types d'objets. L'accès aléatoire aux fichiers E00 est 
généralement lente.

Voir aussi
-----------

  * `Page de la bibliothèque AVCE00 <http://avce00.maptools.org/>`_
  * `Pilote OGR pour AVCBin (Couverture binaire) <http://www.gdal.org/ogr/ogr_avcbin.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2009/02/28 21:34 (trunk 14784)