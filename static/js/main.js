var default_bimage = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA8EAAAIWCAMAAABA2n8RAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA0ppVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8wMy8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6M0ZEMjgwODk3QTEwMTFFNjg3OENFQ0Y5MThEQUNBMTYiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6M0ZEMjgwODg3QTEwMTFFNjg3OENFQ0Y5MThEQUNBMTYiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDowZDNiYWM4My03YTEwLTExZTYtYmQ5ZS1mMWRhMzk4NDE3MTciIHN0UmVmOmRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDowZDNiYWM4My03YTEwLTExZTYtYmQ5ZS1mMWRhMzk4NDE3MTciLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+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';
var _if_newsfeed = false;
var url = window.location.href;
url = url.split("/");

$(document).ready(function(){
  
  $('#proposal').bind("cut copy paste",function(e) {
    e.preventDefault();
  });
  
  var characterReg = /[#$%&\{\}\[\]\\\/]/gi;
  $('#proposal').bind("keyup keydown", function(event){		
  	var inputVal = $(this).val();		
  	if(characterReg.test(inputVal)) {			
  		$(this).val(inputVal.replace(/[#$%&\{\}\[\]\\\/]/gi,''));			
  	}
	});
  
  if(url[3] != ''){
    $.ajax({
      url: url[0] + "//" + url[2] + '/if_ideas_for_newsfeed',
      type: 'GET',
      success: function (json){
        _if_newsfeed = json.result;
        if(_if_newsfeed)
          $('#middle--home--button').attr('href', '/newsfeed');
      } 
    });
  }
  
  $('#defultimg__bimage').attr('src', default_bimage);
  
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
    
    var newData = {
      'concern': $('#concern').val(),
      'proposal': $('#proposal').val(),
      'moreinfo_proposal': $('#moreinfo_proposal').val(),
      'moreinfo_concern': $('#moreinfo_concern').val(),
      'volunteers_goal_num': parseInt($('#volunteers_goal_num').val()),
      'supporters_goal_num': 200
    };
    
    var opt = false;
    if ($('input[name=proposal-anon]').is(":checked"))
        opt = true;
    newData['if_author_public'] = opt;
    
    var first_receivers_emails = [];
    var list_followers = $('#addpro').find('input[type=checkbox]');
    for(var i=0; i< list_followers.length; i++){
    	if(list_followers[i].checked)
    	  first_receivers_emails.push(list_followers[i].value);
    }
    newData['first_receivers_emails'] = first_receivers_emails;
    
    //newData['image'] = $('#defultimg__bimage').attr('src');
    newData['image'] = null;
    if($('#cropme_bidea img').length)
      newData['image'] = $('#cropme_bidea img').attr('src');
    
    //console.log(newData);
    if ($('#volunteers_goal_num').val() >= 0 ) {
      $.ajax({
        url: url[0] + "//" + url[2] + '/add_idea_to_user',
        type: 'POST',
        data: JSON.stringify(newData),
        headers: {
          'Content-Type': 'application/json'
        },
        dataType: 'json',
        success: function (json) {
          alert(json.result_msg);
          window.location = '../home';
          //console.log(json);
        },
        error: function(response){
          //console.log('Error');
          //console.log(response);
        }
      });
    }else{
      $('#volunteers_goal_num').css("border-color", "red");
    }
  });

  var current_email = $('#host_email').val();
  if(url[3] == 'newsfeed' || url[3] == 'participants' || url[3] == 'home' || url[3] == 'topten'){
    $.ajax({
      url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
      type: 'GET',
      success: function (json){
        ////console.log(json);
        if(json.followers_num > 0){
          followerproposal = '';  
          for(var i = 0; i < json.followers_num; i++){
            followerproposal += '<li><input class="checkbox check--followers" type="checkbox" name="check[]" value="'+json.followers_info[i].email+'" checked>';
            followerproposal += '<img class="new--user--icon--login" src="'+json.followers_info[i].profilepic_url+'">';
            followerproposal += '<p><a href="#">'+json.followers_info[i].username+'</a>';
            followerproposal += '<br>'+json.followers_info[i].fullname+'</p></li>';
            
          }
          $('#addpro').append(followerproposal);
          
        }
      } 
    });
  }

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
            if(url[3] == 'participants'){
              red_flag_idea.remove();
              var active_p = $('.participant__active--p .activess').html();
              $('.participant__active--p .activess').html(active_p-1);
            } else if(url[3] == 'topten'){
              red_flag_idea.remove();
              location.reload();
            } else if(url[3] == 'newsfeed'){
                var id_newsfeed = $('#list__id').val();
                removeElementFromList(id_newsfeed);
                if(list.length == 0){
                  $('.spinner').show();
                  var answer = '<br><br>There are no more ideas left! <br>Redirecting to <strong>Home</strong>';
                  $('#invitation-modal-info p#modal--invitation').empty().append(answer);
                  $('#invitation-modal-info').modal('toggle');
                }
            }
          },
          error: function(response){
            //console.log('Error');
            //console.log(response);
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
  
  $(document).on('click', '.add--proposal--button', function(){
    $('.edit--proposal--hint').hide();
		$('#modal_proposal1').find('h4.modal-title').html('Add Proposal (1/3)');
		$('#modal_proposal2').find('h4.modal-title').html('Add Proposal (2/3)');
		$('#modal_proposal3').find('h4.modal-title').html('Add Proposal (3/3)');
		$('#modal_proposal3').find('.modal-prev > button').attr("onclick", "showModal('modal_proposal2')");
  	$('.add--proposal--provisional').show();
  	$('.edit--proposal--provisional').hide();
  	$('#modal_proposal2 .modal-body').css('height', '');
  	$('#modal_proposal2 .modal-body').children().children().first().show();
  	$('#modal_proposal2 .modal-body').children().children().first().next().show();
  	
  	$('input#proposal').val('');
  	$('input#concern').val('');
  	$('textarea#moreinfo_proposal').val('');
  	$('textarea#moreinfo_concern').val('');
  	$('input#volunteers_goal_num').val(0);
  	$('#cropme_bidea img').remove();
  });

});

function showModal(id) {
    $('.modal').modal('hide');
    $("#" + id).modal();
  }



  
  
