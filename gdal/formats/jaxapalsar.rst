.. _`gdal.gdal.formats.jaxapalsar`:

================================
JAXA PALSAR Processed Products
================================

Ce pilote fournie une gestion améliorée pour les produits PALSAR traités à partir 
du processeur JAXA PALSAR. Cela contient des produits récupérés des organisations 
suivantes :

* JAXA (Japanese Aerospace eXploration Agency)
* AADN (Alaska Satellite Facility)
* ESA (European Space Agency) 

Ce pilote ne gère pas les produits créer en utilisant le processeur Vexcel 
(c'est à dire les produits distribués par ERSDAV et les organisations affiliées).

La gestion est fournie pour les fonctionnalités suivantes des produits PALSAR :

* Lecture des produits traités de niveau 1.1 et 1.5 ;
* Géoréférencement pour les produits de niveau 1.5 ;
* Méta-données basique (information des capteurs, espacement des pixels au sol, 
  etc.)
* Données multi-canal (i.e. jeux de données dual-polarisation ou complètement 
  polarimétrique)

C'est un pilote en lecture seul.

Pour ouvrir un produit PALSAR, sélectionnez le répertoire du volume (par exemple, 
*VOL-ALPSR000000000-P1.5_UA* ou *VOL-ALPSR000000000-P1.1__A*). Le pilote 
utilisera alors les informations contenu dans le fichier du répertoire du volume 
pour trouver les fichiers images (les fichiers IMG-*), ansi que les fichiers 
*Leader*. Notez que le fichier *Leader* est essentiel pour des opérations 
correctes du pilote.

.. seealso::

* `Données échantillon RESTEC <http://www.alos-restec.jp/sampledata_e.html>`_

.. softlibre at gloobe.org, Yves Jacolin - 2008/04/01 21:01 (trunk 13809)