// Evenement lancé quand le JSON est récupéré
let JSONRetrievedEvent = new Event('JSONRetrieved');

// Tableau contenant tous les arrondissements
let arrondissements;

// Le div où est mise la carte
let element;

// La carte
let map;

window.addEventListener("load", init);
document.addEventListener("JSONRetrieved", displayArrondissements);





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

    // On créé la target (les Mines)
    let target = L.latLng("48.844952", "2.339193");

    // On définit la vue de la carte (centrée sur les Mines, avec un zoom de 14)
    map.setView(target, 18);

    // On place un marqueur sur la carte sur les Mines
    L.marker(target).addTo(map);

    getArrondissements();
}




/**
 * Parses the JSON file
 * Fires a JSONRetrievedEvent when ready
 */
function getArrondissements() {
    jQuery.getJSON('arrondissements.json',
        function(data) {
            // if the request succeeds
            console.log("Request succeeded");
            arrondissements = data;
            document.dispatchEvent(JSONRetrievedEvent);
        }
    );
}




/**
 * Displays the arrondissements on the map
 * Fired when the JSONRetrievedEvent is called
 */
function displayArrondissements() {
    console.log("Displaying arrondissements");

    for(let arrondissement of arrondissements) {
        let data0 = arrondissement['fields']['geom'];
        console.log(data0);

        L.geoJSON(data0, {color: 'red'}).addTo(map);
    }
}