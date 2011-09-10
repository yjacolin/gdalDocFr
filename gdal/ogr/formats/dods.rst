.. _`gdal.ogr.formats.dods`:

==============
DODS/OPeNDAP
==============

Ce pilote implémente la gestion en lecture seule pour la lecture des données 
géométriques à partir de serveurs OPeNDAP (DODS). Il est inclus en option dans 
OGR s'il est compilé avec la bibliothèque de gestion d'OPeNDAP.

Lors de l'ouverture d'une base de données, son nom doit être définie sous la 
forme *DODS:url*. L'URL peut inclure une expression de contrainte comme vue 
ici. Notez qu'il peut être nécessaire de mettre entre guillemet ou tout autre 
protection de l'URL DODS dans la ligne de commande si elle inclue des points 
d'interrogation ou des esperluettes (&) puisqu'ils ont souvent des 
significations dans une console.
::
    
    DODS:http://dods.gso.uri.edu/dods-3.4/nph-dods/broad1999?&press=148

Par défaut, les Séquences, Grilles et Objets tableau de haut niveau seront 
traduit en couche correspondante. Les Séquences sont (par défaut) traitées 
comme des couches ponctuelles avec la géométrie récupéré à partir des variables 
lat et lon si disponible. Pour fournir une traduction plus sophistiquée des 
séquences, grilles et tableaux vers des géométries il est nécessaire de fournir 
des informations additionnelles à OGR sous forme de DAS (*dataset auxilary 
information*) soit sous forme de serveur distant soit sous forme locale via le 
mécanisme AIS.

Une définition DAS pour une couche OGR doit ressembler à ceci :
::
    
    Attributes {
        ogr_layer_info {
            string layer_name WaterQuality;
            string spatial_ref WGS84;
            string target_container Water_Quality;
            layer_extents {
                Float64 x_min -180;
                Float64 y_min -90;
                Float64 x_max 180;
                Float64 y_max 90;
            }
            x_field {
                string name YR;
                string scope dds;
            }
            y_field {
                string name JD;
                string scope dds;
            }
        }
    }

Avertissement
==============

* Aucune largeurs de champ n'est capturée pour les champs attributaires à partir 
  du format DODS.
* Les performances pour des requêtes répétées sont améliorées de façon 
  significative en activant le cache du format DODS. Essayez la définition de 
  *USE_CACHE=1* dans votre fichier *~/.dodsrc*.

Voir également
==============

* `OPeNDAP <http://www.opendap.org/>`_

.. yjacolin at free.fr, Yves Jacolin - 2009/02/23 19:40 (trunk 5732)