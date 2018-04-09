'use strict';
// Global station json related variables
const jcdUrl = "https://api.jcdecaux.com/vls/v1/stations";
const jcdParams = "?contract=Dublin&apiKey=8b0bfe2e205616b7ebec9f675e2168f7b9726683";
var stationData = {};
var stationsUpdated = false;


function updateStationData(url, callback) {
    if (stationsUpdated === false) {
        $.getJSON(url, function(result){
            stationData = result;
            callback(stationData);
            console.log(stationData);
        });
        trueWaitFalse(stationsUpdated, 60000);
    }
}

function trueWaitFalse(bool, waitTime) {
    bool = true;
    setTimeout(function() {
        bool = false;
    }, waitTime);
}

function updateStations(stationName) {
    //drawStationCharts(this);
    //drawStationChartsWeekly(this);
    for (var i = 0; i < stationData.length; i++) {
        var station = stationData[i];
        //console.log(station.address);
        if (station.address == stationName) {
            $.getJSON(jcdUrl+"/"+station.number.toString()+jcdParams, function(result) {
                var html = "<h2>" + stationName + "</h2><div class='text-content'>";
                html += "<p>Available bikes: " + result.available_bikes + "</p>";
                html += "<p>Free bike stands: " + result.available_bike_stands + "</p></div>";
                document.getElementById('station-info').innerHTML = html;
            });
            break;
        }
    }
}

function dropDownStations(url) {
    $.getJSON(url, function(result){
        stationData = result;
        console.log(stationData);
        var html = "";
        for (var i = 0; i < stationData.length; i++) {
            var name = stationData[i].address;
            html += ('<li><a href="#" onclick="updateStations(\''+ name + '\')">' + name + '</a></li>');
        }
        document.getElementById("station-dropdown").innerHTML = html;
    });
}


// Page load actions
$(document).ready(function(){
    // Dropdown list to select station
    dropDownStations("/static/data/station_data.json");
});

//updateStationData(jcdUrl, dropDownStations); // update station data //FIXME


//Adds Google map to display panel using Google Maps API | ref: https://developers.google.com/maps/documentation/javascript/
function initMap() {
    //Create map object and specify the element in which to display it
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 53.345, lng: -6.27},
        zoom: 13
    });

    addMarkers(map, jcdUrl + jcdParams);
}

//Add marker for each station to Google map
function addMarkers(map, url) {
    $.getJSON(url, function(result) {
        stationData = result;
        for (var i = 0; i < stationData.length; i++) {
            var station = stationData[i];
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
            marker.addListener("click", updateStations.bind(null, marker.title));
        }
    });

}
