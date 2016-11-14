var url = window.location.href;
url = url.split("/");

$(document).ready(function(){
	$('.home--content').css('background-image','url("")');
	$('#nav--home').css('display', 'none');
	$('#nav--participants').css('display', 'none');
	$('#nav--top_ten').css('display', 'none');
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
        console.log(json);
        $('.newsfeed--name a').append(json.author_username);
        $('.duration--info').append(json.duration);
        var support_percent = (json.supporters_num * 100)/ json.supporters_goal_num;
        $('.newsfeed--bar').css('width',support_percent+'%');
	    var volunter_percent = (json.volunteers_num * 100)/ json.volunteers_goal_num;
	    $('.newsfeed--bar2').css('width',volunter_percent+'%');
	    $('.newsfeed--goals p').append(json.supporters_num+"/"+json.supporters_goal_num+" supporters goals<br>"+json.volunteers_num+"/"+json.volunteers_goal_num+" volunteers goals");
        $('.newsfeed--problem').append(json.concern);
        $('.newsfeed--proposal').append(json.proposal);
        var total = ((json.supporters.length * 100) / (json.supporters.length + json.rejectors.length));
        if((json.supporters.length + json.rejectors.length) == 0)
          total = 0;
        $('.input--percent label').append('Support Rate: '+Math.floor(total)+'%');
        /****************************************** Add Supporters to the Supporters List ****************************************/
        if(json.supporters.length > 0){
          for(var i =0; i<=2; i++){
            $('#newsfeed--supporters ul').append("<a href='#'><li>"+json.supporters[i].username+"</li></a>");
          }
        }
        if(json.supporters.length > 3){
          $('#newsfeed--supporters ul').append("<a href='#' class='last--liked'><li>"+(json.supporters.length - 3)+"</li></a>");
        }
        else if(json.supporters.length == 0){
          $('#newsfeed--supporters ul').append("<a href='#' class='last--liked'><li>0 people</li></a>");
        }
        /****************************************** Add Supporters to the Supporters List ****************************************/
        if(json.supporters.rejectors > 0){
          for(var i =0; i<=2; i++){
            $('#newsfeed--rejectors ul').append("<a href='#'><li>"+json.rejectors[i].username+"</li></a>");
          }
        }
        if(json.rejectors.length > 3){
          $('#newsfeed--rejectors ul').append("<a href='#' class='last--liked'><li>"+(json.rejectors.length - 3)+"</li></a>");
        }
        else if(json.rejectors.length == 0){
          $('#newsfeed--rejectors ul').append("<a href='#' class='last--liked'><li>0 people</li></a>");
        }
      },
      error: function(response){
        if(response.responseText == "redirect to Home"){
          alert("Redirecting to Home");
          window.location = '/home';
        }
      }
    });
});