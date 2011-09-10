.. _`gdal.gdal.formats.wcs`:

================================
WCS -- OGC Web Coverage Service
================================

Le pilote optionnel WCS pour GDAL permet l'utilisation de couverture dans un 
serveur WCS comme un jeu de données raster. GDAL agit comme un client au serveur 
WCS.

Accéder à nu serveur WCS est réalisé en créant un fichier xml de description de 
service local ressemblant à quelque chose comme ce qui suit, avec l'url du 
serveur de couverture, et le nom de la couverture à accéder. Il est important 
qu'il n'y est pas d'espace ou d'autre contenu avec l'élément <WCS_GDAL>.
::
    
    <WCS_GDAL>
        <ServiceURL>http://laits.gmu.edu/cgi-bin/NWGISS/NWGISS?</ServiceURL>
        <CoverageName>AUTUMN.hdf</CoverageName>
    </WCS_GDAL>

Lors de la première ouverture, GDAL cherchera la description de la couverture, 
et une petite image de test pour établir les détails du raster. Cette 
information sera mis en cache dans le fichier de description du service pour 
permettre une ouverture future plus rapide – aucun accès au serveur ne doit 
être requis tant que l'imagerie est lu pour de future ouverture.

Le pilote WCS doit géré les serveurs WCS 1.0.0 et 1.1.0, mais les serveurs WCS 
0.7 ne sont pas gérés. N'importe quel format qui est un fichier simple, et qui 
est dans un format géré par GDAL doit fonctionner. Le pilote préférera un format 
avec l'extension tiff dans le nom, sinon il se rabattra au premier format 
offert. Les systèmes de coordonnée sont lu à partir du résultat de 
*DescribeCoverage*, et doivent être sous la forme EPSG:n dans l'élément 
<supportedCRSs>.

Le fichier de description de service possède les éléments suivants additionnels 
comme enfant immédiat de l'élément *WCS_GDAL* pour être définie en option.

* **PreferredFormat :** le format à utiliser pour les appels *GetCoverage*.
* **BandCount :** nombre de bande dans le jeu de données, normalement 
  capturé à partir de la requête de test.
* **BandType :** le type de donnée du pixel. Normalement établit à partir 
  de la requête de test.
* **BlockXSize :** la largeur du bloc à utiliser pour l'accès distant en 
  cache du bloc.
* **BlockYSize :** la hauteur du bloc à utiliser pour l'accès distant en 
  cache du bloc.
* **NoDataValue :** La valeur nodata à utiliser pour toutes les bandes 
  (vide pour pas de valeur). Normalement par défaut celui récupéré des 
  informations de *CoverageOffering*.
* **Timeout :** le timeout à utiliser pour les requêtes au service 
  distant. S'il n'est pas fournit, la valeur par défaut de libcurl est utilisé.
* **UserPwd :** peut être définir avec *userid:password* pour envoyer un 
  identifiant d'utilisateur et un mot de passe au serveur distant.
* **HttpAuth :** peut être BASIC, NTLM ou ANY pour contrôler la méthode 
  d'authentification à utiliser.
* **OverviewCount :** le nombre d'aperçu pour représenter les bandes. Par 
  défaut un nombre tel que le haut de l'aperçu soit assez petit (plus petit que 
  1K x 1K environ).
* **GetCoverageExtra :** un jeu additionnel de mots-clé à ajouter aux 
  requêtes *GetCoverage* sous la forme d'url encodé  par exemple 
  ``&RESAMPLE=BILINEAR&Band=1``
* **DescribeCoverageExtra :** un jeu additionnel de mots-clé à ajouter aux 
  requêtes *DescribeCoverage* sous la forme d'url encodé  par exemple 
  ``&CustNo=775``
* **Version :** définie une version spécifique du WCS à utiliser. Pour 
  l'instant par défaut à 1.0.0 et 1.1.0 est également géré.
* **FieldName :** nom du champ qui est accédé. Utilisé seulement avec WCS 
  1.1.0 et supérieur. Par défaut au premier champs du résultat de DescribeCoverage.
* **DefaultTime :** un timePosition à utiliser par défaut lors de l'accès aux 
  couvertures avec une dimension temps. Rempli avec la dernière position du temps 
  offerte par défaut.

Time
-----

À partir de GDAL 1.9.0, ce pilote inclues la gestion expérimentale des serveurs 
WCS 1.0.0 basé sur le temps. Lors de l'accès initial la dernière position du 
temps offerte sera identifié comme *DefaultTime*. Chaque position de temps 
disponible pour la couverture sera traité comme sous jeu de données.

Notez que les jeux de données basés sur le temps ne sont pas gérés lorsque la 
description du service est le nom du fichier. Pour le moment la gestion du temps 
n'est pas disponible pour les versions autres que WCS 1.0.0. 

Voir également
==============

* Standards WCS de l'OGC : http://www.opengeospatial.org/standards/wcs

.. yjacolin at free.fr, Yves Jacolin - 2011/09/03(trunk 22590)