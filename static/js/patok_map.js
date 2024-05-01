console.log("JS masok")

const HGU = "/map/api/v1/hgu/"
const Patok = "/map/api/v1/patok/"

let dataPatok = [];
let dataHGU = [];

function getColor(periode) {
    // Define colors based on 'periode'
    // Example: Assuming 'periode' can have values 'Q1', 'Q2', 'Q3', 'Q4', and null
    var colors = {
        'Q1': '#003f5c',
        'Q2': '#58508d',
        'Q3': '#bc5090',
        'Q4': '#ff6361',
        'null': '#ffa600' // Note: 'null' is a string here, not null
    };

    // Return color based on 'periode'
    return colors[periode] || '#808080'; // Return color or default if 'periode' not found
}

async function fetchData() {
    try {
        // Fetch data
        const responseHGU = await fetch(HGU);
        var dataHGU = await responseHGU.json();
        console.log("Data from HGU endpoint:", dataHGU);

        const responsePatok = await fetch(Patok);
        var dataPatok = await responsePatok.json();
        console.log("Data from Patok endpoint:", dataPatok);

        // adding geojson Layer into leaflet
        var hgu = L.geoJSON(dataHGU, {
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
                var circleMarker = L.circleMarker(latlng, {
                    radius: 4,
                    fillColor: getColor(feature.properties.periode),
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });

                // Bind a popup to the circle marker with multiple lines of content
                circleMarker.bindPopup(
                    "Patok: " + feature.properties.no_patok + "<br>" +
                    "Periode: " + feature.properties.periode + "<br>" +
                    '<a href="/dashboard/patok/table/' + feature.properties.objectid + '/" target="_blank">Edit</a>'
                );

                return circleMarker;
            }
        }).addTo(map);

        // Fit map bounds after adding layers
        map.fitBounds(hgu.getBounds(), { padding: [5, 5], maxZoom: 15 });

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