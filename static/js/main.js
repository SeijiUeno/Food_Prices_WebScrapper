document.addEventListener('DOMContentLoaded', function () {
	// Retrieve the chart data JSON passed from Flask
	const chartDataScript = document.getElementById('chartData');
	if (!chartDataScript) {
	  console.error("No chartData element found in the DOM.");
	  return;
	}
  
	const chartData = JSON.parse(chartDataScript.textContent || '{}');
	const datasets = [];
	let labels = [];
  
	const categorias = Object.keys(chartData);
	if (categorias.length > 0) {
	  labels = chartData[categorias[0]].dates;
	}
  
	categorias.forEach(categoria => {
	  datasets.push({
		label: categoria,
		data: chartData[categoria].prices,
		fill: false,
		borderColor: '#' + Math.floor(Math.random() * 16777215).toString(16),
		borderWidth: 3,
		tension: 0.4,
		pointRadius: 5,
		pointHoverRadius: 8
	  });
	});
  
	const ctx = document.getElementById('priceChart').getContext('2d');
	new Chart(ctx, {
	  type: 'line',
	  data: {
		labels: labels,
		datasets: datasets
	  },
	  options: {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
		  legend: {
			position: 'bottom',
			labels: {
			  font: { size: 14 }
			}
		  },
		  tooltip: {
			mode: 'index',
			intersect: false,
			backgroundColor: 'rgba(0, 0, 0, 0.7)'
		  }
		},
		scales: {
		  x: {
			title: {
			  display: true,
			  text: 'Data',
			  font: { size: 16 }
			}
		  },
		  y: {
			title: {
			  display: true,
			  text: 'Preço Médio (BRL)',
			  font: { size: 16 }
			}
		  }
		},
		interaction: {
		  mode: 'nearest',
		  intersect: false
		}
	  }
	});
  });
  