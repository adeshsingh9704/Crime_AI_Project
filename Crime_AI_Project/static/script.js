let map;

let userMarker = null;

let hotspotLayer = null;

let userLocation = null;

let watchId = null;


// ----------------------------------------------------
// INITIALIZE MAP
// ----------------------------------------------------

function initializeMap() {

    map = L.map("map").setView(
        [28.6139, 77.2090],
        12
    );


    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);


    hotspotLayer = L.layerGroup().addTo(map);

    loadHotspots();
}


// ----------------------------------------------------
// LOAD HOTSPOTS
// ----------------------------------------------------

async function loadHotspots() {

    try {

        const response =
            await fetch("/api/hotspots");

        const data =
            await response.json();


        if (data.status !== "OK") {

            return;
        }


        hotspotLayer.clearLayers();


        data.hotspots.forEach(
            hotspot => {

                let radius = 250;

                if (
                    hotspot.risk_level === "High"
                ) {

                    radius = 500;

                } else if (
                    hotspot.risk_level === "Medium"
                ) {

                    radius = 350;
                }


                const circle =
                    L.circle(
                        [
                            hotspot.lat,
                            hotspot.lon
                        ],
                        {
                            radius: radius,

                            fillOpacity: 0.25,

                            color: "#dc2626"
                        }
                    );


                circle.bindPopup(
                    `
                    <b>Hotspot #${hotspot.id}</b><br>
                    Risk: ${hotspot.risk_level}<br>
                    Incidents: ${hotspot.incident_count}
                    `
                );


                circle.addTo(
                    hotspotLayer
                );


                L.marker([
                    hotspot.lat,
                    hotspot.lon
                ])
                .bindPopup(
                    `
                    <b>Hotspot #${hotspot.id}</b><br>
                    Risk: ${hotspot.risk_level}<br>
                    Incidents: ${hotspot.incident_count}
                    `
                )
                .addTo(hotspotLayer);

            }
        );


        renderHotspotList(
            data.hotspots
        );


    } catch (error) {

        console.error(
            "Hotspot error:",
            error
        );
    }
}


// ----------------------------------------------------
// HOTSPOT LIST
// ----------------------------------------------------

function renderHotspotList(
    hotspots
) {

    const container =
        document.getElementById(
            "hotspotList"
        );


    if (!hotspots.length) {

        container.innerHTML =
            "No hotspots detected.";

        return;
    }


    container.innerHTML = "";


    hotspots.forEach(
        hotspot => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "hotspot-item";


            item.innerHTML = `
                <div class="hotspot-title">
                    Hotspot #${hotspot.id}
                </div>

                <div>
                    Risk:
                    <b>${hotspot.risk_level}</b>
                </div>

                <div>
                    Incidents:
                    ${hotspot.incident_count}
                </div>

                <div>
                    Location:
                    ${hotspot.lat},
                    ${hotspot.lon}
                </div>
            `;


            container.appendChild(
                item
            );

        }
    );
}


// ----------------------------------------------------
// START LIVE GPS
// ----------------------------------------------------

function startTracking() {

    if (
        !navigator.geolocation
    ) {

        alert(
            "Geolocation is not supported."
        );

        return;
    }


    if (watchId !== null) {

        navigator.geolocation.clearWatch(
            watchId
        );
    }


    watchId =
        navigator.geolocation.watchPosition(

            position => {

                const lat =
                    position.coords.latitude;

                const lon =
                    position.coords.longitude;


                userLocation = {
                    lat: lat,
                    lon: lon
                };


                updateUserMarker(
                    lat,
                    lon
                );


                checkLocation(
                    lat,
                    lon
                );

            },

            error => {

                console.error(
                    error
                );

                document.getElementById(
                    "locationResult"
                ).innerText =
                    "Unable to access GPS location.";

            },

            {
                enableHighAccuracy: true,

                maximumAge: 5000,

                timeout: 10000
            }
        );
}


// ----------------------------------------------------
// USER MARKER
// ----------------------------------------------------

function updateUserMarker(
    lat,
    lon
) {

    if (userMarker) {

        userMarker.setLatLng([
            lat,
            lon
        ]);

    } else {

        userMarker =
            L.marker([
                lat,
                lon
            ]).addTo(map);

        userMarker.bindPopup(
            "Your current location"
        );

    }


    map.setView(
        [lat, lon],
        14
    );
}


// ----------------------------------------------------
// LOCATION CHECK
// ----------------------------------------------------

async function checkLocation(
    lat,
    lon
) {

    try {

        const response =
            await fetch(
                "/api/location",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        lat: lat,
                        lon: lon
                    })
                }
            );


        const data =
            await response.json();


        if (data.status !== "OK") {

            return;
        }


        document.getElementById(
            "currentRisk"
        ).innerText =
            data.risk_level;


        document.getElementById(
            "nearestDistance"
        ).innerText =
            data.nearest_distance_km !== null
                ? `${data.nearest_distance_km} km`
                : "-";


        document.getElementById(
            "locationResult"
        ).innerHTML = `

            <b>Current Location</b><br>

            Latitude:
            ${lat.toFixed(6)}<br>

            Longitude:
            ${lon.toFixed(6)}<br>

            Area:
            ${data.area}<br>

            Risk:
            <b>${data.risk_level}</b><br>

            Nearest hotspot:
            ${data.nearest_distance_km ?? "-"} km<br>

            Most common crime in nearby hotspot:
            ${data.possible_crime}

        `;


    } catch (error) {

        console.error(
            error
        );

    }
}


// ----------------------------------------------------
// PREDICTION
// ----------------------------------------------------

async function predictCurrentLocation() {

    if (!userLocation) {

        document.getElementById(
            "predictionResult"
        ).innerText =
            "Start live location first.";

        return;
    }


    try {

        const response =
            await fetch(
                "/api/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        userLocation
                    )
                }
            );


        const data =
            await response.json();


        let probabilityHTML = "";


        Object.entries(
            data.probabilities || {}
        ).forEach(
            ([crime, probability]) => {

                probabilityHTML +=
                    `
                    <div>
                        ${crime}:
                        ${probability}%
                    </div>
                    `;

            }
        );


        document.getElementById(
            "predictionResult"
        ).innerHTML = `

            <b>Predicted category:</b>
            ${data.prediction}

            <hr>

            ${probabilityHTML}

            <br>

            <small>
                ${data.note}
            </small>

        `;


    } catch (error) {

        document.getElementById(
            "predictionResult"
        ).innerText =
            "Prediction failed.";

    }
}


// ----------------------------------------------------
// STATISTICS
// ----------------------------------------------------

async function loadStatistics() {

    try {

        const response =
            await fetch(
                "/api/statistics"
            );


        const data =
            await response.json();


        document.getElementById(
            "totalIncidents"
        ).innerText =
            data.total_incidents;


        document.getElementById(
            "totalHotspots"
        ).innerText =
            data.total_hotspots;


        const container =
            document.getElementById(
                "crimeDistribution"
            );


        container.innerHTML = "";


        Object.entries(
            data.crime_types
        ).forEach(
            ([crime, count]) => {

                const row =
                    document.createElement(
                        "div"
                    );


                row.className =
                    "crime-row";


                row.innerHTML = `
                    <span>${crime}</span>
                    <strong>${count}</strong>
                `;


                container.appendChild(
                    row
                );

            }
        );


    } catch (error) {

        console.error(
            error
        );

    }
}


// ----------------------------------------------------
// IMAGE COMPARISON
// ----------------------------------------------------

async function scanImage() {

    const input =
        document.getElementById(
            "imageFile"
        );


    if (!input.files.length) {

        document.getElementById(
            "faceResult"
        ).innerText =
            "Please select an image.";

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        input.files[0]
    );


    try {

        const response =
            await fetch(
                "/scan",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        document.getElementById(
            "faceResult"
        ).innerHTML = `

            <b>${data.message || ""}</b>

            <br>

            ${
                data.reference_id
                    ? "Reference image: "
                      + data.reference_id
                    : ""
            }

            <br>

            ${
                data.similarity_score !== undefined
                    ? "Image difference score: "
                      + data.similarity_score
                    : ""
            }

        `;


    } catch (error) {

        document.getElementById(
            "faceResult"
        ).innerText =
            "Image comparison failed.";

    }
}


// ----------------------------------------------------
// LEGAL AI
// ----------------------------------------------------

async function getLegalHelp() {

    const text =
        document.getElementById(
            "caseText"
        ).value.trim();


    if (!text) {

        document.getElementById(
            "legalResult"
        ).innerText =
            "Please enter case details.";

        return;
    }


    try {

        const response =
            await fetch(
                "/api/legal",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        case: text
                    })
                }
            );


        const data =
            await response.json();


        document.getElementById(
            "legalResult"
        ).innerHTML = `

            <b>Similar lawyer record:</b>
            ${data.lawyer}

            <br>

            Fee:
            ₹${data.fee}

            <br>

            Historical dataset win rate:
            ${data.historical_win_rate}

            <br>

            Similarity:
            ${data.similarity}

            <br><br>

            <small>
                ${data.message}
            </small>

        `;


    } catch (error) {

        document.getElementById(
            "legalResult"
        ).innerText =
            "Legal search failed.";

    }
}


// ----------------------------------------------------
// AUTO REFRESH
// ----------------------------------------------------

setInterval(
    loadHotspots,
    10000
);


// ----------------------------------------------------
// START
// ----------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeMap();

        loadStatistics();

    }
);