'use strict';

//Adds Google map to display panel using Google Maps API | ref: https://developers.google.com/maps/documentation/javascript/
function initMap() {
    //Create map object and specify the element in which to display it
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 53.3462763, lng: -6.2825708},
        zoom: 13
    });

    markers(map);
}

//Add marker for each station to Google map
function markers(map) {
    var xmlhttp = new XMLHttpRequest();
    var url_stations = "/static/data/station_data.json";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //Parse the JSON data to a JavaScript variable
            var parsedObj = JSON.parse(xmlhttp.responseText);
            //Function (defined below) to generate new page content from the parsed JSON data
            addMarkers(parsedObj, map);
        }
    }

    xmlhttp.open("GET", url_stations, true);
    xmlhttp.send();

    //Function to generate new page content from the daily JSON data
    function addMarkers(obj, map) {
        for (var i = 0; i < obj.length; i++) {
            var station = obj[i];
            //console.log(station.available_bikes);

            // Color marker (pin) according to availability
            var markColor = '#919191';
            if (station.available_bikes === 0) {
                markColor = '#919191';
            } else if (station.available_bikes < 5) {
                markColor = '#F74565';
            } else if (station.available_bikes < 10) {
                markColor =  '#fc6ae8';
            } else {
                markColor = '#6A6AFC';
            }

            // Create custom pin icon
            var pinIcon = new google.maps.MarkerImage(
                'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|' + markColor,
                null, /* size is determined at runtime */
                null, /* origin is 0,0 */
                null, /* anchor is bottom center of the scaled image */
                new google.maps.Size(21, 34)
            );

            // Create marker at station location
            var marker = new google.maps.Marker({
                position: station.position,
                size: 0,
                map: map,
                icon: {
                   path: google.maps.SymbolPath.CIRCLE,
                   fillColor: markColor,
                   strokeColor: '#FFF',
                   strokeWeight: 1,
                   fillOpacity: 0.7,
                   scale: Math.max(Math.min(station.available_bike_stands, 14), 8) // size according to free stands, but compress range as otherwise size differences too extreme
                },
                animation: google.maps.Animation.DROP,
                title: station.address
            });

            // Change details and charts to corresponding station on clicking marker
            marker.addListener("click", function() {
                //drawStationCharts(this);
                //drawStationChartsWeekly(this);
                for (var i = 0; i < obj.length; i++) {
                    var station = obj[i];
                    //console.log(station);
                    if (station.address == this.title) {
                        var html = "<h2>" + this.title + "</h2><div class='text-content'>";
                        html += "<p>Available bikes: " + station.available_bikes + "</p>";
                        html += "<p>Free bike stands: " + station.available_bike_stands + "</p></div>";
                        break;
                    }
                }

            document.getElementById('station-info').innerHTML = html;
            console.log(this.title);
            });
        }
    }

}
