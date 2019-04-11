    var ctx1 = document.getElementById('myChart1');
    var ctx2 = document.getElementById('myChart2');
    var graph_data_past = graph_data_past;


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
    }
}
});


var chart2 = new Chart(ctx2, {
// The type of chart we want to create
type: 'line',

// The data for our dataset
data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December'],
    datasets: [{
        label: 'Which ever label',
        backgroundColor: '#1f567c',
        borderColor: 'black',
        data: [0, 10, 5, 2, 20, 30, 45, 12, 15, 25, 30, 5]
    }]
},

// Configuration options go here
options: {
        title: {
        display: true,
        text: 'Available bikes at: "name of the station"',
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
                suggestedMax: 25,
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