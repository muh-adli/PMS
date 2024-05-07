console.log("JS masok")

const HGU = "/map/api/v1/hgu/"
const Planted = "/map/api/v1/planted/"

let dataPlanted = [];
let dataHGU = [];

async function fetchData() {
    try {
        // Fetch data
        const responseHGU = await fetch(HGU);
        var dataHGU = await responseHGU.json();
        console.log("Data from HGU endpoint:", dataHGU);

        const responsePlanted = await fetch(Planted);
        var dataPlanted = await responsePlanted.json();
        console.log("Data from Planted endpoint:", dataPlanted);

        // adding geojson Layer into leaflet
        L.geoJSON(dataHGU, {
            style: {
                color: '#ff4122',
                fillRule: 'evenodd',
                bubblingMouseEvents: false,
                weight: 5,
                fillOpacity: 0
            }
        }).addTo(map);

        L.geoJSON(dataPlanted).addTo(map);

        // Fit map bounds after adding layers
        map.fitBounds(L.geoJSON(dataHGU).getBounds(), { padding: [5, 5], maxZoom: 15 });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
// Call the function to fetch data
fetchData();

// Leaflet Map
var map = L.map('map').setView(
    [1.2098191417100188, 117.90810018140084],
    10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | <a href="https://www.linkedin.com/in/muh-adli/">Contributors</a>'
}).addTo(map);