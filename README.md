# Mines ParisTech - PSL

## UE22 - Projet d'informatique - Ecosystème Logistique

### Judith Bellon, Gabrielle Vernet, César Almecija, Louis-Justin Tallot

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

* Ressources, plugins, packages :
  * [`OpenStreetMap`](https://www.openstreetmap.org) pour les fonds de carte
  * [Base OpenData Île de France](https://data.iledefrance.fr/) et notamment les bases de données suivantes :
    * [Base Sirene des entreprises et de leurs établissements](https://data.iledefrance.fr/explore/dataset/base-sirene)
    * [BAN - Base Adresse Nationale - Paris](https://data.iledefrance.fr/explore/dataset/base-adresse-75)
    * [BAN - Base Adresse Nationale - Hauts-de-Seine](https://data.iledefrance.fr/explore/dataset/base-adresse-92)
    * [BAN - Base Adresse Nationale - Val-de-Marne](https://data.iledefrance.fr/explore/dataset/base-adresse-94)
    * [BAN - Base Adresse Nationale - Val-de-Marne](https://data.iledefrance.fr/explore/dataset/base-adresse-94)
    * [BAN - Base Adresse Nationale - Seine-Saint-Denis](https://data.iledefrance.fr/explore/dataset/base-adresse-93)

  * Les plugins Javascript :
    * [`Leaflet`](https://leafletjs.com/) pour insérer des cartes OSM dans les pages web
    * le projet [`Leaflet/Leaflet.markercluster`](https://github.com/Leaflet/Leaflet.markercluster) pour regrouper les points et accélèrer l'affichage
    * le projet [`pointhi/leaflet-color-markers`](https://github.com/pointhi/leaflet-color-markers) pour des marqueurs de couleurs variées
  * Les packages Python :
    * [`GeoPandas`](https://geopandas.org/) pour analyser et traiter les données géographiques
    * [`Folium`](https://python-visualization.github.io/folium/) pour générer des cartes et fichiers `HTML`
    * [`json`](https://docs.python.org/fr/3/library/json.html) pour traiter des fichiers `JSON`
    * [`ijson`](https://pypi.org/project/ijson/) pour traiter de manière itérative de lourds fichiers `JSON`
    * [`time`](https://docs.python.org/fr/3/library/time.html) pour mesurer le temps de traitement
    * [`matplotlib`](https://matplotlib.org) pour analyser les données issues des bases ainsi que visualiser le résultat du clustering
    * [`Jupyter`](https://jupyter.org/) pour développer de manière plus rapide (supporte même `Folium`)
    * [`PyQt5`](https://www.riverbankcomputing.com/software/pyqt/) pour réaliser l'interface homme-machine
  * Les librairies `C++` :
    * `iostream` pour les entrées/sorties
    * `fstream` pour lire/écrire les fichiers
    * `string` pour manipuler les chaînes de caractères
    * `chrono` pour mesurer le temps d'exécution des différentes parties du programme
