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
* Plot : `data.plot` plote les formes géométriques stockées dedans, lorsqu'elles sont compatibles avec `shapely` (nécessite le module `descartes`)
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

  
Pour plus de détails, voir [ce document](https://automating-gis-processes.github.io/2016/Lesson2-geopandas-basics.html)

## Geocoding

Le geocoding est une technologie permettant de passer d'adresse à coordonnées (et vice-versa), grâce à une API tierce.
Pour faire un appel à une API, importer `from geopandas.tools import geocode` et utiliser la fonction : `geocode` en spécifiant une clé api.

A faire... (césar)