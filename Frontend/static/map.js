var map;
map = L.map("map").setView([41.850033, -87.6500523], 2);

let area = [];
let clicksCounter = 0;
let body = {
    searchTerm: "",
    fromTimeInterval: null,
    toTimeInterval: null,
    points: [],
};
//from cloud.maptiler.com
L.tileLayer(
    "https://api.maptiler.com/maps/toner/256/{z}/{x}/{y}.png?key=r11GGACGHOIGD74xtrUt", {
        attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    }
).addTo(map);

map.on("click", (e) => {
    area[clicksCounter] = [e.latlng.lat, e.latlng.lng];
    clicksCounter++;

    if (clicksCounter == 4) {
        var polygon = L.polygon(area, { color: "yellowgreen" }).addTo(map);
        body.points = area;
        clicksCounter = 0;
        document.getElementById("keyword").style.display = "block";

        document.getElementById("keyword").addEventListener("keydown", (e) => {
            if (e.key == "Enter") {
                var keyword = document.getElementById("keyword").value;
                body.searchTerm = keyword;
                document.getElementById("keyword").style.display = "none";
                document.getElementById("T1").style.display = "block";
            }
        });
        document.getElementById("T1").addEventListener("keydown", (e) => {
            if (e.key == "Enter") {
                var fromInterval = document.getElementById("T1").value;
                body.fromTimeInterval = fromInterval;
                document.getElementById("T1").style.display = "none";
                document.getElementById("T2").style.display = "block";
            }
        });
        document.getElementById("T2").addEventListener("keydown", (e) => {
            if (e.key == "Enter") {
                var toInterval = document.getElementById("T2").value;
                body.toTimeInterval = toInterval;
                document.getElementById("T2").style.display = "none";
                document.getElementById("insight").style.display = "block";
                document.getElementById('map').style.display = "none";
                document.getElementById('sen').style.display = "none";
                Plot();



                //console.log(body);
            }
        });


        //document.getElementById('map').style.display = "none";
    }
});



function Plot() {
    //lng and lat
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const response = xhttp.response;
        var values = JSON.parse(response)
        new Chart("PLOT", {
            type: "bar",
            data: {
                labels: values.xValues,
                datasets: [{
                    backgroundColor: "yellowgreen",
                    data: values.yValues
                }]
            },
            options: {
                legend: { display: false },
                title: {
                    display: true,
                    text: "Tweet Frequency Plot"
                }
            }
        })

    };
    xhttp.open("POST", "http://localhost:5000/plot", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhttp.send(
        "keyword=" +
        body["searchTerm"] +
        "&T1=" +
        body["fromTimeInterval"] +
        "&T2=" +
        body["toTimeInterval"] +
        "&lat1=" +
        body["points"][0][0] +
        "&lng1=" +
        body["points"][0][1] +
        "&lat2=" +
        body["points"][2][0] +
        "&lng2=" +
        body["points"][2][1]
    );
}

function Insight() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const xmlDoc = xhttp.response;
        var tweets = String(xmlDoc);
        document.getElementById("modal").innerHTML = tweets;
    };
    xhttp.open("POST", "http://localhost:5000/insights", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("keyword=" +
        body["searchTerm"] +
        "&T1=" +
        body["fromTimeInterval"] +
        "&T2=" +
        body["toTimeInterval"] +
        "&lat1=" +
        body["points"][0][0] +
        "&lng1=" +
        body["points"][0][1] +
        "&lat2=" +
        body["points"][1][0] +
        "&lng2=" +
        body["points"][1][1]
    );
}