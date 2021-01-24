function createChart(chartId, chartDict, colorScale, colorRangeInfo, chartType) {
    const chartElement = $('#chart-' + chartId);
    console.log(chartElement)
    const dataLength = chartDict.data.length;

    /* Create color array */
    var COLORS = interpolateColors(dataLength, colorScale, colorRangeInfo);

    /* Create chart */
    const myChart = new Chart(chartElement, {
        type: chartType,
        data: {
            labels: chartDict.labels,
            datasets: [{
                backgroundColor: COLORS,
                hoverBackgroundColor: COLORS,
                data: chartDict.data
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: chartDict.title,
            }
        }
    });

    return myChart;
}
$(document).ready(function () {
    const chart_list = JSON.parse($('#chart_list').text());
    const colorScale = d3.interpolateRainbow; //https://github.com/d3/d3-scale-chromatic/blob/master/README.md

    const colorRangeInfo = {
        colorStart: 0,
        colorEnd: 1,
        useEndAsStart: false,
    };

    for (let i = 0, len = chart_list.length; i < len; i++) {
        const chartDict = chart_list[i];
        const chart = createChart(chartDict.id, chartDict, colorScale, colorRangeInfo, 'doughnut');
    }
    function beforePrintHandler() {
        for (var id in Chart.instances) {
            Chart.instances[id].resize();
        }
    }
    window.addEventListener("beforeprint", beforePrintHandler());
});