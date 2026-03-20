// รับ chart data จาก Django template แล้ว render ด้วย Plotly
function renderCharts(chartsData) {
    chartsData.forEach(function (chartJson, index) {
        var elementId = 'chart_' + (index + 1);
        var fig = JSON.parse(chartJson);
        Plotly.newPlot(elementId, fig.data, fig.layout, { responsive: true });
    });
}