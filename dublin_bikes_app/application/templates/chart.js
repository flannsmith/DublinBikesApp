//The first daily chart
<script>
        var chart = document.getElementById('dailyChart').getContext('2d');
          
        var barChart = new Chart(chart,{
            
            type: 'bar',
            data: {
                labels:["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                
                datasets: [
                    {
                        label: "Number",
                        backgroundColor: "#3cba9f",
                        data : [{% for item in values %}
                                    {{item}},
                                {% endfor %}]
                    }
                ]
            },
            options: {
                legend: { display: true },
                title: {
                    display: true,
                    text: 'The daily average'
                }
            }
        });
</script>
//The hourly chart
<script>
        var CHART = document.getElementById('hourlyChart').getContext('2d');
          
        var lineChart = new Chart(CHART, {
            type: 'line',
            data: {
                labels:["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00","24:00"],
                datasets: [{ 
                    data: [{% for item in mondayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Monday",
                    borderColor: "#3e95cd",
                    fill: true
                  }, { 
                    data: [{% for item in tuesdayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Tuesday",
                    borderColor: "#8e5ea2",
                    fill: true
                  }, { 
                    data: [{% for item in wednesdayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Wednesday",
                    borderColor: "#3cba9f",
                    fill: true
                  }, { 
                    data: [{% for item in thursdayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Thursday",
                    borderColor: "#e8c3b9",
                    fill: true
                  }, { 
                    data: [{% for item in fridayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Friday",
                    borderColor: "#c45850",
                    fill: true
                  }, { 
                    data: [{% for item in saturdayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Saturday",
                    borderColor: "#e8c",
                    fill: true
                  }, { 
                    data: [{% for item in sundayData %}
                                    {{item}},
                                {% endfor %}],
                    label: "Sunday",
                    borderColor: "#c45",
                    fill: true
                  }
                ]
              },
            options:{
                title: {
                    display: true,
                    text: 'The hourly average'
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                    boxWidth: 80,
                    fontColor: 'black'
                    }
                }
            }
                
        });
</script>

//The weather chart
<script>
        var weatChart = document.getElementById('weatherChart').getContext('2d');
          
        var barChart = new Chart(weatChart,{
            
            type: 'bar',
            data: {
                labels:["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                
                datasets: [
                    {
                        label: "Number",
                        backgroundColor: "#3cba9f",
                        data : [{% for item in values %}
                                    {{item}},
                                {% endfor %}]
                    },
                    {
                        label: "Number",
                        backgroundColor: "#3cba9f",
                        data : [{% for item in values %}
                                    {{item}},
                                {% endfor %}]
                    },
                    {
                        label: "Number",
                        backgroundColor: "#3cba9f",
                        data : [{% for item in values %}
                                    {{item}},
                                {% endfor %}]
                    }
                    
                ]
            },
            options: {
                legend: { display: true },
                title: {
                    display: true,
                    text: 'The weather'
                }
            }
        });
      </script>