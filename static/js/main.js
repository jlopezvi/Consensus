
var url = window.location.href;
url = url.split("/");

$(document).ready(function(){
	$('.menu--mobile--icon').addClass('close');
	$('.menu--mobile--icon').on('click',function(){
		if($('.menu--mobile--icon').hasClass('close')) {
			$('.nav--style ul li a').css('display','block');
			$('.menu--mobile--icon').removeClass('close');
			$('.menu--mobile--icon').addClass('open');
		}else {
			$('.nav--style ul li a').css('display','none');
			$('.menu--mobile--icon').addClass('close');
			$('.menu--mobile--icon').removeClass('open');
		}
	});
	  $('.next--proposal1').on('click',function(){
    $('#modal_proposal1').css('visibility','hidden');
  });
  /** check all ***/
  $('#select_all').on('click',function(){ 
      $("#select_none").removeClass('check-selection'); 
      $(this).addClass("check-selection");
      $('.addproposal--step2').find('.check--followers').prop('checked',true);
  });
  $('#select_none').on('click',function(){ 
      $("#select_all").removeClass('check-selection');
      $(this).addClass("check-selection");
      $("#select_all").prop('checked', true); 
      $('.addproposal--step2').find('.check--followers').each(function(){
          $(this).prop('checked',false);
      });
  });
  /** end of check all  ***/

  $(document).on('click', '.add--proposal--provisional', function(){

    fData = new FormData();
    fData.append('volunteers_goal_num', $('#volunteers_goal_num').val());
    fData.append('concern', $('#concern').val());
    fData.append('proposal', $('#proposal').val());
    fData.append('moreinfo_proposal', $('#moreinfo_proposal').val());
    fData.append('moreinfo_concern', $('#moreinfo_concern').val());
    fData.append('volunteers_goal_num', $('#volunteers_goal_num').val());
    fData.append('supporters_goal_num', 200);
    
    if($('#fileUpload').val() != '')
      fData.append('fileUpload', $('#fileUpload')[0].files[0]);
    console.log(fData.get('fileUpload'));
    $.ajax({
      url: url[0] + "//" + url[2] + '/add_idea_to_user',
      type: 'POST',
      data: fData,
      processData: false,
      contentType: false,
      success: function (json) {
        //console.log(json);
        if(json.result != 'OK'){
          console.log('entre '+url[3]);
          if(url[3] == 'participants'){
            var count = $('.participant__active--p').children().first().text();
            count++;
            $('.participant__active--p').children().first().text(count);
            var newIdea = '';
            newIdea += '<div class="col-sm-12"><div class="row home--header"><div class="col-sm-2" style="padding-left: 0px;margin-left: -15px;">';
            newIdea += '<div class="home--profile--picture"><img src=""></div></div><div class="col-sm-1 home--name">';
            newIdea += '<a href="#">'+$('.participant__name').children('a').text()+'</a></div><div class="col-sm-2 newsfeed--duration">';
            newIdea += '<p><img style="width: 15px;position: relative;top: -3px;" src="static/images/clock-icon.png">&nbsp;0</p>';
            newIdea += '</div><div class="col-sm-3 home--charge"><div class="progress home--progress">';
            newIdea += '<input type="text" value="'+0*100/1+'" id="supporters--percent" hidden>';
            newIdea += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div></div>';
            newIdea += '<div class="progress home--progress2"><input type="text" value="'+0*100/1+'" id="volunters--percent" hidden>';
            newIdea += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div></div></div>';
            newIdea += '<input type="button" name="more-info" class="home--button"></div></div></div>';
            newIdea += '<div class="row newsfeed--persons"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
            newIdea += '<img src=""></div><div class="col-sm-11 newsfeed--likes">';
            newIdea += '<ul><a href="#" class="last--liked"><li>'+0+' people</li></a></ul></div></div>';
            newIdea += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="static/images/x-small.png">';
            newIdea += '</div><div class="col-sm-11 newsfeed--likes"><ul><a href="#"><li>'+0+'</li></a></ul></div></div></div>';
            newIdea += '<div class="row home--share"><div class="col-sm-12 home--share--icons"><div class="col-sm-6" style="padding:0;width: 100%;">';
            newIdea += '<img src="static/images/x-icon.png"><img style="width: 50px;" src="static/images/check-icon.png"><img style="width: 48px;" src="static/images/checkmark.png">';
            newIdea += '<img style="width: 50px;" src="static/images/ignore-icon.png"></div><div class="col-sm-6 home--followers" style="width: 100%;"><i class="fa fa-share-alt"></i>';
            newIdea += '<p>Share with: followers</p></div></div></div></div>';
            $('.participant__newsfeed').prepend(newIdea);  
          }
        } else {
          alert(json.result_msg);
        }
      },
      error: function(response){
        console.log(response);
      }
    });
  });

  var current_email = $('#host_email').val();
  $.ajax({
      url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
      type: 'GET',
      success: function (json){
        //console.log(json);
        if(json.followers_num > 0){
          followerproposal = '';  
          for(var i = 0; i < json.followers_num; i++){
            followerproposal += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
            followerproposal += '<img src="'+json.followers_info[i].profilepic_url+'">';
            followerproposal += '<p><a href="#">'+json.followers_info[i].username+'</a>';
            followerproposal += '<br>'+json.followers_info[i].fullname+'</p></li>';
            
          }
          $('#addpro ul').append(followerproposal);
          
        }
      } 
    });

  $("#fileUpload").on('change', function () {

        if (typeof (FileReader) != "undefined") {

            var image_holder = $("#image-holder");
            image_holder.empty();

            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "thumb-image"
                }).appendTo(image_holder);

            }
            image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } else {
            alert("This browser does not support FileReader.");
        }
    });

  $(document).on('click', '.logout__button', function(){
    $('#logout__modal').modal('toggle');
  });

  $(document).on('click', '#accept__logout', function(){
    $.ajax({
      url: url[0] + "//" + url[2] + '/logout',
      type: 'GET',
      success: function (json){
        window.location = '/';
      } 
    });
  });

});

function showModal(id) {
    $('.modal').modal('hide');
    $("#" + id).modal();

  }



  
  
