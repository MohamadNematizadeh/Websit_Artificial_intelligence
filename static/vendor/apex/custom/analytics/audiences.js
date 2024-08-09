var options = {
	series: [40, 70],
	chart: {
		height: 320,
		type: "radialBar",
	},
	plotOptions: {
		radialBar: {
			hollow: {
				margin: 2,
				size: "5%",
			},
			dataLabels: {
				name: {
					fontSize: "22px",
				},
				value: {
					fontSize: "16px",
				},
				total: {
					show: true,
					label: "Total",
					formatter: function (w) {
						// By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
						return 350;
					},
				},
			},
		},
	},
	labels: ["New", "Subscribed"],
	colors: ["#5b4fb9", "#8ec9db"],
};

var chart = new ApexCharts(document.querySelector("#audiences"), options);
chart.render();
