.. _`gdal.ogr.formats.georss`:

GeoRSS : Geographically Encoded Objects pour les flux RSS
=========================================================

(Pilote disponible à partir de GDAL 1.7.0)

GeoRSS est une manière d'encoder une localisation dans des flux RSS ou Atom.

OGR gère la lecture et l'écriture du GeoRSS. La gestion de la lecture est 
seulement disponilbe si GDAL a été compilé avec la gestion de la bibliothèque 
expat.

Le pilote gère les documents RSS au format RSS 2.0 ou Atom 1.0.

Il gère également les 
`3 manières d'encoder la localisation <http://georss.org/model>`_ : GeoRSS 
simple, GeoRSS GML et W3C Geo (ce dernier étant obsolète).

Le pilote peut lire et écrire des documents sans information de localisation également.

Le datum par défaut pour les documents GeoRSS est le datum WGS84 (EPSG:4326) 
bien que les localisations GeoRSS soit encodé dans l'ordre latitude-longitude 
dans le fichier XML, toutes les coordonnées reportées ou attendus par le pilote 
sont dans l'ordre longitude-latitude. L'ordre longitude/latitude utilisé par 
OGR est voulu pour compatibilité avec la plupart des autres pilotes et commandes 
OGR. Pour les localisations encodées dans GML, le pilote gérera l'attribut 
*srsName* pour la description des autres SRS.

L'encodage Simple et GML gèrent la notion de boîte comme une géométrie. Cela 
sera décodé comme un rectangle (géométrie polygonale) dans le modèle Simple 
Feature d'OGR.

Une couche seule est renvoyée pendant la lecture du document RSS. Les objets 
sont récupérés à partir du contenu des éléments *<item>* (document RSS) ou 
*<entry>* (document Atom).

Problèmes d'encodage
--------------------

La bibliothèque Expat gère la lecture des encodages internes suivants :

* US-ASCII
* UTF-8
* UTF-16
* ISO-8859-1

OGR 1.8.0 ajoute la gestion pour l'encodage Windows-1252 (pour les versions 
antérieures, la modification de l'encodage mentionné dans l'en-tête XML à 
ISO-8859-1 peut fonctionner dans certain cas).

Le contenu retourné par OGR sera encodé en UTF-8, après la conversion à partir de 
l'encodage mentionné par le fichier d'en-tête.

Si votre fichier GeoRSS n'est pas encodé dans un de ces encodages, il ne sera 
pas parsé par le pilote GeoRSS. Vous pouvez le convertir dans l'un des encodages 
gérés avec la commande *iconv* par exemple et changer en fonction la valeur 
du paramètre encodage dans l'en-tête XML.

Lors de l'écriture du fichier GeoRSS, le pilote s'attend à ce que du contenu en 
UTF-8 lui soit passé.

Définitions des champs
----------------------

Lors de la lecture d'un document, le pilote réalisera d'abord une lecture 
complète du document pour obtenir les définitions du champ.

Le pilote renverra les éléments trouvés dans le schéma de base d'un canal RSS ou 
d'un flux Atom. Il renverra également les éléments d'extension qui sont 
autorisés dans les espaces de nom.

Les attributs des éléments de premier niveau seront exposés comme champs.

Les contenus complexes (élément dans des éléments de premier niveau) seront 
renvoyé comme blob XML.

Quand un même élément est répété, un nombre apparaîtra à la fin du nom de 
l'attribut pour les répétitions. Cela est utile pour l'élément *<category>* 
dans les documents RSS et Atom par exemple.

Le contenu suivant :
::
    
    <item>
        <title>Mon titre</title>
        <link>http://www.mylink.org</link>
        <description>Cool description !</description>
        <pubDate>Wed, 11 Jul 2007 15:39:21 GMT</pubDate>
        <guid>http://www.mylink.org/2007/07/11</guid>
        <category>Computer Science</category>
        <category>Logiciel Open Source</category>
        <georss:point>49 2</georss:point>
        <myns:name type="mon_type">Mon Nom</myns:name>
        <myns:complexcontent>
            <myns:subelement>Subelement</myns:subelement>
        </myns:complexcontent>
    </item>

Sera interprété dans le modèle SF d'OGR comme :
::
    
    title (String) = Mon titre
    link (String) = http://www.mylink.org
    description (String) = Cool description !
    pubDate (DateTime) = 2007/07/11 15:39:21+00
    guid (String) = http://www.mylink.org/2007/07/11
    category (String) = Computer Science
    category2 (String) = Logiciel Open Source
    myns_name (String) = Mon Nom
    myns_name_type (String) = mon_type
    myns_complexcontent (String) = <myns:subelement>Subelement</myns:subelement>
    POINT (2 49)

Problèmes lors de la création
-----------------------------

À l'export, toutes les couches sont écrites en un seul fichier. La mise à jour 
de fichiers existant n'est pas gérée.

Si le fichier en sortie existe déjà, l'écriture n'aura pas lieu. Vous devez 
d'abord effacer le fichier existant.

Une couche qui est créé ne peut pas être immédiatement lu sans fermeture et 
réouverture du fichier. Ceci afin de dire qu'un jeu de données est en écriture 
seul ou en lecture seul au cours de la session.

Géométries gérées :

* Objets de type wkbPoint/wkbPoint25D.
* Objets de type wkbLineString/wkbLineString25D.
* Objets de type wkbPolygon/wkbPolygon25D.

Les autres types de géométrie ne sont pas gérés et seront ignoré silencieusement.

Le pilote GeoRSS gère ces options de création de jeux de données suivantes :

* **FORMAT=RSS|ATOM :** si le document doit être au format RSS 2.0 ou Atom 
  1.0 format. Valeur par défaut : RSS
* **GEOM_DIALECT=SIMPLE|GML|W3C_GEO (RSS or ATOM document) :** l'encodage des 
  informations de localisation. Valeur par défaut : SIMPLE W3C_GEO ne gère que 
  les géométries ponctuelles. SIMPLE ou W3C_GEO ne gère que les géométries avec 
  des coordonnées WGS84.
* **USE_EXTENSIONS=YES|NO.*** valeur par défaut : *NO*. Si définie à *YES*, 
  les champs étendus (c'est à dire le champs qui ne ont pas dans le schéma de 
  base des documents RSS ou Atom) seront écrit. si le nom du champ non trouvé 
  dans le schéma de base correspond au motif *foo_bar*, *foo* sera considéré 
  comme le namespace de l'élément et un élément *<foo:bar>*sera écrit autrement 
  les éléments seront écrit dans le namespace *<ogr:>*.
* **WRITE_HEADER_AND_FOOTER=YES|NO.*** valeur par défaut : *YES*. Si définie à 
  *NO*, seul les éléments *<entry>* ou *<item>* seront écrit. L'utilisateur 
  devra fournir les en-têtes et pieds de page appropriés du document. Les 
  options suivantes ne sont pas utile dans ce cas.
* **HEADER (RSS ou document Atom) :** contenu XML qui sera placé entre 
  l'élément *<channel>* et le premier élément *<item>*pour un document RSS, ou 
  entre la balise xml et le premier élément *<entry>* pour un document Atom. 
  Si cela est définie, cela écrasera les options qui suivent.
* **TITLE (RSS ou document Atom) :** les valeurs placées entre l'élément 
  *<title>* dans l'en-tête. Si elle n'est pas fournie, une valeur factice sera 
  utilisée puisque cet élément est obligatoire.
* **DESCRIPTION (document RSS) :** les valeurs placées entre l'élément 
  *<description>* dans l'en-tête. Si elle n'est pas fournie, une valeur factice 
  sera utilisée puisque cet élément est obligatoire.
* **LINK (RSS document) :** les valeurs placées entre l'élément *<link>* dans 
  l'en-tête. Si elle n'est pas fournie, une valeur factice sera utilisée puisque 
  cet élément est obligatoire.
* **UPDATED (document Atom) :** les valeurs placées entre l'élément 
  *<updated>* dans l'en-tête. Elle doit être formatée comme une datetime xml. 
  Si elle n'est pas fournie, une valeur factice sera utilisée puisque cet 
  élément est obligatoire.
* **AUTHOR_NAME (document Atom) :** les valeurs placées entre l'élément 
  *<author><name>* dans l'en-tête. Si elle n'est pas fournie, une valeur 
  factice sera utilisée puisque cet élément est obligatoire.
* **ID (document Atom) :** les valeurs placées entre l'élément *<id>* dans 
  l'en-tête. Si elle n'est pas fournie, une valeur factice sera utilisée puisque 
  cet élément est obligatoire.

Lors de la translation d'un de jeu de données source, il peut être nécessaire 
de renommer les noms du champ à partir du jeu de données source dans les noms 
d'attributs RSS ou ATOM attendu, tels que *<title>*, *<description>*, etc. Cela 
peut être réalisé avec un :ref:`gdal.ogr.formats.vrt`, ou en utilisant 
l'option *-sql* de la commande ogr2ogr (voir RFC21 : 
`cast des types SQL d'OGR et alias des noms de champ <http://trac.osgeo.org/gdal/wiki/rfc21_ogrsqlcast>`_)

Exemple
----------

* la commande ''ogrinfo'' peut être utilisé pour dumper le contenu d'un fichier 
  de données GeoRSS :
  ::
    
    ogrinfo -ro -al input.xml

* la commande ''ogr2ogr'' peut être utilisé pour réaliser une translation de 
  GeoRSS vers GeoRSS. Par exemple un document Atom dans un document RSS.
  ::
    
    ogr2ogr -f GeoRSS output.xml input.xml "select link_href as link, title, 
      content as description, author_name as author, id as guid from georss" 

  .. note::
    Dans cet exemple nous faisons une correspondance entre des champs 
    équivalents à partir du nom source vers le nom attentdu du format de 
    destination.

* Le script Python suivant montre comment lire le contenu d'un flux GeoRSS en 
  ligne :
  ::
    
    #!/usr/bin/python
    import gdal
    import ogr
    import urllib2

    url = 'http://earthquake.usgs.gov/eqcenter/catalogs/eqs7day-M5.xml'
    content = None
    try:
        handle = urllib2.urlopen(url)
        content = handle.read()
    except urllib2.HTTPError, e:
        print 'HTTP service for %s is down (HTTP Error: %d)' % (url, e.code)
    except:
        print 'HTTP service for %s is down.' %(url)

    # Créé un fichier en mémoire à partir du contenu téléchargé
    gdal.FileFromMemBuffer('/vsimem/temp', content)

    ds = ogr.Open('/vsimem/temp')
    lyr = ds.GetLayer(0)
    feat = lyr.GetNextFeature()
    while feat is not None:
        print feat.GetFieldAsString('title') + ' ' + feat.GetGeometryRef().ExportToWkt()
        feat.Destroy()
        feat = lyr.GetNextFeature()

    ds.Destroy()

    # Libère la mémoire associé avec le fichier en mémoire
    gdal.Unlink('/vsimem/temp')

Voir aussi
-----------

* `Page pour le format GeoRSS <http://georss.org/>`_
* `Page Wikipedia pour le format GeoRSS <http://fr.wikipedia.org/wiki/GeoRSS>`_
* `Page Wikipedia pour le format RSS <http://fr.wikipedia.org/wiki/RSS_(format)>`_
* `Spécification RSS 2.0 <http://www.rssboard.org/rss-specification>`_
* `Page Wikipedia pour le format Atom <http://fr.wikipedia.org/wiki/Atom_(standard)>`_
* `Spécification Atom 1.0 <http://www.ietf.org/rfc/rfc4287.txt>`_


.. yjacolin@free.fr, Yves Jacolin - 2009/03/04 19:54 (trunk 18832)