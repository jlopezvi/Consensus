
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

  $('#next').on('click', function(){
    if ($('#proposal').val() != "" ) {
        showModal('modal_proposal2');
      }else{
        $('#proposal').css("border-color", "red");
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
    fData.append('concern', $('#concern').val());
    fData.append('proposal', $('#proposal').val());
    fData.append('moreinfo_proposal', $('#moreinfo_proposal').val());
    fData.append('moreinfo_concern', $('#moreinfo_concern').val());
    fData.append('volunteers_goal_num', $('#volunteers_goal_num').val());
    fData.append('supporters_goal_num', 200);
    
    var opt = false;
    if ($('input[name=proposal-anon]').is(":checked"))
        opt = true;
    fData.append('if_author_public', opt);
    
    var first_receivers_emails = '';
    var list_followers = $('#addpro').find('input[type=checkbox]');
    for(var i=0; i< list_followers.length; i++){
    	if(list_followers[i].checked)
    	  first_receivers_emails += list_followers[i].value + ' ';
    }
    fData.append('first_receivers_emails', first_receivers_emails);
    
    if($('#fileUpload').val() != '')
      fData.append('fileUpload', $('#fileUpload')[0].files[0]);
    //var img = $('#fileUpload').val();
  
    
    if ($('#volunteers_goal_num').val() > 0 ) {
      $.ajax({
        url: url[0] + "//" + url[2] + '/add_idea_to_user',
        type: 'POST',
        data: fData,
        processData: false,
        contentType: false,
        success: function (json) {
          alert(json.result_msg);
          window.location = '../home';
          console.log(json);
        },
        error: function(response){
          console.log('Error');
          console.log(response);
        }
      });
    }else{
      $('#volunteers_goal_num').css("border-color", "red");
    }
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
            followerproposal += '<li><input class="checkbox check--followers" type="checkbox" name="check[]" value="'+json.followers_info[i].email+'" checked>';
            followerproposal += '<img src="'+json.followers_info[i].profilepic_url+'">';
            followerproposal += '<p><a href="#">'+json.followers_info[i].username+'</a>';
            followerproposal += '<br>'+json.followers_info[i].fullname+'</p></li>';
            
          }
          $('#addpro').append(followerproposal);
          
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
/*
  $(document).on('click', '.logout__button', function(){
    $('#logout__modal').modal('toggle');
  });
*/
  $(document).on('click', '#accept__logout', function(){
    $.ajax({
      url: url[0] + "//" + url[2] + '/logout',
      type: 'GET',
      success: function (json){
        window.location = '/';
      } 
    });
  });
  
  var red_flag_idea;
  $(document).on('click', '.redflag', function(){
    $('#redflag-modal').modal('toggle');
    red_flag_idea = $(this).parent().parent().parent().parent();
    var proposal = red_flag_idea.children().first().children('input.idea__id').val();
    $('#idea_index').val(proposal);
  });
  
  $('#accept_redflag').on('click', function(){
    var data = { 
      'reason' : $('#reason').val(), 
      'idea_index' : $('#idea_index').val() 
    };
    
    if($('#reason').val() != ''){
      $('#reason').css({'border-color': 'rgb(169, 169, 169)'});
      if(confirm("Are you sure you want to delete this?")){
        $.ajax({
          url: url[0] + "//" + url[2] + '/redflag_idea',
          type: 'POST',
          data: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          },
          dataType: 'json',
          success: function (json) {
            alert(json.result_msg);
            $('#redflag-modal').modal('hide');
            red_flag_idea.remove();
          },
          error: function(response){
            console.log('Error');
            console.log(response);
          }
        });
      }
      else{
        return false;
      }
    } else {
      $('#reason').css({'border-color': '#FF0000'});
    }
    
  });

});

function showModal(id) {
    $('.modal').modal('hide');
    $("#" + id).modal();
  }



  
  
