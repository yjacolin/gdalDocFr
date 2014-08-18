.. _`gdal.gdal.formats.vrt`:

=======================
Format virtuel de GDAL
=======================

Introduction
==============

Le pilote VRT est un pilote de format pour GDAL qui permet de créer des jeux de 
données GDAL virtuel à partir d'autres jeux de données GDAL avec des 
repositionnements et potentiellement des algorithmes appliqués ainsi que divers 
types d'ajout et de modification de méta-données. Les descriptions VRT des jeux 
de données peuvent être sauvé dans un format XML avec l'extension .vrt.

Un exemple d'un fichier .vrt simple se référent à un jeu de données de 512x512 
avec une bande chargé à partir d'un fichier *utm.tif* ressemblerait à ceci :
::
    
    <VRTDataset rasterXSize="512" rasterYSize="512">
    <GeoTransform>440720.0, 60.0, 0.0, 3751320.0, 0.0, -60.0</GeoTransform>
    <VRTRasterBand dataType="Byte" band="1">
        <ColorInterp>Gray</ColorInterp>
        <SimpleSource>
        <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
        <SourceBand>1</SourceBand>
        <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
        <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
        </SimpleSource>
    </VRTRasterBand>
    </VRTDataset>


De nombreux aspects des fichiers VRT sont la conséquence directe de l'encodage 
XML du modèle de données de GDAL qui devraient être revus pour la compréhension 
de la sémantique des différents éléments.

Les fichiers VRT peuvent être produit par traduction vers le format VRT. Le 
fichier résultat peut alors être édité pour modifier la cartographie, ajouter 
des méta-données ou d'autres choses. Les fichiers VRT peuvent aussi être produit 
par programmation de diverses manières.

Cette section couvrira le format de fichier .vrt (appropriée pour les 
utilisateurs éditant des fichiers .vrt), et comment les fichiers .vrt peuvent 
être crée et manipulé par programmation pour les développeurs.

Format .vrt
============

Les fichiers virtuels stockés sur le disque sont laissé au format XML avec les 
éléments suivants :

* **VRTDataset :** c'est l'élément racine pour l'ensemble du jeu de données 
  GDAL. Il doit avoir les attributs rasterXSize et rasterYSize décrivant la 
  largeur et la hauteur du jeu de données en pixels. Il peut avoir des 
  sous-éléments SRS, GeoTransform, GCPList, Metadata, MaskBand et VRTRasterBand.

  ::
    
    <VRTDataset rasterXSize="512" rasterYSize="512">

  Les sous-éléments autorisés pour VRTDataset sont :

    * **SRS :** cet élément contient le système de référence spatial (système de 
      coordonnées) au format WKT de l'OGC. Notez qu'il doit être échappé pour le 
      XML, ainsi les items comme les guillemets auront les séquences esperluette 
      (&) d'échappement substitué. De même, le WKT, et les méthodes 
      *SetFromUserInput()* valide en entrée (tel que les noms well known GEOGCS, et 
      le format PROJ.4) est également autorisé dans l'élément SRS.
      ::
        
        <SRS>PROJCS[&quot;NAD27 / UTM zone 
        11N&quot;,GEOGCS[&quot;NAD27&quot;,DATUM[&quot;North_American_Datum_1927&quot;,SPHEROID[&quot;Clarke 
        1866&quot;,6378206.4,294.9786982139006,AUTHORITY[&quot;EPSG&quot;,&quot;7008&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6267&quot;]],PRI
        MEM[&quot;Greenwich&quot;,0],UNIT[&quot;degree&quot;,0.0174532925199433],AUTHORITY[&quot;EPSG&quot;,&quot;4267&quot;]],PROJECTION[&quo
        t;Transverse_Mercator&quot;],PARAMETER[&quot;latitude_of_origin&quot;,0],PARAMETER[&quot;central_meridian&quot;,-117],PARAMETER[&quot;
        scale_factor&quot;,0.9996],PARAMETER[&quot;false_easting&quot;,500000],PARAMETER[&quot;false_northing&quot;,0],UNIT[&quot;metre&quot;,
        1,AUTHORITY[&quot;EPSG&quot;,&quot;9001&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;26711&quot;]]</SRS>

    * **GeoTransform :** cet élément contient une transformation spatiales affine à 
      6 valeurs pour le jeu de données, créant une cartographie entre les 
      coordonnées en pixel/ligne et les coordonnées géoréférencées.

      :: 
        
        <GeoTransform>440720.0,  60,  0.0,  3751320.0,  0.0, -60.0</GeoTransform>

    * **Metadata :** cet élément contient une liste de pair nom/valeur de 
      méta-données associé à VRTDataset comme un tout, ou à VRTRasterBand. Il a un 
      sous-élément <MDI> (méta-données item) qui possède un attribut "key" et la 
      valeur comme une donnée de cet élément.
      ::
        
        <Metadata>
            <MDI key="md_key">Metadata value</MDI>
        </Metadata>

    * **MaskBand :** (GDAL >= 1.8.0) cet élément représente une bande de masque 
      qui est partagé entre toutes les bandes sur le jeu de données (voir GMF_PER_DATASET 
      dans RFC 15). Il doit contenir un seul élément enfant VRTRasterBand, qui est 
      la description de la bande du masque lui-même.

      ::
        
        <MaskBand>
            <VRTRasterBand dataType="Byte">
            <SimpleSource>
                <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
                <SourceBand>mask,1</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
                <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            </SimpleSource>
            </VRTRasterBand>
        </MaskBand>

    * **VRTRasterBand** : il représente une bande du jeu de données. il aura un 
      attribut dataType avec le type de données pixel associé à cette bande (utilise 
      les termes de Byte, UInt16, Int16, UInt32, Int32, Float32, Float64, CInt16, 
      CInt32, CFloat32 ou CFloat64) et la bande que cete élément représente (1 
      based). Cet élément peut avoir des sous-éléments Metadata, ColorInterp, 
      NoDataValue, HideNoDataValue, ColorTable, Description et MaskBand ainsi que diverses éléments sources 
      tel que SimpleSource, ComplexSource, etc. Une bande raster peut avoir plusieurs « sources » 
      indiquant d'où les données du raster réel doivent être recherché, et comment 
      il doit être drapé dans l'espace des pixels des bandes du raster.

    Les sous-éléments autorisés pour VRTRasterBand sont :

        * **ColorInterp :** la données de cet élément doit être le nom d'un type 
          d'interprétation de couleur . Un parmi *Gray*, *Palette*, *Red*, *Green*, 
          *Blue*, *Alpha*, *Hue*, *Saturation*, *Lightness*, *Cyan*, *Magenta*, 
          *Yellow*, *Black*, ou *Unknown*.
          :: 
            
            <ColorInterp>Gray</ColorInterp>:

        * **NoDataValue :**  élément existe une bande raster a une valeur *nodata* associé 
          à la valeur données dans cet élément.
          :: 
            
            <NoDataValue>-100.0</NoDataValue>

        * **HideNoDataValue :** si cette valeur est 1, la valeur *nodata* ne sera 
          pas renvoyée. Essentiellement, le *caller* ne sera pas au courant du 
          pixel *nodata* quand il en lit un. Tout jeux de données copié/traduit 
          à partir de celui-ci n'aura pas de valeur *nodata*. Ceci est utile 
          lorsque vous voulez spécifier une valeur d'arrière plan fixe pour 
          le jeu de données. L'arrière plan sera la valeur définie par l'élément 
          NoDataValue.

          La valeur par défaut est 0 quand cet élément est absent.

          ::
            
            <HideNoDataValue>1</HideNoDataValue>

        * **ColorTable :** cet élément est un parent d'élément Entry définissant les 
          entrées dans une table de couleur. Pour l'instant seul les tables de couleurs 
          RVBA sont gérées avec c1 correspondant au rouge, c2 au vert, c3 au bleu et 
          c4 au canal alpha. Les entrées sont ordonnées et sont présumé démarrer à 
          l'entrée  0 de la table de couleur.
          ::
            
            <ColorTable>
            <Entry c1="0" c2="0" c3="0" c4="255"/>
            <Entry c1="145" c2="78" c3="224" c4="255"/>
            </ColorTable>
        * **Description :** cet élément contient la description optionnelle d'une 
          bande raster au format texte.
          :: 
            
            <Description>Crop Classification Layer</Description>
        * **UnitType :** cet élément optionnel contient l'unité vertical pour les 
          données de la bande d'élévation. Un parmi "m" pour mètres ou "ft" pour feet. 
          Par défaut les mètres sont utilisé.
          ::
            
            <UnitType>ft</UnitType>
        * **Offset :** cet élément optionnel contient l'offset qui doit être appliqué 
          lors du calcul des pixel réel à partir des valeurs du pixel sur une bande 
          raster. 0.0 par défaut.
          :: 
            
            <Offset>0.0</Offset>
        * **Scale :** cet élément optionnel contient l'échelle qui doit être appliqué 
          lors du calcul des valeurs du pixel réel à partir des valeurs des pixels sur 
          une bande raster. 1.0 est la valeur par défaut.
          :: 
            
            <Scale>0.0</Scale>

        * **Overview :** cet élément optionnel décrit un niveau d'aperçu pour la 
          bande. Il doit avoir un élément enfant *SourceFilename* et *SourceBand*.
          L'élément *SourceFilename* peut avoir un attribut booléen *relativeToVRT*. 
          Plusieurs éléments peuvent être utilisé pour décrire plusieurs aperçus.

          ::
            
            <Overview>
            <SourceFilename relativeToVRT="1">yellowstone_2.1.ntf.r2</SourceFilename>
            <SourceBand>1</SourceBand>
            </Overview>

        * **CategoryNames :** cet élément optionnel contient une liste de sous-élément 
          de Category avec les noms des catégories pour les bandes raster classifiées.
          ::
            
            <CategoryNames>
                <Category>Missing</Category>
                <Category>Non-Crop</Category>
                <Category>Wheat</Category>
                <Category>Corn</Category>
                <Category>Soybeans</Category>
            </CategoryNames>

        * **SimpleSource :** La balise *SimpleSource* indique que les données raster 
          doivent être lues à partir d'un jeu de données séparés, en indiquant le jeu 
          de données, et les bandes à partir de les lire, et comment les données doivent 
          être drapées dans ces bandes raster. La balise *SimpleSource* peut contenir 
          les sous-éléments *SourceFilename*, *SourceBand*, *SrcRect*, et *DstRect*. 
          L'élément *SrcRect* indiquera quel rectangle du fichier source indiqué doit 
          être lu, et l'élément *DstRect* indique comment le rectangle des données 
          sources doit être drappé dans l'espace *VRTRasterBands*.

          L'attribut *relativeToVRT* dans l'élément *SourceFilename* indique si le nom du 
          fichier doit être interprété comme relatif au fichier .vrt (sa valeur est 1) ou 
          non relatif au fichier .vrt (sa valeur est 0). 0 par défaut.

          Certaines caractéristiques de la bande source peuvent être définie dans la 
          balise optionnelle *SourceProperties* pour permettre au pilote VRT de différer 
          l'ouverture du jeu de données source jusqu'à ce qu'il ait réellement besoin de 
          lire les données. Cela est particulièrement utile lors de la construction de 
          VRT avec un grand nombre de jeu de données source. Les paramètres nécessaires 
          sont les dimensions du raster, la taille des blocs et le type de données. Si la 
          balise *SourceProperties* n'est pas présente, le jeu de données source sera 
          ouvert en même temps que le fichier VRT lui-même.
  
          À partir de GDAL 1.8.0, le contenu du sous-élément *SourceBand* peut se 
          référer à une bande de masque. Par exemple *mask,1* signifie la bande 
          de masque de la première bande de la source

          ::
            
            <SimpleSource>
            <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
            <SourceBand>1</SourceBand>
            <SourceProperties RasterXSize="512" RasterYSize="512" DataType="Byte" BlockXSize="128" BlockYSize="128"/>
            <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            </SimpleSource>

        * **AveragedSource :** *AveragedSource* est dérivé de *SimpleSource* et partage 
          les mêmes propriétés sauf qu'il utilise un réechentillonnage moyen au lieu de 
          l'algorithme de plus proche voisin comme dans *SimpleSource*, quand la taille 
          du rectangle de destination n'est pas le même que la taille du rectangle source.

        * **ComplexSource :** le paramètre *ComplexSource* est dérivé de *SimpleSource* 
          (il partage donc les éléments *SourceFilename*, *SourceBand*, *SrcRect* et 
          *DestRect*), mais il fournit la gestion du reéchentillonage et l'écart des 
          valeurs source. Certaines zones de la source peuvent être masquées en 
          définissant la valeur *NODATA*.

          Le paramètre *ComplexSource* gère l'ajout de table lookup (LUK) 
          personnalisée pour transformer les valeurs sources vers la destination. Les LUT 
          peuvent être définie en utilisant la forme suivante :
          ::
            
            <LUT>[src valeur 1]:[dest valeur 1],[src valeur 2]:[dest valeur 2],...</LUT>

          Les valeurs intermédiaire sont calculées en utilisant une interpolation linéaire 
          entre les valeurs de destination de liaison du domaine correspondant.

          Le paramètre *ComplexSource* gère la recherche de composant de couleur d'une 
          bande raster source qui possède une table de couleur. La valeur 
          *ColorTableComponent* est l'index du composant de couleur à extraire : 1 pour la 
          bande rouge, 2 pour la bande verte, 3 pour la bande bleue ou 4 pour la bande alpha.

          Lors de la transformation des valeurs sources les opérations sont exécutées dans 
          l'ordre suivant :

          1. masquage des Nodata ;
          2. expansion de la table de couleur ;
          3. application du ratio d'échelle ;
          4. application du décalage d'échelle ;
          5. lecture de la table.

          ::
            
            <ComplexSource>
            <SourceFilename relativeToVRT="1">utm.tif</SourceFilename>
            <SourceBand>1</SourceBand>
            <ScaleOffset>0</ScaleOffset>
            <ScaleRatio>1</ScaleRatio>
            <ColorTableComponent>1</ColorTableComponent>
            <LUT>0:0,2345.12:64,56789.5:128,2364753.02:255</LUT>
            <NODATA>0</NODATA>
            <SrcRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            <DstRect xOff="0" yOff="0" xSize="512" ySize="512"/>
            </ComplexSource>

        * **KernelFilteredSource :** c'est un pixel source dérivé de Simple Source (il 
          partage donc les éléments SourceFilename, SourceBand, SrcRect et DestRect 
          éléments), mais il passe également les données à travers un simple filtre 
          définie avec l'élément Kernel. L'élément Kernel doit avoir deux éléments 
          enfants, Size et Coefs et en option l'attribut booléen normalisé (par défaut 
          à false=0). La taille doit doit toujours être un nombre impair, et la 
          paramètre Coefs doit contenir Size * Size entrées séparées par des espaces.
          ::
            
            <KernelFilteredSource>
            <SourceFilename>/debian/home/warmerda/openev/utm.tif</SourceFilename>
            <SourceBand>1</SourceBand>
            <Kernel normalized="1">
                <Size>3</Size>
                <Coefs>0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111 0.11111111</Coefs>
            </Kernel>
            </KernelFilteredSource>

        * **MaskBand :** (GDAL >= 1.8.0) cet élément représente une bande de masque 
          qui est spécifique à *VRTRasterBand* qu'il contient. Il doit contenir un 
          seule élément enfant *VRTRasterBand*, qui est la description de la bande 
          de masque lui-même.

Description des .vrt pour les fichiers brutes
==============================================

Jusqu'ici nous avons décris comment dérivé de nouveaux jeux de données à partir 
de fichiers existants  géré par GDAL. Cependant, il est également commun d'avoir 
à utiliser des fichiers raster binaires brutes pour lesquels la structure des 
données est connus mais pour lequel aucun pilote spécifique à ce format n'existe. 
Cela peut être accomplit en écrivant un fichier .vrt décrivant le fichier brute.

Par exemple, le fichier .vrt suivant décrit un fichier raster brute contenant 
des pixels complexes en point flottant dans un fichier appelé *l2p3hhsso.img*. 
Les données images débutent à partir du premier byte (``mageOffset=0``). La distance 
des bytes entre les pixels est de 8 (``PixelOffset=8``), la taille d'un *Cfloat32*. 
La distance es bytes du début d'une ligne au début de la suivante est de 9376 
bytes (``LineOffset=9376``) ce qui correspond à la largeur (1172) fois la taille 
d'un pixel (8).
::
    
    <VRTDataset rasterXSize="1172" rasterYSize="1864">
        <VRTRasterBand dataType="CFloat32" band="1" subClass="VRTRawRasterBand">
            <SourceFilename relativetoVRT="1">l2p3hhsso.img</SourceFilename>
            <ImageOffset>0</ImageOffset>
            <PixelOffset>8</PixelOffset>
            <LineOffset>9376</LineOffset>
            <ByteOrder>MSB</ByteOrder>
        </VRTRasterBand>
    </VRTDataset>

Il est à noter que  VRTRasterBand a un déterminant subClass de "VRTRawRasterBand". 
Également,  VRTRawRasterBand contient un nombre d'éléments non vue précédemment 
mais aucune information « source ».  VRTRawRasterBands peut ne jamais avoir de 
sources (c'est à dire  SimpleSource), mais doit contenir les éléments suivants 
en plus de tous les éléments de méta-données précédemment décrit qui sont encore 
géré.

* ``SourceFilename`` : le nom du ficher brute contenant les données pour cette 
  bande. L'attribut relativeToVRT peut être utilisé pour indiquer si 
  SourceFilename est relative au fichier .vrt (1) ou non (0).
* ``ImageOffset`` : la distance en bytes du début du premier pixel de données de 
  cette bande d'image.  Zéro par défaut.
* ``PixelOffset`` : la distance en bytes du début d'un pixel et du suivant sur 
  la même ligne. Dans des données simples en paquet (packed single band) cela 
  correspondra à la taille de dataType en bytes.
* ``LineOffset`` : la distance en bytes du début de la ligne de données et de 
  la suivante. Dans les  données simple en paquet (packed single band) cela 
  correspondra à PixelOffset * rasterXSize.
* ``ByteOrder`` : définie l'ordre des bytes des données sur le disque. Soit 
  LSB (*Least Significant Byte first*) tel que l'ordre naturel sur les systèmes 
  Intel x86 systems ou MSB (*Most Significant Byte first*) tel que sur les systèmes 
  Motorola ou Sparc systems. Par défaut celui de l'ordre de la machine locale.

**D'autre remarques :**

Les données de l'image sur le disque sont supposées être du même type de 
données que la bande dataType de *VRTRawRasterBand*.
Tous les attributs ne venant pas de la source du *VRTRasterBand* sont gérés, 
incluant les tables de couleurs, les méta-données, et l'interprétation des couleurs.

*VRTRawRasterBand* gère la mise à jour du raster alors que la source basé sur 
*VRTRasterBand* est toujours en lecture seule.
L'outil OpenEV inclut un menu Fichier pour entrer des paramètres décrivant le 
fichier raster brute dans nue interface graphique et créer le fichier .vrt 
correspondant.

Les bandes multiples dans un fichier .vrt peuvent venir du même fichier brute. 
Assurez vous juste que les définitions *ImageOffset*, *PixelOffset*, et *LineOffset* 
pour chaque bande sont appropriées pour le pixel de cette bande particulière.
Un autre exemple, dans ce cas une image de pixel entrelacé de 400x300 RVB.
::
    
    <VRTDataset rasterXSize="400" rasterYSize="300">
        <VRTRasterBand dataType="Byte" band="1" subClass="VRTRawRasterBand">
            <ColorInterp>Red</ColorInterp>
            <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
            <ImageOffset>0</ImageOffset>
            <PixelOffset>3</PixelOffset>
            <LineOffset>1200</LineOffset>
        </VRTRasterBand>
        <VRTRasterBand dataType="Byte" band="2" subClass="VRTRawRasterBand">
            <ColorInterp>Green</ColorInterp>
            <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
            <ImageOffset>1</ImageOffset>
            <PixelOffset>3</PixelOffset>
            <LineOffset>1200</LineOffset>
        </VRTRasterBand>
        <VRTRasterBand dataType="Byte" band="3" subClass="VRTRawRasterBand">
            <ColorInterp>Blue</ColorInterp>
            <SourceFilename relativetoVRT="1">rgb.raw</SourceFilename>
            <ImageOffset>2</ImageOffset>
            <PixelOffset>3</PixelOffset>
            <LineOffset>1200</LineOffset>
        </VRTRasterBand>
    </VRTDataset>


Création programmée de jeux de données VRT
============================================

Le pilote VRT gère plusieurs méthodes de création de jeux de données VRT. En 
tant que partie de GDAL 1.2.0 le fichier inclue *vrtdataset.h* doit être installé 
avec les fichiers inclues coeur de GDAL, permettant un accès direct au fichier 
aux classes VRT. Cependant, même sans cela, la plupart des possibilités 
resteront disponible à travers les interfaces standards de GDAL.

Pour créer un jeu de données VRT qui est un clone d'un jeu de données existants 
utilisez la méthode *CreateCopy()*. Par exemple pour cloner utm.tif dans un 
fichier wrk.vrt en C++ le code suivant pourra être utilisé :
::
    
    GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
    GDALDataset *poSrcDS, *poVRTDS;

    poSrcDS = (GDALDataset *) GDALOpenShared( "utm.tif", GA_ReadOnly );

    poVRTDS = poDriver->CreateCopy( "wrk.vrt", poSrcDS, FALSE, NULL, NULL, NULL );

    GDALClose((GDALDatasetH) poVRTDS);
    GDALClose((GDALDatasetH) poSrcDS);

Notez l'utilisation de *GDALOpenShared()* lors de l'ouverture du jeu de données 
source. Il est conseillé d'utiliser *GDALOpenShared()* dans cette situation afin 
d'être capable de publier la référence explicite à celle-ci avant de fermer le 
jeu de données VRT lui-même. En d'autes mots, dans l'exemple précédent, vous 
pouvez également inverser les deux dernières lignes, tandis que si vous ouvrez 
le jeu de données source avec *GDALOpen()*, vous devrez fermer le jeu de données 
VRT avant de fermer le jeu de données source.

Pour créer une copie virtuelle d'un jeu de données avec des attributs ajoutés 
ou modifiés tels que les méta-données ou les systèmes de coordonnées qui sont 
souvent difficile de changer dans les autres formats, vous pouvez faire ce qui 
suit. Dans ce cas, le jeu de données virtuel est crée « en mémoire » seulement 
par virtualisation de sa création avec un nom de fichier vide, puis utilisé 
comme source modifiée pour passer à une méthode *CreateCopy()* créant le format TIFF.
::
    
    poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

    poVRTDS->SetMetadataItem( "SourceAgency", "United States Geological Survey");
    poVRTDS->SetMetadataItem( "SourceDate", "July 21, 2003" );

    poVRTDS->GetRasterBand( 1 )->SetNoDataValue( -999.0 );

    GDALDriver *poTIFFDriver = (GDALDriver *) GDALGetDriverByName( "GTiff" );
    GDALDataset *poTiffDS;

    poTiffDS = poTIFFDriver->CreateCopy( "wrk.tif", poVRTDS, FALSE, NULL, NULL, NULL );

    GDALClose((GDALDatasetH) poTiffDS);

Dans les exemples ci-dessus la valeur *nodata* est définie à -999. Vous pouvez 
définir l'élément *HideNoDataValue* dans la bande du jeu de données VRT en 
utilisant *SetMetadataItem()* sur cette bande.

::
    
    poVRTDS->GetRasterBand( 1 )->SetMetadataItem( "HideNoDataValue" , "1" );

Dans cet exemple, un jeu de données est crée avec la méthode Create(), et on 
ajoute des bandes et des sources par programmation, mais toujours à l'aide de 
l'API « générique ». Un attribut spécial des jeux de données VRT permet 
d'ajouter des sources aux VRTRasterBand (mais pas à VRTRawRasterBand) en passant 
le XML décrivant la source dans *SetMetada()* sur la cible du domaine spécial 
« new_vrt_sources ». Le domaine cible « vrt_sources » peut également être utilisé, 
auquel cas n'importe quelle source  sera rejetée avant d'en ajouter de nouvelle. 
Dans cet exemple nous construisons un simple filtre moyen  à la place de source 
simple.
::

    // construct XML for simple 3x3 average filter kernel source.
    const char *pszFilterSourceXML  =
    "<KernelFilteredSource>"
    "  <SourceFilename>utm.tif</SourceFilename><SourceBand>1</SourceBand>"
    "  <Kernel>"
    "    <Size>3</Size>"
    "    <Coefs>0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111</Coefs>"
    "  </Kernel>"
    "</KernelFilteredSource>";

    // Create the virtual dataset. 
    poVRTDS = poDriver->Create( "", 512, 512, 1, GDT_Byte, NULL );
    poVRTDS->GetRasterBand(1)->SetMetadataItem("source_0",pszFilterSourceXML",
                                                "new_vrt_sources");

Une manière plus générale de cela et qui produira un clone 3x3 moyen de 
n'importe quelle source de données en entrée pourrait ressembler à ce qui suit. 
Dans ce cas nous définissons délibérément la source de données filtrée comme 
dans le domaine « vrt_sources » pour écraser la SimpleSource crée par la méthode 
*CreateCopy()*. Le fait que nous utilisons  CreateCopy() nous assure que tous 
les autres méta-données, géoréférencement et autre seront préservé à partir du 
jeu de données source ... La seule chose que nous somme en train de changer est 
la source des données pour chaque bande.
::
    
    int   nBand;
    GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
    GDALDataset *poSrcDS, *poVRTDS;

    poSrcDS = (GDALDataset *) GDALOpenShared( pszSourceFilename, GA_ReadOnly );

    poVRTDS = poDriver->CreateCopy( "", poSrcDS, FALSE, NULL, NULL, NULL );

    for( nBand = 1; nBand <= poVRTDS->GetRasterCount(); nBand++ )
    {
        char szFilterSourceXML[10000];

        GDALRasterBand *poBand = poVRTDS->GetRasterBand( nBand );

        sprintf( szFilterSourceXML, 
            "<KernelFilteredSource>"
            "  <SourceFilename>%s</SourceFilename><SourceBand>%d</SourceBand>"
            "  <Kernel>"
            "    <Size>3</Size>"
            "    <Coefs>0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111 0.111</Coefs>"
            "  </Kernel>"
            "</KernelFilteredSource>", 
            pszSourceFilename, nBand );
            
        poBand->SetMetadataItem( "source_0", szFilterSourceXML, "vrt_sources" );
    }

La classe *VRTDataset* est une des quelques implémentations de jeux de données 
qui gère la méthode *AddBand()*. Les options passées à la méthode *AddBand()* 
peut être utilisées pour contrôler le type de bande créé (*VRTRasterBand*, 
*VRTRawRasterBand*, *VRTDerivedRasterBand*), et dans le cas de 
*VRTRawRasterBand* de définir ses différentes paramètres. Pour le standard 
*VRTRasterBand*, les sources doivent être définie avec les exemples 
*SetMetadata()* / *SetMetadataItem()* ci-dessus.

::
    
    GDALDriver *poDriver = (GDALDriver *) GDALGetDriverByName( "VRT" );
    GDALDataset *poVRTDS;

    poVRTDS = poDriver->Create( "out.vrt", 512, 512, 0, GDT_Byte, NULL );
    char** papszOptions = NULL;
    papszOptions = CSLAddNameValue(papszOptions, "subclass", "VRTRawRasterBand"); // if not specified, default to VRTRasterBand
    papszOptions = CSLAddNameValue(papszOptions, "SourceFilename", "src.tif"); // mandatory
    papszOptions = CSLAddNameValue(papszOptions, "ImageOffset", "156"); // optionnal. default = 0 
    papszOptions = CSLAddNameValue(papszOptions, "PixelOffset", "2"); // optionnal. default = size of band type 
    papszOptions = CSLAddNameValue(papszOptions, "LineOffset", "1024"); // optionnal. default = size of band type * width 
    papszOptions = CSLAddNameValue(papszOptions, "ByteOrder", "LSB"); // optionnal. default = machine order
    papszOptions = CSLAddNameValue(papszOptions, "RelativeToVRT", "true"); // optionnal. default = false
    poVRTDS->AddBand(GDT_Byte, papszOptions);
    CSLDestroy(papszOptions);

    delete poVRTDS;

Utilisation des bandes dérivées
=================================

Un type de bande spécialisé est une bande 'dérivée' qui dérive ses informations 
des pixels de ses bandes sources. Avec ce type de bande vous devez définir une 
fonction pixel, qui a la responsabilité de générer le raster de sortie. Les 
fonctions pixel sont crée par une application puis enregistré avec GDAL en 
utilisant une clé unique.

En utilisant des bandes dérivées vous pouvez créer des jeux de données VRT qui 
manipule des bandes à la volées sans créer de nouveau fichier de bandes sur le 
disque. Par exemple, vous pouvez générer une bande en utilisant 4 bandes source 
à partir d'une neuvième bande d'un jeu de données en entré (x0, x3, x4, et x8) : 
band_value = sqrt((x3*x3+x4*x4)/(x0*x8));

Vous pouvez écrire la fonction pixel pour calculer cette valeur puis 
l'enregistrer avec GDAL avec le nom « MyPremiereFonction ». Puis, le fichier 
XML VRT suivant pourra être utilisé pour afficher cette bande dérivée :
::
    
    <VRTDataset rasterXSize="1000" rasterYSize="1000">
        <VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">>
            <Description>Magnitude</Description>
            <PixelFunctionType>MyFirstFunction</PixelFunctionType>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>1</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>4</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
                <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>5</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
            <SimpleSource>
                <SourceFilename relativeToVRT="1">nine_band.dat</SourceFilename>
                <SourceBand>9</SourceBand>
                <SrcRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
                <DstRect xOff="0" yOff="0" xSize="1000" ySize="1000"/>
            </SimpleSource>
        </VRTRasterBand>
    </VRTDataset>

En plus de la spécification de la sous-classe ( VRTDerivedRasterBand) et la 
valeur de PixelFunctionType, il y a un nouveau paramètre qui peut être utile : 
sourceTransferType. Typiquement, les rasters sources sont obtenu en utilisant le 
type de donnée de la bande dérivée. Parfois, il se peut que lorsque vous voulez 
que la fonction pixel puisse accéder à une source de données de plus haute 
résolution que le type de donnée qui est générée. Par exemple, vous pouvez avoir 
une bande dérivée de type « FLOAT », qui prend une source simple de type 
« CFloat32 » ou « CFloat64 » et renvoi la portion imaginaire. Pour accomplir 
cela, définissez le paramètre SourceTransfertType à « CFloat64 ». Autrement la 
source sera converti en « Float » avant d'appeler  la fonction pixel, et la 
partie imaginaire sera perdue.
::
    
    <VRTDataset rasterXSize="1000" rasterYSize="1000">
        <VRTRasterBand dataType="Float32" band="1" subClass="VRTDerivedRasterBand">>
            <Description>Magnitude</Description>
            <PixelFunctionType>MyFirstFunction</PixelFunctionType>
            <SourceTransferType>CFloat64</SourceTransferType>
            ...

Écrire des fonctions pixels
=============================

Pour enregistrer cette fonction avec GDAL (avant d'accéder à un jeu de données 
VRT avec des bandes dérivées qui utilisent cette fonction), une application 
appelle  ``GDALAddDerivedBandPixelFunc`` avec une clé et 
``GDALDerivedPixelFunc`` : ``GDALAddDerivedBandPixelFunc("MyFirstFunction", TestFunction);``

Le bon moment pour faire cela se situe au début d'une application quand les 
pilotes GDAL sont enregistrés. GDALDerivedPixelFunc est définie avec une 
signature similaire à IRasterIO :

**Paramètres :**

+---------------+------------------------------------------------------------------------------------------+
+ papoSources   + Un pointeur pour entasser des rasters ; un par source. Tous leurs types de donnée doivent+
+               + être le même, définie dans le paramètre eSrcType.                                        +
+---------------+------------------------------------------------------------------------------------------+
+ nSources      + Le nombre de source rasters.                                                             +
+---------------+------------------------------------------------------------------------------------------+
+ pData         + Le buffer dans lequel les données doivent être lu, ou dans lequel il doit être écrit. Ce +
+               + buffer doit contenir au moins nBufXSize * nBufYSize mots de type eBufType. L'ordre des   +
+               + pixel est organisé de gauche à droite, de haut en bas. L'espacement est contrôlé par les +
+               + paramètres nPixelSpace, et nLineSpace.                                                   +
+---------------+------------------------------------------------------------------------------------------+
+ nBufXSize     + La largeur du buffer de l'image dans laquelle la région désirée doit être lue, ou dans   +
+               + lequel il doit être écrit.                                                               +
+---------------+------------------------------------------------------------------------------------------+
+ nBufYSize     + La hauteur du buffer de l'image dans laquelle la région désirée doit être lue, ou dans   +
+               + lequel il doit être écrit.                                                               +
+---------------+------------------------------------------------------------------------------------------+
+ eSrcType      + Le type des valeurs des pixels dans le tableau raster papoSources.                       +
+---------------+------------------------------------------------------------------------------------------+
+ eBufType      + Le type des valeurs des pixels que la fonction pixel doit générer dans le buffer de      + 
+               + données pData.                                                                           +
+---------------+------------------------------------------------------------------------------------------+
+ nPixelSpace   + La distance des bytes du début de la valeur d'un pixel dans pData de la prochaine valeur +
+               + du pixel dans une ligne. Si la valeur par défaut doit être utilisée la taille du type de +
+               + données eBufType est utilisée.                                                           +
+---------------+------------------------------------------------------------------------------------------+
+ nLineSpace    + La distance des bytes à partir du début d'une ligne dans pData au début de la suivante.  +
+---------------+------------------------------------------------------------------------------------------+

**Retour :**
::
    
    CE_Failure on failure, otherwise CE_None.
    typedef CPLErr
    (*GDALDerivedPixelFunc)(void **papoSources, int nSources, void *pData,
                        int nXSize, int nYSize,
                        GDALDataType eSrcType, GDALDataType eBufType,
                        int nPixelSpace, int nLineSpace);

Ce qui suit est une implémentation de la fonction pixel :
::
    
    #include "gdal.h"

    CPLErr TestFunction(void **papoSources, int nSources, void *pData,
                    int nXSize, int nYSize,
                    GDALDataType eSrcType, GDALDataType eBufType,
                    int nPixelSpace, int nLineSpace)
    {

        int ii, iLine, iCol;
        double pix_val;
        double x0, x3, x4, x8;
    
        // ---- Init ---- 
        if (nSources != 4) return CE_Failure;
    
        // ---- Set pixels ----
        for( iLine = 0; iLine < nYSize; iLine++ )
        {
            for( iCol = 0; iCol < nXSize; iCol++ )
            {
                ii = iLine * nXSize + iCol;
    
                /* Source raster pixels may be obtained with SRCVAL macro */
                x0 = SRCVAL(papoSources[0], eSrcType, ii);
                x3 = SRCVAL(papoSources[1], eSrcType, ii);
                x4 = SRCVAL(papoSources[2], eSrcType, ii);
                x8 = SRCVAL(papoSources[3], eSrcType, ii);
    
                pix_val = sqrt((x3*x3+x4*x4)/(x0*x8));
             
                GDALCopyWords(&pix_val, GDT_Float64, 0,
                           ((GByte *)pData) + nLineSpace * iLine + iCol * nPixelSpace,
                           eBufType, nPixelSpace, 1);
             }
        }
    
        // ---- Return success ---- //
        return CE_None;
    }

Problèmes de Multi-threading
==============================

Lors de l'utilisation de jeux de données VRT dans un environnement 
multi-threading, vous devez être prudent lors de l'ouverture de jeu de données 
VRT par le thread qui va l'utiliser par la suite. La raison de cela est que le 
jeu de données VRT utilise *GDALOpenShared* lors de l'ouverture des jeux de 
données sous-jacent. Si vous ouvrez deux fois le même jeu de données VRT par le 
même thread, l'ensemble des jeux de données VRT partageront la même prise en 
charge des jeux de données sous-jacent.

.. yjacolin at free.fr, Yves Jacolin - 2011/08/31 (trunk 22897)