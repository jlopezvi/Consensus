$(document).ready(function(){
	$('.home--content').css('background-image','url("")');
	var percent = $('#percent').val();
	var total = Math.floor(percent);
	$('#percent').val(total + '%');
	$('#newsfeed--progress .newsfeed--bar').css('width',$('#supporters--percent').val()+'%');

});