$(document).ready(function(){
	$('.home--content').css('background-image','url("")');
	var percent = $('#percent').val();
	var total = Math.floor(percent);
	$('.input--percent').append(total + '%');
	var support_percent = $('#supporters--percent').val();
	$('.newsfeed--bar').css('width',support_percent+'%');

	var volunter_percent = $('#volunters--percent').val();
	$('.newsfeed--bar2').css('width',volunter_percent+'%');
});