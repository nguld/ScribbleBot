var inputText = "";
var delayTimer;

$(document).ready(function() {
	$("input").on('input', function() {
		inputText = $("input").val();
		clearTimeout(delayTimer);
		delayTimer = setTimeout(function() {
			$("input").val("");
			$.post("parse.php"+window.location.search, { input: inputText }).done(function(data) {
				if (data != "") {
					alert(data);
				}
			});
		}, 1500);
	});
});
