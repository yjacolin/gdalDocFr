.. _`gdal.gdal.nearblack`:

nearblack
==========

Convertie des bords plus ou moins en noirs/blanc en noir.

Usage
------
::
    
    nearblack [-of format] [-white] [-color c1,c2,c3...cn]*] [-near dist] [-nb non_black_pixels]
          [-setalpha] [-setmask] [-o outfile] [-q]  [-co "NAME=VALUE"]* infile


Description
-------------

Cette commande va scanner une image et tenter de définir tous les pixels qui sont 
proches du noir (ou proche du blanc) autour du bord en noir (ou blanc) exact. 
Cela est souvent utilisé pour corriger les photos aériennes compressées avec 
perte afin que les pixels de couleur puissent être traités comme transparents 
lors du mosaïquage.

* **-o outfile :** le nom du fichier en sortie à créer. Les fichiers 
  nouvellement créés sont toujours créés avec le pilote HFA (Erdas Imagine - 
  .img) par défaut.
* **-of format :** (GDAL 1.8.0 ou supérieur) sélectionne le format en sortie. 
  Utilisez le nom de format court (GTiff pour GeoTIFF par exemple).
* **-co "NAME=VALUE" :** (GDAL 1.8.0 ou supérieur) passe une option de création 
  au pilote du format en sortie. Plusieurs options *-co* peuvent être listées. 
  Voyez la documentation spécifique au format pour les options de création 
  légales pour chaque format. Seulement valide lors de la création d'un nouveau 
  fichier.
* **-white :** recherche pour les pixels proche du blanc (255) au lieu des 
  pixels proche du noir.
* **-color c1,c2,c3...cn :** (GDAL >= 1.9.0) Recherche les pixels proche de la 
  couleur définie. Peut être définie plusieurs fois. Lorsque *-color* est définie 
  les pixels qui sont considérés comme le collier sont définie à 0.
* **-near dist :** sélectionne la distance du noir (ou du blanc) dans laquelle 
  les valeurs du pixel peuvent être encore considéré comme noir (ou blanc). 15 
  par défaut.
* **-nb non_black_pixels :** nombre de pixels différent du noir qui peut être 
  rencontré avant d'abandonner la recherche à l'intérieur. 2 par défaut.
* **-setalpha :** (GDAL 1.8.0 ou supérieur) ajoute une bande alpha si le fichier 
  en sortie est définie et si le fichier en entrée possède trois bandes, ou 
  définie la bande alpha du fichier en sortie s'il est définie et le fichier 
  en entrée possède quatre bandes, ou bien définie la bande alpha du fichier 
  en entrée s'il possède 4 bandes et aucun fichier en sortie n'est définie. 
  La bande alpha est définie à 0 dans le collier de l'image et à 255 partout 
  ailleurs.
* **-setmask :** (GDAL 1.8.0 ou supérieur)  ajoute une bande de masque au 
  fichier en sortie ou ajoute une bande de masque au fichier en entrée s'il 
  n'en a pas un déjà et aucun fichier n'est définie. La bande de masque est 
  définie à 0 dans le collier de l'image et à 255 partout ailleurs.
* **-q :** (GDAL 1.8.0 ou supérieur) supprime la barre de progression et les 
  autres informations affichées.
* **infile :** le fichier en entrée. N'importe quel format géré par GDAL, de 
  n'importe quel nombre de bandes, normalement des bandes sous 8 bytes.

L'algorithme traite l'image une ligne à la fois. Un scan intérieur est réalisé 
à partir du pixel défini à la fin à noir (blanc) jusqu'à au moins 
*"non_black_pixels"* pixels qui sont éloignés d'au moins *dist* niveaux de noir, 
de blanc ou d'une couleur choisie rencontré avant l'arrêt du scan. Les pixels 
proches du noir, du blanc ou d'une couleur choisie sont définis en noir (ou 
blanc). L'algorithme scan également du haut vers le bas puis du bas vers le haut 
pour identifier les indentations en haut ou en bas.

Le traitement est entièrement réalisé en 8 bits (Bytes).

Si le fichier en sortie est omis, le résultat calculé sera écrit dans le fichier 
en entrée - qui doit gérer la mise à jour.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (http://gdal.org/nearblack.html Trunk r25410)
