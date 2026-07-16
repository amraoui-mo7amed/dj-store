document.addEventListener('DOMContentLoaded', function () {
  // Revenue Line Chart
  var revenueChartEl = document.getElementById('revenueChart');
  if (!revenueChartEl) return;

  var revenueLabels, revenueData;
  try {
    revenueLabels = JSON.parse(revenueChartEl.getAttribute('data-labels') || '[]');
    revenueData = JSON.parse(revenueChartEl.getAttribute('data-values') || '[]');
  } catch (e) {
    return;
  }

  var revenueCtx = revenueChartEl.getContext('2d');
  new Chart(revenueCtx, {
    type: 'line',
    data: {
      labels: revenueLabels,
      datasets: [{
        label: 'الإيرادات (دج)',
        data: revenueData,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.05)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointBackgroundColor: '#fff',
        pointBorderColor: '#3b82f6',
        pointBorderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: '#f1f5f9' },
          ticks: { font: { family: 'inherit' } }
        },
        x: { grid: { display: false } }
      }
    }
  });

  // Status Doughnut Chart
  var statusChartEl = document.getElementById('statusDoughnut');
  if (!statusChartEl) return;

  var statusLabels, statusValues;
  try {
    statusLabels = JSON.parse(statusChartEl.getAttribute('data-labels') || '[]');
    statusValues = JSON.parse(statusChartEl.getAttribute('data-values') || '[]');
  } catch (e) {
    return;
  }

  var statusCtx = statusChartEl.getContext('2d');
  new Chart(statusCtx, {
    type: 'doughnut',
    data: {
      labels: statusLabels,
      datasets: [{
        data: statusValues,
        backgroundColor: ['#fbbf24', '#3b82f6', '#8b5cf6', '#10b981', '#ef4444'],
        borderWidth: 0,
        hoverOffset: 10
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { boxWidth: 12, padding: 20, font: { family: 'inherit' } }
        }
      },
      cutout: '70%'
    }
  });
});
