$(document).ready( function() {
  $('.home--select div').slideUp();
	$('.select--triangle').on('click',function(){
    if( $('.select--options').css('display') == 'block'){
      $('.select--options').slideUp('fast');
      $('.select--triangle').removeClass('active-triangle');
    }
    else {
      $('.select--options').slideDown();
      $('.select--triangle').addClass('active-triangle');
    }
  });
  $('.unselected--option').on('click',function(){
    var current_opt = $('.selected--option').html();
    $('.selected--option').html('').html($(this).html());
    $(this).html('').html(current_opt);
    $('.select--options').slideUp(100);
    $('.select--triangle').removeClass('active-triangle');
  });
  var percent = $('#percent').val();
  var total = Math.floor(percent);
  $('.input--percent').append(total + '%');
  var support_percent = $('#supporters--percent').val();
  $('.newsfeed--bar').css('width',support_percent+'%');

  var volunter_percent = $('#volunters--percent').val();
  $('.newsfeed--bar2').css('width',volunter_percent+'%');

}); 