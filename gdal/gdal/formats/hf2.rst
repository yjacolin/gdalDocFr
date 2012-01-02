.. _`gdal.gdal.formats.hf2`:

HF2 -- HF2/HFZ heightfield raster
=================================

(Disponible à partir de GDAL >= 1.8.0)

GDAL gère la lecture et l'écriture des jeux de données raster heightfield 
HF2/HFZ/HF2.GZ .

HF2 est un format heightfield qui enregistre les différences entre les valeurs 
des cellules consécutives. Les fichiers HF2 peuvent aussi être optionnellement 
compressés par l'algorithme gzip, et donc les fichiers HF2.GZ (ou HFZ, équivalent) 
peuvent être significativement plus petit que les données non compressées. Le 
format de fichier permet à l'utilisateur d'avoir un contrôle sur la véracité 
désirée via le paramètre de précision verticale.

GDAL peut lire et écrire les informations de géoréférencement via les blocs 
d'en-tête étendue.

Options de création
---------------------

* **COMPRESS=YES/NO :** si le fichier doit être compressé avec GZip ou non. NO par défaut.
* **BLOCKSIZE=>block_size :** taille des tuiles internes. Doit être >= 8. 256 par défaut.
* **VERTICAL_PRECISION=vertical_precision :** doit être > 0. 0.01 par défaut.

Augmenter la précision verticale (*[NdT] vertical precision*, i.e. le degré de 
reproductibilité) diminue la taille du fichier, spécialement avec COMPRESS=YES, 
mais avec une perte de précision (*[NdT] accuracy*, i.e. la véracité).

Voir également
--------------

* `Spécification du format HF2/HFZ <http://www.bundysoft.com/docs/doku.php?id=l3dt:formats:specs:hf2>`_
* `Spécification des blocs d'en-tête étendue de HF2 <http://www.bundysoft.com/docs/doku.php?id=l3dt:formats:specs:hf2#extended_header>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 19930)