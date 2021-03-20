# Fiche : GIS en python

## Module `shapely`

**Fonction** : librairie pour des formes géométriques

**Installation** : `conda install shapely`

**Comment importer (en général)** : faire `from shapely.geometry import Point, LineString, Polygon`

**Classes principales** :
* `Point` : représente un point géographique
* `LineString` : représente une ligne brisée (*ie* contient plusieurs points)
* `Polygon` : représente un polygone (avec un extérieur et intérieur pour autoriser des aires négatives)

Et leurs version "multi", où un objet `MultiPoint`, `MultiLineString` et `MultiPolygon` représentent une collection de tels objets.

Il existe des opérations sur ces objets (aire, centre de masse, etc.)

**Opérations géométriques** :
* Point (ou ligne ou polygone) dans un polygone : au choix, `polygon.contains(point)` ou `point.within(polygon)`. 
* Intersection / contact : le contact est un cas particulier d'intersection (où les points commus doivent nécessairement être sur la frontière). Utiliser les méthodes `intersects` et `touches`

Pour plus de détails, voir [ce document](https://automating-gis-processes.github.io/2016/Lesson1-Geometric-Objects.html)

## Module `geopandas`

**Fonction** : surcouche de `pandas` pour les fichiers géographiques (GIS, Geographic Information System).
Permet par exemple d'ouvrir les `shapefile`, standard pour ce les fichiers GIS.

**Installation** : `conda install geopandas`

**Comment importer** : faire `import geopandas as gpd`

**Fonctions principales** :
* Ouvertures de fichiers comme avec `pandas` (ex : `gpd.read_file(chemin)`)
* Ecriture de fichiers comme avec `pandas` (ex : `gpd.to_file(chemin)`)
* Sélection comme avec `pandas` :
  * `dataframe.loc(...)` pour les accès (slices autorisés) et les écritures
  * `dataframe.iterrows()` pour itérer sur les numéros de ligne et leur contenu à la fois
  * `dataframe['nom_de_colonne'] = None` pour créer une nouvelle colonne
  * `dataframe['nom_de_colonne'].mean()` pour faire une opération numpy sur une colonne de données (ici, moyenne)
* Plot : `data.plot` plote les formes géométriques stockées dedans, lorsqu'elles sont compatibles avec `shapely` (nécessite le module `descartes`) (cf. section correspondante)
* Regroupement : `dataframe.groupby('nom_de_colonne')` créé un objet semblable à un dictionnaire :
  * les clés sont les objets de la colonne sélectionnée par lesquels on regroupe les objets (par exemple, le nom de l'espèce marine)
  * les valeurs sont une `DataFrame` contenant les mêmes colonnes que la `DataFrame` originale, mais uniquement les lignes correspondant à la valeur par laquelle on regroupe
  
**Fonctions de join** :
Il existe plusieurs fonctionnalités selon ce qu'on entend par join, ou plus généralement les opérations ensemblistes :
* Table join (comme en SQL):
  * Pour l'utiliser : `dataframe1.merge(dataframe2, on='nom_de_colonne')`. 
  * Si les noms de colonnes sont différents, fournir les paramètres `left_on` et `right_on`.
* Overlay : fait des intersections spatiales entre plusieurs tables, ou plus généralement des opérations ensemblistes spatiales (union, différence, etc.) (ex : intersecte une `DataFrame` de polygones avec une autre)
* Join spatial : un peu plus subtil, fusionne des `GeoDataFrame` avec un critère particulier : `intersects`, `contains` et `within` (ex : fusionne les lignes où un point d'une table est dans un polygone d'une autre table) 

**Agrégation** :
Fonctionnalité permettant d'agréger (rassembler) des lignes d'une `DataFrame` avec un critère particulier (ex : la valeur d'une colonne)
Exemple d'utilisation : fusionner des zones géographiques par temps d'itinéraire vers une gare.
Utilisation : `dataframe.dissolve(by="colonne_par_laquelle_trier")`

**Applications d'opérateurs binaires**
Voir [ce document](https://automating-gis-processes.github.io/2016/Lesson4-reclassify.html#)

  
Pour plus de détails, voir [ce document](https://automating-gis-processes.github.io/2016/Lesson2-geopandas-basics.html)

## Affichage sur une carte

Il existe plein de modules permettant d'afficher sur une carte.

### Avec `geopandas` (ie `matplotlib`)

Ce sont des **cartes statiques**

On utilise `dataframe.plot()`.
* Retourne le plot correspondant (si on veut l'utiliser plus tard), utile pour :
* `ax=` pour indiquer si on veut superposer l'affichage sur un plot déjà existant (ex : routes sur une carte)
* Si une colonne est spécifiée (`column='ma_colonne'`), sépare la carte en classes d'équivalences en fonction de la valeur de la colonne, en fonction du schema spécifié
* Le schema c'est la façon avec laquelle le module créé les classes d'équivalences. Le paramètre `k` définit le nombre de classes d'équivalences à utiliser. Exemple de schéma = `scheme="quantiles"`. Le schema est coloré par une `cmap`.  
* Couleur :
  * soit `color='r'` : colore uniformément en rouge
  * soit `cmap="Reds"` : colore avec une "carte de couleurs" (ici rouge) reconnue par le module (utile si on a spécifié une colonne par exemple)
* La transparence : `alpha=0.9` par exemple (1 totalement opaque, 0 totalement transparent)
* `linewidth=` permet de définir l'épaisseur des lignes

`plt.tight_layout()` permet d'afficher plus sur la même fenêtre.

### Avec `bokeh`

Ce sont des **cartes dynamiques**

**Installation** : `conda install bokeh`

A faire (césar)

### Avec `leaflet` (ie `folium`)

C'est le module `folium` dans pyton qui fait le boulot.

**Installation** : `conda install folium`

* Créer une carte : folium.Map() avec les paramètres
  * `location=[lat,lon]` : position initiale de la carte
  *  `zoom_start=10` : zoom initial (plus c'est grand, plus c'est proche)
  * `control_scale=true` : affichage de l'échelle
  * `tiles` : indique quelle carte utiliser (ex : `tiles="OpenStreeMap")
  
Pour plus d'infos, voir [ce document](https://python-visualization.github.io/folium/quickstart.html)


## CRS (Coordinate Reference System)

C'est un attribut des `shapefile`, permettant de savoir quels systèmes de coordonnées ils utilisent.
* Pour connaître le CRS d'une table, faire `dataframe.crs`
* Pour changer le CRS d'une table, faire `dataframe.to_crs(crs=un_crs_donne, inplace=true)` (ou `inplace=false` si on veut pas de surplace)

## Geocoding

Le geocoding est une technologie permettant de passer d'adresse à coordonnées (et vice-versa), grâce à une API tierce.
Pour faire un appel à une API, importer `from geopandas.tools import geocode` et utiliser la fonction : `geocode` en spécifiant une clé api.

A faire... (césar)