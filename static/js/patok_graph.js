    // data
    var trace1 = {
        type: 'bar',
        x: ['Q1', 'Q2', 'Q3', 'Q4', 'N/A'],
        y: [5, 10, 2, 8, 30],
        marker: {
            color: '#C8A2C8',
            line: {
                width: 2.5
            }
        },
        xaxis: 'x1',
        yaxis: 'y1'
    };
    var trace2 = {
        type: 'line',
        x: [1, 2, 3, 4],
        y: [5, 10, 2, 8],
        marker: {
            color: '#C8A2C8',
            line: {
            }
        },
        xaxis: 'x2',
        yaxis: 'y2'
    };
    var data = [ trace1 ];

    // layouting
    var layout = {
        title: 'Patok Status',
        font: {size: 14}
    };

    // configuration
    var config = {
        responsive: true,
        displayModeBar: false,
    }

    Plotly.newPlot('graph', data, layout, config);