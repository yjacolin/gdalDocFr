.. _`gdal.gdal.formats.jpipkak`:

=========================
JPIPKAK - JPIP Streaming
=========================

JPEG 2000 Interactive Protocol (JPIP) flexibilité en ce qui concerne l'accès 
aléatoire, ordonnancement du flux du code et décodage incrémental est hautement 
exploitable dans un environnement réseau permettant l'accès aux gros fichiers 
distants avec une bande passante des connexions limitée ou des réseaux à haute 
concurrence.

JPIPKAK - aperçu JPIP
=======================

Un bref aperçu de la séquence des événements JPIP  est présenté dans cette section, 
plus d'information peut être trouvé dans `JPEG 2000 Interactive Protocol (Part 
9 - JPIP) <http://www.jpeg.org/jpeg2000/j2kpart9.html>`_ et la spécification 
peut (et doit) être acheté à partir du site de l'`ISO <http://www.iso.org>`_.  

Une version antérieure du JPEG 2000 partie 9 est disponible ici
`http://www.jpeg.org/public/fcd15444-9v2.pdf <http://www.jpeg.org/public/fcd15444-9v2.pdf>`_, 
notez le copyright ISO, les diagrammes ne sont pas répliqués dans cette documentation.

Une abstraction du protocole JPIP a été réalisé dans ce pilote de format, les 
requêtes ont été réalisé à une niveau de résolution 1:1.

.. image:: _static/jpipsequence.png


1. la demande JPIP  initiale pour une image cible, un id cible, un session sur 
   http, les données devant être renvoyées comme jpp-stream sont demandé et une 
   longueur maximale est placé dans la réponse. Dans ce cas aucune fenêtre initiale 
   est demandée, bien que cela peut l'être.
   Le serveur répond avec un identifiant cible qui peut être utilisé pour identifier 
   l'image sur le serveur et en-tête de réponse JPIP-Cnew qui inclut le chemin 
   vers le serveur JPIP qui va traiter toutes les demandes à venir et l'identifiant 
   cid de la session. Une session est nécessaire afin que que le serveur puisse 
   modéliser l'état de la connexion du client, envoi seulement les données nécessaire.
2. Le client demande des fenêtres de vue particulière sur l'image cible avec une 
   longueur de réponse maximale et comprend l'identifiant de session établie 
   dans la communication précédente .
   'fsiz' est utilisé pour identifier la résolution associée avec la demande de 
   la fenêtre de vue. Les valeurs 'fx' et 'fy' définissent les dimensions de 
   la résolution de l'image désirée.
   'roff' est utilisé pour identifier le coin supérieur gauche en dehors de la 
   région spatiale associée à la fenêtre de vue demandée.
   'rsiz' est utilisé pour identifier l'étendue horizontal et vertical de la 
   région spatiale associée à la fenêtre de vue demandée.

JPIPKAK - approche
===================

Le pilote JPIPKAK utilise une approche qui a d'abord été démontré ici, 
`J2KViewer <http://www.drc-dev.ohiolink.edu/browser/J2KViewer>`_, par Juan Pablo 
Garcia Ortiz en séparant la couche de communication (socket / http) à partir de 
l'objet kdu_cache Kakadu. Séparer la couche de communication de l'objet données 
est désirable puiqu'elle permet l'utilisation de bibliothèques client http 
optimisée tels que libcurl, Apache HttpClient (notez que jportiz utilise un 
Java complet) et permet la communication SSL entre le client et le serveur.

L'implémentation Kakadu de la communication du client avec un serveur JPIP utilise 
un socket, et cette connexion du socket détient l'état de cette session du client. 
Une session client avec Kakadu peut être recréer en utilisant les opérations de 
cache de JPIP entre le client et le serveur, mais aucune utilisation des cookies 
HTTP traditionnel est géré puisque JPIP est neutre pour la couche transport.

Le pilote JPIPKAK est écrit en utilisant une bibliothèque client HTTP avec l'objet 
cache de Kakadu et la gestion de la communication optimisée ave un serveur JPIP 
(qui peut ou non gérer les sessions HTTP) et le kdu_region_decompressor haute 
performance de Kakadu.

.. image:: _static/components.png

JPIPKAK - implémentation
=========================

L'implémentation gère les API C et C++ de GDAL et fournie un wrapper SWIG initial 
pour ce pilote avec un exemple ImageIO Java (**TODO** - Exemple qGIS).

Le pilote utilise un modèle simple de threading pour gérer les requêtes de lecture 
des données et la récupération distance. Ce modèle de threading gère deux fenêtres 
clientes séparées, avec juste une connexion sur le serveur. Les requêtes vers le 
serveur sont multiplexées pour utiliser la bande passant disponible efficacement. 
Le client identifie ces fenêtres en utilisant les valeurs "0" (faible) ou "1" 
(haut) pour une option de la requête de métadonnées "PRIORITY".

.. note:: gestion SSL
    Si le client est compilé avec la gestion de SSL, alors le pilote détermine s'il 
    utilise SSL si la requête est un protocole jpips:// en opposition à jpip://. Notez 
    que le pilote ne vérifie pas les certificats des serveurs en utilisant le bundle 
    du certificat de Curl et il est pour le moment définir pour accepter tous les 
    certificats du serveur SSL.

.. note:: libCurl
    JPIP définie des valeurs client/serveur en utilisant les en-têtes HTTP, les 
    modifications ont été faire dans la bibliothèque de portabilité HTTP de GDAL pour 
    gérer cela.

.. _`gdal.gdal.formats.jpip.sequence`:

.. figure:: _static/gdalsequence.png

    Le diagramme de séquence de JPIP

1. *GDALGetDatasetDriver*
   
   récupère le pilote auquel ce jeu de données est lié.
2. *Open*
   
   Si le nom du fichier contenu dans l'objet ``GDALOpenInfo`` a un schéma d'URI 
   insensible à la casse de jpip ou jpips le ``JPIPKAKDataset`` est créé et 
   initialisé, autrement NULL est retourné.
3. *Initialize*

   L'initialisation implique de faire une connexion initiale au serveur JPIP pour 
   établir une session et pour récupérer les métadonnées initiales sur l'image 
   (ref. :ref:`gdal.gdal.formats.jpip.sequence`).

   si la connexion échoue, la fonction renvoie false et la fonction ``Open`` 
   retourne NULL indiquant que l'ouverture du jeu de données avec ce pilote a 
   échouée.

   Si la connexion est réussie, alors les demandes suivantes au serveur JPIP sont 
   réalisé pour récupérer toutes les métadonnées disponibles des images. Les 
   items des métadonnées sont définie en utilisant 
   ``GDALMajorObject->SetMetadataItem`` dans le domanie "JPIP".

   Si la métadonnée renvoyée du serveur inclus la boîte GeoJP2 UUID, ou une boîte 
   XML GMLJP2 alors cette métadonnées est parsée et définie la métadonnées 
   géographique de ce jeu de données.

4. *GDALGetMetadata*

   API C vers ``JPIPKAKDataset->GetMetadata``
5. *GetMetadata*

   retourne les métadonnées pour le domaine "JPIP", les clés sont "JPIP_NQUALITYLAYERS", 
   "JPIP_NRESOLUTIONLEVELS", "JPIP_NCOMPS" et "JPIP_SPRECISION" 
6. *GDALEndAsyncRasterIO*

   si le raster IO asynchrone est actif et pas nécessaire, l'API C appelle 
   ``JPIPKAKDataset->EndAsyncRasterIO``
7. *EndAsyncRasterIO*

   L'objet JPIPKAKAsyncRasterIO est supprimé
8. *delete*
9. *GDALBeginAsyncRasterIO*

   API C vers ``JPIPKAKDataset->BeginAsyncRasterIO``
10. *BeginAsyncRasterIO*

    le client a définie la fenêtre de visualisation demandée à 1:1 et à définie 
    optionnellement les items des métadonnées du niveau d'annulation, la qualité 
    des couches et la priorité des threads.
11. *Create*

    créé un objet JPIPKAKAsyncRasterIO
12. *Start*

    Configure la machinerie de kakadu et démarre un thread d'arrière-plan (s'il 
    ne fonctionne pas déjà) pour communiquer au serveur la demande de la fenêtre 
    de visualisation acutelle. 
    Le thread d'arrière-plan résulte dans la mise à jour de l'objet ``kdu_cache`` 
    tant que le serveur JPIP envoie un message "End Of Response" (EOR) pour la 
    demande de fenêtre de visualisation actuelle.
13. *API C vers LockBuffer*
14. *LockBuffer*

    Non implémented dans ``JPIPKAKAsyncRasterIO``, un blocage est nécessaire dans 
    ``JPIPKAKAsyncRasterIO->GetNextUpdatedRegion``
15. *GDALGetNextUpdatedRegion*

    C API to GetNextUpdatedRegion
16. *GetNextUpdatedRegion*

    La fonction décompresse les données disponibles pour générer une image (en 
    fonction du type de buffer du jeu de données définie dans 
    ``JPIPKAKDataset->BeginAsyncRasterIO``). La largeur et la hauteur de la fenêtre 
    (au niveau de rejet demandée) décompressée est renvoyée dans la pointeur de 
    la région et peut être affichée par le client. Le statut de l'opération de 
    rendue est une parmi ``GARIO_PENDING, GARIO_UPDATE, GARIO_ERROR, 
    GARIO_COMPLETE`` à partir de la structure ``GDALAsyncStatusType``. 
    ``GARIO_UPDATE, GARIO_PENDING`` nécessite plusieurs lectures de GetNextUpdatedRegion 
    pour obtenir les données image complète, ceci est le rendu progressif de JPIP. 
    ``GARIO_COMPLETE`` indique que la fenêtre est complète.
    
    ``GDALAsyncStatusType`` est une structure utilisée par ``GetNextUpdatedRegion`` 
    pour indiquer si la fonction doit être appelée encore lorsque soit kakadu a 
    plus de données dans son cache à décompresser, ou le serveur n'a pas envoyé 
    un message End Of Response (EOR) pour indiquer que la fenêtre demandée est 
    complète.

    La région passée dans cette fonction est envoyée par référence, et *l'appelleur 
    peut lire cette région quand le résultat renvoie pour trouver la région qui 
    a été décompressée ([NdT] phrase en anglais peu clair)*. Les données images 
    sont placées dans le buffer, par exemple RGB si la région demandée possède 3 
    composants.
17. *GDALUnlockBuffer*

    Api C vers UnlockBuffer
18. *UnlockBuffer*

    Non implémenté dans ``JPIPKAKAsyncRasterIO``, un blocage est acquis dans 
    ``JPIPKAKAsyncRasterIO->GetNextUpdatedRegion``
19. *Draw*

    Client réalise le rendu des données image
20. *GDALLockBuffer*
21. *LockBuffer*
22. *GDALGetNextUpdatedRegion*
23. *GetNextUpdatedRegion*
24. *GDALUnlockBuffer*
25. *UnlockBuffer*
26. *Draw*

JPIPKAK - exigences d'installation
====================================

* `Libcurl 7.9.4 <http://curl.haxx.se/>`_
* `OpenSSL 0.9.8K <http://www.openssl.org/>`_ (si SSL est nécessaire, une 
  connexion JPIPS)
* `Kakadu <http://www.kakadusoftware.com>`_ (testé avec v5.2.6 et v6)

Pour le moment seulement un makefile Windows est fournie, cependant cela devrait 
compiler sous Linux également puisqu'il n'y a pas de dépendances Windows.

.. seealso::

* `JPEG 2000 Interactive Protocol (Part 9 - JPIP) <http://www.jpeg.org/jpeg2000/j2kpart9.html>`_
* `http://www.opengeospatial.org/standards/gmljp2 <http://www.opengeospatial.org/standards/gmljp2>`_
* `Kakadu Software <http://www.kakadusoftware.com>`_
* `IAS demo (example JPIP(S) streams) <http://iasdemo.ittvis.com/>`_

Notes
======

Pilote développé originellement par <http://www.ittvis.com">ITT VIS</a> et donné 
à GDAL pour permettre le flux de jeux de données JPEG 2000 de client JPIP avec 
le SSL activé .

.. yjacolin at free.fr, Yves Jacolin - 2011/08/08 (trunk 21570)