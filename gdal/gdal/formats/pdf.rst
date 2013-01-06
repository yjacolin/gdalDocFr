.. _`gdal.gdal.formats.pdf`:

===============
Geospatial PDF
===============

.. versionadded:: 1.8.0

GDAL gère la lecture des documents PDF géospatial, en extrayant les informations 
géoréférencement et rasterise les données. Les documents PDF non géospatial seront 
aussi reconnu par le pilote.

GDAL doit compiler avec la gestion de libpoppler (licencé en GPL), et libpoppler 
lui même doit avoir été configuré avec ``--enable-xpdf-headers`` afin que les 
en têtes xpdf C++ soient disponibles. Note : l'API C++ poppler n'est pas stable, 
la compilation du pilote peut donc échouer avec des versions trop ancienne ou 
trop récente. Les versions testés avec succès sont poppler >= 0.12.X and <= 0.16.0.

.. versionadded:: 1.9.0 comme une alternative, le pilote PDF peut être compilé 
  avec libpodofo (sous licence LGPL) pour éviter la dépendance avec libpoppler. 
  Cela est suffisant pour obtenir les informations de géoréférencement. Cependant, pour
  obtenir l'imagerie, l'utilitaire pdftoppm qui vient avec la distribution poppler 
  doit être disponible dans le PATH du système. Un fichier temporaire sera généré 
  dans un répertoire déterminé par les options de configuration suivantes : *CPL_TMPDIR*, 
  *TMPDIR* ou *TEMP* (dans cet ordre). Si aucun n'est définie, le répertoire courant 
  sera utilisé. Testé avec succès avec les versions 0.8.4 et 0.9.1 de libpodofo.

Le pilote gère la lecture de géoréférencement encodées dans l'un des deux moyens 
existants acutellemnt : en fonction des meilleures pratiques d'encodage de l'OGC, 
ou selon le supplément d'Adobe de la norme ISO 32000.

Les dimensions des raster peuvent être contrôlé en définissant le DPI de la 
rasterisation avec l'option de configuration *GDAL_PDF_DPI*. Sa valeur par défaut 
est 150.

Les documents de plusieurs pages sont exposés comme sous jeux de données, un 
sous jeu de données par page du document.

Les encarts (pour les meilleurs pratiques de l'OGC) ou les bounding box (style 
Adobe) seront reportés comme des items de métadonnées NEATLINE, afin qu'il 
puisse être utilisé plus tard comme une ligne de découpe pour l'algorithme de 
déformation.

.. versionadded:: 1.9.0, les métadonnées XMP peuvent être extraites du fichier, 
  et seront stockées comme contenu brute XML dans le domaine de métadonnées xml:XMP.

Restrictions
=============

L'ouverture d'un document PDF (pour obtenir le géoréférencement) est rapide, mais 
au premier accès à un bloc raster, la page entière sera rasterisée, ce qui peut 
être une opération lente.

Seuls quelques-uns des systèmes de référence possibles disponibles dans les 
spécifications des meilleures pratiques de l'OGC ont été actuellement mappée
dans le pilote. Les systèmes de référence non reconnus seront considérés comme 
étant basé sur l'ellipsoïde WGS84.

Pour les documents qui contiennent plusieurs lignes ordonnées dans une page 
(encart), le géoréférencement sera extrait de l'encart qui aura la plus grande 
superficie (en terme de points sur l'écran).

Il n'y a pour l'instant aucune gestion de sélection du rendu de couche.

.. seealso::

* `Bonne pratique de l'encodage GeoPDF de l'OGC version 2.2 <http://portal.opengeospatial.org/files/?artifact_id=33332>`_
* `Supplément  d'Adobe pour l'ISO 32000 <http://www.adobe.com/devnet/acrobat/pdfs/adobe_supplement_iso32000.pdf>`_
* `Homepage de Poppler <http://poppler.freedesktop.org/>`_
* `Quelques échantillons PDF Geospatial <http://acrobatusers.com/gallery/geospatial>`_
* `D'autres échantillon PDF Geospatial <http://www.agc.army.mil/geopdf_gallery.html>`_

.. yjacolin at free.fr, Yves Jacolin - 2011/08/17 (trunk 22678)