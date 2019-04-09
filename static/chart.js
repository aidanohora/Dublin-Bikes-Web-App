    var ctx = document.getElementById('myChart');
    var chart = new Chart(ctx, {
// The type of chart we want to create
type: 'line',

// The data for our dataset
data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    'November', 'December'],
    datasets: [{
        label: 'Which ever label',
        backgroundColor: 'gray',
        borderColor: 'black',
        data: [0, 10, 5, 2, 20, 30, 45, 12, 15, 25, 30, 5]
    }]
},

// Configuration options go here
options: {
        title: {
        display: true,
        text: 'Available bikes at: "name of the station"',
        fontSize: 35
    },
    scales: {
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: "What ever we want",
                fontSize: 35
            }
        }],
        yAxes: [{
            ticks: {
                beginAtZero: true,
                suggestedMax: 50,
            },
            scaleLabel: {
                display: true,
                labelString: "Available bikes",
                fontSize: 35
            }
        }]
    }
}
});