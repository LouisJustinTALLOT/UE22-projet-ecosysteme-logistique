// Evenement lancé quand le JSON est récupéré
let JSONRetrievedEvent1 = new Event("JSONRetrieved1");
let JSONRetrievedEvent2 = new Event("JSONRetrieved2");

// Tableau contenant des magasins
let magasins;
// Tableau contenant des restaurants
let restaurants;

// Le div où est mise la carte
let element;

// La carte
let map;

var greenIcon = new L.Icon({
    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var restaurantIcon = new L.Icon({
    iconUrl: "https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/img/restaurant-map-icon.png",
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
    iconSize: [41, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

var shopIcon = new L.Icon({
    iconUrl: "https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/img/shop-map-icon.png",
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
    iconSize: [41, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

class DataSource {
    constructor(name, url, icon) {
        this.name = name;
        this.source_url = url;
        this.icon = icon;
    }
}

function get_and_display(DataSourceObject) {
    let current_name = DataSourceObject.name
    console.log("Loading JSON..." + DataSourceObject.name);
    let url = DataSourceObject.source_url;
    console.log(url);

    jQuery.getJSON(url,
        function (data) {
            // if the request succeeds
            console.log("Loaded " + current_name);

            console.log("Displaying " + current_name);

            let markers = L.markerClusterGroup();

            for (let data_unit of data["features"]) {
                let data0 = data_unit["geometry"];
                let title = data_unit["properties"]["name"] + ", " + data_unit["properties"]["type"];

                let marker = L.marker(
                    new L.LatLng(data0["coordinates"][1], data0["coordinates"][0]),
                    {
                        title: title,
                        icon: DataSourceObject.icon
                    }
                );
                marker.bindPopup(title);
                markers.addLayer(marker);
            }
            map.addLayer(markers);

            console.log("Displayed");
        }
    );


}

window.addEventListener("load", init);

/* Fonction d'initialisation.
 * En particulier, créé la carte à l'aide de  Leaflet
 */
function init() {
    // Où veut-on afficher la carte ?
    element = document.getElementById("osm-map");

    // Hauteur
    element.style = "height: 100%;";

    // Par Leaflet, on crée une "Carte Leaflet" sur l'élément où l'on veut afficher la carte
    map = L.map(element);

    // Tile Layer (surcouche) d'OSM (Open Street Map) : c'est de là que l'on récupère nos données
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution:
            "&copy; <a href=\"http://osm.org/copyright\" target=\"_blank\">OpenStreetMap</a> contributors"
    }).addTo(map);

    // On crée la target (les Mines)
    let target = L.latLng("48.844952", "2.339193");

    // On définit la vue de la carte (centrée sur les Mines, avec un zoom de 12)
    map.setView(target, 12);

    let restau_points = new DataSource(
        "Restaurants",
        "https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/tests/donnees/paris_3e_arrondissement_restaurant_2021-03-06.geojson",
        restaurantIcon,
        "restaurants"
    );

    let shop_points = new DataSource(
        "Magasins",
        "https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/tests/donnees/paris_3e_arrondissement_shop_craft_office_2021-03-06.geojson",
        shopIcon,
        "magasins"
    );

    get_and_display(restau_points);
    get_and_display(shop_points);
function toggle_display_data(data_source) {
    let checkbox = document.getElementById(data_source.id_name);

    if (checkbox.checked) {
        // on montre le layer correspondant

    } else {
        // on cache le layer correspondant
    }
}