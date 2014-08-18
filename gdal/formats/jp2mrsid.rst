.. _`gdal.gdal.formats.jp2mrsid`:

====================================
JP2MrSID --- JPEG2000 via MrSID SDK
====================================

Le format de fichier JPEG2000 est géré en lecture avec le DSDK MrSID. Il gère 
également l'écriture avec l'ESDK MrSID.

La gestion du JPEG2000 de MrSID est seulement disponible avec la version 5.X ou 
plus récente du DSDK et du EDSK.

Options de création
====================

Si vous avez l'ESDK de MrSID (5.X ou plus récent), il peut être utilisé pour 
écrire des fichiers JPEG2000. Les options de création suivantes sont gérées :

* **WORLDFILE=YES** : pour écrire un fichier world ESRI (avec l'extension .j2w). 
* **COMPRESSION=n** : indique le taux de compression désiré. Zéro indique un 
  taux de compression de 20:1 (l'image sera compressée au 1/20 de la taille 
  originale).
* **XMLPROFILE=[chemin vers le fichier]** : indique un chemin au profile XML 
  spécifique de LizardTech qui peut être utilisé pour paramétrer l'encodage en 
  JPEG2000. Ils peuvent être créer en utilisant l'ESDK de MrSID, ou avec 
  GeoExpress, ou à la main en utilisant l'exemple suivant comme modèle :

::
    
    <?xml version="1.0"?>
    <Jp2Profile version="1.0">
        <Header>
            <name>Default</name> 
            <description>LizardTech preferred settings (20051216)</description>
        </Header>
        <Codestream>
            <layers>
                8
            </layers>
            <levels>
                99
            </levels>
            <tileSize>
                0 0
            </tileSize>
            <progressionOrder>
                RPCL
            </progressionOrder>
            <codeblockSize>
                64 64
            </codeblockSize>
            <pltMarkers>
                true
            </pltMarkers>
            <wavelet97>
                false
            </wavelet97>
            <precinctSize>
                256 256
            </precinctSize>
        </Codestream>
    </Jp2Profile>

.. seealso::

  * Implémenté dans *gdal/frmts/mrsid/mrsiddataset.cpp*.
  * Site de LizardTech : http://www.lizardtech.com/

.. yjacolin at free.fr, Yves Jacolin - 2013/01/01(trunk 9914)
