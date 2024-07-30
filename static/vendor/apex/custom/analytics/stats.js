// Graph 1
var options1 = {
	series: [80],
	chart: {
		type: "radialBar",
		width: 72,
		height: 72,
		sparkline: {
			enabled: true,
		},
	},
	colors: ["#5b4fb9", "#9196a2", "#66a4ff"],
	dataLabels: {
		enabled: false,
	},
	plotOptions: {
		radialBar: {
			hollow: {
				margin: 0,
				size: "50%",
			},
			track: {
				margin: 0,
			},
			dataLabels: {
				show: false,
			},
		},
	},
};
var chart1 = new ApexCharts(document.querySelector("#radial1"), options1);
chart1.render();

// Graph 2
var options2 = {
	series: [70],
	chart: {
		type: "radialBar",
		width: 72,
		height: 72,
		sparkline: {
			enabled: true,
		},
	},
	colors: ["#7aa748", "#9196a2", "#66a4ff"],
	dataLabels: {
		enabled: false,
	},
	plotOptions: {
		radialBar: {
			hollow: {
				margin: 0,
				size: "50%",
			},
			track: {
				margin: 0,
			},
			dataLabels: {
				show: false,
			},
		},
	},
};
var chart2 = new ApexCharts(document.querySelector("#radial2"), options2);
chart2.render();

// Graph 3
var options3 = {
	series: [60],
	chart: {
		type: "radialBar",
		width: 72,
		height: 72,
		sparkline: {
			enabled: true,
		},
	},
	colors: ["#00a1ff", "#9196a2", "#66a4ff"],
	dataLabels: {
		enabled: false,
	},
	plotOptions: {
		radialBar: {
			hollow: {
				margin: 0,
				size: "50%",
			},
			track: {
				margin: 0,
			},
			dataLabels: {
				show: false,
			},
		},
	},
};
var chart3 = new ApexCharts(document.querySelector("#radial3"), options3);
chart3.render();

// Graph 4
var options4 = {
	series: [50],
	chart: {
		type: "radialBar",
		width: 72,
		height: 72,
		sparkline: {
			enabled: true,
		},
	},
	colors: ["#f27436", "#9196a2", "#66a4ff"],
	dataLabels: {
		enabled: false,
	},
	plotOptions: {
		radialBar: {
			hollow: {
				margin: 0,
				size: "50%",
			},
			track: {
				margin: 0,
			},
			dataLabels: {
				show: false,
			},
		},
	},
};
var chart4 = new ApexCharts(document.querySelector("#radial4"), options4);
chart4.render();
