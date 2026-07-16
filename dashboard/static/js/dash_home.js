document.addEventListener("DOMContentLoaded", () => {

    // ── Helper ──
    function initChart(elId, type, labels, values, opts = {}) {
      const ctx = document.getElementById(elId);
      if (!ctx) return;
      new Chart(ctx, {
        type,
        data: {
          labels,
          datasets: [{ data: values, borderWidth: 1 }]
        },
        options: opts
      });
    }

    // ── Sales Week Chart ──
    const swCard = document.getElementById('salesWeekChartCard');
    if (swCard) {
      const labels = JSON.parse(swCard.dataset.bsLabels || '[]');
      const values = JSON.parse(swCard.dataset.bsValues || '[]');
      initChart('salesWeekChart', 'line', labels, values, {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      });
    }

    // ── Products by Category ──
    const catCard = document.getElementById('productsByCategoryChartCard');
    if (catCard) {
      const labels = JSON.parse(catCard.dataset.bsLabels || '[]');
      const values = JSON.parse(catCard.dataset.bsValues || '[]');
      initChart('productsByCategoryChart', 'bar', labels, values, {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { x: { beginAtZero: true } }
      });
    }

    // ── Orders by Status ──
    const stCard = document.getElementById('ordersByStatusChartCard');
    if (stCard) {
      const labels = JSON.parse(stCard.dataset.bsLabels || '[]');
      const values = JSON.parse(stCard.dataset.bsValues || '[]');
      initChart('ordersByStatusChart', 'bar', labels, values, {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      });
    }

});
