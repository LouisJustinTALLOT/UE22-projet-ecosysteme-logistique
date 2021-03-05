// Where you want to render the map.
var element = document.getElementById("osm-map");

// Height has to be set. You can do this in CSS too.
element.style = "height: 100%;";

// Create Leaflet map on map element.
var map = L.map(element);

// Add OSM tile leayer to the Leaflet map.
L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
    attribution:
        '&copy; <a href="http://osm.org/copyright" target="_blank">OpenStreetMap</a> contributors',
}).addTo(map);

// Target's GPS coordinates.
var target = L.latLng("48.844952", "2.339193");

// Set map's center to target with zoom 14.
map.setView(target, 14);

// Place a marker on the same location.
L.marker(target).addTo(map);

// let arrondissements = JSON.parse();
var arrondissements;

// console.log(arrondissements);

jQuery.getJSON('https://raw.githubusercontent.com/LouisJustinTALLOT/UE22-projet-ecosysteme-logistique/main/tests/arrondissements.json',
    function (data) {
        console.log("ici");
        console.log(data);
        arrondissements = data;
    }
);


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
console.log("là");
console.log(arrondissements);