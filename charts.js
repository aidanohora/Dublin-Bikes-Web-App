queue()
    .defer(d3.csv, "Dublin Bike Info.txt")
    .await(makeGraph);

function makeGraph(error, securitiesData) {

    let ndx = crossfilter(securitiesData);


    //parseDate tell the program that this is the date format needed to be used with the file
    let parseDate = d3.time.format("%d/%m/%Y").parse;

    //the below directly below links the file with here and creates a loop to run every string date given in file to a date format here to be picked up by the created chart.
    transactionsData.forEach(function(d) {
        d.date = parseDate(d.date);
    });

    // dimensions (x-axis)----------------
    let dateDim = ndx.dimension(dc.pluck("Dates"));

    let availableBikes = dateDim.group().reduceSum(dc.pluck("availableBikes"));

    //the two lines below tells to take the lowest and highest values if we wanted lowest 2 we would write .bottom(2). We need the lowest value for the linechart. these are to give the top and bottom values for the x-axis.
    let minDate = dateDim.bottom(1)[0].date;
    let maxDate = dateDim.top(1)[0].date;

    dc.lineChart("HTML location")
        .width(500)
        .height(300)
        .dimension(dateDim)
        .group(totalSpendByTime)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .xAxisLabel("Month");


    dc.renderAll();
}