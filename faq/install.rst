.. _`gdal.faq.install`:

================================
FAQ installation et compilation
================================

Où est ce que je peux trouver une version de développement de GDAL ?
======================================================================

Vous pouvez la récupérer directement du dépôt SVN. Visitez la page Wiki 
`Downloading GDAL/OGR Source <http://trac.osgeo.org/gdal/wiki/DownloadSource#Subversion>`_ 
pour des instructions détaillées.

Puis je avoir un fichier de projet pour MS Visual Studio pour GDAL ?
======================================================================

Les développeurs de GDAL trouve plus pratique de compiler avec ``makefiles`` et 
l'utilitaire 
`Visual Studio NMAKE <http://msdn2.microsoft.com/en-us/library/dd9y37ha(vs.80).aspx>`_. 
Maintenir un ensemble parallèle de fichier projet pour GDAL implique trop de 
travail, il n'y a donc pas de fichiers de projet complet directement disponible 
des mainteneurs.

Il existe des fichiers projet très simple disponible depuis GDAL/OGR 1.4.0 qui 
invoque juste les makefiles pour la compilation, mais permet le débugage plus 
pratique. Ce sont les fichiers *makegdal71.vcproj* et *makegdal80.vcproj* dans 
le répertoire racine de GDAL. Lisez la page 
`Using Makefile Projects <http://trac.osgeo.org/gdal/wiki/MakeFileProjects>` 
pour plus de détails.

Occasionnellement d'autres utilisateurs prépare des fichiers projets complets, 
et vous pouvez y avoir accès en le demandant sur la liste 
`gdal-dev list <http://lists.maptools.org/mailman/listinfo/gdal-dev/>`_. 
Cependant, je vous recommande fortement d'utiliser le système compilé basé sur 
``NMAKE``. Avec le mode débugage activé vous pouvez encore débuguer dans GDAL 
avec Visual Studio. 

Puis je compiler GDAL avec MS Visual C++ 2008 Édition Express ?
================================================================

Oui, depuis au moins GDAL/OGR 1.5 ce qui devrait être simple. Avant de procéder 
à la compilation normale basée sur NMAKE faite simplement en sorte que la macro 
MSVC_VER vers le haut du fichier *GDAL/nmake.opt* soit changé en 1500 pour tenir 
compte de la version du compilateur (Visual C++ 9.0). Cela va modifier la 
compilation pour sauter l'interface VB6 qui dépend de composants ATL non 
disponibles dans l'édition express.

`Téléchargement de Microsoft Édition Express <http://www.microsoft.com/express/download/>`_ 

Puis je compiler GDAL avec MS Visual C++ 2005 Express Edition ?
================================================================

Oui, vous pouvez. Il est également possible d'utiliser les bibliothèques GDAL 
dans une application développée en utilisant 
`Microsoft Visual C++ 2005 Express Edition <http://msdn.microsoft.com/vstudio/express/visualc/>`_.

* Téléchargez et installez `Visual C++ 2005 Express Edition <http://msdn.microsoft.com/vstudio/express/visualc/download/>`_. 
  Suivez les instructions présentées sur ce site.
* Téléchargez et installez `Microsoft Platform SDK <http://msdn.microsoft.com/vstudio/express/visualc/usingpsdk/>`_. 
  Encore, suivez les instructions soigneusement sans omettre une étape.
* ajouter les chemins suivants pour inclure les fichiers dans les paramètres de 
  l'IDE de Visual C++. Faites le de la même manière présenté dans 
  l'`étape 3 <http://msdn.microsoft.com/vstudio/express/visualc/usingpsdk/>`_ 
  du site ci-dessus.

  C:\\Program Files\\Microsoft Platform SDK\\Include\\atl
  C:\\Program Files\\Microsoft Platform SDK\\Include\\mfc

* Puisque vous voulez compiler GDAL à partir de la ligne de commande en 
  utilisant l'outil ``nmake``, vous avez besoin également de définir ou de 
  mettre à jour les variables d'environnement *INCLUDE* et *LIB* manuellement. 
  Vous pouvez le faire de deux manières :

     - en utilisant l'appliet système disponible dans le panneau de contrôle ;
     - en éditant le script *vsvars32.bat* localisé dans *C:\Program Files\Microsoft Visual Studio 8\Common7\Tools\vsvars32.bat*

Ces variables doivent avoir les valeurs assignées suivantes :
::
    
    INCLUDE=C:\\Program Files\\Microsoft Visual Studio 8\\VC\\Include;
        C:\\Program Files\\Microsoft Platform SDK\\Include;
        C:\\Program Files\\Microsoft Platform SDK\\Include\\mfc;
        C:\\Program Files\\Microsoft Platform SDK\\Include\\atl;%INCLUDE%

    LIB=C:\\Program Files\\Microsoft Visual Studio 8\\VC\\Lib;
        C:\\Program Files\\Microsoft Visual Studio 8\\SDK\\v2.0\\lib;
        C:\\Program Files\\Microsoft Platform SDK\\lib;%LIB%

.. note::
    Si vous avez édité les variables système *LIB* et *INCLUDE* en utilisant 
    l'applet système, chaque console (cmd.exe) sera proprement définie. Mais si 
    vous les avez édité par le script *vsvars32.bat*, vous devrez lancé ce script 
    avant chaque compilation.</note>

* Patchez l'en-tête *atlwin.h* : à la ligne 1725 ajoutez la déclaration 
  *int i;* afin que cela ressemble à ceci :

::
    
    BOOL SetChainEntry(DWORD dwChainID, CMessageMap* pObject, DWORD dwMsgMapID = 0)
    {
        int i;
        // first search for an existing entry
    
        for(i = 0; i < m_aChainEntry.GetSize(); i++)
    
* Patchez l'en-tête *atlbase.h* : à la ligne 287, commentez les fonctions 
  *AllocStdCallThunk?* et *FreeStdCallThunk?* et ajoutez les macros de remplacement :
  ::
    
    /***************************************************
    PVOID __stdcall __AllocStdCallThunk(VOID);
    VOID __stdcall __FreeStdCallThunk(PVOID);
    
    #define AllocStdCallThunk() __AllocStdCallThunk()
    #define FreeStdCallThunk(p) __FreeStdCallThunk(p)
    
    #pragma comment(lib, "atlthunk.lib")
    ***************************************************/
    
    /* NEW MACROS */
    #define AllocStdCallThunk() HeapAlloc(GetProcessHeap(),0,sizeof(_stdcallthunk))
    #define FreeStdCallThunk(p) HeapFree(GetProcessHeap(), 0, p)


* Compilez GDAL :

  * Ouvrez une console Windows (Démarrez -> Éxécutez -> cmd.exe -> OK)
  * si vous avez édité le script *vsvars32.bat*, vous devez le lancer en 
    utilisant le chemin complet : ``C:\> "C:\\Program Files\\Microsoft Visual Studio 8\\Common7\\Tools\\vsvars32.bat"``

* Définir l'environnement pour utiliser les outiles Microsoft Visual Studio 2005 x86 :

  * Allez dans le répertorie racine des sources de GDAL, par exemple ``C:\> cd work\gdal``
  * Lancez ``nmake`` pour compiler ``C:\work\gdal> nmake /f makefile.vc``
  * Si aucune erreur n'est apparue, après quelques minutes vous devez voir les 
    bibliothèques GDAL dans *C:\work\gdal*.

Maintenant vous pouvez utiliser ces bibliothèques dans vos applications 
développées en utilisant Visual C++ 2005 Express Edition. 

Puis je compiler GDAL avec Cygwin ou MinGW ?
=============================================

GDAL peut être compilé avec `Cygwin <http://www.cygwin.com/>`_ en utilisant la 
méthodologie de compilation du style type-Unix. Il est également possible de 
compiler avec MinGW <http://www.mingw.org/>`_ et MSYS bien qu'il peut y avoir 
des complications. Ce qui suit devrait fonctionner :
::
    
    ./configure --prefix=$PATH_TO_MINGW_ROOT --host=mingw32 \
	--without-libtool --without-python $YOUR_CONFIG_OPTIONS

Utiliser des bibliothèques win32 externe sera souvent problématique avec l'un 
de ses environnements - cela nécessitera au moins un développement du fichier 
*GDALmake.opt*.

Comment compiler le bindings Python (NG) :
::
    
    cd swig\python
    python setup.py build -c mingw32
    cp build\lib.win32-2.5\* c:\python25\lib\site-packages\

(certains détails devront être ajusté).

Comment compiler le bindings Perl :

::
    
    cd swig\perl
    perl Makefile.PL
    make.bat
    make.bat install


(Il peut être nécessaire de `compiler Perl avec MinGW <http://www.adp-gmbh.ch/blog/2004/october/9.html>`_)

Si vous avez ``swig``, le bindings peut être régénéré dans le prompt de MSYS 
par la commande ``make generate``. 

Puis je compiler GDAL avec Borland C ou d'autres compilateurs C ?
==================================================================

Ce ne sont pas des compilateurs gérés pour GDAL ; Cependant GDAL est assez 
générique, si vous êtes prêt à prendre en charge la tache de compiler un 
*makefile* approprié ou un ficher de projet cela doit être possible. vous 
trouverez la plupart des problèmes de compatibilité dans le fichier 
`gdal/port/cpl_port.h <http://www.gdal.org/cpl__port_8h.html>`_ et vous devrez 
préparer un fichier 
`gdal/port/cpl_config.h <http://www.gdal.org/cpl__config_8h-source.html>`_ 
approprié à votre plateforme. Utiliser le fichier 
`cpl_config.h.vc <http://trac.osgeo.org/gdal/browser/trunk/gdal/port/cpl_config.h.vc>`_ 
comme guide peut être utile.

Pourquoi Visual C++ 8.0 plante avec une erreur C2894 dans wspiapi.h lors de la compilation de GDAL ...
========================================================================================================

Voici le message d'erreur complet de ce problème :

::
    
    C:\Program Files\Microsoft Visual Studio 8\VC\PlatformSDK\include\wspiapi.h(44) : 
    error C2894: templates cannot be declared to have 'C' linkage

C'est un `bug connus <http://curl.haxx.se/mail/tracker-2007-11/0027.html>`_ dans 
l'en-tête *wspiapi.h*. Une solution possible est de patcher manuellement le 
fichier *curl.h* en replaçant les lignes 153 - 154 :

::
    
    #include <winsock2.h>
    #include <ws2tcpip.h>

par les lignes suivantes :

::
    
    #ifdef __cplusplus
    }
    #endif
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #ifdef __cplusplus
    extern "C" {
    #endif

Ce problème arrive avec `libcurl <http://curl.haxx.se/libcurl/>`_ < 7.17.1. 
peut être qu'une version plus récente de ``libcurl`` inclura ce correctif.

Comment puis je ajouter des LDFLAGS particulier avec GDAL < 1.5 ?
===================================================================

Exportez la variable *LNK_FLAGS* avec votre contenu *LDFLAGS* habituel :
::
    
    export LNK_FLAGS=-Wl,-rpath=/foo/lib -l/foo/lib

J'ai des soucis lors de la compilation avec des bibliothèques externes, que puis je faire ?
============================================================================================

Il y a des astuces et suggestions pour la compilation de GDAL pour différentes 
gestions des bibliothèques externes dans le sujet `Astuces <http://trac.osgeo.org/gdal/wiki/BuildHints>`_.


.. yjacolin at free.fr, Yves Jacolin - 2008/08/23 10:57