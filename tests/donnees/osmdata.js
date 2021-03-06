// Evenement lancé quand le JSON est récupéré
let JSONRetrievedEvent = new Event('JSONRetrieved');

// Tableau contenant des magasins
let osmdata;

// Le div où est mise la carte
let element;

// La carte
let map;

window.addEventListener("load", init);
document.addEventListener("JSONRetrieved", displayMagasins);


/*
* Fonction d'initialisation.
* En particulier, créé la carte à l'aide de Leaflet
*/
function init() {
    // Où veut-on afficher la carte ?
    element = document.getElementById("osm-map");

    // Hauteur
    element.style = "height: 100%;";

    // Par Leaflet, on créé une "Carte Leaflet" sur l'élément où l'on veut afficher la carte
    map = L.map(element);

    // Tile Layer (surcouche) d'OSM (Open Street Map) : c'est de là que l'on récupère nos données
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    }).addTo(map);


    getMagasins();
}




/**
 * Parses the JSON file
 * Fires a JSONRetrievedEvent when ready
 */
function getMagasins() {
    console.log("Loading JSON...");

    jQuery.getJSON('https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/tests/donnees/paris_3e_arrondissement_shop_craft_office_2021-03-06.geojson',
        function(data) {
            // if the request succeeds
            console.log("Loaded");
            osmdata = data;
            document.dispatchEvent(JSONRetrievedEvent);
        }
    );
}




/**
 * Displays the arrondissements on the map
 * Fired when the JSONRetrievedEvent is called
 */
function displayMagasins() {
    console.log("Displaying magasins...");

    for(let mag of osmdata['features']) {
        let data0 = mag['properties']['geometry'];
        L.geoJSON(data0, {color: 'red'}).addTo(map);
    }

    console.log("Displayed");
}