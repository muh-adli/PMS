console.log("JS masok")

const HGU = "/map/api/v1/hgu/"
const Block = "/map/api/v1/block/"
const Jangkos = "/map/api/v1/jangkos/"

let dataBlock = [];
let dataHGU = [];

async function fetchData() {
    try {
        // Fetch data from HGU endpoint
        const responseHGU = await fetch(HGU);
        var dataHGU = await responseHGU.json();
        console.log("Data from HGU endpoint:", dataHGU);
    
        // Fetch data from Block endpoint
        const responseBlock = await fetch(Block);
        var dataBlock = await responseBlock.json();
        console.log("Data from Block endpoint:", dataBlock);
    
        L.geoJSON(dataBlock, {
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
        // // Add polygons for HGU data
        // dataHGU.features.forEach(feature => {
        //     const coordinates = feature.geometry.coordinates[0][0]; // Accessing the coordinates
        //     const latLngs = coordinates.map(coord => [coord[1], coord[0]]); // Converting to Leaflet LatLng format
        //     L.polygon(latLngs).addTo(map); // You can use any property here
        // });

        // // Add polygons for Block data
        // dataBlock.forEach(block => {
        //     const coordinates = block.geometry.coordinates[0][0]; // Accessing the coordinates
        //     const latLngs = coordinates.map(coord => [coord[1], coord[0]]); // Converting to Leaflet LatLng format
        //     L.polygon(latLngs)
        //     .addTo(map)
        //     .bindPopup(block.name);
        // });
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
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);