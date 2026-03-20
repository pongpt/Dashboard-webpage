const PLOTLY_CONFIG = { responsive: true, displaylogo: false };

function renderChart(chartId, fig) {
    const el = document.getElementById(chartId);
    if (!el || !fig) return;
    Plotly.newPlot(el, fig.data, fig.layout, PLOTLY_CONFIG);
}

function renderAllCharts(chartsData) {
    chartsData.forEach(function(chart) {
        renderChart(chart.id, chart.fig);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    if (typeof CHARTS_DATA !== 'undefined') {
        renderAllCharts(CHARTS_DATA);
    }
});