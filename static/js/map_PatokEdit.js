console.log("JS masok")

const HGU = "/map/api/v1/hgu/"
const Patok = "/map/api/v1/patok/"
const Bridge = "/map/api/v1/jembatan/"
// const Road = "/map/api/v1/jangkos/"

let dataBlock = [];
let dataHGU = [];

var geojsonMarkerOptions = {
    radius: 3,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 1
};
var geojsonMarkerOptionss = {
    radius: 3,
    fillColor: "#ffffff",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 1
};

async function fetchData() {
    try {
        // Fetch data
        const responseHGU = await fetch(HGU);
        var dataHGU = await responseHGU.json();
        console.log("Data from HGU endpoint:", dataHGU);

        const responsePatok = await fetch(Patok);
        var dataPatok = await responsePatok.json();
        console.log("Data from Block endpoint:", dataPatok);

        const responseBridge = await fetch(Bridge);
        var dataBridge = await responseBridge.json();
        console.log("Data from Block endpoint:", dataBridge);

        // adding geojson Layer into leaflet
        L.geoJSON(dataHGU, {
            style: {
                color: '#ff4122',
                fillRule: 'evenodd',
                bubblingMouseEvents: false,
                weight: 3,
                fillOpacity: 0
            }
        }).addTo(map);

        L.geoJSON(dataPatok, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, geojsonMarkerOptions);
            }
        }).addTo(map); // TODO: make popup /w patok att

        L.geoJSON(dataBridge, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, geojsonMarkerOptionss);
            }
        }).addTo(map); // TODO: clustering point and popup /w att


        // Fit map bounds after adding layers
        map.fitBounds(dataHGU.getBounds(), { padding: [5, 5], maxZoom: 15 });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
// Call the function to fetch data
fetchData(); // TODO: make function that show load screen while fetching data

// Leaflet Map
var map = L.map('map').setView(
    [1.2098191417100188, 117.90810018140084],
    10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | <a href="https://www.linkedin.com/in/muh-adli/">Contributors</a>'
}).addTo(map);