# Mines ParisTech - PSL

## UE22 - Projet d'informatique - Ecosystème Logistique

### Judith Bellon, Gabrielle Vernet, César Almecija, Louis-Justin Tallot

#### Documentation

La documentation du projet est disponible à cette adresse : 

[https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique](https://louisjustintallot.github.io/UE22-projet-ecosysteme-logistique)

#### Dépendances

Ce projet dépend des technologies et ressources suivantes :

* Langages :
  * `HTML 5`, `CSS 3`, et `Javascript`
  * `Python`
  * `C++` compilé avec `g++`

* Formats de fichiers :
  * [`JSON`](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation) majoritairement
  * [`GEOJSON`](https://fr.wikipedia.org/wiki/GeoJSON) également, parfois plus adapté
  * [`CSV`](https://fr.wikipedia.org/wiki/Comma-separated_values) pour explorer les données de manière plus convéniente avec Excel

* Logiciels :
  * [Google Earth](https://www.google.fr/intl/fr/earth/) pour explorer le terrain de l'Île-de-France et faire des choix géographiques
  * [QGIS](https://www.qgis.org/fr/site/) pour construire les shapefiles à partir des bases de données géographiques

* Générateurs de documentation :
  * [Doxygen](https://www.doxygen.nl) pour les fichiers `C++`
  * [Sphinx](https://www.sphinx-doc.org) pour générer les pages web de la documentation ainsi que pour les fichiers `python`
  * [Breathe](https://breathe.readthedocs.io) pour incorporer la documentation générée par doxygen pour les fichiers `C++` dans les pages créées par Sphinx

* Ressources, plugins, packages :
  * [`OpenStreetMap`](https://www.openstreetmap.org) pour les fonds de carte
  * [Base OpenData Île de France](https://data.iledefrance.fr/) et notamment les bases de données suivantes :
    * [Base Sirene des entreprises et de leurs établissements](https://data.iledefrance.fr/explore/dataset/base-sirene)
    * [BAN - Base Adresse Nationale - Paris](https://data.iledefrance.fr/explore/dataset/base-adresse-75)
    * [BAN - Base Adresse Nationale - Hauts-de-Seine](https://data.iledefrance.fr/explore/dataset/base-adresse-92)
    * [BAN - Base Adresse Nationale - Val-de-Marne](https://data.iledefrance.fr/explore/dataset/base-adresse-94)
    * [BAN - Base Adresse Nationale - Val-de-Marne](https://data.iledefrance.fr/explore/dataset/base-adresse-94)
    * [BAN - Base Adresse Nationale - Seine-Saint-Denis](https://data.iledefrance.fr/explore/dataset/base-adresse-93)
    * [Base IRIS](https://data.iledefrance.fr/explore/dataset/iris/information/) pour les contours de l'Île-de-France
  * [Base APUR](https://www.data.gouv.fr/fr/datasets/apur-hydrographie-surfacique-ile-de-france/), hydrographie surfacique de l'Île-de-France

  * Les plugins Javascript :
    * [`Leaflet`](https://leafletjs.com/) pour insérer des cartes OSM dans les pages web
    * le projet [`Leaflet/Leaflet.markercluster`](https://github.com/Leaflet/Leaflet.markercluster) pour regrouper les points et accélèrer l'affichage
    * le projet [`pointhi/leaflet-color-markers`](https://github.com/pointhi/leaflet-color-markers) pour des marqueurs de couleurs variées
  
  * Les packages Python :
    * [`GeoPandas`](https://geopandas.org/) pour analyser et traiter les données géographiques
    * [`Folium`](https://python-visualization.github.io/folium/) pour générer des cartes et fichiers `HTML`
    * [`shapely`](https://shapely.readthedocs.io/en/stable/manual.html) pour manipuler les données géographiques sous forme de points et de polygones
    * [`json`](https://docs.python.org/fr/3/library/json.html) pour traiter des fichiers `JSON`
    * [`ijson`](https://pypi.org/project/ijson/) pour traiter de manière itérative de lourds fichiers `JSON`
    * [`time`](https://docs.python.org/fr/3/library/time.html) pour mesurer le temps de traitement
    * [`matplotlib`](https://matplotlib.org) pour analyser les données issues des bases ainsi que visualiser le résultat du clustering
    * [`Jupyter`](https://jupyter.org/) pour développer de manière plus rapide (supporte même `Folium`)
    * [`PyQt5`](https://www.riverbankcomputing.com/software/pyqt/) pour réaliser l'interface homme-machine
    * [`QtWebEngine`](https://wiki.qt.io/QtWebEngine) pour afficher les fichiers `HTML` générés par `Folium` dans l'interface `PyQt`
    * [`Cython`](https://cython.org/) pour compiler certains de nos modules et accélérer notre code
  * Les librairies `C++` :
    * `iostream` pour les entrées/sorties
    * `fstream` pour lire/écrire les fichiers
    * `string` pour manipuler les chaînes de caractères
    * `chrono` pour mesurer le temps d'exécution des différentes parties du programme

#### Contribuer au projet

Les contributions sont bienvenues !

Pour cela, il vous faudra possèder sur votre ordinateur :

* Le système de gestion de version [Git](https://git-scm.com/) (par exemple en installant [Git-Bash](https://gitforwindows.org/) sur Windows)
* Un éditeur de texte comme [Sublime Text](https://gitforwindows.org/) ou [Visual Studio Code](https://code.visualstudio.com/)
* Python, distribué sous [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/) (plus lourd)

Puis vous devrez `clone` ce répo Github : pour cela, ouvrez un shell
(invite de commande) dans le dossier où vous voudrez ensuite retrouver le projet.
Puis, tapez `git clone https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique.git`
et faite Entrer. Git va télécharger le répo et son historique dans le dossier. Vous pouvez
changer le nom du dossier en entrant **à la place** `git clone https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique.git <nom de dossier choisi par vous>`.
Une fois cela effectué, vous êtes presque prêt à commencer à contribuer !


Il reste une dernière étape, qui est d'installer les dépendances du projet.
Pour cela, dans le shell, placez-vous à la racine du dossier avec la commande `cd`
et exécutez la commande : `conda env create -f environment.yml`.
Conda va installer toute les dépendances du projet.

Il ne vous reste plus qu'à faire `conda activate ecosysteme_logistique` quand vous
travaillez sur le projet !

#### Signaler un bug

Si vous pensez avoir trouvé un bug ou avez une question sur le projet,
ouvrez une *issue* Github (par exemple en cliquant ici : 
[nouvelle issue](https://github.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/issues/new)).

