// Chart 1
var options1 = {
	chart: {
		height: 100,
		width: 250,
		type: "line",
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
		width: 5,
	},
	series: [
		{
			name: "Orders",
			data: [5, 10, 30, 15, 35, 25, 45],
		},
	],
	grid: {
		show: false,
	},
	xaxis: {
		categories: ["S", "M", "T", "W", "T", "F", "S"],
	},
	yaxis: {
		labels: {
			show: false,
		},
	},
	colors: ["#f27436", "#9196a2", "#66a4ff"],
	markers: {
		show: false,
	},
};
var chart1 = new ApexCharts(document.querySelector("#orders1"), options1);
chart1.render();

// Chart 2
var options2 = {
	chart: {
		height: 100,
		width: 250,
		type: "line",
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
		width: 5,
	},
	series: [
		{
			name: "Orders",
			data: [5, 10, 30, 15, 35, 25, 45],
		},
	],
	grid: {
		show: false,
	},
	xaxis: {
		categories: ["S", "M", "T", "W", "T", "F", "S"],
	},
	yaxis: {
		labels: {
			show: false,
		},
	},
	colors: ["#5b4fb9", "#9196a2", "#66a4ff"],
	markers: {
		show: false,
	},
};
var chart2 = new ApexCharts(document.querySelector("#orders2"), options2);
chart2.render();
