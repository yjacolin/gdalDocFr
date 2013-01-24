.. _`gdal.gdal.formats.pdf`:

===============
Geospatial PDF
===============

.. versionadded:: 1.8.0

GDAL gère la lecture des documents PDF géospatial, en extrayant les informations 
géoréférencement et rasterise les données. Les documents PDF non géospatial seront 
aussi reconnu par le pilote.

.. versionadded:: 1.10 les documents PDF peuvent être créé à partir de jeux de 
   données raster GDAL, et les sources de données OGR peuvent également être 
   dessinées en option en haut de la couche raster (voir les options de création 
   OGR_* dans la section plus bas).

GDAL doit compiler avec la gestion de libpoppler (licencé en GPL), et libpoppler 
lui même doit avoir été configuré avec ``--enable-xpdf-headers`` afin que les 
en têtes xpdf C++ soient disponibles. Note : l'API C++ poppler n'est pas stable, 
la compilation du pilote peut donc échouer avec des versions trop ancienne ou 
trop récente. Les versions testées avec succès sont poppler >= 0.12.X et <= 0.22.0.

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

Les documents de plusieurs pages sont exposés comme sous jeux de données, un 
sous jeu de données par page du document.

Les encarts (pour les meilleurs pratiques de l'OGC) ou les bounding box (style 
Adobe) seront reportés comme des items de métadonnées NEATLINE, afin qu'il 
puisse être utilisé plus tard comme une ligne de découpe pour l'algorithme de 
déformation.

.. versionadded:: 1.9.0, les métadonnées XMP peuvent être extraites du fichier, 
  et seront stockées comme contenu brute XML dans le domaine de métadonnées xml:XMP.

.. versionadded:: 1.10.0 des métadonnées supplémentaires, tels que trouvés 
   dans les PDF Topo d'USGS peuvent être extrait du fichier et seront 
   stockés comme contenu brute XML dans le domaine de métadonnées 
   EMBEDDED_METADATA.

Options de configuration
========================

* **GDAL_PDF_DPI :** Pour contrôler les dimensions des raster en définissant le DPI de la 
  rasterisation avec l'option de configuration *GDAL_PDF_DPI*. Sa valeur par défaut 
  est 150. À partir de GDAL 1.10, le pilote s'efforcera de deviner la valeur du DPI 
  soit à partir d'une entréede métadonnées spécifique contenu dans un fichier PDF, 
  ou à partir des images raster contenu dans le PDF (dans les cas simples).
* **GDAL_PDF_NEATLINE :** (GDAL >= 1.10.0 ) Le nom de la neatline à sélectionner 
  (seulement disponible pour les PDF geospatial, encodé selon les Bonnes pratiques 
  OGC). "Map Layers" par défaut pour les PDF Topo de l'USGS. Si non trouvé, la 
  neatline qui couvre la surface la plus grande.

.. versionadded:: 1.10 et lorsque GDAL est compilé avec libpoppler, les options 
   suivantes sont également disponibles :

   * **GDAL_PDF_RENDERING_OPTIONS :** une combinaison parmi 
     VECTOR, BITMAP et TEXT séparés par des virgules, pour sélectionner si les 
     entités vecteur, raster ou texte doivent avoir un rendu. Si l'option n'est 
     pas définie, toutes les entités auront un rendu.
   * **GDAL_PDF_BANDS = 3 ou 4 :** si le PDF doit avoir un rendu en image RVB (3) ou RVBA (4).
     3 par défaut.
   * **GDAL_PDF_LAYERS =** liste de couches (séparée par des virgules) à activer (ou "ALL" 
     pour activer toutes les couches). Les noms des couches peuvent être obtenus en 
     interrogeant le domaine de métadonnées LAYERS. Quand cette option est définie, les 
     couches non explicitement listé seront désactivées.
   * **GDAL_PDF_LAYERS_OFF  =** liste de couches (séparée par des virgules) à désactiver. 
     Les noms des couches peuvent être obtenus en interrogeant le domaine de métadonnées 
     LAYERS. Quand cette option est définie, les couches non explicitement listé seront 
     désactivées.

Domaine de métadonnées LAYERS
===============================

.. versionadded:: 1.10 lorsque GDAL est compilé avec libpoppler, le domaine de métadonnées 
   LAYERS peut être interrogé pour récupérer les noms des couches qui peuvent être 
   activé ou pas. Cela est utile pour connaître quelles valeurs spécifier pour les options 
   de configuration *GDAL_PDF_LAYERS* ou *GDAL_PDF_LAYERS_OFF*.

Par exemple :

::
	
	  $ gdalinfo ../autotest/gdrivers/data/adobe_style_geospatial.pdf -mdd LAYERS
	  
	  Driver: PDF/Geospatial PDF
	  Files: ../autotest/gdrivers/data/adobe_style_geospatial.pdf
	  [...]
	  Metadata (LAYERS):
	    LAYER_00_NAME=New_Data_Frame
	    LAYER_01_NAME=New_Data_Frame.Graticule
	    LAYER_02_NAME=Layers
	    LAYER_03_NAME=Layers.Measured_Grid
	    LAYER_04_NAME=Layers.Graticule
	  [...]
	  
	  $ gdal_translate ../autotest/gdrivers/data/adobe_style_geospatial.pdf out.tif --config GDAL_PDF_LAYERS_OFF "New_Data_Frame"


Restrictions
=============

L'ouverture d'un document PDF (pour obtenir le géoréférencement) est rapide, mais 
au premier accès à un bloc raster, la page entière sera rasterisée, ce qui peut 
être une opération lente.

.. note::
    .. versionadded:: 1.10, Certains fichiers PDF contenant que des rasters (tels 
	   que certains des fichiers GeoPDF de l'USGS), qui sont régulièrement tuilés 
	   sont exposé comme jeu de données tuilé par le pilote PDF de GDAL et 
	   peuvent être réalisé soit avec Popple soit avec Podofo.

Seuls quelques-uns des systèmes de référence possibles disponibles dans les 
spécifications des meilleures pratiques de l'OGC ont été actuellement mappée
dans le pilote. Les systèmes de référence non reconnus seront considérés comme 
étant basé sur l'ellipsoïde WGS84.

Pour les documents qui contiennent plusieurs lignes ordonnées dans une page 
(encart), le géoréférencement sera extrait de l'encart qui aura la plus grande 
superficie (en terme de points sur l'écran).


Problèmes de création (GDAL >= 1.10)
=====================================

Les documents PDF peuvent être créé à partir de jeux de données raster GDAL, 
qui ont une bande (niveau de gris ou avec une table de couleur), 3 bandes 
(RVB) ou 4 bandes (RVBA).

Les informations de géoréférencement  seront écrit par défaut selon les 
spécification ISO32000. Il est également possible de les écrire selon les 
convention Best Practice de l'OGC (mais limité à quelques ellipsoïdes et types 
de projection).

.. note:: La gestion de l'écriture de PDF ne nécessite pas la liaison avec 
   poppler ou podofo.

Options de création
********************

* **COMPRESS=[NONE/DEFLATE/JPEG/JPEG2000] :** Définie la compression à utiliser 
  pour les données raster. DEFLATE par défaut.
* **STREAM_COMPRESS=[NONE/DEFLATE] :** Définie la compression à utiliser pour les 
  objets flux. DEFLATE est la valeur par défaut.
* **DPI=value :** Définie la DPI à utiliser. 72 par défaut.
* **PREDICTOR=[1/2] :** Seulement pour la compression *DEFLATE*. Peut être définie 
  à 2 pour utiliser un prédicteur horizontal qui peut créer des fichiers plus 
  petits (mais pas toujours). 1 par défaut.
* **JPEG_QUALITY=[1-100] :**  Définie la qualité JPEG lors de l'utilisation du 
  JPEG. Une valeur de 100 est la meillure qualité (moins de compression) et 1 
  est la pire qualité (meilleure compression). La valeur par déféaut est 75.
* **JPEG2000_DRIVER=[JP2KAK/JP2ECW/JP2OpenJPEG/JPEG2000] :** Définie le pilote 
  JPEG2000 à utiliser. Si non définie, il sera cherché dans la liste précédente.
* **TILED=YES :** Par défaut des fichiers mono-blocs sont créés.Cette option peut 
  être utilisé pour forcer la création de fichiers PDF tuilés.
* **BLOCKXSIZE=n :** Définie la largeur des tuiles, 256 par défaut.
* **BLOCKYSIZE=n :** Définie la hauteur des tuiles, 256 par défaut.
* **CLIPPING_EXTENT=xmin,ymin,xmax,ymax :** Définie l'étendu de découpe pour 
  le jeu de données source principal et pour les rasters supplémentaires 
  optionels. Les coordonées sont définie dans les unité du SRS du jeu de 
  données. Si non définie, l'étendue de découpe est définie par l'étendue 
  du jeu de données source principal.
* **LAYER_NAME=name :** Nom pour la couche où le raster est situé. Si définie, le 
  raster sera placé dans une couche qui pourra être basculé ou non dans l'arbre 
  des couches du lecteur PDF.
* **EXTRA_RASTERS=dataset_ids :** Une liste de rasters géoréférencés à insérer 
  séparés par des virgules dans la page. Ces rasters sont 
  affichés en haut du raster source principal. Ils doivent être 
  géoréférencés dans la même projection et ils doivent être 
  découpés à l'étendue du raster source principal.
* **EXTRA_RASTERS_LAYER_NAME=dataset_names :**  Une liste de noms séparés 
  par des virgules pour chaque raster définie dans EXTRA_RASTERS. Si définie, 
  chaque raster supplémentaire sera placé dans une couche, nommée avce la 
  valeur définie qui peut être chargé dans l'arbre des couches du lecteur 
  PDF. Si non définie, tous les rasters supplémentaires seront placés dans 
  la couche par défaut.
* **EXTRA_STREAM=content :** Un flux de contenu PDF à dessiner après l'image, 
  typiquement pour ajouter du texte. Il peut se référer aux polices */FTimesRoman* 
  et */FTimesBold*.
* **EXTRA_IMAGES=image_file_name,x,y,scale[,link=some_url] (potentiellement répété) :** Une liste 
  d'images (non géoréférencées) à insérer dans la page comme contenu supplémentaire. 
  Cela est utile pour insérer des logos, légendes, etc. x et y sont en unité 
  utilisateur à partir du coin bas gauche de la page et le point d'ancrage est 
  est le pixel le plus bas à gauche de l'image. Scale est un ratio de 
  grossissement (utiliser 1 si vous n'êtes pas sur de vous). Si link=some_url 
  est définie, l'image sera sélectionnable et sa sélection entrainera 
  l'ouverture du navigateur web sur une URL définie.
* **EXTRA_LAYER_NAME=name :** Nom pour la couche où le contenu supplémentaire 
  définie avec *EXTRA_CONTENT_STREAM* ou *EXTRA_IMAGES* est placé. Si définie, 
  le contenu supplémentaire sera placé dans une couche qui peut être basculé ou 
  non dans l'arbre des couches du lecteur PDF.
* **JAVASCRIPT=script :** Contenu Javascript à lancer à l'ouverture du document. 
  Voir
  `Référence d'Acrobat(R) JavaScript Scripting <http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_.
* **JAVASCRIPT_FILE=script_filename :** Nom du fichier Javascript à inclure et 
  à lancer à l'ouverture du document. Voir 
  `Référence d'Acrobat(R) JavaScript Scripting<http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_.
* **MARGIN/LEFT_MARGIN/RIGHT_MARGIN/TOP_MARGIN/BOTTOM_MARGIN=value :** marge autour 
  de l'image en unité utilisateur.
* **GEO_ENCODING=[NONE/ISO32000/OGC_BP/BOTH] :** Définie la méthode d'encodage 
  géo à utiliser. ISO32000 par défaut.
* **XMP=[NONE/xml_xmp_content] :** Par défaut, si le jeux de données source a des 
  données dans le domaine de métadonnées 'xml:XMP', ces données seront copiées vers 
  le PDF en sortie sauf si cette optin est définie à NONE. La chaîne xml XMP peut 
  également être définie directement par cette option.
* **NEATLINE=polygon_definition_in_wkt :** Définie la NEATLINE à utiliser.
* **WRITE_INFO=[YES/NO] :** Par défaut, les informations AUTHOR, CREATOR, 
  CREATION_DATE, KEYWORDS, PRODUCER, SUBJECT et TITLE  seront écrit dans le bloc 
  info du PDF à partir du jeu de données source ou, s'ils ne sont pas définie, à 
  partir de l'option de création correspondante. Si cette option est définie à 
  *NO*, aucune information ne sera écrite.
* **AUTHOR**, **CREATOR**, **CREATION_DATE**, **KEYWORDS**, **PRODUCER**, 
  **SUBJECT** et **TITLE** : métadonnées qui peut être écrit dans le bloc info du PDF.
  .. note:: Le format de la valeur pour **CREATION_DATE** doit être D:YYYYMMDDHHmmSSOHH'mm'
  (e.g. D:20121122132447+02'00' pour 22 nov 2012 13:24:47 GMT+02) (voir 
  `Référence PDF, version 1.7 <http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf>`_ 
  page 160).
* **OGR_DATASOURCE=name :** Nom de la source de données OGR à afficher en haut de la 
  couche raster.
* **OGR_DISPLAY_FIELD=name :** Nom du champ (correspondant au nom du champ à partir 
  de la définition de couche d'OGR) à utiliser pour construire l'étiquette des entités 
  qui apparaissent dans le composant UI "Model Tree" d'un visualiseur PDF bien connus. 
  Par exemple, si la couche OGR a un champ nommé "ID", cela peut être utilisé comme 
  valeur pour cette option : les entités dans l'arbre du model seront étiquettées 
  à partir de leur valeur du champ "ID". Si non spécifié, des étiquettes 
  génériques séquentielles seront utilisées ("feature1", "feature2", etc... ).
* **OGR_DISPLAY_LAYER_NAMES=names :** Liste séparée par des virgules de noms de couches 
  OGR à afficher dans l'arborescence d'entités. Cette option est utile pour fournir des 
  noms personnalisés au lieu de noms de couches OGR qui sont utilisés quand 
  cette option n'est pas définie. Lorsque définie, le nombre de noms doit être 
  le même que le nombre de couche OGR dans la source de données (et dans l'ordre 
  où ils apparaissent lorsqu'ils sont listés par ogrinfo par exemple).
* **OGR_WRITE_ATTRIBUTES=YES/NO :** S'il faut écrire les attributs des entités OGR. *YES* 
  par défaut.
* **OGR_LINK_FIELD=name :** Nom du champ (correspondant au nom du champ à 
  partir de la définition de couche OGR) à utiliser pour entrainer des clics 
  sur les entités OGR pour ouvrir un navigateur web sur l'URL définie par la 
  valeur du champ.
* **OFF_LAYERS=names :** Liste de noms de couches séparés par une virgule qui 
  doit être initialiement cachés. Par défaut, toutes les couches sont 
  visibles. Les noms des couches peuvent provenirde LAYER_NAME (nom de couche 
  raster principal), EXTRA_RASTERS_LAYER_NAME, EXTRA_LAYER_NAME et OGR_DISPLAY_LAYER_NAMES.
* **EXCLUSIVE_LAYERS=names :** Liste de noms de couches séparés par des 
  virgules, tel que seulement une de ces couches peut être visible à la fois. 
  C'est le comportement d'un bouton radio dans une interface graphique 
  utilisateur. Les noms de couches peuvent provenir de LAYER_NAME (nom de 
  couche du raster principal), EXTRA_RASTERS_LAYER_NAME, EXTRA_LAYER_NAME et 
  OGR_DISPLAY_LAYER_NAMES.


Mise à jour de fichiers existants (GDAL <= 1.10)
*************************************************

Les fichiers PDF existants (créé ou pas avec GDAL) peuvent être ouvert en mode update 
dans le but de définir our mettre à jour les éléments suivants :

* Projection associée et géoréférencement (avec *SetGeoTransform()* et *SetProjection()*)
* les points d'amers ou GCP (avec *SetGCPs()*)
* Neatline avec *SetMetadataItem("NEATLINE", polygon_definition_in_wkt)*)
* Contenu de l'objet Info (avec *SetMetadataItem(clé, valeur)*  où *clé* est une parmi 
  AUTHOR, CREATOR, CREATION_DATE, KEYWORDS, PRODUCER, SUBJECT et TITLE)
* métadonnées xml:XMP (avec *SetMetadata(md, "xml:XMP")*)


Pour le géoréférencement ou les points d'amers, la méthode d'encodage Geo utilisée par 
défaut est l'ISO32000. OGC_BP peut être sélectionné en définissant l'option de 
configuration *GDAL_PDF_GEO_ENCODING* à *OGC_BP*.

Les élements mis à jour sont écrit à la fni du fichier, suivant la méthode de mise à jour 
incrémentale décrite dans les spécifications du PDF.

Exemples
========

* Créer un PDF à partir de deux raster (main_raster et another_raster) tel que 
  main_raster est d'abord affiché et qu'ils sont exclusivement affiché :
  
  ::
	
	gdal_translate -of PDF main_raster.tif my.pdf -co LAYER_NAME=main_raster
	               -co EXTRA_RASTERS=another_raster.tif -co EXTRA_RASTERS_LAYER_NAME=another_raster
	               -co OFF_LAYERS=another_raster -co EXCLUSIVE_LAYERS=main_raster,another_raster

* Créer un PDF avec du JavaScript :
  ::
	
	gdal_translate -of PDF my.tif my.pdf -co JAVASCRIPT_FILE=script.js

  où script.js est :
  ::
	
	  button = app.alert({cMsg: 'This file was generated by GDAL. Do you want to visit its website ?', cTitle: 'Question', nIcon:2, nType:2});
	  if (button == 4) app.launchURL('http://gdal.org/');

.. seealso::

  * :ref:`gdal.ogr.formats.pdf`

  Spécifications :

  * `Bonne pratique de l'encodage GeoPDF de l'OGC version 2.2 (08-139r3) <http://portal.opengeospatial.org/files/?artifact_id=40537>`_
  * `Supplément  d'Adobe pour l'ISO 32000 <http://www.adobe.com/devnet/acrobat/pdfs/adobe_supplement_iso32000.pdf>`_
  * `Référence PDF, version 1.7 <http://www.adobe.com/devnet/acrobat/pdfs/pdf_reference_1-7.pdf>`_
  * `Référence JavaScript scripting d'Acrobat (R) <http://partners.adobe.com/public/developer/en/acrobat/sdk/AcroJS.pdf>`_

  Bibliothèques :

  * `Homepage de Poppler <http://poppler.freedesktop.org/>`_
  * `Homepage de PoDoFo <http://podofo.sourceforge.net/>`_

  Échantillons :

  * `Quelques échantillons PDF Geospatial <http://acrobatusers.com/gallery/geospatial>`_
  * `D'autres échantillon PDF Geospatial <http://www.agc.army.mil/geopdf_gallery.html>`_
  * `Tutorial pour générer des cartes PDF géospatiales à partir de données OSM <http://latuviitta.org/documents/Geospatial_PDF_maps_from_OSM_with_GDAL.pdf>`_
.. yjacolin at free.fr, Yves Jacolin - 2011/08/17 (trunk 25536)
