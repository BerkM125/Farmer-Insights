<script>
	import { onMount, onDestroy } from 'svelte';
	import {
		Chart,
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		CategoryScale,
		Title,
		Tooltip,
		Legend,
		Filler
	} from 'chart.js';

	// Register Chart.js components
	Chart.register(
		LineController,
		LineElement,
		PointElement,
		LinearScale,
		CategoryScale,
		Title,
		Tooltip,
		Legend,
		Filler
	);

	let { chartData = [] } = $props();

	let canvas;
	let chart;

	// Accent colors from app.css
	const accentColors = [
		{ border: 'hsl(0, 65%, 65%)', background: 'hsla(0, 65%, 65%, 0.1)' }, // red-1
		{ border: 'hsl(45, 65%, 60%)', background: 'hsla(45, 65%, 60%, 0.1)' }, // yellow-1
		{ border: 'hsl(80, 55%, 50%)', background: 'hsla(80, 55%, 50%, 0.1)' }, // green-1
		{ border: 'hsl(170, 55%, 50%)', background: 'hsla(170, 55%, 50%, 0.1)' } // blue-1
	];

	// Simple hash function to consistently assign colors to crops
	function hashString(str) {
		let hash = 0;
		for (let i = 0; i < str.length; i++) {
			const char = str.charCodeAt(i);
			hash = (hash << 5) - hash + char;
			hash = hash & hash; // Convert to 32bit integer
		}
		return Math.abs(hash);
	}

	// Helper function: Get color for crop
	function getCropColor(cropName) {
		const index = hashString(cropName.toLowerCase()) % accentColors.length;
		return accentColors[index];
	}

	function createChart() {
		if (!canvas || !chartData || chartData.length === 0) return;

		// Destroy existing chart if it exists
		if (chart) {
			chart.destroy();
		}

		// Prepare datasets
		const datasets = chartData.map((cropData) => {
			const colors = getCropColor(cropData.crop);
			return {
				label: cropData.crop.charAt(0).toUpperCase() + cropData.crop.slice(1),
				data: cropData.prices.map((p) => p.price),
				borderColor: colors.border,
				backgroundColor: colors.background,
				borderWidth: 2.5,
				tension: 0.3,
				fill: true,
				pointRadius: 3,
				pointHoverRadius: 5,
				pointBackgroundColor: colors.border,
				pointBorderColor: colors.border,
				pointBorderWidth: 2,
				pointHoverBackgroundColor: colors.border,
				pointHoverBorderColor: colors.border,
				pointHoverBorderWidth: 2
			};
		});

		// Get labels from the first dataset (assuming all have same dates)
		const labels =
			chartData[0]?.prices.map((p) => {
				const date = new Date(p.date);
				return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
			}) || [];

		// Create chart
		const ctx = canvas.getContext('2d');
		chart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: labels,
				datasets: datasets
			},
			options: {
				responsive: true,
				maintainAspectRatio: true,
				aspectRatio: 1.5,
				interaction: {
					intersect: false,
					mode: 'index'
				},
				plugins: {
					legend: {
						display: true,
						position: 'bottom',
						labels: {
							color: 'rgb(107, 114, 128)',
							font: {
								size: 12,
								family: 'Rethink Sans, sans-serif'
							},
							padding: 15,
							usePointStyle: true,
							pointStyle: 'circle'
						}
					},
					tooltip: {
						backgroundColor: 'rgba(255, 255, 255, 0.95)',
						titleColor: 'rgb(17, 24, 39)',
						bodyColor: 'rgb(55, 65, 81)',
						borderColor: 'rgb(55, 65, 81)',
						borderWidth: 1,
						padding: 12,
						displayColors: true,
						callbacks: {
							label: function (context) {
								let label = context.dataset.label || '';
								if (label) {
									label += ': ';
								}
								if (context.parsed.y !== null) {
									label += '$' + context.parsed.y.toFixed(2);
								}
								return label;
							}
						}
					}
				},
				scales: {
					x: {
						grid: {
							color: 'rgba(55, 65, 81, 0.3)',
							drawBorder: false
						},
						ticks: {
							color: 'rgb(107, 114, 128)',
							font: {
								size: 11,
								family: 'Rethink Sans, sans-serif'
							}
						}
					},
					y: {
						beginAtZero: false,
						grid: {
							color: 'rgba(55, 65, 81, 0.3)',
							drawBorder: false
						},
						ticks: {
							color: 'rgb(107, 114, 128)',
							font: {
								size: 11,
								family: 'Rethink Sans, sans-serif'
							},
							callback: function (value) {
								return '$' + value.toFixed(2);
							}
						}
					}
				}
			}
		});
	}

	onMount(() => {
		createChart();
	});

	$effect(() => {
		// Recreate chart when data changes
		chartData;
		createChart();
	});

	onDestroy(() => {
		if (chart) {
			chart.destroy();
		}
	});
</script>

<div class="chart-container">
	<canvas bind:this={canvas}></canvas>
</div>

<style>
	.chart-container {
		position: relative;
		width: 100%;
		height: auto;
	}
</style>
