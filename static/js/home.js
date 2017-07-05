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
    var type_vote = $(this).attr('id');
    $('.selected--option').html('').html($(this).html());
    $(this).html('').html(current_opt);
    $('.select--options').slideUp(100);
    $('.select--triangle').removeClass('active-triangle');
    
    $('#home--proposals').empty();
    loadHomeIdeas(type_vote);
  });
  
  var percent = $('#percent').val();
  var total = Math.floor(percent);
  $('.input--percent').append(total + '%');
  var support_percent = $('#supporters--percent').val();
  $('.newsfeed--bar').css('width',support_percent+'%');

  var volunter_percent = $('#volunters--percent').val();
  $('.newsfeed--bar2').css('width',volunter_percent+'%');
  
  loadHomeIdeas('supported');

}); 

function loadHomeIdeas(type_vote){
  $.ajax({
    url: url[0] + "//" + url[2] + '/ideas_for_home',
    type: 'POST',
    data: JSON.stringify({'vote_type': type_vote}),
    headers: {
      'Content-Type': 'application/json'
    },
    success: function(json){
      console.log(json.data);
      for(i=0; i<json.data.length;i++){
        showIdeas(json.data[i]);
      }
    },
    error: function(response){
      console.log('error');
      console.log(response);
    }
	});
}

function showIdeas(list){
  var code = '';
  code += '<div class="col-sm-6 home--content--proposal">';
  code += '<div class="row home--header">';
	code += '<div class="col-sm-2" style="padding-left: 0px;">';
	code += '<div class="home--profile--picture"><img src="'+list.author_photo_url+'"></div></div>';
	code += '<div class="col-sm-1 home--name"><a href="#">'+list.author_username+'</a></div>';
	code += '<div class="col-sm-2 newsfeed--duration">';
	code += '<p><img style="width: 19px;position: relative;top: -3px;" src="/static/images/clock-icon.png">&nbsp;';
	code += list.duration+'</p></div>';
	code += '<div class="col-sm-3 home--charge"><div class="progress home--progress">';
	code += '<input type="text" value="'+(list.supporters_num*100)/list.supporters_goal_num+'" id="supporters--percent" hidden>';
	code += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div>';
	code += '</div>	<div class="progress home--progress2">';
	code += '<input type="text" value="'+(list.volunteers_num*100)/list.volunteers_goal_num+'" id="volunters--percent" hidden>';
	code += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div>';
	code += '</div></div><div class="col-sm-4 newsfeed--goals">';
	code += '<p>'+list.supporters_num+'/'+list.supporters_goal_num+' supporters goals<br>';
	code += '<p>'+list.volunteers_num+'/'+list.volunteers_goal_num+' volunteers goals<br>';
	code += '</div></div><div class="row home--proposals--body"><div class="col-sm-12">';
	code += '	<div class="col-sm-8 newsfeed--problem">'+list.concern+'</div>';
	code += '</div><div class="col-sm-12" style="margin-top: 180px;"><div class="col-sm-8 col-sm-offset-4 newsfeed--proposal">'+list.proposal+'</div></div>';
	code += '</div><div class="row newsfeed--footer">';
	code += '<div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;"><div class="col-sm-1 redflag--img">';
	code += '<img src="/static/images/redflag.png"></div><div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
	code += '<input type="text" value="" id="percent" hidden>';
	code += '<div class="input--percent"><label>	Support Rate: </label></div>';
	code += '</div>	<div class="col-sm-2 neewsfeed--moreinfo" style="float:right;"><input type="button" name="more-info" class="home--button">';
	code += '</div></div></div><div class="row newsfeed--persons"><div class="col-sm-12">';
	code += '<div class="col-sm-1" style="padding:0;"><img src="/static/images/check-small.png"></div>';
	code += '<div class="col-sm-11 newsfeed--likes"><ul>';
	if(list.supporters.length > 0){
    cont = 1;
    for(var i=0; i<list.supporters.length; i++){
      if(cont <= 3)
        code += '<a href="#"><li>'+list.supporters[i].username+'</li></a>';
      cont++;
    }
  }
  if(list.supporters.length > 3){
    code += '<a href="#" class="last--liked"><li>+ '+(list.supporters.length-3)+' people</li></a>';
  }
  else if(list.supporters.length == 0){
    code += '<a href="#" class="last--liked"><li>0 people</li></a>';
  }
	code += '</ul></div></div><div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="/static/images/x-small.png"></div>';
	code += '<div class="col-sm-11 newsfeed--likes"><ul>';
	if(list.rejectors.length > 0){
    cont = 1;
    for(var i=0; i<list.rejectors.length; i++){
      if(cont <= 3)
        code += '<a href="#"><li>'+list.rejectors[i].username+'</li></a>';
      cont++;
    }
  }
  if(list.rejectors.length > 3){
    code += '<a href="#" class="last--liked"><li>+ '+(list.rejectors.length-3)+' people</li></a>';
  }
  else if(list.rejectors.length == 0){
    code += '<a href="#" class="last--liked"><li>0 people</li></a>';
  }
  code += '</ul></div></div></div><div class="row home--share"><div class="col-sm-12 home--share--icons">';
	code += '<div class="col-sm-6" style="padding:0;"><img src="/static/images/x-icon.png">';
	code += '<img style="width: 50px;" src="/static/images/check-icon.png"><img style="width: 48px;" src="/static/images/checkmark.png">';
	code += '</div><div class="col-sm-6 home--followers"><i class="fa fa-share-alt"></i><p>Share with: followers</p></div></div></div></div>';
	
	$('#home--proposals').append(code);
}