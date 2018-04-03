'use strict';
$(document).ready(function(){
    // Get static station data from JSON file
    var xmlhttp = new XMLHttpRequest();
    var url_stations = "/static/data/station_data.json";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //Parse the JSON data to a JavaScript variable
            var staticStation = JSON.parse(xmlhttp.responseText);
            var html = "";
            for (var i = 0; i < staticStation.length; i++) {
                html += ('<li><a href="#">' + staticStation[i].address + '</a></li>');
            }
            document.getElementById('station-dropdown').innerHTML = html;
        }
    }

xmlhttp.open("GET", url_stations, true);
xmlhttp.send();

});

//Adds Google map to display panel using Google Maps API | ref: https://developers.google.com/maps/documentation/javascript/
function initMap() {
    //Create map object and specify the element in which to display it
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 53.344, lng: -6.27},
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
                        var html = "<h2 class='bottom-pad-20'>" + this.title + "</h2>";
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


//Function to round decimal values from the weather data | ref: http://www.jacklmoore.com/notes/rounding-in-javascript/
function round(value, num_places) {
    return Number(Math.round(value + 'e' + num_places) + 'e-' + num_places);
}

//Loads new content into panel on click of submission button
function submitPeriod() {
    //Set period value based on selected radio button | ref: https://stackoverflow.com/questions/9618504/get-radio-button-value-with-javascript
    var radios = document.getElementsByName('period');
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            //set period value
            var period = radios[i].value;
            break; //No need to check rest as only one radio ever on
        }
    }
    //Assign boolen values based on homepage check boxes. These will be used as arguments for dailyFC() where they determine which of the extra weather parmeters to include
    var press = document.getElementById('pressCheck').checked;
    var humid = document.getElementById('humCheck').checked;
    var wind = document.getElementById('windCheck').checked;

    dailyFC(period, press, humid, wind);
}

//Update dislpay to show daily forecast
function dailyFC(period, press, humid, wind) {
    var xmlhttp = new XMLHttpRequest();
    var url_daily = "/static/data/daily.json";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //Parse the JSON data to a JavaScript variable
            var parsedObj = JSON.parse(xmlhttp.responseText);
            //Function (defined below) to generate new page content from the parsed JSON data
            dailyContent(parsedObj);
        }
    }

    xmlhttp.open("GET", url_daily, true);
    xmlhttp.send();

    //Function to generate new page content from the daily JSON data
    function dailyContent(obj) {

        //Declare the list object that contains the required data from the json file
        var list = obj.list;
        //Declare time related variables
        var date = new Date();
        var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        //Declare variable to contain the content with which to update the display-panel div
        var html = "";

        for (var i = 0; i < period; i++) {
            //Variables to represent data within the list variable
            //Temperature max
            if (typeof(list[i].temp.max) != "undefined") {
                var temp_max = round(list[i].temp.max, 2) + " &#8451";
            } else {
                temp_max = "N/A";
            }
            //Temperature min
            if (typeof(list[i].temp.min) != "undefined") {
                var temp_min = round(list[i].temp.min, 2) + " &#8451";
            } else {
                temp_min = "N/A";
            }
            //Humidity
            if (typeof(list[i].humidity) != "undefined" && list[i].humidity != 0) {
                var hum = list[i].humidity + "%";
            } else {
                hum = "N/A";
            }
            //Pressure
            if (typeof(list[i].pressure) != "undefined") {
                var p = list[i].pressure + " hPa";
            } else {
                p = "N/A";
            }
            //Wind speed
            if (typeof(list[i].speed) != "undefined") {
                var wspeed = round(list[i].speed * 60**2/1000, 2) + " km/h";
            } else {
                wspeed = "N/A";
            }
            //Set date from JSON file
            date.setTime(list[i].dt * 1000);
            //Generate new html for display panel. Note day 1 (oct 19) is half day, while rest are full days; hence onclick='detailedFC(i + 0.5)'
            html += "<div class='daily-block container-middle'><div class='column-two'><h2>"
            + months[date.getMonth()] + " " + date.getDate()
            + "</h2><div><img src='http://openweathermap.org/img/w/"
            + list[i].weather[0].icon
            + ".png' alt='light rain icon'></div><div class='daily-descript'>"
            + list[i].weather[0].description
            +"</div><div><button id='detailButton' name='detailed' onclick='detailedFC(" + (i + 0.5) + ")'>Detailed Forecast</button></div></div>"
            //Summary Stats table
            + "<div class='column-two'><h3>Summary Stats</h3><table><tr><td class='col-th'>Temp (max)</td><td>"
            + temp_max + "</td></tr><tr><td class='col-th'>Temp (min)</td><td>"
            + temp_min + "</td></tr>";
            //Add extra stats if selected by user (checked)
            if (press) {
                html += "<tr><td class='col-th'>Pressure</td><td>"
                + p + "</td></tr>";
            }
            if (humid) {
                html += "<tr><td class='col-th'>Humidity</td><td>"
                + hum + "</td></tr>";
            }
            if (wind) {
                html += "<tr><td class='col-th'>Wind Speed</td><td>"
                + wspeed + "</td></tr>";
            }
            //Finish table
            html += "</table></div></div>";
        }
        //Ensure starting new content from top of page and adjust display panel padding
        document.documentElement.scrollTop = 0;
        document.getElementById('display-panel').style['padding-top'] = "10px";
        //Replace display panel content with the newly generated content
        document.getElementById('display-panel').innerHTML = html;
    }
}

//Loads new content (based on the detailed JSON data) into display panel on click of detailed forecast button
function detailedFC(day) {
    //Declare variables
    var xmlhttp = new XMLHttpRequest();
    var url_detailed = "/static/data/detailed.json";

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //Parse the JSON data to a JavaScript variable.
            var parsedObj = JSON.parse(xmlhttp.responseText);
            // This function is defined below and deals with the JSON data parsed from the file.
            detContent(parsedObj);
        }
    }

    xmlhttp.open("GET", url_detailed, true);
    xmlhttp.send();

    function detContent(obj) {

        //Declare the list object that contains the required data from the json file
        var list = obj.list;
        //Set date from JSON file depending on the day input to detailedFC() via the detailed button
        //Day1 (oct 19) is half day (4 three-hour periods), while rest are full days (8 three-hour periods)
        if (day > 0.5) {
            var date = new Date(list[day * 8 - 8].dt * 1000);
        } else {
            var date = new Date(list[0].dt * 1000);
        }
        var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        var html = "<h2>" + months[date.getMonth()] + " " + date.getDate() + "</h2>";

        //Generate table (using loop) for each three-hour period of day; note is half day (only 4 three-hour periods)
        //Initialize loop variables for first (half) day
        var start = 0;
        var end = 4;
        //For other days assign the following calculated values
        if (day > 0.5) {
            start = day * 8 - 8;
            end = day * 8;
        }

        for (var i = start; i < end; i++) {
            //Set date (time) from JSON file (note: time is set to 1 hour ahead [western european time] so s1 hour is substracted)
            date.setTime(list[i].dt * 1000 - 1);
            //Variables to represent the required JSON data
            //Temperature max
            if (typeof(list[i].main.temp_max) != "undefined") {
                var temp_max = round(list[i].main.temp_max, 2) + " &#8451";
            } else {
                temp_max = "N/A";
            }
            //Temperature min
            if (typeof(list[i].main.temp_min) != "undefined") {
                var temp_min = round(list[i].main.temp_min, 2) + " &#8451";
            } else {
                temp_min = "N/A";
            }
            //Rain
            if (typeof(list[i].rain['3h']) != "undefined") {
                var rain = round(list[i].rain['3h'], 2) + " mm";
            } else {
                rain = "N/A";
            }
            //Wind speed
            if (typeof(list[i].wind.speed) != "undefined") {
                var wspeed = round(list[i].wind.speed * 60**2/1000, 2) + " km/h";
            } else {
                wspeed = "N/A";
            }
            //Wind direction
            var wdir = "";
            if (typeof list[i].wind.deg != "undefined") {
                if (Math.abs(list[i].wind.deg - 45) < 15) {
                    wdir = "NE";
                } else if (Math.abs(list[i].wind.deg - 90) <= 15) {
                    wdir = "E";
                } else if (Math.abs(list[i].wind.deg - 135) < 15) {
                    wdir = "SE";
                } else if (Math.abs(list[i].wind.deg - 180) <= 15) {
                    wdir = "S";
                } else if (Math.abs(list[i].wind.deg - 225) < 15) {
                    wdir = "SW";
                } else if (Math.abs(list[i].wind.deg - 270) <= 15) {
                    wdir = "W";
                } else if (Math.abs(list[i].wind.deg - 315) < 15) {
                    wdir = "NW";
                } else {
                    wdir = "N";
                }
            } else {
                wdir = "N/A"
            }
            //Clouds
            if (typeof(list[i].clouds.all) != "undefined") {
                var clouds = list[i].clouds.all + "%";
            } else {
                clouds = "N/A";
            }
            //Humidity
            if (typeof(list[i].main.humidity) != "undefined") {
                var humid = list[i].main.humidity + "%";
            } else {
                humid = "N/A";
            }
            //Pressure at gound level
            if (typeof(list[i].main.grnd_level) != "undefined") {
                var pg = round(list[i].main.grnd_level, 2) + " hPa";
            } else {
                pg = "N/A";
            }
            //Pressure at sea level
            if (typeof(list[i].main.sea_level) != "undefined") {
                var ps =round(list[i].main.sea_level, 2) + " hPa";
            } else {
                ps = "N/A";
            }

            //Generate new html for display panel
            html += "<div class='detailed-block container-middle'><h3>Time:&nbsp;&nbsp;" + (date.getHours()-1)
            + ":00&ndash;" + (date.getHours() + 1) + ":59" + "</h3><div><img src='http://openweathermap.org/img/w/"
            + list[i].weather[0].icon
            + ".png' alt='light rain icon'><span class='detailed-descript'>"
            + list[i].weather[0].description
            + "</span></div><div><table><tr><th>Temp (max)</th><th>Temp (min)</th><th>Rainfall</th><th>Wind Speed</th><th>Wind Direction</th><th>Cloud Cover</th><th>Humidity</th><th>Pressure (ground)</th><th>Pressure (sea)</th></tr><tr><td>"
            + temp_max + "</td><td>"
            + temp_min + "</td><td>"
            + rain + "</td><td>"
            + wspeed + "</td><td>"
            + wdir + "</td><td>"
            + clouds + "</td><td>"
            + humid + "</td><td>"
            + pg + "</td><td>"
            + ps + "</td></tr></table></div></div>";
        }

        //Ensure starting new content from top of page and adjust display panel padding
        document.documentElement.scrollTop = 0;
        document.getElementById('display-panel').style['padding-top'] = '30px';
        //Replace display panel content with the newly generated content
        document.getElementById("display-panel").innerHTML = html;
    }
}
