var options = {
	chart: {
		height: 320,
		type: "bar",
		toolbar: {
			show: false,
		},
	},
	plotOptions: {
		bar: {
			horizontal: false,
			columnWidth: "70px",
			distributed: true,
			borderRadius: 30,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		show: true,
		width: 1,
		colors: ["#8ec9db", "#5b4fb9", "#8ec9db", "#5b4fb9", "#8ec9db"],
	},
	series: [
		{
			name: "New",
			data: [2000, 3000, 4000, 5000],
		},
	],
	legend: {
		show: false,
	},
	xaxis: {
		categories: ["Sales", "Visits", "Income", "Revenue"],
	},
	yaxis: {
		show: false,
	},
	fill: {
		opacity: 1,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return +val;
			},
		},
	},
	grid: {
		borderColor: "#ccd2da",
		strokeDashArray: 3,
		xaxis: {
			lines: {
				show: true,
			},
		},
		yaxis: {
			lines: {
				show: false,
			},
		},
		padding: {
			top: 0,
			right: 0,
			bottom: 0,
			left: 20,
		},
	},
	colors: ["#8ec9db", "#5b4fb9", "#8ec9db", "#5b4fb9", "#8ec9db"],
};
var chart = new ApexCharts(document.querySelector("#sales"), options);
chart.render();
