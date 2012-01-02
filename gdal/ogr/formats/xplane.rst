.. _`gdal.ogr.formats.xplane`:

X-Plane/Flightgear aeronautical data
=====================================

(disponible depuis GDAL 1.6.0)

Les données aéronautique X-Plane sont gérées en lecture seule. Ces données sont 
utilisées par exemple par le logiciel Flihgear et X-Plane.

Le pilote est capable de lire les fichiers suivants :

+----------------------------+----------------------+-----------------+
+ Nom du fichier             + Description          + Versions gérées +
+============================+======================+=================+
+ apt.dat                    + Données Aéroport     + 850, 810        +
+----------------------------+----------------------+-----------------+
+ nav.dat (ou earth_nav.dat) + Aides à la navigation+ 810, 740        +
+----------------------------+----------------------+-----------------+
+ fix.dat (ou earth_fix.dat) + Intersections IFR    + 600             +
+----------------------------+----------------------+-----------------+
+ awy.dat (ou earth_awy.dat) + Route de vol         + 640             +
+----------------------------+----------------------+-----------------+

Chaque fichier sera retourné comme un ensemble de couches dont le schéma de 
données est données ci-dessous. Le schéma des données est généralement aussi 
proche que possible que les schémas des données originelles décrit dans la 
spécification X-Plane. Cependant, vous noterez s'il vous plaît que les mètres 
(ou kilomètre) sont toujours utilisés pour retourner les hauteurs, les élévations, 
les distances (largeurs et longueurs), etc., même si les données originales sont 
parfois exprimées en pied ou en miles nautiques.

Les données sont retournées comme étant exprimé en datum WGS84 (latitude, 
longitude), bien que la spécification n'est pas très claire sur ce sujet).

L'option de configuration OGR_XPLANE_READ_WHOLE_FILE peut être définie à FALSE 
lors de la lecture d'un gros fichier en fonction de la RAM disponible (vrai tout 
particulièrement pour apt.dat). Cette option force le pilote à ne pas mettre en 
cache les features en RAM, mais juste à les récupérer de la couche en cours. Bien 
sur, cela aura un impact négatif sur les performances.

Exemples
---------

convertir toutes les couches contenu dans *apt.dat* dans un ensemble de shapefiles :

  % ogr2ogr apt_shapes apt.dat

convertir toutes les couches contenu dans *apt.dat* dans une base de données PostgreSQL :

  % PG_USE_COPY=yes ogr2ogr -overwrite -f PostgreSQL PG:"dbname=apt" apt.dat

Voir également
--------------

* `Définition du fichier données X-Plane <http://data.x-plane.com/designers.html>`_


Airport data (apt.dat)
----------------------

Ce fichier contient la description des éléments définissant les aéroports, les 
héliports, les bases nautiques, avec leur pistes et route de taxi, les 
fréquences ATC, etc.

Les couches suivantes sont retournées :

* APT (Point)
* RunwayThreshold (Point)
* RunwayPolygon (Polygone)
* WaterRunwayThreshold (Point)
* WaterRunwayPolygon (Polygone)
* Stopway (Polygon)
* Helipad (Point)
* HelipadPolygon (Polygone)
* TaxiwayRectangle (Polygone)
* Pavement (Polygone)
* APTBoundary (Polygone)
* APTLinearFeature (Line String)
* StartupLocation (Point)
* APTLightBeacon (Point)
* APTWindsock (Point)
* TaxiwaySign (Point)
* VASI_PAPI_WIGWAG (Point)
* ATCFreq (Aucun)

Toutes les couches autre que APT se référeront à l'aéroport grâce à la colonne 
*apt_icao*, qui peut servir de clé étrangère.

Couche APT
***********

Principale description pour un aéroport. La position rapportée sera la position 
de la tour de contrôle si présente, autrement la position trouvée du premier 
seuil de la piste.

**Champs :**

* apt_icao  : Chaine (4.0). Code *ICAO* de l'aéroport.
* apt_name  : Chaine (0.0). Nom complet de l'aéroport.
* type: Integer (1.0). Airport type : 0 pour les aéroport régulier, 1 pour les 
  bases d'hydravion, 2 pour les héliports (ajouté dans GDAL 1.7.0)
* elevation_m  : Réel (8.2). Altitude de l'aéroport (en mètres).
* has_tower : Integer (1.0). Définie à 1 si l'aéroport a une tour de contrôle.
* hgt_tower_m  : Réel (8.2). Hauteur de la tour de contrôle si présente.
* tower_name  : Chaine (32.0). Nom de la tour de contrôle si présente.

Couche RunwayThreshold
```````````````````````

Cette couche contient la description d'un seuil  d'une piste.
La piste en elle-même est complètement décrite par ces deux seuils, et la couche 
*RunwayPolygon*.

.. note::
    quand une piste a un seuil déplacé, le seuil sera rapporté comme deux 
    géométries : une à la position du seuil non déplacé (*is_displaced=0*), et 
    l'autre à la position du seuil déplacé (*is_displaced=1*).


**Champs :**

* apt_icao : Chaine (4.0). code *ICAO* pour l'aéroport de ce seuil de piste.
* rwy_num : Chaine (3.0). Code pourla piste, tel que18, 02L, etc. Unique pour 
  chaque aéroport.
* width_m : Réel (3.0). Largeur en mètre.
* surface : Chaine (0.0). Type de la surface parmi :

    * Asphalt
    * Concrete
    * Turf/grass
    * Dirt
    * Gravel
    * Dry lakebed
    * Water
    * Snow
    * Transparent 

* shoulder : Chaine (0.0). Type d'accotement de la piste parmi :

    * None
    * Asphalt
    * Concrete 

* smoothness : Réel (4.2). Douceur de la piste. Pourcentage entre 0.00 et 1.00. 
  1.25 est la valeur par défaut.
* centerline_lights : Entier (1.0). Définie à 1 si la piste a des lumières 
  centrales
* edge_lighting : Chaine (0.0). Type de bord lumineux parmi :

  * None
  * Yes (quand importé des enregistrements V810)
  * LIRL : Lumière de piste de faible intensité(proposé  pour V90x)
  * MIRL : Lumière de piste de moyenne intensité
  * HIRL : Lumière de piste de haute intensité (proposé  pour V90x) 

* distance_remaining_signs : Entier (1.0). Définie à 1 si la piste a des 
  lumières de 'distance restante'.
* displaced_threshold_m : Réel (3.0). Distance entre le seuil et le seuil 
  déplacé.
* is_displaced : Entier (1.0). Définie à 1 si la position est la position du 
  seuil déplacé.
* stopway_length_m : Réel (3.0). Longueur de la piste d'arrêt/de la zone de 
  décollage/de la zone de dépassement à la fin de l'approche de la piste en 
  mètre.
* markings : Chaine (0.0). Marquage de la piste pour la fin de piste parmi :

    * None
    * Visual
    * Non-precision approach
    * Precision approach
    * UK-style non-precision
    * UK-style precision 

* approach_lighting : Chaine (0.0). Lumière d'approche pour la fin de la piste 
  parmi :

    * None
    * ALSF-I
    * ALSF-II
    * Calvert
    * Calvert ISL Cat II and III
    * SSALR
    * SSALS (Enregistrements V810)
    * SSALF
    * SALS
    * MALSR
    * MALSF
    * MALS
    * ODALS
    * RAIL
 
* touchdown_lights: Integer (1.0). Set to 1 if the runway has touchdown-zone 
  lights (TDZL)
* REIL : Chaine (0.0). Lumière d'Identification de fin de piste, *Runway End 
  Identifier Lights* (REIL) parmi :

  * None
  * Omni-directional
  * Unidirectionnal 

* length_m : Réel (5.0). (Champ calculé). Longueur en mètre entre les deux 
  seuils aux deux extrémités de la piste. Les seuils déplacés ne sont pas pris 
  en compte dans ce calcul.
* true_heading_deg : Réel (6.2). (Champ calculé). En-tête réel en degré à 
  l'approche de la fin de la piste.

Couche RunwayPolygon
``````````````````````

Cette couche contient la forme rectangulaire de la piste. Elle est calculé à 
partir des informations de seuil de la piste. Quand cela n'est pas définie, la 
signification du champ est la même que la couche *RunwayThreshold*. 

**Champs :**

* apt_icao : Chaine (4.0)
* rwy_num1 : Chaine (3.0). Code pour le premier seuil de la piste. Par exemple *20L*.
* rwy_num2 : Chaine (3.0). Code pour le second seuil de la piste. Par exemple *02R*.
* width_m : Réel (3.0)
* surface : Chaine (0.0)
* shoulder : Chaine (0.0)
* smoothness : Réel (4.2)
* centerline_lights : Entier (1.0)
* edge_lighting : Chaine (0.0)
* distance_remaining_signs : Entier (1.0)
* length_m : Réel (5.0)
* true_heading_deg : Réel (6.2). En-tête réel de la première à la seconde piste.

WaterRunwayThreshold (Point)
`````````````````````````````

**Champs :**

* apt_icao : Chaine (4.0)
* rwy_num : Chaine (3.0). Code pour la piste, parexemple 18. Unique pour chaque 
  aéroport.
* width_m : Réel (3.0)
* has_buoys : Entier (1.0). Définie à 1 si la piste doit être marqué avec des 
  bouées flottantes sur l'eau.
* length_m : Réel (5.0). (Champ calculé) Longueur entre les deux extrémités de 
  la piste amerrissage.
* true_heading_deg : Réel (6.2). (Champ calculé). En-tête réel en degré à 
  l'approche de la fin de la piste.

WaterRunwayPolygon (Polygone)
``````````````````````````````

Cette couche contient la forme rectangulaire d'une piste d'ammerissage. Elle est 
construite à partir des informations des seuils des pistes d'atterrissage de l'eau.

 **Champs :**

* apt_icao : Chaine (4.0)
* rwy_num1 : Chaine (3.0)
* rwy_num2 : Chaine (3.0)
* width_m : Réel (3.0)
* has_buoys: Integer (1.0)
* length_m : Réel (5.0)
* true_heading_deg : Réel (6.2) 

Stopway layer (Polygon)
```````````````````````

(À partir de GDAL 1.7.0)

Cette couche contient la forme rectangulaire du prolongement d'arrêt qui peut être 
trouvé au début de la piste. C'est une partie du tarmac mais qui n'est pas censé 
être utilisée pour les opérations normales.

Il est calculé à partir des informations de longueur du prolongement d'arrêt de 
la piste et seulement présent si la longueur est différente de zéro.

Lorsqu'il n'est pas spécifié, la signification des champs est le même que pour 
la couche RunwayThreshold.

Champs :

* apt_icao: String (4.0)
* rwy_num: String (3.0).
* width_m: Real (3.0)
* length_m: Real (5.0) : longueur du prolongement de l'arrêt / du blastpad / du 
  dépassement à la fin de l'approche de la piste en mètre.

Helipad (Point)
````````````````

Cette couche contient le centre de la piste d'atterrissage d'hélicoptères.

**Champs :**

* apt_icao : Chaine (4.0)
* helipad_name : Chaine (5.0). Nom de la piste d'atterrissage d'hélicoptères de 
  la forme "Hxx". Unique pour chaque aéroport.
* true_heading_deg : Réel (6.2)
* length_m : Réel (5.0)
* width_m : Réel (3.0)
* surface : Chaine (0.0). Voyez ci-dessus pour les codes de surfaces des pistes.
* markings : Chaine (0.0). Voyez ci-dessus pour les codes de marquage des pistes.
* shoulder : Chaine (0.0). Voyez ci-dessus pour les codes d'accotement des pistes.
* smoothness : Réel (4.2). Voyez ci-dessus pour la description simple des pistes.
* edge_lighting : Chaine (0.0). Bord de piste d'atterrissage d'hélicoptère 
  lumineux parmi :

    * None
    * Yes (Enregistrement V810)
    * Yellow
    * White (proposé pour V90x)
    * Red (Enregistrement V810) 

HelipadPolygon (Polygone)
``````````````````````````

Cette couche contient la forme rectangulaire d'une aire d'atterrissage 
d'hélicoptères. Les champs sont identique à la couche *Helipad*.

TaxiwayRectangle (Polygone) - Enregistrement V810
````````````````````````````````````````````````````

Cette couche content la forme rectangulaire d'une voie de taxie.

**Champs :**

* apt_icao : Chaine (4.0)
* true_heading_deg : Réel (6.2)
* length_m : Réel (5.0)
* width_m : Réel (3.0)
* surface : Chaine (0.0). Voyez ci-dessus les codes des surfaces des pistes 
  d'atterrissage.
* smoothness : Réel (4.2). Voyez ci-dessus la description douce des pistes 
  d'atterrissage.
* edge_lighting : Entier (1.0). Définie à 1 si la piste de taxi a des bords lumineux.

Pavement (Polygone)
```````````````````

Cette couche contient des tronçons polygonaux de chaussée  pour les voies de 
taxi et des tabliers. Les polygones peuvent inclure des troues.

Le fichier source peut contenir des courbes de Béziers comme côté de polygone. 
Dû à un manque de gestion de telle géométrie dans le modele d'Objet Simple 
(Simple Feature) d'OGR, les coubres de Bézier sont discrétisées en morceaux 
linéaires.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0)
* surface : Chaine (0.0). Voyez ci-dessus les codes des surfaces des pistes 
  d'aviation.
* smoothness : Réel (4.2). Voyez ci-dessus la descriptions en douceur des pistes 
  d'aviations.
* texture_heading : Réel (6.2). Direction du grain de texture de la chaussée en 
  degré réel

APTBoundary (Polygone)
```````````````````````

Cette couche contient les limites de l'aéroport. Il y a au maximum une telle 
géométrie par aéroport. Le polygone peut inclure des troues. Les courbes de 
béziers sont discrétisées en morceaux linéaires.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0) 

APTLinearFeature (Chaîne linéaire)
````````````````````````````````````

Cette couche contienr les objets linéaires. Les courbes de béziers sont d
iscrétisées en morceaux linéaire.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0) 

StartupLocation (Point)
```````````````````````

Définie les positions des portes, locations de rampe, etc.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0)
* true_heading_deg : Réel (6.2) 

APTLightBeacon (Point)
```````````````````````

Définie les balises-lumières des aéroports.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0)
* color : Chaine (0.0). Couleur de la lumière de la balise parmi :

    * None
    * White-green : aérogare
    * White-yellow : base d'hydravion
    * Green-yellow-white : héliports
    * White-white-green : champ militaire

APTWindsock (Point)
````````````````````

Définie les biroutes des aéroports.

**Champs :**

* apt_icao : Chaine (4.0)
* name : Chaine (0.0)
* is_illuminated: Integer (1.0)

TaxiwaySign (Point)
````````````````````

Définie les signes des voies de taxi des aéroports.

**Champs :**

* apt_icao : Chaine (4.0)
* text : Chaine (0.0). C'est d'une manière ou d'une autre encodé dans un format 
  spécifique. Voyez les `spécification <http://x-plane.org/home/robinp/Apt850.htm#SignTextSpec>`_ 
  d'X-Plane pour plus de détails.
* true_heading_deg : Réel (6.2)
* size: Integer (1.0). De  1 à 5. Voyez les spécification d'X-Plane pour plus de détails.

VASI_PAPI_WIGWAG (Point)
`````````````````````````

Définie un *VASI*, *PAPI* ou *Wig-Wag*. Pour les valeurs *PAPI* et *Wig-Wags*, 
les coordonnées est le centre de l'affichage. Pour la valeur *VASI*, c'est le 
point central entre les deux unités de lumière des *VASI*.

**Champs :**

* apt_icao : Chaine (4.0)
* rwy_num : Chaine (3.0). Clé étrangère pour le champ *rwy_num* de la couche 
* RunwayThreshold*.
* type : Chaine (0.0). Type comprenant :

    * VASI
    * PAPI Left
    * PAPI Right
    * Space Shuttle PAPI
    * Tri-colour VASI
    * o Wig-Wag lights 

* true_heading_deg : Réel (6.2)
* visual_glide_deg : Réel (4.2) 

ATCFreq (None)
```````````````

Définie une réquence ATC d'nu aéroport. Notez que cette couche n'a pas de géométrie.

**Champs :**

* apt_icao : Chaine (4.0)
* atc_type : Chaine (4.0). Type de la fréquence parmi (dérivé du numéro du type 
  d'enregistrement) :

  * ATIS : AWOS (*Automatic Weather Observation System*), ASOS (*Automatic 
    Surface Observation System*) ou ATIS (*Automated Terminal Information 
    System*)

       * CTAF : Unicom ou CTAF (USA), radio (UK)
       * CLD : Clearance delivery (CLD)
       * GND : Sol
       * TWR : Tour
       * APP : Approche
       * DEP : Départ

* freq_name : Chaine (0.0). Nom de la fréquence ATC. C'est souvent une 
  abréviation (tel que GND pour "*Ground*").
* freq_mhz : Réel (7.3). Fréquence en MHz.

Aides à la navigation (nav.dat)
--------------------------------

Ce fichier contient la description de divers phare d'aides à la navigation.

Les couches suivantes sont retournées :

* ILS (Point)
* VOR (Point)
* NDB (Point)
* GS (Point)
* Marker (Point)
* DME (Point)
* DMEILS (Point)

ILS (Point)
************

*Localiser* qui est une partie d'un ILS complet, ou un *localiser* indépendant 
(LOC) également inclut un LDA (*Landing Directional Aid*) ou un SDF (*Simplified 
Directional Facility*).

**Champs :**

* navaid_id : chaine (4.0). Identification du *nav-aid*. *NON* unique.
* apt_icao : chaine (4.0). Clé étrangère du champ *apt_icao* de la couche 
  *RunwayThreshold*
* rwy_num : chaine (3.0). Clé étrangère du champ *rwy_num* de la couche 
  *RunwayThreshold*.
* subtype : chaine (10.0). Sous-type dont :

    * ILS-cat-I
    * ILS-cat-II
    * ILS-cat-III
    * LOC
    * LDA
    * SDF
    * IGS
    * LDA-GS 

* elevation_m : réel (8.2). Élévation d'un *nav-aid* en mètres.
* freq_mhz : réel (7.3). Fréquence d'un *nav-aid* en MHz.
* range_km : réel (7.3). Largeur d'un *nav-aid* en km.
* true_heading_deg : réel (6.2). En-tête réel du *localiser* en degré.

VOR (Point)
************

*Navaid* du type *VOR*, *VORTAC* ou *VOR-DME*.

**Champs :**

* navaid_id : chaine (4.0). Identification de nav-aid. *NON* unique.
* navaid_name : chaine (0.0)
* subtype : chaine (10.0). Fonction *VOR*, *VORTAC* ou *VOR-DME*.
* elevation_m : réel (8.2)
* freq_mhz : réel (7.3)
* range_km : réel (7.3)
* slaved_variation_deg : réel (6.2). Indique la variation du *cylindre* d'un 
  *VOR/VORTAC* en degré.

NDB (Point)
************

**Champs :**

* navaid_id : chaine (4.0). Identification de nav-aid. *NON* unique.
* navaid_name : chaine (0.0)
* subtype : chaine (10.0). Fonction de NDB, LOM, NDB-DME.
* elevation_m : réel (8.2)
* freq_khz : réel (7.3). Fréquence en kHz
* range_km : réel (7.3) 

GS - Glideslope (Point)
************************

Glideslope nav-aid.

**Champs :**

* navaid_id : chaine (4.0). Identification du nav-aid. *NON* unique.
* apt_icao : chaine (4.0). Clé étrangère du champ *apt_icao* de la couche *RunwayThreshold*.
* rwy_num : chaine (3.0). Clé étrangère du champ *rwy_num* de la couche *RunwayThreshold*.
* elevation_m : réel (8.2)
* freq_mhz : réel (7.3)
* range_km : réel (7.3)
* true_heading_deg : réel (6.2). En-tête réel du *glideslope* en degré.
* glide_slope : réel (6.2). Angle du *glide-slope* en degré (typiquement 3 degrés) 

Marker - ILS marker beacons. (Point)
*************************************

*Nav-aids* de type *Outer Marker* (OM), *Middle Marker* (MM) ou *Inner Marker* (IM).

**Champs :**

* apt_icao : chaine (4.0). Clé étrangère du champ *apt_icao* de la couche 
  *RunwayThreshold*.
* rwy_num : chaine (3.0). Clé étrangère du champ *rwy_num* de la couche 
  *RunwayThreshold*.
* subtype : chaine (10.0). Fonction de OM, MM ou IM.
* elevation_m : réel (8.2)
* true_heading_deg : réel (6.2). En-tête réel du *glideslope* en degré. 

DME (Point)
************

DME, incluant l'élément DME d'un VORTAC, VOR-DME ou NDB-DME.

**Champs :**

* navaid_id : chaine (4.0). Identification de nav-aid. *NON* unique.
* navaid_name : chaine (0.0)
* subtype : chaine (10.0). Fonction de VORTAC, VOR-DME, TACAN ou NDB-DME
* elevation_m : réel (8.2)
* freq_mhz : réel (7.3)
* range_km : réel (7.3)
* bias_km : réel (6.2). Ce biais doit être soustrait à la distance calculé au 
  DME pour donner la lecture du cockpit désirée.

DMEILS (Point)
**************

Élément DME d'un ILS.

**Champs :**

* navaid_id : chaine (4.0). Identification du nav-aid. *NON* unique.
* apt_icao : chaine (4.0). Clé étrangère pour le champ *apt_icao* de la couche 
  *RunwayThreshold*.
* rwy_num : chaine (3.0). Clé étrangère pour le champ *rwy_num* de la couche 
  *RunwayThreshold*.
* elevation_m : réel (8.2)
* freq_mhz : réel (7.3)
* range_km : réel (7.3)
* bias_km : réel (6.2). Ce biais doit être soustrait de la distance calculée au 
  DME pour donner la lecture du cockpit désiré.


Intersections IFR (fix.dat)
----------------------------

Ce fichier contient les intersections IFR (souvent nommé *fixes*).

La couche suivante est renvoyée :

* FIX (Point)

FIX (Point)
************

**Champs :**

* fix_name : Chaine (5.0). Nom de l'intersection. *NON* unique. 

Airways (awy.dat)
-----------------

Ce fichier contient la description des segments de la route de vol.

Les couches suivantes sont retournées :

* AirwaySegment (chaine ligne)
* AirwayIntersection (point)

AirwaySegment (Line String)
****************************

**Champs :**

* segment_name : chaine (0.0)
* point1_name : chaine (0.0) : Nom de l'intersection ou nav-aid au début de ce 
  segment
* point2_name : chaine (0.0) : Nom de l'intersection ou nav-aid au début de ce 
  segment
* is_high : entier (1.0) : Définie à 1 si c'est une route aérienne "High"
* base_FL : entier (3.0) : Niveau de vol (en centaine de pied) de la base de la 
  route de vol.
* top_FL : entier (3.0) : Niveau de vol (en centaine de pied) du haut de la 
  route de vol. 

AirwayIntersection (Point)
**************************

**Champ :**

* name : Chaine (0.0) : Nom de l'intersection ou nav-aid 

.. yjacolin at free.fr, Yves Jacolin - 2011/08/03 (trunk 18548)