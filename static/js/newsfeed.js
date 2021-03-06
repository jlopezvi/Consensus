var url = window.location.href;
url = url.split("/");
var list;

$(document).ready(function(){
  
	$('.home--content').css('background-image','url("")');
	$('#nav--home').css('display', 'none');
	$('#nav--participants').css('display', 'none');
	$('#nav--top_ten').css('display', 'none');
	$('.menu--mobile--icon').css('display', 'none');
	$('.add--proposal--button').css('display', 'none');
	$('#middle--home--button').on('click', function(e){
      e.preventDefault();
	});
	
	
	$.ajax({
    url: url[0] + "//" + url[2] + '/ideas_for_newsfeed',
    type: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    dataType: 'json',
    success: function(json) {
      list = json.data;
      //console.log(list.length);
      $('#list__id').val(0);
      if(list.length == 0){
        window.location = '/home';
      }
      if(list.length > 1){
        $('.arrow__newsfeed__right').show();
      }
      showContent(0);
      setTimeout(function(){
	      $('#newsfeed__body').show();
	      $('.spinner').hide();
      }, 4000);
    },
    error: function(response){
      if(response.responseText == "redirect to Home"){
        alert("Redirecting to Home");
        window.location = '/home';
      }
    }
  });
  
  $(document).on('click', '.glyphicon', function(){
    var side = $(this).attr('id');
    var id = $('#list__id').val();
    moveFeed(side, id);
  });
  
  $(document).on('click', '.vote__idea--button', function(){
      var vote_ifvolunteered = false;
      var type = $(this).attr('id');
      if(type == 'support__plus--button'){
        vote_ifvolunteered = true;
        type = 'supported';
      }
      var id = $('#list__id').val();
      
      var data = {
        'idea_proposal': $(document).find('.idea__id').val(),
        'vote_ifvolunteered': vote_ifvolunteered,
        'vote_type': type
      };
      //console.log(data.idea_proposal);
      //console.log(data.vote_ifvolunteered);
      //console.log(data.vote_type);
      
      removeElementFromList(id);
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
          $('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
          if(data.vote_type == 'supported')
            var answer = 'Now you are supporting this idea!';
          else if(data.vote_type == 'rejected')
            var answer = 'Idea rejected successfully!';
          else
            var answer = 'You ignored this idea!';
          if(list.length == 0)
            answer += '<br><br>There are no more ideas left! <br>Redirecting to <strong>Home</strong>';
          if(json.result == 'OK: User vote was created')
            $('#invitation-modal-info p#modal--invitation').empty().append(answer);
          $('#invitation-modal-info').modal('toggle');
        },
        error: function(response){
          console.log('error');
          console.log(response);
        }
    	});
  });
});

function showContent(id){
  $('#list__id').val(id);
  $('.idea__id').val(list[id].proposal);
  //console.log(list[id]);
  
  $('.duration--info').empty().append(list[id].duration);
  if(list[id].if_author_public){
    $('#picture__profile').attr('src', list[id].author_profilepic_url).show();
    $('.newsfeed--name a').empty().append(list[id].author_username).show();
    $('.newsfeed--name a').attr('href', '/participants/'+list[id].author_email);
    $('.newsfeed--duration').removeClass('uknown__user--duration');
    var _html = $('.duration--info').parent();
    _html.remove().clone().insertAfter($('.newsfeed--name'));
    $('.newsfeed--name').css('visibility','visible');
  } else {
    $('#picture__profile').attr('src', list[id].author_profilepic_url).hide();
    $('.duration--info').empty().append(list[id].duration);
    var _html = $('.duration--info').parent();
    _html.remove().clone().insertBefore($('.profile--picture').parent());
    $('.newsfeed--duration').addClass('uknown__user--duration');
    $('.newsfeed--name').css('visibility','hidden');
  }
  
  $('.newsfeed--body').css('background-image', 'url('+list[id].image_url+')');
  var support_percent = (list[id].supporters_num * 100)/ list[id].supporters_goal_num;
  $('.newsfeed--bar').css('width',support_percent+'%');
  var volunter_percent = (list[id].volunteers_num * 100)/ list[id].volunteers_goal_num;
  if (list[id].volunteers_goal_num == "" || list[id].volunteers_goal_num == 0) {
    $('.newsfeed--progress2').hide();
    $('#support__plus--button').hide();
    $('.newsfeed--charge, .newsfeed--goals').addClass('one--progress__bar');
  } else {
    $('.newsfeed--progress2').show();
    $('#support__plus--button').show();
    $('.newsfeed--charge, .newsfeed--goals').removeClass('one--progress__bar');
  }
  $('.newsfeed--bar2').css('width',volunter_percent+'%');
  $('.newsfeed--goals p').empty().append(list[id].supporters_num+"/"+list[id].supporters_goal_num+" supporters<br>"+list[id].volunteers_num+"/"+list[id].volunteers_goal_num+" volunteers");
  if (list[id].volunteers_goal_num == "" || list[id].volunteers_goal_num == 0) {
    $('.newsfeed--goals p').empty().append(list[id].supporters_num+"/"+list[id].supporters_goal_num+" supporters");
  }
  $('.newsfeed--problem').empty().append(list[id].concern);
  $('.newsfeed--proposal').empty().append(list[id].proposal);
  $('#more--info--modal').empty().append('<p><h4>  More information about the problem: </h4> '+list[id].moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+list[id].moreinfo_proposal+'</p>');
  $('.input--percent label').empty().append('Support Rate: '+list[id].support_rate+'%');
  /****************************************** Add Supporters to the Supporters List ****************************************/
  var support_html = '';
  if(list[id].identified_supporters.length > 0){
		for(var f=0; f<list[id].identified_supporters.length; f++){
			if(list[id].identified_supporters[f].email != 'user')
				support_html += '<a href="/participants/'+list[id].identified_supporters[f].email+'"><li>'+list[id].identified_supporters[f].username+'</li></a>';
			else
				support_html += '<a href="/participants"><li>'+list[id].identified_supporters[f].username+'</li></a>';
		}
	}
	support_html += '<a style="margin-left: 10px;" href="#" class="last--liked"><li>'+list[id].unidentified_supporters_text+'</li></a>';
  $('#newsfeed--supporters ul').empty().append(support_html);
  
  /****************************************** Add Supporters to the Supporters List ****************************************/
  var reject_html = '';
  if(list[id].identified_rejectors.length > 0){
		for(var f=0; f<list[id].identified_rejectors.length; f++){
			if(list[id].identified_rejectors[f].email != 'user')
				reject_html += '<a style="margin-left: 10px;" href="/participants/'+list[id].identified_rejectors[f].email+'"><li>'+list[id].identified_rejectors[f].username+'</li></a>';
			else
				reject_html += '<a style="margin-left: 10px;" href="/participants"><li>'+list[id].identified_rejectors[f].username+'</li></a>';
		}
  }
  reject_html += '<a style="margin-left: 10px;" href="#" class="last--liked"><li>'+list[id].unidentified_rejectors_text+'</li></a>';
  $('#newsfeed--rejectors ul').empty().append(reject_html);
}

function moveFeed(element, id){
  var intID = parseInt(id);
  if((element == 'left__feed') && (id > 0)){
    $('#newsfeed__body').hide();
    $('.spinner').show();
    showContent(intID-1);
    setTimeout(function(){
      $('#newsfeed__body').show();
      $('.spinner').hide();
    }, 2500);
    if(id == 1)
      $('#'+element).hide();
    else
      $('#'+element).show();
  } else if((id < (list.length-1))){
    $('#newsfeed__body').hide();
    $('.spinner').show();
    
    $('#left__feed').show();
    showContent(intID+1);
    setTimeout(function(){
      $('#newsfeed__body').show();
      $('.spinner').hide();
    }, 2500);
    
    if(id == (list.length-2))
      $('#'+element).hide();
    else
      $('#'+element).show();
  }
}

function removeElementFromList(id){
  list.splice(id,1);
  //console.log(list);
  if(list.length > 0){
    $('#newsfeed__body').hide();
    $('.spinner').show();
    showContent(0);
    setTimeout(function(){
      $('#newsfeed__body').show();
      $('.spinner').hide();
    }, 2500);
    $('.arrow__newsfeed__right').hide();
    $('.arrow__newsfeed__left').hide();
  } else {
    setTimeout(function(){
      window.location = '/home';
    }, 4000);
  }
}
$(document).ready(function(){
  $('input[name=more-info]').on('click', function(){
    $('#more--info--modal').slideToggle('slow');
    //if(modal.css('display') == 'none')
    //  modal.slideDown('slow');
    //else
  }); 
  $('.vote--on').on('click',function(){
    $('.vote--on span').toggleClass('rotated');
	  $('.newsfeed--share').toggleClass('displayShare');
	  $('.newsfeed--share--icons img').toggleClass('displayVote');
  });
});

