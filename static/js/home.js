var url = window.location.href;
url = url.split("/");
var list;

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
    
    $('#home--proposals').empty().hide();
    loadHomeIdeas(type_vote);
  });
  
  loadHomeIdeas('supported');
  
  $(document).on('click', '.home--share--button', function(){
    var vote_type = $(this).attr('id');
    var index_idea = $(this).parent().children('input').val();
    var vote_ifvolunteered = false;
    if(vote_type == 'supported-plus'){
      vote_ifvolunteered = true;
      vote_type = 'supported';
    }
    var element = $(this).parent().parent().parent();
      
    var data = {
      'idea_proposal': list[index_idea]['proposal'],
      'vote_ifvolunteered': vote_ifvolunteered,
      'vote_type': vote_type
    };
      
    $.ajax({
      url: url[0] + "//" + url[2] + '/vote_on_idea',
      type: 'POST',
      data: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function(json){
        //console.log(json);
        if(data.vote_type == 'supported' || data.vote_type == 'supported-plus')
          var answer = 'Now you are supporting this idea!';
        else
          var answer = 'Idea rejected successfully!';
        if(json.result == 'OK: User vote was modified'){
          $('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
          $('#invitation-modal-info p#modal--invitation').empty().append(answer);
          element.fadeOut('slow', function(){ element.remove(); });
        } else if (json.result == 'Wrong: User vote exists of same type'){
          $('#invitation-modal-info h4.modal-title').empty().append('Error');
          $('#invitation-modal-info p#modal--invitation').empty().append('You can not vote the same for this idea.');
        }
        $('#invitation-modal-info').modal('toggle');
      },
      error: function(response){
        console.log('error');
        console.log(response);
      }
  	});
  });

}); 

function loadHomeIdeas(type_vote){
  $('.spinner').show();
  $.ajax({
    url: url[0] + "//" + url[2] + '/ideas_for_home',
    type: 'POST',
    data: JSON.stringify({'vote_type': type_vote}),
    headers: {
      'Content-Type': 'application/json'
    },
    success: function(json){
      //console.log(json.data);
      list = json.data;
      for(i=0; i<json.data.length;i++){
        showIdeas(json.data[i], i);
      }
      setTimeout(function(){
        $('#home--proposals').show();
        $('.spinner').hide();
      }, 2500);
    },
    error: function(response){
      console.log('error');
      console.log(response);
    }
	});
}

function showIdeas(list, index){
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
	var support_percent = (list.supporters_num*100)/list.supporters_goal_num;
	code += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+support_percent+'%"></div>';
	code += '</div>	<div class="progress home--progress2">';
	var volunter_percent = (list.volunteers_num*100)/list.volunteers_goal_num;
	code += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunter_percent+'%"></div>';
	code += '</div></div><div class="col-sm-4 newsfeed--goals">';
	code += '<p>'+list.supporters_num+'/'+list.supporters_goal_num+' supporters goals<br>';
	code += '<p>'+list.volunteers_num+'/'+list.volunteers_goal_num+' volunteers goals<br>';
	code += '</div></div><div class="row home--proposals--body" style="background-image: url('+list.image_url+');">';
	code += '<div class="col-sm-12"><div class="col-sm-8 newsfeed--problem">'+list.concern+'</div>';
	code += '</div><div class="col-sm-12" style="margin-top: 180px;"><div class="col-sm-8 col-sm-offset-4 newsfeed--proposal">'+list.proposal+'</div></div>';
	code += '</div><div class="row newsfeed--footer">';
	code += '<div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;"><div class="col-sm-1 redflag--img">';
	code += '<img src="/static/images/redflag.png"></div><div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
  var percent = (list.supporters.length * 100)/(list.supporters.length + list.rejectors.length);
  var total = Math.floor(percent);
	code += '<div class="input--percent"><label>	Support Rate: '+total+'%</label></div>';
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
  code += '</ul></div></div></div><div class="row home--share"><div class="col-sm-6 home--share--icons">';
  code += '<input type="hidden" class="index--idea" value="'+index+'"';
	code += '<div class="col-sm-6" style="padding:0;">';
	code += '<img src="/static/images/x-icon.png" class="home--share--button" id="rejected">';
	code += '<img style="width: 50px;" src="/static/images/check-icon.png" class="home--share--button" id="supported">';
	code += '<img style="width: 48px;" src="/static/images/checkmark.png" class="home--share--button" id="supported-plus">';
	code += '</div><div class="col-sm-6 home--followers"><i class="fa fa-share-alt"></i><p>Share with: followers</p></div></div></div></div>';
	
	$('#home--proposals').append(code);
}