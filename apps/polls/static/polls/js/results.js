function createChart(chartId, chartDict, chartType) {
    const chartElement = document.getElementById('chart-' + chartId);

    const myChart = new Chart(chartElement, {
        type: chartType,
        data: {
            labels: chartDict.labels,
            datasets: [{
                data: chartDict.data
            }],
        },
        options: {
            respobnsive: true,
            plugins: {
                title: {
                    display: true,
                    text: chartDict.title,
                },
                autocolors: {
                    mode: "data"
                }
            }
        }
    });

    return myChart;
}

$(function () {
    const chart_list = JSON.parse($('#chart_list').text());
    const autocolors = window['chartjs-plugin-autocolors'];

    Chart.register(autocolors);

    for (let i = 0, len = chart_list.length; i < len; i++) {
        const chartDict = chart_list[i];
        const chart = createChart(chartDict.id, chartDict, 'doughnut');
    }
});