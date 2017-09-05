var url = window.location.href;
url = url.split("/");
var list;

$(document).ready(function(){
  $('html').css('overflow-y','hidden');
  
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
      console.log(data.idea_proposal);
      console.log(data.vote_ifvolunteered);
      console.log(data.vote_type);
      
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
    $('.newsfeed--name a').empty().append(list[id].author_username);
    $('.newsfeed--duration').removeClass('uknown__user--duration');
  } else {
    $('.duration--info').empty().append(list[id].duration);
    var _html = $('.duration--info').parent();
    _html.remove().clone().insertBefore($('.profile--picture').parent());
    $('.newsfeed--duration').addClass('uknown__user--duration');
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
  if(list[id].supporters_num > 0){
		for(var f=0; f<list[id].supporters_num; f++){
			if(f<=3){
				if(list[id].known_supporters[f].email != 'user')
					support_html += '<a href="/participants/'+list[id].known_supporters[f].email+'"><li>'+list[id].known_supporters[f].username+'</li></a>';
				else
					support_html += '<a href="/participants"><li>'+list[id].known_supporters[f].username+'</li></a>';
			} else {
				if((list[id].supporters_num-4) > 0)
					support_html += '<a href="#" class="last--liked"><li>'+(list[id].supporters_num-4)+' people</li></a>';
				break;
			}
		}
	} else {
		support_html += '<a href="#" class="last--liked"><li>'+list[id].supporters_num+' people</li></a>';
	}
  $('#newsfeed--supporters ul').empty().append(support_html);
  /*
  if(list[id].supporters.length > 0){
    cont = 1;
    for(var i =0; i<list[id].supporters.length; i++){
      if(cont <= 3)
        $('#newsfeed--supporters ul').empty().append("<a href='#'><li>"+list[id].supporters[i].username+"</li></a>");
      cont++;
    }
  }
  if(list[id].supporters.length > 3){
    $('#newsfeed--supporters ul').empty().append("<a href='#' class='last--liked'><li>"+(list[id].supporters.length - 3)+"</li></a>");
  }
  else if(list[id].supporters.length == 0){
    $('#newsfeed--supporters ul').empty().append("<a href='#' class='last--liked'><li>0 people</li></a>");
  }
  */
  /****************************************** Add Supporters to the Supporters List ****************************************/
  var reject_html = '';
  if(list[id].rejectors_num > 0){
		for(var f=0; f<list[id].rejectors_num; f++){
			if(f<=3){
				if(list[id].known_rejectors[f].email != 'user')
					reject_html += '<a href="/participants/'+list[id].known_rejectors[f].email+'"><li>'+list[id].known_rejectors[f].username+'</li></a>';
				else
					reject_html += '<a href="/participants"><li>'+list[id].known_rejectors[f].username+'</li></a>';
			} else {
				if((list[id].rejectors_num-4) > 0)
					reject_html += '<a href="#" class="last--liked"><li>'+(list[id].rejectors_num-4)+' people</li></a>';
				break;
			}
		}
	} else {
		reject_html += '<a href="#" class="last--liked"><li>'+list[id].rejectors_num+' people</li></a>';
	}
  $('#newsfeed--rejectors ul').empty().append(reject_html);
  /*
  if(list[id].rejectors.length > 0){
    cont = 1;
    for(var i=0; i<list[id].rejectors.length; i++){
      if(cont <= 3)
        $('#newsfeed--rejectors ul').empty().append("<a href='#'><li>"+list[id].rejectors[i].username+"</li></a>");
      cont++;
    }
  }
  if(list[id].rejectors.length > 3){
    $('#newsfeed--rejectors ul').empty().append("<a href='#' class='last--liked'><li>"+(list[id].rejectors.length - 3)+"</li></a>");
  }
  else if(list[id].rejectors.length == 0){
    $('#newsfeed--rejectors ul').empty().append("<a href='#' class='last--liked'><li>0 people</li></a>");
  }
  */
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
  if(list.length > 0){
    if(list.length == 1){
      $('#newsfeed__body').hide();
      $('.spinner').show();
      showContent(0);
      setTimeout(function(){
        $('#newsfeed__body').show();
        $('.spinner').hide();
      }, 2500);
      $('.arrow__newsfeed__right').hide();
      $('.arrow__newsfeed__left').hide();
    } else if(id == (list.length-1)) {
      moveFeed('left__feed', id);
    } else {
      moveFeed('right__feed', id);
    }
  } else {
    setTimeout(function(){
      window.location = '/home';
    }, 6000);
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

