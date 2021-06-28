Mines ParisTech - PSL
=====================

UE22 - Projet d'informatique - Ecosystème Logistique
----------------------------------------------------

Judith Bellon, Gabrielle Vernet, César Almecija, Louis-Justin Tallot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation
^^^^^^^^^^^^^

La documentation du projet est disponible à cette adresse :

`https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique <https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique>`__

Dépendances
^^^^^^^^^^^

Ce projet dépend des technologies et ressources suivantes :

-  Langages :
-  ``HTML 5``, ``CSS 3``, et ``Javascript``
-  ``Python``
-  ``C++`` compilé avec ``g++``

-  Formats de fichiers :
-  ```JSON`` <https://fr.wikipedia.org/wiki/JavaScript_Object_Notation>`__
   majoritairement
-  ```GEOJSON`` <https://fr.wikipedia.org/wiki/GeoJSON>`__ également,
   parfois plus adapté
-  ```CSV`` <https://fr.wikipedia.org/wiki/Comma-separated_values>`__
   pour explorer les données de manière plus convéniente avec Excel

-  Logiciels :
-  `Google Earth <https://www.google.fr/intl/fr/earth/>`__ pour explorer
   le terrain de l'Île-de-France et faire des choix géographiques
-  `QGIS <https://www.qgis.org/fr/site/>`__ pour construire les
   shapefiles à partir des bases de données géographiques

-  Ressources, plugins, packages :
-  ```OpenStreetMap`` <https://www.openstreetmap.org>`__ pour les fonds
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
   -  `Base
      IRIS <https://data.iledefrance.fr/explore/dataset/iris/information/>`__
      pour les contours de l'Île-de-France

-  `Base
   APUR <https://www.data.gouv.fr/fr/datasets/apur-hydrographie-surfacique-ile-de-france/>`__,
   hydrographie surfacique de l'Île-de-France

-  Les plugins Javascript :

   -  ```Leaflet`` <https://leafletjs.com/>`__ pour insérer des cartes
      OSM dans les pages web
   -  le projet
      ```Leaflet/Leaflet.markercluster`` <https://github.com/Leaflet/Leaflet.markercluster>`__
      pour regrouper les points et accélèrer l'affichage
   -  le projet
      ```pointhi/leaflet-color-markers`` <https://github.com/pointhi/leaflet-color-markers>`__
      pour des marqueurs de couleurs variées

-  Les packages Python :

   -  ```GeoPandas`` <https://geopandas.org/>`__ pour analyser et
      traiter les données géographiques
   -  ```Folium`` <https://python-visualization.github.io/folium/>`__
      pour générer des cartes et fichiers ``HTML``
   -  ```json`` <https://docs.python.org/fr/3/library/json.html>`__ pour
      traiter des fichiers ``JSON``
   -  ```ijson`` <https://pypi.org/project/ijson/>`__ pour traiter de
      manière itérative de lourds fichiers ``JSON``
   -  ```time`` <https://docs.python.org/fr/3/library/time.html>`__ pour
      mesurer le temps de traitement
   -  ```matplotlib`` <https://matplotlib.org>`__ pour analyser les
      données issues des bases ainsi que visualiser le résultat du
      clustering
   -  ```Jupyter`` <https://jupyter.org/>`__ pour développer de manière
      plus rapide (supporte même ``Folium``)
   -  ```PyQt5`` <https://www.riverbankcomputing.com/software/pyqt/>`__
      pour réaliser l'interface homme-machine
   -  ```QtWebEngine`` <https://wiki.qt.io/QtWebEngine>`__ pour afficher
      les fichiers ``HTML`` générés par ``Folium`` dans l'interface
      ``PyQt``
   -  ```Cython`` <https://cython.org/>`__ pour compiler certains de nos
      modules et accélérer notre code

-  Les librairies ``C++`` :

   -  ``iostream`` pour les entrées/sorties
   -  ``fstream`` pour lire/écrire les fichiers
   -  ``string`` pour manipuler les chaînes de caractères
   -  ``chrono`` pour mesurer le temps d'exécution des différentes
      parties du programme


