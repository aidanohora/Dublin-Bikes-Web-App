    var ctx1 = document.getElementById('myChart1');
    var ctx2 = document.getElementById('myChart2');
    var graph_data_past = graph_data_past;
    var graph_data_future = graph_data_future;

// loop through the past data to create a list to pass to the graph
    var max_past = 0;
    var past_x = [];
    var past_y = [];
    for (i = 0; i < graph_data_past.length; i++) {
        past_x.push(graph_data_past[i][2]);
        past_y.push(graph_data_past[i][0])
        if (graph_data_past[i][0] > max_past) {
            max_past = graph_data_past[i][0];
        } else {
            continue;
        }
    }

// loop through the prediction data to create a list to pass to the prediction graph
    var max_future = 0;
    var future_x = [];
    var future_y = [];
    for (i = 0; i < graph_data_future.length; i++) {
        future_x.push(graph_data_future[i][2]);
        future_y.push(graph_data_future[i][0])
        if (graph_data_future[i][0] > max_future) {
            max_future = graph_data_future[i][0];
        } else {
            continue;
        }
    }



// graph rendering the past data for the station searched----------------------
    var chart1 = new Chart(ctx1, {
// The type of chart we want to create
type: 'line',

// The data for our dataset
data: {
    labels: past_x,
    datasets: [{
        label: 'Available bikes',
        backgroundColor: '#1f567c',
        borderColor: 'black',
        data: past_y
    }]
},

// Configuration options go here
options: {
        title: {
        display: true,
        text: 'Past available bikes at station number ' + graph_data_past[0][3],
        fontSize: 15
    },
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: "Last 24 hours",
                fontSize: 15
            }
        }],
        yAxes: [{
            ticks: {
                beginAtZero: true,
                suggestedMax: max_past,
            },
            scaleLabel: {
                display: true,
                labelString: "Available bikes",
                fontSize: 15
            }
        }]
    },
}
});


// graph rendering the prediction data for the station searched----------------
var chart2 = new Chart(ctx2, {
// The type of chart we want to create
type: 'line',

// The data for our dataset
data: {
    labels: future_x,
    datasets: [{
        label: 'Available bikes',
        backgroundColor: '#1f567c',
        borderColor: 'black',
        data: future_y
    }]
},

// Configuration options go here
options: {
        title: {
        display: true,
        text: 'Future available bikes at station number ' + graph_data_future[0][3],
        fontSize: 15
    },
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: "Predictions for the next 24 hours",
                fontSize: 15
            }
        }],
        yAxes: [{
            ticks: {
                beginAtZero: true,
                suggestedMax: max_future,
            },
            scaleLabel: {
                display: true,
                labelString: "Available bikes",
                fontSize: 15
            }
        }]
    }
}
});

