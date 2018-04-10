'use strict';
//--------------------------------------------------------------
// Global variables
//--------------------------------------------------------------
const jcdUrl = "https://api.jcdecaux.com/vls/v1/stations";
const jcdParams = "?contract=Dublin&apiKey=8b0bfe2e205616b7ebec9f675e2168f7b9726683";

// var stationData = {};
// var stationsUpdated = false;

//--------------------------------------------------------------
// Functions
//--------------------------------------------------------------

function updateStations(stationNumber) {
    var url = jcdUrl+"/"+stationNumber+jcdParams;
    $.getJSON(url, function(result) {
        // Station info
        var html = "<h2>" + result.address + "</h2><div class='text-content'>";
        html += "<p>Available bikes: " + result.available_bikes + "</p>";
        html += "<p>Free bike stands: " + result.available_bike_stands + "</p></div>";
        document.getElementById('station-info').innerHTML = html;
    })
    .fail(function() {
        console.log( "Error: Failed to get JSON data from "+ url );
    });
}

function dropDownStations(url) {
    $.getJSON(url, function(result){
        var stationData = result;
        //console.log(stationData);
        var html = "";
        for (var i = 0; i < stationData.length; i++) {
            var name = stationData[i].name;
            var number = stationData[i].number;
            html += ('<li><a href="#" onclick="updateStations(\''+ number + '\')">' + name + '</a></li>');
        }
        document.getElementById("station-dropdown").innerHTML = html;
    })
    .fail(function() {
        console.log( "Error: Failed to get JSON data from "+ url );
    });
}

//-- Charts (chartJS) --
function createBarChart(elemId, chartData, labels, title) {
    // DOM element to hold chart
    var chart = document.getElementById(elemId).getContext('2d');

    // Initialize chart
    var barChart = new Chart(chart,{
        type: 'bar',
        data: {
            labels: labels,

            datasets: [
                {
                    label: "Average",
                    backgroundColor: "#1996ff",
                    data: chartData
                }
            ]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: title
            },
            scales: {
                yAxes: [{
                    ticks: { beginAtZero: true }
                }]
            }
        }
    });

    return barChart
}

function initCharts(url) {
    $.getJSON(url, function(result) {
        console.log(result.station_stats.daily_avg);
        // Daily chart
        var dailyData = result.station_stats.daily_avg;
        var chartDataDaily = [dailyData.Monday, dailyData.Tuesday, dailyData.Wednesday, dailyData.Thursday, dailyData.Friday, dailyData.Saturday, dailyData.Sunday];
        var labelsDaily = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        // Create daily chart in canvas on html page
        dailyChart = createBarChart("daily-chart", chartDataDaily, labelsDaily, "Average bike availability per day");

        // Hourly chart
    })
    .fail(function() {
        console.log( "Error: Failed to get JSON data from "+ url );
    });
}

function updateCharts(stationNumber) {
    var url = $SCRIPT_ROOT + "/station_stats/" + stationNumber
    console.log(url);

    $.getJSON(url, function(result) {
        console.log(result.station_stats.daily_avg);
        var dailyData = result.station_stats.daily_avg;
        var chartData = [dailyData.Monday, dailyData.Tuesday, dailyData.Wednesday, dailyData.Thursday, dailyData.Friday, dailyData.Saturday, dailyData.Sunday];
        dailyChart.data.datasets[0].data = chartData;
        //console.log(chart1.data.datasets[0].data);
        //chart1.data.datasets.data = [1,2,3,4,5,6,7];
        dailyChart.update();
    })
    .fail(function() {
        console.log( "Error: Failed to get JSON data from "+ url );
    });
}

// function updateStationData(url, callback) {
//     if (stationsUpdated === false) {
//         $.getJSON(url, function(result){
//             stationData = result;
//             callback(stationData);
//             console.log(stationData);
//         })
//         .fail(function() {
//             console.log( "Error: Failed to get JSON data from "+ url );
//         });
//         trueWaitFalse(stationsUpdated, 60000);
//     }
// }
//
// function trueWaitFalse(bool, waitTime) {
//     bool = true;
//     setTimeout(function() {
//         bool = false;
//     }, waitTime);
// }

// updateStationData(jcdUrl, dropDownStations); // update station data //FIXME

//--------------------------------------------------------------
// Initial page
//--------------------------------------------------------------

//$(document).ready(function(){

    // Dropdown list to select station
    dropDownStations("/static/data/station_data.json");

    // Initialize daily average chart
    var url = $SCRIPT_ROOT + "/station_stats/" + "37";
    // Daily chart
    var chartDataDaily = [1,1,1,1,1,1,1];
    var labelsDaily = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    // Create daily chart in canvas on html page
    var dailyChart = createBarChart("daily-chart", chartDataDaily, labelsDaily, "Average bike availability per day");
    // Add data from database via API call to flask app
    updateCharts("37");

//});

//-- Google Map --

// Adds Google map to display panel using Google Maps
function initMap() {
    //Create map object and specify the element in which to display it
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 53.345, lng: -6.27},
        zoom: 13
    });

    // Add markers to map
    addMarkers(map, jcdUrl + jcdParams);
}

// Add marker for each station to Google map
function addMarkers(map, url) {
    $.getJSON(url, function(result) {
        var stationData = result;
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
                title: station.address,
                number: station.number
            });
            // Change details and charts to corresponding station on clicking marker
            marker.addListener("click", updateStations.bind(null, marker.number));
            //marker.addListener("click", updateCharts.bind(null, dailyChart, 'chart2', marker.number)); // FIXME: chart 2
            marker.addListener("click", updateCharts.bind(null, marker.number)); // FIXME: chart 2

        }
    });
}
