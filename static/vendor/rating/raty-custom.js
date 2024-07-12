// Rating
$(function () {
	$.fn.raty.defaults.path = "img";
	$("#rate1").raty({ score: 4 });
	$("#rate2").raty({ score: 5 });
	$("#rate3").raty({ score: 5 });
	$("#rate4").raty({ score: 4 });
	$("#rate5").raty({ score: 3 });
	$("#rate6").raty({ score: 2 });

	$(".rate1").raty({ score: 4 });
	$(".rate2").raty({ score: 5 });
	$(".rate3").raty({ score: 5 });
	$(".rate4").raty({ score: 4 });
	$(".rate5").raty({ score: 3 });
	$(".rate6").raty({ score: 2 });

	$(".rateA").raty({ score: 5 });
	$(".rateB").raty({ score: 4 });
	$(".rateC").raty({ score: 3 });
	$(".rateD").raty({ score: 2 });
	$(".rateE").raty({ score: 1 });

	$(".readonly1").raty({ readOnly: true, score: 1 });
	$(".readonly2").raty({ readOnly: true, score: 2 });
	$(".readonly3").raty({ readOnly: true, score: 3 });
	$(".readonly4").raty({ readOnly: true, score: 4 });
	$(".readonly5").raty({ readOnly: true, score: 5 });
});
