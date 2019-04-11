    var ctx1 = document.getElementById('myChart1');
    var ctx2 = document.getElementById('myChart2');


    var chart1 = new Chart(ctx1, {
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
                labelString: "What ever we want",
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
                labelString: "What ever we want",
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