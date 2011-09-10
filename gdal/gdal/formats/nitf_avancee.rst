.. _`gdal.gdal.formats.nitf_avancee`:

==========================================
NITF -- Information Avancée sur le pilote
==========================================

Le pilote NITF (*National Imagery Transmission Format*) dans GDAL inclue un 
nombre d'options avancée et plus ou moins ésotérique ne convient pas à la 
`documentation générale de l'utilisation <http://www.gdal.org/frmt_nitf.html>`_ 
pour le pilote. Cette information est collecté ici et est surtout utilisable 
pour les développeurs et les utilisateurs avancés.

Segments CGM
=============

Les fichiers NITF qui ont des données CGM (qui sont un segment de type GR - 
graphique, ou SY avec un STYPE de valeur 'C') rendront cette information 
disponible comme méta-données dans le domaine CGM. Les méta-données renvoyées 
ressemblera à cela :

::
    
    SEGMENT_COUNT=1
    SEGMENT_0_SLOC_ROW=25
    SEGMENT_0_SLOC_COL=25
    SEGMENT_0_SDLVL=2
    SEGMENT_0_SALVL=1
    SEGMENT_0_SLOC_ROW=25
    SEGMENT_0_SLOC_COL=25
    SEGMENT_0_SDLVL=2
    SEGMENT_0_SALVL=1
    SEGMENT_0_CCS_ROW=00025
    SEGMENT_0_CCS_COL=00025
    SEGMENT_0_DATA= \0!\0...

Les valeurs SLOC_ROW et SLOC_COL sont l'emplacement de l'objet CGM relatif à 
l'image de base (SALVL). Les valeurs CCS_ROW/COL sont relatives au système de 
coordonnées commun. _SDLVL est le niveau d'affichage. DATA est les données brutes 
CGM avec une protection par des \ appliquées. Toutes les occurrence de zéro ASCII 
sera traduit en "\0", et tous les symboles \ et " seront protégés avec \. La 
fonction ``CPLUnescapeString()`` peut être utilisé pour protégé les données avec / 
en format binaire en utilisant le schéma *CPLES_BackslashQuotable*.

À partir de 1.8.0, pour ajouter des données CGM à une image NITF, vous pouvez 
passer des options de création dans le format suivant :

::
    
    CGM=SEGMENT_COUNT=1
    CGM=SEGMENT_0_SLOC_ROW=25
    CGM=SEGMENT_0_SLOC_COL=25
    CGM=SEGMENT_0_SDLVL=2
    CGM=SEGMENT_0_SALVL=1
    CGM=SEGMENT_0_DATA=\0!\0...

Notez que passer CGM comme options de création écrasera le segment CGM lu dans le 
domaine de métadonnées CGM.

Bien que GDAL ne gère pas le parsage ou le rendu de données CGM, au moins un 
utilisateur a trouvé la bibliothèque  `UniConverter <http://sk1project.org/modules.php?name=Products&product=uniconvertor>`_  
utile pour cela.

Fichiers NITF Multi-Image
==========================

Les fichiers NITF avec plus d'un segment d'image (IM) présentera les segments 
d'image comme des sous jeux de données. L'ouverture de multiple fichiers NITF 
par noms de fichier fournira un accès au premier segment d'image. Les 
méta-données des sous jeux de données pour les trois fichiers NITF images 
ressemblera à cela :

::
    
    Subdatasets:
        SUBDATASET_1_NAME=NITF_IM:0:multi_image_jpeg_2.0.ntf
        SUBDATASET_1_DESC=Image 1 of multi_image_jpeg_2.0.ntf
        SUBDATASET_2_NAME=NITF_IM:1:multi_image_jpeg_2.0.ntf
        SUBDATASET_2_DESC=Image 2 of multi_image_jpeg_2.0.ntf
        SUBDATASET_3_NAME=NITF_IM:2:multi_image_jpeg_2.0.ntf
        SUBDATASET_3_DESC=Image 3 of multi_image_jpeg_2.0.ntf

Dans ce cas l'ouverture de *multi_image_jpeg_2.0.ntf* directement donnera un 
accès à *NITF_IM:0:multi_image_jpeg_2.0.ntf*. Pour ouvrir les autres utilisez 
les noms des sous jeux de données correspondant. Le mécanisme de sous jeu de 
données est un concept GDAL générique  discuté dans le 
`document Modèle de données <http://www.gdal.org/gdal_datamodel.html>`_.

Segments Texte
===============

Les fichiers NITF qui ont des segments textes (qui est un segment de type TX) 
rendra cette information disponible comme méta-données dans le domaine TEXT. 
La méta-données renvoyée ressemblera à :

::
    
    EADER_0=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATA_0=This is test text file 01.
 
    HEADER_1=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATA_1=This is test text file 02.
 
    HEADER_2=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATA_2=This is test text file 03.
 
    HEADER_3=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATA_3=This is test text file 04.
 
    HEADER_4=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    DATA_4=This is test text file 05.

L'argument à DATA_n est le texte brute du n :sup:`ième` (à partir de 0) segment 
texte avec aucune protection de quelque forme que ce soit appliquée.

À partir de GDAL 1.8.0, les données d'en-tête du segment TEXT sont préservé dans 
l'item des métadonnées HEADER_n.

La méthode ``CreateCopy()`` sur le pilote NITF gère également la création de 
segments texte sur le fichier de sortie aussi longtemps que le fichier en entré 
possède des méta-données dans le domaine TEXT comme définie ci-dessus.

À partir de GDAL 1.8.0, pour ajouter des données TEXT à une image NITF, vous pouvez 
aussi passer les options de création dans le format suivant :

::
    
    TEXT=HEADER_0=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    TEXT=DATA_0=This is test text file 01.
    TEXT=HEADER_1=TE       00020021216151629xxxxxxxxxxxxxxxxxxxxxxxxxxx
    TEXT=DATA_1=This is test text file 02.

Notez que passer TEXT comme option de création écrasera le texte existant lu dans 
le domaine de métadonnées TEXT.

TRE
=====

Les fichiers NITF avec des extensions enregistrées (ou non enregistrées ?) sur 
l'en-tête du fichier, ou l'en-tête de l'image géoréférencée les rendront 
disponible sous une forme brute dans les méta-données via le domaine TRE. Le 
domaine TRE contiendra une méta-données par TRE qui aura le nom du TRE comme 
nom, et la données du TRE comme contenu. La donnée contenue sera protégé par 
comme les données CGM ci-dessus.

Dans le cas d’occurrences multiples du même TRE, la seconde occurrence sera 
nommée "TRENAME_2", le troisième "TRENAME_3" où TRENAME est le *nom TRE*.

::
    
    Metadata (TRE):
        GEOPSB=MAPM  World Geodetic System 1984                                       
               WGE World Geodetic System 1984                                   
                   WE Geodetic                                                  
                      GEODMean Sea                                              
                          MSL 000000000000000                                   
                                                0000
    PRJPSB=Polar Stereographic                                                    
         PG2-00090.00000250000039.99999884000000000000000000000000000000
    MAPLOB=M  0598005958-000003067885.8-000002163353.8

TREs comme xml:TRE
===================
 
À partir de GDAL 1.9.0, tous les TRE trouvé dans le fichier et correspondant à 
l'une des descriptions de TRE du fichier `nitf_spec.xml <http://trac.osgeo.org/gdal/browser/trunk/gdal/data/nitf_spec.xml>`_ 
dans le répertoire données de GDAL seront reporté comme contenu XML dans le 
domaine de métadonnées xml:TRE.

::
    
    Metadata (xml:TRE):
    <tres>
    <tre name="RSMDCA" location="des TRE_OVERFLOW">
        <field name="IID" value="2_8" />
        <field name="EDITION" value="1101222272-2" />
        <field name="TID" value="1101222272-1" />
        <field name="NPAR" value="06" />
        <field name="NIMGE" value="001" />
        <field name="NPART" value="00006" />
        <repeated name="IMAGE" number="1">
        <group index="0">
            <field name="IID" value="2_8" />
            <field name="NPARI" value="06" />
        </group>
        </repeated>
        <field name="XUOL" value="-2.42965895449297E+06" />
        <field name="YUOL" value="-4.76049894293300E+06" />
        <field name="ZUOL" value="+3.46898407315533E+06" />
        <field name="XUXL" value="+8.90698769551156E-01" />
        <field name="XUYL" value="+2.48664813021570E-01" />
        <field name="XUZL" value="-3.80554217799520E-01" />
        <field name="YUXL" value="-4.54593996792805E-01" />
        <field name="YUYL" value="+4.87215943350720E-01" />
        <field name="YUZL" value="-7.45630553709282E-01" />
        <field name="ZUXL" value="+0.00000000000000E+00" />
        <field name="ZUYL" value="+8.37129879594448E-01" />
        <field name="ZUZL" value="+5.47004172461403E-01" />
    [...]
        <repeated name="DERCOV" number="21">
        <group index="0">
            <field name="DERCOV" value="+5.77388827727787E+04" />
        </group>
    [...]
        <group index="20">
            <field name="DERCOV" value="+1.14369570920252E-02" />
        </group>
        </repeated>
    </tre>
    <tre name="RSMECA" location="des TRE_OVERFLOW">
    [...]
    </tre>
    <tre name="RSMIDA" location="des TRE_OVERFLOW">
    [...]
    </tre>
    <tre name="RSMPCA" location="des TRE_OVERFLOW">
    [...]
    </tre>
    </tres>


Fichier brute/ En-tête d'image
===============================

Dans certains cas l'application peut avoir besoin de récupérer des informations 
très spécifique à partir de l'image ou de l'en-tête du fichier qui n'est pas 
disponible normalement comme métadonnées. Dans ce cas il est possible d'interroger 
le domaine de métadonnées "NITF_METADATA". Le fichier complet et les en-têtes 
d'image seront renvoyés comme métadonnées au format encodé en base64. Quelque 
chose comme :

::
    
    Metadata (NITF_METADATA):
        NITFFileHeader=002213 TklURjAyLjAwMDEgICAgVTIxN0cwSjA...
        NITFImageSubheader=439 SU1NaXNzaW5nIElEMjUxNTI1NTlaTU...

Notez que les valeurs numériques encodées en ascii préfixant l'en-tête encodé en 
base64 est la longueur (décodé) en octets, suivit d'une espace.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/15 (trunk 22866)