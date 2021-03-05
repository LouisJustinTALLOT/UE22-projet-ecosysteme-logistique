let JSONRetrievedEvent = new Event('JSONRetrieved');
let arrondissements;

window.addEventListener("load", init);

document.addEventListener("JSONRetrieved", displayArrondissements);

/*
* Fonction d'initialisation.
* En particulier, créé la carte à l'aide de Leaflet
*/
function init() {
    // Où veut-on afficher la carte ?
    let element = document.getElementById("osm-map");

    // Hauteur
    element.style = "height: 100%;";

    // Par Leaflet, on créé une "Carte Leaflet" sur l'élément où l'on veut afficher la carte
    let map = L.map(element);

    // Tile Layer (surcouche) d'OSM (Open Street Map) : c'est de là que l'on récupère nos données
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    }).addTo(map);

    // On créé la target (les Mines)
    let target = L.latLng("48.844952", "2.339193");

    // On définit la vue de la carte (centrée sur les Mines, avec un zoom de 14)
    map.setView(target, 18);

    // On place un marqueur sur la carte
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
 * TODO
 */
function displayArrondissements() {
    console.log("Displaying arrondissements");
    console.log(arrondissements);
}




    // jQuery.getJSON('https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/tests/arrondissements.json'
    // ).done(
    //     function (json) {
    //         console.log(typeof(json))
    //         console.log("here");
    //         // arrondissements =
    //         JSON.parse(json);
    //         console.log(arrondissements);
    //     }
    // )