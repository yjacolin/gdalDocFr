.. _`gdal.gdal.formats.msgn`:

=======================================================================
MSGN -- Meteosat Second Generation (MSG) Format Natif d'Archive (.nat)
=======================================================================


GDAL gère la lecture seulement des fichiers natifs MSG. Ces fichiers peuvent 
avoir entre 1 et 12 bandes, toutes à une résolutions de 10 bits.

La gestion pour la 12e bande (HRV - High Resolution Visible) incluse. Cela est 
implémenté dans un sous jeu, c'est à dire, il est nécessaire de préfixer le nom 
du fichier avec la balise "HRV:".

De même, il est possible d'obtenir des valeurs de radiance de virgule flottante 
à la place des nombres numériques de 10 bit (DNs). Ce sous jeu est accédé en 
préfixant le nom du fichier avec la balise "RAD:".

Le géoréférencement est actuellement géré mais les résultats ne sont pas 
acceptable (pas assez précis) en fonction de vos besoins. L'astuce actuelle est 
d'implémenter la projection géostationnaire CGMS directement, en utilisant le 
code disponible sur EUMETSAT. 

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (trunk 11698)
