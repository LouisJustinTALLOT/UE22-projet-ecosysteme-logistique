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

let res;

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
    constructor(name, url, icon, id_name) {
        this.name = name;
        this.source_url = url;
        this.icon = icon;
        this.id_name = id_name;
    }
}

function get_and_display(DataSourceObject) {
    // console.log(typeof (control_panel));

    let current_name = DataSourceObject.name;
    console.log("Loading JSON..." + DataSourceObject.name);
    let url = DataSourceObject.source_url;
    console.log(url);
    let res;

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
            // let overlay_map = {
            //     current_name: markers
            // }
            //L.control.layers(null, overlay_map).addTo(map);
            // control_panel.addOverlay(overlay_map, current_name);
            // console.log("Displayed");
            /*res = {
                "name": current_name, "markers": markers
            }
            console.log("ici")
            return res; */
        }
    )

    // setTimeout(() => { console.log("là"); return res; }, 400);
    // return res;

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
    //var grayscale = L.tileLayer(mapboxUrl, {id: 'MapID', tileSize: 512, zoomOffset: -1, attribution: mapboxAttribution}),
    //    streets   = L.tileLayer(mapboxUrl, {id: 'MapID', tileSize: 512, zoomOffset: -1, attribution: mapboxAttribution});
    /*
        var map = L.map('map', {
            center: [48.844952, 2.339193],
            zoom: 12,
            layers: [grayscale]
        }); */

    /* var baseMaps = {
         "Grayscale": grayscale,
         "Streets": streets
     }; */

    /*var overlayMaps = {
        "Cities": cities
    }; */
    //L.control.layers(baseMaps, overlayMaps).addTo(map);

    // Tile Layer (surcouche) d'OSM (Open Street Map) : c'est de là que l'on récupère nos données
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution:
            "&copy; <a href=\"http://osm.org/copyright\" target=\"_blank\">OpenStreetMap</a> contributors"
    }).addTo(map);

    // On crée la target (les Mines)
    let target = L.latLng("48.844952", "2.339193");

    // On définit la vue de la carte (centrée sur les Mines, avec un zoom de 12)
    map.setView(target, 12);
    var layer_control = new L.control.layers(null, null, { collapsed: false }).addTo(map);


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

    let list_data_sources = [restau_points, shop_points];
    let list_overlay_layers = [];
    let data_source;

    // for (data_source of list_data_sources) {
    //     let div_checkboxes = document.getElementById("checkboxes-data-selection");
    //     let new_input = document.createElement("input");
    //     new_input.type = "checkbox";
    //     new_input.id = data_source.id_name;
    //     new_input.name = data_source.name;
    //     new_input.onclick = toggle_display_data(data_source);
    //
    //     let new_label = document.createElement("label");
    //     //new_label.for = data_source.name;
    //     new_label.textContent = data_source.name;
    //
    //     div_checkboxes.append(new_input);
    //     div_checkboxes.append(new_label);
    // }

    // setTimeout(() => {
    get_and_display(restau_points);
    get_and_display(shop_points);
    // }, 200);

    /*
        for (data_source of list_data_sources) {
            new_overlay_layer = get_and_display(data_source);
            setTimeout(() => {
                console.log(new_overlay_layer);
    
                layer_control.addOverlay(new_overlay_layer.markers, new_overlay_layer.name);
            }, 500).then()      
        } */


}

function toggle_display_data(data_source) {
    let checkbox = document.getElementById(data_source.id_name);

    if (checkbox.checked) {
        // on montre le layer correspondant

    } else {
        // on cache le layer correspondant
    }
}