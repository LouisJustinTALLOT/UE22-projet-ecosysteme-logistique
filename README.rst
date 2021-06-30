.. Mines ParisTech - PSL
.. =====================

.. UE22 - Projet d'informatique - Ecosystème Logistique
.. ----------------------------------------------------

.. Judith Bellon, Gabrielle Vernet, César Almecija, Louis-Justin Tallot
.. ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. Documentation
.. ^^^^^^^^^^^^^

.. La documentation du projet est disponible à cette adresse :

.. `https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique <https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique>`__

Dépendances
^^^^^^^^^^^^^

Ce projet dépend des technologies et ressources suivantes :

-  Langages :

   -  ``HTML 5``, ``CSS 3``, et ``Javascript``
   -  ``Python``
   -  ``C++`` compilé avec ``g++``

-  Formats de fichiers :

   -  `JSON <https://fr.wikipedia.org/wiki/JavaScript_Object_Notation>`__
      majoritairement
   -  `GEOJSON <https://fr.wikipedia.org/wiki/GeoJSON>`__ également,
      parfois plus adapté
   -  `CSV <https://fr.wikipedia.org/wiki/Comma-separated_values>`__
      pour explorer les données de manière plus convéniente avec Excel

-  Logiciels :

   -  `Google Earth <https://www.google.fr/intl/fr/earth/>`__ pour explorer
      le terrain de l'Île-de-France et faire des choix géographiques
   -  `QGIS <https://www.qgis.org/fr/site/>`__ pour construire les
      shapefiles à partir des bases de données géographiques

-  Ressources, plugins, packages :

   -  `OpenStreetMap <https://www.openstreetmap.org>`__ pour les fonds
      de carte
   -  `Base OpenData Île de France <https://data.iledefrance.fr/>`__ et
      notamment les bases de données suivantes :
   -  `Base Sirene des entreprises et de leurs
      établissements <https://data.iledefrance.fr/explore/dataset/base-sirene>`__
   -  `BAN - Base Adresse Nationale -
      Paris <https://data.iledefrance.fr/explore/dataset/base-adresse-75>`__
   -  `BAN - Base Adresse Nationale -
      Hauts-de-Seine <https://data.iledefrance.fr/explore/dataset/base-adresse-92>`__
   -  `BAN - Base Adresse Nationale -
      Val-de-Marne <https://data.iledefrance.fr/explore/dataset/base-adresse-94>`__
   -  `BAN - Base Adresse Nationale -
      Val-de-Marne <https://data.iledefrance.fr/explore/dataset/base-adresse-94>`__
   -  `BAN - Base Adresse Nationale -
      Seine-Saint-Denis <https://data.iledefrance.fr/explore/dataset/base-adresse-93>`__
   -  `Base IRIS <https://data.iledefrance.fr/explore/dataset/iris/information/>`__
      pour les contours de l'Île-de-France
   -  `Base APUR <https://www.data.gouv.fr/fr/datasets/apur-hydrographie-surfacique-ile-de-france/>`__,
      hydrographie surfacique de l'Île-de-France

-  Les plugins Javascript :

   -  `Leaflet <https://leafletjs.com/>`__ pour insérer des cartes
      OSM dans les pages web
   -  le projet
      `Leaflet/Leaflet.markercluster <https://github.com/Leaflet/Leaflet.markercluster>`__
      pour regrouper les points et accélèrer l'affichage
   -  le projet
      `pointhi/leaflet-color-markers <https://github.com/pointhi/leaflet-color-markers>`__
      pour des marqueurs de couleurs variées

-  Les packages Python :

   -  `GeoPandas <https://geopandas.org/>`__ pour analyser et
      traiter les données géographiques
   -  `Folium <https://python-visualization.github.io/folium/>`__
      pour générer des cartes et fichiers ``HTML``
   -  `json <https://docs.python.org/fr/3/library/json.html>`__ pour
      traiter des fichiers ``JSON``
   -  `ijson <https://pypi.org/project/ijson/>`__ pour traiter de
      manière itérative de lourds fichiers ``JSON``
   -  `time <https://docs.python.org/fr/3/library/time.html>`__ pour
      mesurer le temps de traitement
   -  `matplotlib <https://matplotlib.org>`__ pour analyser les
      données issues des bases ainsi que visualiser le résultat du
      clustering
   -  `Jupyter <https://jupyter.org/>`__ pour développer de manière
      plus rapide (supporte même ``Folium``)
   -  `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/>`__
      pour réaliser l'interface homme-machine
   -  `QtWebEngine <https://wiki.qt.io/QtWebEngine>`__ pour afficher
      les fichiers ``HTML`` générés par ``Folium`` dans l'interface
      ``PyQt``
   -  `Cython <https://cython.org/>`__ pour compiler certains de nos
      modules et accélérer notre code

-  Les librairies ``C++`` :

   -  ``iostream`` pour les entrées/sorties
   -  ``fstream`` pour lire/écrire les fichiers
   -  ``string`` pour manipuler les chaînes de caractères
   -  ``chrono`` pour mesurer le temps d'exécution des différentes
      parties du programme

Contribuer au projet
^^^^^^^^^^^^^^^^^^^^^^

Les contributions sont bienvenues !

Pour cela, il vous faudra possèder sur votre ordinateur :

* Le système de gestion de version `Git <https://git-scm.com/>`_ (par exemple en installant `Git-Bash <https://gitforwindows.org/>`_ sur Windows)
* Un éditeur de texte comme `Sublime Text <https://gitforwindows.org/>`_ ou `Visual Studio Code <https://code.visualstudio.com/>`_
* Python, distribué sous `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ ou `Anaconda <https://www.anaconda.com/>`_ (plus lourd)

Puis vous devrez :code:`clone` ce répo Github : pour cela, ouvrez un shell
(invite de commande) dans le dossier où vous voudrez ensuite retrouver le projet.
Puis, tapez :code:`git clone https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique.git`
et faite Entrer. Git va télécharger le répo et son historique dans le dossier. Vous pouvez
changer le nom du dossier en entrant **à la place** :code:`git clone https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique.git <nom de dossier choisi par vous>`.
Une fois cela effectué, vous êtes presque prêt à commencer à contribuer !


Il reste une dernière étape, qui est d'installer les dépendances du projet.
Pour cela, dans le shell, placez-vous à la racine du dossier avec la commande :code:`cd`
et exécutez la commande : :code:`conda env create -f environment.yml`.
Conda va installer toute les dépendances du projet.

Il ne vous reste plus qu'à faire :code:`conda activate ecosysteme_logistique` quand vous
travaillez sur le projet !

Pour proposer vos changements, il faut que vous commitiez vos changements
puis que vous les publiez en faisant :code:`git push` et en suivant les instructions.
(Normalement, VS Code guide l'utilisateur). Il faudra *forker* le répo puis
*push* vos changements sur votre branche, et enfin ouvrir une *pull request*
pour que nous puissions revoir vos changements et les intégrer au projet.

Signaler un bug
^^^^^^^^^^^^^^^^^

Si vous pensez avoir trouvé un bug ou avez une question sur le projet,
ouvrez une *issue* Github (par exemple en cliquant ici : 
`nouvelle issue <https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/issues/new>`_).

