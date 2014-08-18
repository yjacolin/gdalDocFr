.. _`gdal.gdal.formats.gxf.details`:

======
GXF-3
======

Introduction
=============

La bibliothèque GXF-3 a pour objectif d'être une implémentation correcte d'un
lecteur du format de fichiers GXF-3 facilité. Elle consiste en un code source 
libre (Open Source) pour des fonctions de lecture de fichiers raster GXF-3 et 
en un programme exemple les utilisant pour convertir des données GXF au format 
GeoTIFF.

GXF (Grid eXchange File) est un format de fichier ASCII standard pour échanger 
des données en grille entre différents logiciels. Les logiciels qui gère le 
standard GXF seront capable d'importer proprement les fichiers GXF et d'exporter 
les grilles au format GXF. GXF-3 est un format standard adopté du Comité 
Gravity/Magnetics de la Society of Exploration Geophysicists (SEG). GXF-3 est 
le format initial d'échange de données en grille pour `Geosoft <http://www.geosoft.com/>`_.

Ressources
===========

* `Documentation de l'API GXF-3 <http://home.gdal.org/projects/gxf/gxfopen.h.html>`_
* `API GXF-3 en .tar.gz <ftp://home.gdal.org/pub/outgoing/gxf3_1_0.tar.gz>`_
* `API GXF-3 en ZIP <ftp://home.gdal.org/pub/outgoing/gxf3_1_0.zip>`_
* `Spécification du format de fichier GXF-3 (pdf) <http://home.gdal.org/projects/gxf/gxfr3d9_1.pdf>`_

License
========

Cette bibliothèque est offerte sous licence `Open Source <http://www.opensource.org/>`_. 
En particulier, sous la licence X Consortium qui ne tente pas d'imposer une quelconque 
obligation copyleft ou crédit pour les utilisateurs du code.

La licence précise est :

::
	
	Copyright (c) 1999, Frank Warmerdam

	Permission is hereby granted, free of charge, to any person obtaining a copy of 
	this software and associated documentation files (the "Software"), to deal in 
	the Software without restriction, including without limitation the rights to use, 
	copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
	Software, and to permit persons to whom the Software is furnished to do so, 
	subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all 
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
	THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
	DEALINGS IN THE SOFTWARE.

Compiler les sources
====================

Les développeurs Unix doivent pouvoir décompresser le fichier .tar.gz, 
lancez ``configure`` puis ``make`` pour compiler la bibliothèque (*libgxf3.a*), 
et un programme de test (gxftest.c).

Les développeurs Windows doivent décompresser le fichier .zip, et entrer 
``nmake /f makefile.vc`` pour compiler avec VC++.

Auteur et remerciements
=========================

L'auteur initial de la bibliothèque GXF3 est `Frank Warmerdam <http://pobox.com/~warmerdam>`_, 
et peut être contacté par warmerdam at pobox.com. pour tout rapport de bug ou suggestions.

Je voudrais remercier :

* `Global Geomatics <http://www.globalgeo.com/>`_ qui a financé le développement 
  de la majeure partiedu travail de cette bibliothèque et a accepté qu'elle soit 
  Open Source.
* Ian Macleod de Geosoft qui a répondu à nombre de questions que j'avais et a 
  fournie des fichiers testes.

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01 (trunk 1990)
