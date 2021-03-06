// Evenement lancé quand le JSON est récupéré
let JSONRetrievedEvent = new Event('JSONRetrieved');
let EHPADsRetrievedEvent = new Event('EHPADsRetrieved')

// Tableau contenant tous les arrondissements
let arrondissements;

// les EHPADs
let EHPADs;

// Le div où est mise la carte
let element;

// La carte
let map;

window.addEventListener("load", init);
document.addEventListener("JSONRetrieved", displayArrondissements);
document.addEventListener("EHPADsRetrieved", displayEHPADs)

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
    map.setView(target, 12);
    // map.setView(target, 18);

    // On place un marqueur sur la carte sur les Mines
    L.marker(target).addTo(map);

    getArrondissements();
    getEHPADs();

}

/* Parses the JSON file
 * Fires a JSONRetrievedEvent when ready
 */
function getArrondissements() {
    console.log("Loading JSON...");

    jQuery.getJSON('https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/essais/arrondissements/arrondissements.json',
        function(data) {
            // if the request succeeds
            console.log("Loaded");
            arrondissements = data;
            document.dispatchEvent(JSONRetrievedEvent);
        }
    );
}


/* Displays the arrondissements on the map
 * Fired when the JSONRetrievedEvent is called
 */
function displayArrondissements() {
    console.log("Displaying arrondissements...");

    for(let arrondissement of arrondissements) {
        let data0 = arrondissement['fields']['geom'];
        L.geoJSON(data0, {color: 'red'}).addTo(map);
    }

    console.log("Displayed");
}

function getEHPADs() {
    jQuery.getJSON('https://opendata.paris.fr/api/records/1.0/search/?dataset=liste-des-ehpad&q=&rows=66&facet=nom_de_l_ehpad&facet=ville&facet=coordonnees',
        function(data) {
            // if the request succeeds
            console.log("Loaded EHPADs");
            EHPADs = data;
            document.dispatchEvent(EHPADsRetrievedEvent);
        }
    );
}

function displayEHPADs() {
    let list_ephads = EHPADs['records'];

    for(let EHPAD of list_ephads) {
        let data0 = EHPAD['geometry'];
        L.geoJSON(data0, 
                  {'pointToLayer' : (feature, latLng) => {

                  return new L.circleMarker(latLng, {radius : 5, label : 'EE'})}
                }).bindTooltip(String('EPHAD')).openTooltip().addTo(map);
    }
}