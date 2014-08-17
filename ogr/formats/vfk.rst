.. _`gdal.ogr.formats.vfk`:

VFK - format de données d'échange cadastrale Tchèque
=====================================================

Le pilote VFK peut lire les données dans le *format de données d'échange cadastrale 
Tchèque*. Le fichier VFK est reconnu comme une source de données OGR avec zéro ou 
plusieurs couches OGR.

Les points sont représenté en tant que wkbPoints, lines et boundaries en tant que 
wkbLineStrings et les surfaces en tant que wkbPolygons. Les primitives wkbMulti* 
ne sont pas utilisées. Les types de features ne peuvent pas être mixés dans une 
couche.

Nom de la source de données
----------------------------

Le nom de la source de données est un chemin complet vers le fichier VFK.

Noms des couches
-----------------

Les blocs de données VFK sont utilisés comme noms de couches.

Filtre attributaire
-------------------

Le moteur SQL interne d'OGR est utilisé pour évaluer l'expression. L'évaluation 
est faites une fois lorsque le filtre attributaire est définie.

Filtre spatial
--------------

Bounding boxes des features stockées dans la structure topologique sont utilisés 
pour évaluer si une feature correspond au filtre spatial en cours. L'évaluation 
est faites une fois que le filtre spatiale est définie.

Références
-----------

* `Problèmes d'implémentation du pilote VFK d'OGR <http://josef.fsv.cvut.cz/svn/landa/publications/2010/gis-ostrava-2010/paper/landa-ogr-vfk.pdf>`_
* `Documentation du format de données d'échange Tchèque <http://www.cuzk.cz/Dokument.aspx?PRARESKOD=998&MENUID=0&AKCE=DOC:10-VF_ISKNTEXT>`_ (en Tchèque)

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk )