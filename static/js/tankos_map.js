console.log("JS masok")

const HGU = "/map/api/v1/hgu/"
const Dump = "/map/api/v1/block/"

let dataHgu = [];
let dataDump = [];

async function fetchData() {
    try {
        // Fetch data from HGU endpoint
        const responseHGU = await fetch(HGU);
        var dataHGU = await responseHGU.json();
        console.log("Data from HGU endpoint:", dataHGU);
    
        // Fetch data from Dump endpoint
        const responseDump = await fetch(Dump);
        var dataDump = await responseDump.json();
        console.log("Data from Dump endpoint:", dataDump);
        
        // adding geojson Layer into leaflet
        L.geoJSON(dataDump, {
            style: {
                color: '#C1F2B0', // outline color
                weight: 1,
                opacity: 1,
                fillColor: '#C1F2B0',
                fillOpacity: 0
            }
        }).addTo(map);
        L.geoJSON(dataHGU, {
            style: {
                color: '#ff4122',
                fillRule: 'evenodd',
                bubblingMouseEvents: false,
                weight: 3,
                fillOpacity: 0
            }
        }).addTo(map);
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