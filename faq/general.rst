.. _`gdal.faq.generalite`:

=============
FAQ Générale
=============

Qu'est ce qu'est GDAL ?
=======================

Le nom GDAL est habituellement utilisé pour nommer ce qui suit :

* le projet de bibliothèque de traduction pour les raster (GDAL) et les formats 
  de données vectoriels (OGR), dans ce cas GDAL = GDAL + OGR
* la bibliothèque de traduction pour les formats de données géospatiales.

Quelques notes historiques peuvent `être trouvées ici <http://qgis.org/index.php?option=com_content&task=view&id=58&Itemid=44>`_.

Que signifie GDAL ?
=====================

*GDAL - Geospatial Data Abstraction Library*, Bibliothèque d'Asbtraction de 
Données Géospatiales.

Il est parfois prononcé *goo-doll* (un peu comme goo-gle), bien que d'autres le 
prononce *gee-doll* en anglais et G-dal en français.

À quoi sert OGR ?
==================

L'arborescence de GDAL/OGR contient les sources pour une bibliothèque entré/sortie 
vectorielle inspiré par les `Simple Features <http://www.opengeospatial.org/standards>`_ 
de l'OpenGIS. En théorie il est séparé de GDAL mais réside aujourd'hui dans la 
même arborescence de la source et est en quelque sorte empêtré. Vous pouvez 
trouver plus d'information sur http://www.gdal.org/ogr/. C'est un des objectifs 
de réunir proprement OGR dans GDAL dans le futur. GDAL sera alors une 
bibliothèque raster et vecteur.

Que signifie OGR ?
===================

OGR signifiait *OpenGIS Simple Features Reference Implementation*. Cependant, 
puisqu'OGR ne suit pas complètement la spécification Simple Feature d'OpenGIS 
et n'est pas approuvé comme une implémentation de référence de la spécification 
le nom a été changeait en *OGR Simple Features Library*. Le terme d'OGR dans le 
nom est purement historique. OGR est également le préfixe utilisé partout dans 
le code source pour les noms des classes, des fichiers dans la bibliothèque, etc.

Quand le projet GDAL a t-il démarré ?
======================================

Fin 1998, Frank Warmerdam a commencé à travailler comme consultant sur la 
bibliothèque GDAL/OGR.

Est ce que GDAL/OGR est un logiciel propriétaire ?
==================================================

Non ! GDAL/OGR est un `Logiciel Libre et Open Source <http://en.wikipedia.org/wiki/FLOSS>`_.

Quelle licence utilise GDAL/OGR ?
==================================

La bibliothèque GDAL/OGR est diffusé sous les termes de la Licence 
`X11 <http://fr.wikipedia.org/wiki/Licence_X11>`_ / `MIT <http://www.opensource.org/licenses/mit-license.php>`_.

Elle a pour but de vous donner la permission de faire ce que vous voulez avec 
le code source de GDAL : télécharger, modifier, redistribuer comme vous le 
souhaitez, incluant la compilation en un logiciel commercial et propriétaire, 
aucune permission n'est nécessaire de la part de `Frank Warmerdam <http://home.gdal.org/warmerda/>`_, 
la `Fondation OSGeo <http://www.osgeo.org/>`_ ou quiconque.

Quelques portions de GDAL est sous des termes un peu différents. Par exemple 
les termes de la licence des bibliothèques `libpng <http://www.libpng.org/>`_, 
`libjpeg <http://www.ijg.org/>`_, `libtiff <http://remotesensing.org/libtiff/>`_, 
et `libgeotiff <http://remotesensing.org/geotiff/geotiff.html>`_ peuvent varier 
sensiblement mais pas de manière significative. D'autres bibliothèques qui 
peuvent être utilisé par GDAL sont sous des licences radicalement différentes.

::
    
    Copyright (c) 2000, Frank Warmerdam

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

Sur quels systèmes fonctionne GDAL-OGR ?
==========================================

Vous pouvez utiliser GDAL/OGR sur tous les 
`Unix moderne <http://fr.wikipedia.org/wiki/Type_Unix>`_ : Linux, Solaris, Mac 
OS X ; et les versions les plus récente de 
`Microsoft Windows <http://fr.wikipedia.org/wiki/Windows>`_ (NT/2000/XP/Vista/CE). 
À la fois les architectures 32-bit et 64-bit sont gérés.

Si vous avez utilisé GDAL/OGR sur un système ou architecture qui n'est pas 
listé au-dessus, n'hésitez pas à `nous le dire <http://lists.osgeo.org/mailman/listinfo/gdal-dev>`_.

Y a t-il des interfaces graphiques pour GDAL/OGR ?
==================================================

Voyez la page :ref:`gdal.logicielutilisantgdal`.

Quel compilateur puis je utiliser pour compiler GDAL/OGR ?
============================================================

GDAL/OGR est écrit en C ANSI et C++. Il peut être compilé avec tous les 
compilateurs C/C++ modernes.


J'ai une question. Où puis je trouver plus d'informations ?
==============================================================

Si vous ne trouvez pas de réponse après avoir naviguer dans cette FAQ, il y a 
plusieurs autres ressources disponibles :

* la documentation disponible sur les sites de `site de GDAL <http://gdal.org>`_ 
  et `OGR <http://gdal.org/ogr/>`_ ;
* les `pages Wiki <http://trac.osgeo.org/gdal/wiki/>`_
* les `listes de diffusions <http://trac.osgeo.org/gdal/wiki/MailingLists>`_ en 
  anglais
* le canal IRC #gdal sur irc.freenode.net ;
* le forum `geoLibre <http://georezo.net/forum/viewforum.php?id=37/>`_ sur le 
  portail GeoRezo.net en français.

Garder à l'esprit que la qualité des réponses est en relation à la qualité de 
votre question. Si vous avez besoin d'explication détaillé à ce propos, vous 
pouvez trouver cela dans 
`De la bonne manière de poser les questions <http://www.gnurou.org/writing/smartquestionsfr>`_ 
par Eric S. Raymond. 

Quand est prévue la prochaine version ?
========================================

Lisez la page de `planification <http://trac.osgeo.org/gdal/roadmap>`_.

Comment puis je ajouter un nouveau format à gérer ?
======================================================

C'est maintenant couvert par le Tutorial de Développement de Pilote pour GDAL 
(`GDAL Driver Implementation Tutorial <http://www.gdal.org/gdal_drivertut.html>`_) 
et le Tutorial de Développement de Pilote pour OGR 
(`OGR Driver Implementation Tutorial <http://www.gdal.org/ogr/ogr_drivertut.html>`_), 
tout deux en anglais.


.. yjacolin at free.fr, Yves Jacolin - 2008/08/23 11:00