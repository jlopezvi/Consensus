var url = window.location.href;
url = url.split("/");
var current_vote = '';
$('.cropme2').simpleCropper();
var img_validator;


$(document).ready( function() {
	
	if($('#participant_email').val() == 'None')
		var current_email = $('#host_email').val();
	else {
		var current_email = $('#participant_email').val();
		$('.setting__adapt').hide();
		$('.participant__invite').hide();
		$('#follow-parti').hide();
    	$('#unfollow-parti').hide();
    	$('#newIdea').css('margin-top', '90px');
	}
	
	//GET ALL INFORMATION OF ALL IDEAS CREATED BY PARTICIPANT
	function getIdeasCreatedByParticipant(){
		$.ajax({
			url: url[0] + "//" + url[2] + '/get_ideas_data_created_by_participant/'+current_email,
			type: 'GET',
			success: function (json) {	
				
				////console.log(json);
				var bars_wo_user = '';
				var newIdea = '';
				var url_new = url[0] +'//'+ url[2] +'/static/';
				for (var i = 0; i < json.ideas_data.length; i++) {
					newIdea += '<div class="col-sm-12" style="margin-top:25px;"><div class="row home--header home--header2">';
					newIdea += '<input type="hidden" class="idea__id" value="'+json.ideas_data[i].proposal+'">';
					// IF IDEA DOESNT HAVE ANONYMOUS AUTHOR 
					if(json.ideas_data[i].if_author_public){
						bars_wo_user = 'right: -40px;';
						newIdea += '<div class="col-sm-1" style="padding-left: 0px;">';
						newIdea += '<div class="home--profile--picture"><img class="img-circle new--user--icon--login" id="img-modify" src="'+json.ideas_data[i].author_profilepic_url+'"></div></div><div class="col-sm-3 home--name">';
						newIdea += '<a href="#" id="name--modify">'+json.ideas_data[i].author_username+'</a>';
						newIdea += '</div><div class="col-sm-3 newsfeed--duration participant__duration"><p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">';
						newIdea += '<p class="duration--info">'+json.ideas_data[i].duration+'</p></p></div>';
					
					} else {
						newIdea += '<div class="col-sm-3 newsfeed--duration"><p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">';
						newIdea += '<p class="duration--info">'+json.ideas_data[i].duration+'</p></p></div>';
						newIdea += '<div class="col-sm-1" style="padding-left: 0px;"></div>';
						newIdea += '<div class="col-sm-3 home--name"></div>';
					}
					
					
					var supporters_percent = json.ideas_data[i].supporters_num*100/json.ideas_data[i].supporters_goal_num;
					if (json.ideas_data[i].volunteers_goal_num > 0) {
						newIdea += '<div class="col-sm-3 home--charge"><div class="progress home--progress home--new--bars">';
						newIdea += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
						newIdea += '<div class="progress home--progress2 home--new--bars">';
					}else{
						newIdea += '<div class="col-sm-3 home--charge" style="top: 19px!important;"><div class="progress home--progress home--new--bars">';
						newIdea += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
						newIdea += '<div>';
					}
					var volunteers_percent = json.ideas_data[i].volunteers_num*100/json.ideas_data[i].volunteers_goal_num;
					newIdea += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunteers_percent+'%;"></div></div></div>';
					
					if (json.ideas_data[i].volunteers_goal_num > 0) {
						newIdea += '<div class="col-sm-3 newsfeed--goals newsfeed--goals2" style="'+bars_wo_user+'"><p>'+json.ideas_data[i].supporters_num+'/'+json.ideas_data[i].supporters_goal_num+' supporters';
						newIdea += '<br>'+json.ideas_data[i].volunteers_num+'/'+json.ideas_data[i].volunteers_goal_num+' volunteers';
						newIdea += '</p></div></div><div class="row home--proposals--body home--proposals--body2" style="background-image: url('+json.ideas_data[i].image_url+'); padding-top:47.40%;"><div class="col-sm-12 concern__div">';
					} else {
						newIdea += '<div class="col-sm-3 newsfeed--goals newsfeed--goals2" style="top: 12px!important;'+bars_wo_user+'"><p>'+json.ideas_data[i].supporters_num+'/'+json.ideas_data[i].supporters_goal_num+' supporters';
						newIdea += '</p></div></div><div class="row home--proposals--body home--proposals--body2" style="background-image: url('+json.ideas_data[i].image_url+'); padding-top:47.40%;"><div class="col-sm-12 concern__div">';
						
					}
					
					newIdea += '<div class="col-sm-11 newsfeed--problem">'+json.ideas_data[i].concern+'</div></div><div class="col-sm-12">';
					newIdea += '<div class="col-sm-11 col-sm-offset-1 newsfeed--proposal">'+json.ideas_data[i].proposal+'</div></div></div> <input type="hidden" value="'+json.ideas_data[i].idea_id+'" id="idea__id">';
					newIdea += '<div class="row newsfeed--footer"><div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;">';
					newIdea += '<div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
					
					newIdea += '<input type="text" value="'+json.ideas_data[i].support_rate+'" id="percent" hidden><div class="input--percent">';
					newIdea += '<label> Support Rate: '+json.ideas_data[i].support_rate+'% </label></div></div>';
					newIdea += '<div class="col-sm-1 redflag--img"><input type="hidden" class="id" value="'+json.ideas_data[i].proposal+'"><img class="redflag" src="'+url_new+'images/redflag.png"></div>';
					newIdea += '<div class="col-sm-2 neewsfeed--moreinfo" style="float:right;">';
					newIdea += '<input type="button" name="more-info" class="home--button"></div><div id="more--info--modal" hidden><p><h4>  More information about the problem: </h4> '+json.ideas_data[i].moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+json.ideas_data[i].moreinfo_proposal+'</p></div></div></div>';
					
					if(url.length == 4)
						newIdea += '<div class="row home--share home--share2" style="top: -18px;"><div class="col-sm-12 home--share--icons">';
					else
						newIdea += '<div class="row home--share home--share2" style="top: -29px;"><div class="col-sm-12 home--share--icons">';
					newIdea += '<input type="hidden" class="supporters--input" value="'+json.ideas_data[i].supporters_num+'">';
					newIdea += '<input type="hidden" class="volunteers--input" value="'+json.ideas_data[i].volunteers_num+'">';
					newIdea += '<input type="hidden" class="rejectors--input" value="'+json.ideas_data[i].identified_rejectors.length+'">';
					newIdea += '<input type="hidden" class="supporters--goal--input" value="'+json.ideas_data[i].supporters_goal_num+'">';
					newIdea += '<input type="hidden" class="volunteers--goal--input" value="'+json.ideas_data[i].volunteers_goal_num+'">';
					newIdea += '<div class="col-sm-6" style="padding:0;width: 100%;"><input type="hidden" class="id" value="'+json.ideas_data[i].proposal+'">';
					//MODIFY / DELETE IDEA, ONLY FOR CURRENT LOGGED USER
					if(url.length == 4){
						newIdea += '<div class="col-sm-12 idea--action--buttons"><div class="col-xs-1"><span class="glyphicon glyphicon-edit edit" style="top: 10px;"></span></div>';
		    			newIdea += '<div class="col-xs-1"><span class="glyphicon glyphicon-trash trash"  style="top: 10px;"></span></div></div>';
					}
					//newIdea += '<img class="icons icons2" src="'+url_new+'images/x-icon.png" id="rejected" hidden><img class="icons icons2" style="width: 50px;" src="'+url_new+'images/check-icon.png" id="supported" hidden>';
					newIdea += '<div id="rejected" class="icons icons2 icons2__participant" style="display:none;"></div>';
					newIdea += '<div id="supported" class="icons icons2 icons2__participant" style="display:none;margin-left: 10px;"></div>';
					if (json.ideas_data[i].volunteers_goal_num > 0) {
						//newIdea += '<img class="icons icons2" style="width: 48px;" src="'+url_new+'images/checkmark.png" id="support__plus--button" hidden>';
						newIdea += '<div id="support__plus--button" class="icons icons2 icons2__participant" style="display:none;"></div>';
					}
					
					if(url.length != 4)
						newIdea += '<div class="row newsfeed--persons" style="top:0px;"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
					else
						newIdea += '<div class="row newsfeed--persons newsfeed--persons2" style="top:10px;"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
					newIdea += '<img src="'+url_new+'images/check-hover.png"></div><div class="col-sm-11 newsfeed--likes">';
					newIdea += '<ul class="ul--liked" style="left:0;">';
					if(json.ideas_data[i].identified_supporters.length > 0){
						for(var f=0; f<json.ideas_data[i].identified_supporters.length; f++){
							if(json.ideas_data[i].identified_supporters[f].email != 'user')
								newIdea += '<a href="/participants/'+json.ideas_data[i].identified_supporters[f].email+'"><li>'+json.ideas_data[i].identified_supporters[f].username+'</li></a>';
							else
								newIdea += '<a href="/participants"><li>'+json.ideas_data[i].identified_supporters[f].username+'</li></a>';
						}
					}
					newIdea += '<a href="#" class="last--liked"><li>'+json.ideas_data[i].unidentified_supporters_text+'</li></a>';
					
					newIdea += '</ul></div></div>';
					newIdea += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="'+url_new+'images/reject-hover.png">';
					newIdea += '</div><div class="col-sm-11 newsfeed--likes"><ul class="ul--disliked" style="left:0;">';
					if(json.ideas_data[i].identified_rejectors.length > 0){
						for(var f=0; f<json.ideas_data[i].identified_rejectors.length; f++){
							if(json.ideas_data[i].identified_rejectors[f].email != 'user')
								newIdea += '<a href="/participants/'+json.ideas_data[i].identified_rejectors[f].email+'"><li>'+json.ideas_data[i].identified_rejectors[f].username+'</li></a>';
							else
								newIdea += '<a href="/participants"><li>'+json.ideas_data[i].identified_rejectors[f].username+'</li></a>';
						}
					} 
					newIdea += '<a href="#" class="last--liked"><li>'+json.ideas_data[i].unidentified_rejectors_text+'</li></a>';
					
					newIdea += '</ul></div></div></div>';
					
				    newIdea += '</div><div class="col-sm-6 home--followers hidden" style="width: 100%;">';
				    newIdea += '</div></div></div></div>';
			    }
			    if (json.ifallowed == false) {
			    	$('#newIdea').append('<center><h3>User private</h3></center> ');  	
			    }else if($('#participant_email').val() != 'None' && json.ideas_data.length == 0){
			    	$('#newIdea').append('<center><h3>this user has no active publications</h3></center> ');
			    }else if (json.ideas_data.length != 0) {
			    	$('#newIdea').append(newIdea);
			    }else{
			    	$('#newIdea').append('<center><h3>You have no active publications</h3></center> ');
			    }
			    if($('#participant_email').val() != 'None' ){
			    	$('.icons').show();
			    	$('.home--followers').append('<i class="fa fa-share-alt"></i><p>Share with: followers</p>');
			    }
				
				var left = 1;
	  			$(document).on('click', '.neewsfeed--moreinfo', function(){
	          		$(this).next('div').slideToggle('slow');
	   			});	
	   			
			}	
		});
	}
	getIdeasCreatedByParticipant();

	//GET ALL INFORMATION OF CURRENT LOGGED USER OR SEARCHED
	function getCurrentUserInfo(){
		$.ajax({
			url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+current_email,
			type: 'GET',
			success: function (json) {
				////console.log(json);
				$('.profile--picture img').attr('src', json.participant_data.profilepic_url);
				$('.participant__name a').empty().append(json.participant_data.username);
				$('.participant__name label').empty().append(json.participant_data.fullname);
				$('.participant__active--p').children().first().empty().append(json.participant_data.ideas_num);
				$('.participant__following').children().first().empty().append(json.participant_data.followings_num);
				$('.participant__followers').children().first().empty().append(json.participant_data.followers_num);
			}	
		});
	}
	getCurrentUserInfo();
	
	//GET ALL FOLLOWERS OF CURRENT LOGGED USER OR SEARCHED
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
		type: 'GET',
		success: function (json) {
				////console.log(json);
				if (json.ifallowed == false) {
					$('#menu1 ul').append('<center><h3 >User private</h3></center>');
				}else{		
				followerList = '';	
				for(var i = 0; i < json.followers_num; i++){
					followerList += '<li>';
					var _if_show = 'inline';
					if(url.length > 4)
						_if_show = 'none';
					followerList += '<input value="'+json.followers_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]" style="display:'+_if_show+';">';
					followerList += '<img class="new--user--icon--login" src="'+json.followers_info[i].profilepic_url+'">'
					followerList += '<p><a href="#">'+json.followers_info[i].username+'</a>';					
					followerList += '<br>'+json.followers_info[i].fullname+'</p></li>';
				}
				if ($('#participant_email').val() != 'None' && json.followers_num == 0){
					$('#menu1 ul').append('<center><h3 >this user has no followers</h3></center>');
				}else if (json.followers_num != 0) {
					$('#menu1 ul').append(followerList);
				}else{
					$('#menu1 ul').append('<center><h3 >No one is following you</h3></center>');
				}					
			}
		}

	});

	//GET ALL FOLLOWINGS OF CURRENT LOGGED USER OR SEARCHED
	
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followings_info/'+current_email,
		type: 'GET',
		success: function (json) {
			////console.log(json);
				if (json.ifallowed == false){
					$('#home ul').append('<center><h3>User private</h3></center>');
				}else{
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li>';
					var _if_show = 'inline';
					if(url.length > 4)
						_if_show = 'none';
					followingList += '<input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]" style="display:'+_if_show+';">';
					followingList += '<img class="new--user--icon--login" src="'+json.followings_info[i].profilepic_url+'">';
					followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';					
					followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
				}
				if ($('#participant_email').val() != 'None' && json.followings_num == 0){
					$('#home ul').append('<center><h3 >this user has no followings</h3></center>');
				}else if (json.followings_num != 0) {
					$('#home ul').append(followingList);
				}else{
					$('#home ul').append('<center><h3 id="msg">You are following no one</h3></center>');
				}
			}					
		}	
	});
    
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_all_public_participants_for_user',
		type: 'GET',
		headers: {
		'Content-Type': 'application/json'
		},
		dataType: 'json',
		success: function(json) {
			////console.log(json);
	       	for (var i = 0; i < json.length; i++) {
	       		if_following = '';
	       		if(json[i].if_following)
	       			if_following = 'value="Unfollow"';
	       		else
	       			if_following = 'value="Follow"';
	       		newParti = '';
	       		newParti += '<li><img class="new--user--icon--login" src="'+json[i].profilepic_url+'"><p>'; 
	       		newParti += '<a href="#">'+json[i].fullname+'</a>';
	       		newParti += '<br><label>'+json[i].position+'</label></p>';
	       		newParti += '<input type="hidden" value="'+json[i].email+'">';
	       		newParti += '<input class="form-control invite__button" type="button" '+if_following+' id="btn-follow"></li>';

	       		if (json[i].group == 'Governing Board') {
	       			$('.governing').show();
	       			$('.governing').append(newParti);
	       		}	
	       		if (json[i].group == 'Marketing') {
	       			$('.marketing').show();
	       			$('.marketing').append(newParti);
	       		}	
	       		if (json[i].group == 'Sales') {
	       			$('.sales').show();
	       			$('.sales').append(newParti);
	       		}	
	       		if (json[i].group == 'Technical') {
	       			$('.technical').show();
	       			$('.technical').append(newParti);
	       		}	
	       		if (json[i].group == 'Human Resources') {
	       			$('.human').show();
	       			$('.human').append(newParti);
	       		}	

	       	}
	       	////console.log(newParti);
		}
	});

	$('body').removeClass('container').addClass('container-fluid');
	
	$(document).on('click', '#send_invitation-btn', function(){
		$('.span--error').remove();
		var guest_email = $('#emails_input').val().split(", ");
		var host_email = $('#host_email').val();
		var msg = '';
		var validation = false;
		if(guest_email != ''){
			for(var i=0; i<guest_email.length; i++){
				////console.log(guest_email[i]);
				if( !isValidEmailAddress( guest_email[i] ) ) {
					validation = true;
					break;
				}
			}
		} else
			validation = true;
		if(validation){
			$('#emails_input').css('border-color', '#FF0000').after('<span class="span--error"><br>All emails must be valid!</span>');
		}else{
			$('#send_invitation-btn').prop('disabled', true);
			$('#emails_input').css('border-color', 'rgb(169, 169, 169)');
			for(var i=0; i<guest_email.length; i++){
				$.ajax({
					url: url[0] + "//" + url[2] + '/registration_send_invitation/'+host_email+'/'+guest_email[i],
					type: 'GET'
				});
				msg += '<br><strong>'+guest_email[i]+'</strong>';
			}
			setTimeout(function(){
				$('#send_invitation-btn').prop('disabled', false);
				$('.modal-title').empty().append('Success!!');
				$('.modal-body p#modal--invitation').empty().append('An email with an invitation sent to:'+msg);
				$('#invitation-modal-info').modal('toggle');
			},3000);
		}
	});

	$('#search-input-participant').on('keydown', function(e){
		var code = e.which;
		var search = $('#search-input-participant').val();
		if(code == 13){
			e.preventDefault();
			seaarch_participant(search);
		} else if(code == 8){
			showHideGroups();
			$('.addproposal--step__div ul').find('li.participants__li__private').remove();
			$('#legend__results').remove();
		}
	});

	$('#search-input-participant').on('focus', function(){
		change_view('search');
	});

	$(document).on('click', '.btn__search', function(e){
		e.preventDefault();
		change_view('search');
		var search = $('#search-input-participant').val();
		seaarch_participant(search);
	});

	$(document).on('click', '.back__button', function(){
		change_view('participant');
	});

	$(document).on('click', '#btn-follow', function(){
		var type = $(this).val();
		var user = $(this).prev().val();
		follow_unfollow_participant(type, user);
		if(type == 'Follow')
			$(this).val('Unfollow');
		else
			$(this).val('Follow');
	});	

	$("#change-photo").on('change', function () {
        if (typeof (FileReader) != "undefined") {

            var image_holder = $("#image--holder");
            image_holder.empty();

            var reader = new FileReader();
            reader.onload = function (e) {
                $("<img />", {
                    "src": e.target.result,
                    "class": "new--user--icon--login img-circle"
                }).appendTo(image_holder);
            }       	
            image_holder.show();
            reader.readAsDataURL($(this)[0].files[0]);
        } else {
            alert("This browser does not support FileReader.");
        }
    });
    
    $(document).on('click', '.addproposal--step2 li a', function(e){
    	e.preventDefault();
    	var redirect = $(this).parent().parent().children('input').val();
    	if($(this).parent().parent().hasClass('participants__li__private'))
    		//console.log('Not Allowed');
    	else if($('#host_email').val() == redirect)
    		window.location = '/participants';
    	else
    		window.location = '/participants/'+redirect;

    });

    $(document).on('click', '.public--all', function(){
    	$('#Public--profile').prop("checked", true);
    	$('#Supporting--proposals--visible').prop("checked", true);
    	$('#Rejecting--proposals--visible').prop("checked", true);
    	$('.private__prof').prop("checked", false);
    });

    $(document).on('click', '.private__prof', function(){
    	$('#Public--profile').prop("checked", false);
    	$('#Supporting--proposals--visible').prop("checked", false);
    	$('#Rejecting--proposals--visible').prop("checked", false);
    	$('.public--all').prop("checked", false);
    });

    $.ajax({
		url: url[0] + "//" + url[2] + '/get_user_data',
		type: 'GET',
		headers: {
		'Content-Type': 'application/json'
		},
		dataType: 'json',
		success: function (json) {
			////console.log(json.data);
			$('#p_fullname').val(''+json.data.fullname+'');
			$('#p_username').val(''+json.data.username+'');
			$('#p_email').val(''+json.data.email+'');
			$('#p_confirm-e').val(''+json.data.email+'');
			$('#p_position').val(''+json.data.position+'');
			$('#p_group').val(''+json.data.group+'');
			$('#cropme_profile_edit').append('<img src='+json.data.profilepic_url+'>');
			img_validator = json.data.profilepic_url;
			if(json.data.ifpublicprofile)
				$('#Public--profile').prop('checked', true);
			if(json.data.ifrejectingproposalsvisible)
				$('#Rejecting--proposals--visible').prop('checked', true);
			if(json.data.ifsupportingproposalsvisible)
				$('#Supporting--proposals--visible').prop('checked', true);
		}					
				
	});

    $(document).on('click', '#modify--user', function(){
    	
      	optionpro = false;
      	if($('#Public--profile').is(":checked"))
      		optionpro = true;
      		
		optionSup = false;
      	if($('#Supporting--proposals--visible').is(":checked"))
      		optionSup = true;
      		
		optionRej = false;
      	if($('#Rejecting--proposals--visible').is(":checked"))
      		optionRej = true;
      	
      	var newdata = {
      		'fullname' : $('#p_fullname').val(),
      		'username' : $('#p_username').val(),
      		'new_email' : $('#p_email').val(),
      		'position' : $('#p_position').val(),
      		'group' : $('#p_group option:selected').val(),
      		'ifpublicprofile' : optionpro,
      		'ifsupportingproposalsvisible' : optionSup,
      		'ifrejectingproposalsvisible' : optionRej,
      	};
      	
   		if($('#cropme_profile_edit img').attr('src') != img_validator){
      		newdata['profilepic'] = $('#cropme_profile_edit img').attr('src');
    	}
    	if ($('#p_email').val() == $('#p_confirm-e').val()) {
	      	$('#loader--general').show();
    		$.ajax({
		      url: url[0] + "//" + url[2] + '/modify_user_data/'+current_email,
		      type: 'PUT',
		      data: JSON.stringify(newdata),
		      headers: {
		          'Content-Type': 'application/json'
		      },
		      dataType: 'json',
		      success: function (json) {
		      	$('.close').click();
		      	alert('Edition Completed!');
     	    	location.reload(true);
		      	getCurrentUserInfo();
		        $('.participant__newsfeed').empty();
			    getIdeasCreatedByParticipant();
			    var timer = 3000;
		      	setTimeout(function(){
			        if($('#cropme_profile_edit img').attr('src') != img_validator){
			        	$('.participant__profile--pic div img').prop('src', newdata['profilepic']);
			        	$('.home--profile--picture img').attr('src', newdata['profilepic']);
			        	timer = 5000;
			        }
			        $('#loader--general').hide();
			        $('#modify-user').modal('toggle');
		      	}, timer);
		        /*
		        if($('#cropme_profile_edit img').attr('src') != img_validator){
		        	$('.participant__profile--pic div img').prop('src',newdata['profilepic']);
		        	img_validator = newdata['profilepic'];
		        }
		        */
		      },
		      error: function(response){
		        //console.log(response);
		      }
		    });
    	}else{
    		$('#p_confirm-e').css('border-color', 'red');
    	}
		

     });

    $(document).on('click', '.trash', function(){
    	$('#delete-idea').modal('toggle');
    	var propuestaid = $(this).parent().parent().parent().children().val();
    	$('#delete_idea').next('input').val(propuestaid);
    	$(this).parent().parent().parent().parent().parent().parent().addClass('this-idea');
    });

    $(document).on('click', '#delete_idea', function(){
    	var proposal = {
    		'proposal' : $(this).next('input').val()
    	}
    	var activepub = parseInt($('.activess').text());
    	$.ajax({
			url: url[0] + "//" + url[2] + '/remove_idea',
			type: 'DELETE',
		    data: JSON.stringify(proposal),
		    headers: {
		        'Content-Type': 'application/json'
		    },
		    dataType: 'json',
			success: function (json) {
				alert(json.result_msg);
				$('.close').click();
				$('.this-idea').remove();
				$('.activess').empty();	
				$('.activess').append(activepub-1);
				var vali = parseInt($('.activess').text());
				if (vali <= 0) {
					$('#newIdea').append('<center><h3>You have no active publications</h3></center>');
				}

			}	
		});

    });

    $(document).on('click', '#accept_modify_', function(){
    	setTimeout(function(){
	    	$.ajax({
				url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+current_email,
				type: 'GET',
				success: function (json) {
					////console.log(json);
					$('.profile--picture img').attr('src', '');
					$('.participant__name a').empty();
					$('.participant__name label').empty();
					$('#name--modify').empty();
					$('#img-modify').attr('src', '');
					$('.profile--picture img').attr('src', json.participant_data.profilepic_url);
					$('.participant__name a').append(json.participant_data.username);
					$('.participant__name label').append(json.participant_data.fullname);
					$('#name--modify').append(json.participant_data.username);
					$('#img-modify').attr('src', json.participant_data.profilepic_url);
					img_validator = json.participant_data.profilepic_url;
				}	
			});
    	}, 3000);
    });
    
    $(document).on('click', '.edit', function(){
    	var propid = $(this).parent().parent().parent().children().val();
    	$.ajax({
		url: url[0] + "//" + url[2] + '/get_idea_node_data/'+propid,
		type: 'GET',
		headers: {
		'Content-Type': 'application/json'
		},
		dataType: 'json',
		success: function (json) {
			////console.log(json);
			$('#concern').val(''+json.concern+'');
			$('#proposal').val(''+json.proposal+'');
			$('#moreinfo_concern').val(''+json.moreinfo_concern+'');
			$('#moreinfo_proposal').val(''+json.moreinfo_proposal+'');
			$('#volunteers_goal_num').val(''+json.volunteers_goal_num+'');
			$('#cropme_bidea').empty();
			$('#cropme_bidea').append('<img style="width: 300px; height: 169px;" src='+json.image_url+'>');
			}							
		});
		
		$('.edit--proposal--hint').show();
		$('#modal_proposal1').find('h4.modal-title').html('Edit Proposal (1/3)');
		$('#modal_proposal2').find('h4.modal-title').html('Edit Proposal (2/3)');
		$('#modal_proposal3').find('h4.modal-title').html('Edit Proposal (3/3)');
		$('#modal_proposal3').find('.modal-prev > button').attr("onclick", "showModal('modal_proposal2')");
    	$('#modal_proposal1').modal('toggle');
    	$('#modal_proposal2 .modal-body').css('height', '220px');
    	$('#modal_proposal2 .modal-body').children().children().first().hide();
    	$('#modal_proposal2 .modal-body').children().children().first().next().hide();

    	$('.add--proposal--provisional').hide();
    	$('.edit--proposal--provisional').show();
    	$('.controlss').append('<input type="hidden" id="propoid" value="'+propid+'">')
    });

    $(document).on('click', '.edit--proposal--provisional', function(){
     	var propuestaid = $('#propoid').val(); 
     	var dataedit = {
  			'concern': $('#concern').val(),
  			'moreinfo_proposal': $('#moreinfo_proposal').val(),
  			'moreinfo_concern': $('#moreinfo_concern').val(),
  			'volunteers_goal_num': $('#volunteers_goal_num').val(),
  			'supporters_goal_num': 200
		};    
		dataedit['current_proposal'] = propuestaid;
		if ($('#proposal').val() != propuestaid) {
			dataedit['proposal'] = $('#proposal').val();
		}		
		var opt = false;
		if ($('input[name=proposal-anon]').is(":checked") == true){
    		opt = true;
		}
   	 	dataedit['if_author_public'] = opt;
    	
    	//dataedit['image'] = null;
    	if(!$('#cropme_bidea img').attr('style')){
      		dataedit['image'] = $('#cropme_bidea img').attr('src');
    	}

      	if ($('#volunteers_goal_num').val() >= 0 ) {
     	$.ajax({
     	   url: url[0] + "//" + url[2] + '/modify_idea',
     	   type: 'PUT',
     	   data: JSON.stringify(dataedit),
     	   headers: {
     	     'Content-Type': 'application/json'
     	   },
     	   dataType: 'json',
     	   success: function (json) {
     	     alert(json.result_msg);
			 //window.location = '../home';
     	     $('.close').click();
     	     location.reload(true);
     	     
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
    
    $(document).on('click', '.update--password', function(){
    	$('#message--modify').remove();
    	$('#newpass').val('');
    	$('#con--newpass').val('');
    	$('#oldpass').val('');
    });
    
    $(document).on('click', '#accept_modify_password', function(){
    	$('#message--modify').remove();
    	 newPass = {
    		'old_password': $('#oldpass').val(),
    		'new_password': $('#newpass').val()
    	}
    	
    	if ($('#newpass').val() != '' || $('#con--newpass').val() != '' || $('#oldpass').val() != ''){
	    	if ($('#newpass').val() == $('#con--newpass').val()) {
	    		$.ajax({
		     	   url: url[0] + "//" + url[2] + '/modify_user_password',
		     	   type: 'PUT',
		     	   data: JSON.stringify(newPass),
		     	   headers: {
		     	     'Content-Type': 'application/json'
		     	   },
		     	   dataType: 'json',
		     	   success: function (json) {
		     	   	if (json.result == 'OK') {
		     	   		alert('your password has been changed');
		     	   		$('.close').click();
		     	   		$('#message--modify').remove();
		     	   	}else{
		     	   		$('<span id="message--modify">Old password incorrect</span>').insertAfter('#last--div');
		     	   	}
		     	    	 
		     	   },
		     	   error: function(response){
		     	     //console.log('Error');
		     	     //console.log(response);
		     	   }
		     	});
	    	}else{
	      		$('<span id="message--modify">New password and Confirm password does not match</span>').insertAfter('#last--div');
	    	}
    	} else {
    		$('<span id="message--modify">Password must not be empty</span>').insertAfter('#last--div');
    	}
    });

    $(document).on('click', '.icons', function(){
    	var element = $(this);
    	var vote_ifvolunteered = false;
    	var type = $(this).attr('id');
       	if(type == 'support__plus--button'){
        	vote_ifvolunteered = true;
        	type = 'supported';
      	}
      	var id = $(this).parent().children('input').val();
      	var data_input = {
      		'idea_proposal': id,
        	'vote_ifvolunteered': vote_ifvolunteered,
        	'vote_type': type
      	};
        	
    	/********* GET CURRENT VALUE OF VOTE IF DIFERENT OF SAME TYPE **********/
		$.ajax({
			url: url[0] + "//" + url[2] + '/get_voting_rel_between_user_and_idea/'+data_input.idea_proposal,
			type: 'GET',
			success: function(data){
      			////console.log(data);
				if(data.result == 'OK' && ((data.vote_ifvolunteered) && (data.vote_type == 'supported')))
					current_vote = 'volunteer';
				else if(data.result == 'OK' && ((!data.vote_ifvolunteered) && (data.vote_type == 'supported')))
					current_vote = 'supported';
				else if(data.result == 'OK' && data.vote_type == 'rejected')
					current_vote = 'rejected';
				else
					current_vote = 'ignored';
					
				$.ajax({
			        url: url[0] + "//" + url[2] + '/vote_on_idea',
			        type: 'POST',
			        data: JSON.stringify(data_input),
			        headers: {
			          'Content-Type': 'application/json'
			        },
			        dataType: 'json',
			        success: function(json){   	
			        	var div_header = element.parent().parent().parent().siblings('.home--header');
			        	var div_persons = element.parent().parent().parent().siblings('.newsfeed--persons');
			        	var div_footer = element.parent().parent().parent().siblings('.newsfeed--footer');
		        		
		        		if (json.result != 'Wrong: User vote exists of same type'){
		        			
		        			$.ajax({
						        url: url[0] + "//" + url[2] + '/get_idea_data_for_user/'+data_input.idea_proposal,
						        type: 'GET',
						        success: function(json){
						        	////console.log(json);
						        	var supp_percent = json.idea_data.supporters_num*100/json.idea_data.supporters_goal_num;
						        	var volunt_percent = json.idea_data.volunteers_num*100/json.idea_data.volunteers_goal_num;
						        	div_header.children('.newsfeed--goals').children('p').html('<p>'+json.idea_data.supporters_num+'/'+json.idea_data.supporters_goal_num+' supporters<br>'+json.idea_data.volunteers_num+'/'+json.idea_data.volunteers_goal_num+' volunteers</p>');
						        	div_header.children('.home--charge').children('.home--progress').children().css('width', supp_percent+'%');
						        	div_header.children('.home--charge').children('.home--progress2').children().css('width', volunt_percent+'%');
						        	div_footer.find('.input--percent').children('label').html(' Support Rate: '+json.idea_data.support_rate+'% ');
						        	
						        	var ideaChanged = '';
						        	if(json.idea_data.identified_supporters.length > 0){
										for(var f=0; f<json.idea_data.identified_supporters.length; f++){
											if(json.idea_data.identified_supporters[f].email != 'user')
												ideaChanged += '<a href="/participants/'+json.idea_data.identified_supporters[f].email+'"><li>'+json.idea_data.identified_supporters[f].username+'</li></a>';
											else
												ideaChanged += '<a href="/participants"><li>'+json.idea_data.identified_supporters[f].username+'</li></a>';
										}
						        	}
									ideaChanged += '<a href="#" class="last--liked"><li>'+json.idea_data.unidentified_supporters_text+'</li></a>';
									div_persons.find('.ul--liked').html(ideaChanged);
									
									ideaChanged = '';
						        	if(json.idea_data.identified_rejectors.length > 0){
										for(var f=0; f<json.idea_data.identified_rejectors.length; f++){
											if(json.idea_data.identified_rejectors[f].email != 'user')
												ideaChanged += '<a href="/participants/'+json.idea_data.identified_rejectors[f].email+'"><li>'+json.idea_data.identified_rejectors[f].username+'</li></a>';
											else
												ideaChanged += '<a href="/participants"><li>'+json.idea_data.identified_rejectors[f].username+'</li></a>';
										}
									} 
									ideaChanged += '<a href="#" class="last--liked"><li>'+json.idea_data.unidentified_rejectors_text+'</li></a>';
									div_persons.find('.ul--disliked').html(ideaChanged);
						        	
						        },
						        error: function(response){
						        	//console.log('error');
						        	//console.log(response);
						        }
		        			});
		        			
		        			if(vote_ifvolunteered){
		        				var answer = 'Now you are  <b>Volunteer</b> for this idea';
		        			} else {
		        				var answer = 'Now you are  <b>'+type+'</b> for this idea';
		        			}
		        		
			        		$('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
			      			$('#invitation-modal-info p#modal--invitation').empty().append(answer); 
		        		} else {
		        			$('#invitation-modal-info h4.modal-title').empty().append('Error');
			      			$('#invitation-modal-info p#modal--invitation').empty().append('You can not vote the same for this idea.');
		        		}
		        		$('#invitation-modal-info').modal('toggle');

			        },
			        error: function(response){
			          //console.log('error');
			          //console.log(response);
			        }
		        });
			},
			error: function(response){
				//console.log('error');
				//console.log(response);
			}
		});
    });
});

function seaarch_participant(search){
	var div = $('.addproposal--step__div ul');
	$('#legend__results').remove();
	$('.addproposal--step__div ul').find('li.participants__li__private').remove();
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+search,
		type: 'GET',
		success: function (json) {
			////console.log(json);
			var _exists = false;
			$('.addproposal--step2').find('legend').find('li input').each(function(){
				if($(this).val() == json.participant_data.id)
					return _exists = true;
			});
			if(json.result == 'OK'){
				$('.spinner').show();
				var newAppend = '';
            	newAppend += '<li class="participants__li__private">';
            	newAppend += '<img class="new--user--icon--login" src="'+json.participant_data.profilepic_url+'"><p>';
            	newAppend += '<a href="#">'+json.participant_data.fullname+'</a>'; 
            	newAppend += '<br>'+json.participant_data.position+'</p>';
            	newAppend += '<input type="hidden" value="'+json.participant_data.id+'">';
            	if($('#host_email').val() != search)
                	newAppend += '<input class="form-control invite__button" type="button" value="Follow" id="btn-follow"></li>';
                else
                	newAppend += '<input class="form-control invite__button" type="button" value="It´s you" disabled></li>';
                
                setTimeout(function(){
                	$('.spinner').hide();
					$('.addproposal--step__div ul').find('li.participants__li__private').remove();	
					
	            	if (json.participant_data.group == 'Governing Board') {
		       			$('.marketing, .sales, .governing, .technical, .human').hide();
		       			$('.governing').show();
		       			if(!_exists)
		       				$('.governing').append(newAppend);
		       		}	
		       		if (json.participant_data.group == 'Marketing') {
		       			$('.marketing, .sales, .governing, .technical, .human').hide();
		       			$('.marketing').show();
		       			if(!_exists)
		       				$('.marketing').append(newAppend);
		       		}	
		       		if (json.participant_data.group == 'Sales') {
		       			$('.marketing, .sales, .governing, .technical, .human').hide();
		       			$('.sales').show();
		       			if(!_exists)
		       				$('.sales').append(newAppend);
		       		}	
		       		if (json.participant_data.group == 'Technical') {
		       			$('.marketing, .sales, .governing, .technical, .human').hide();
		       			$('.technical').show();
		       			if(!_exists)
		       				$('.technical').append(newAppend);
		       		}	
		       		if (json.participant_data.group == 'Human Resources') {
		       			$('.marketing, .sales, .governing, .technical, .human').hide();
		       			$('.human').show();
		       			if(!_exists)
		       				$('.human').append(newAppend);
		       		}	
					//div.append(newAppend);
				}, 2000);
			}
		},
		error: function(response){
			$('.spinner').show();
			$('#legend__board').hide();
			setTimeout(function(){
				$('.spinner').hide();
				$('.marketing, .sales, .governing, .technical, .human').hide();
				div.prepend('<legend id="legend__results">No results for: '+search+'</legend>');
			}, 2000);
		}
	});
}

function follow_unfollow_participant(type, user){
	if(type == 'Follow'){
		var finalUrl = '/add_following_contact_to_user/'+user;
		$('#home ul li').remove();
		$('#home ul center h3').remove();
	}else{
		var finalUrl = '/remove_following_contact_to_user/'+user;
		$('#home ul li').remove();
		$('#home ul center h3').remove();
	}
	$.ajax({
		url: url[0] + "//" + url[2] + finalUrl,
		type: 'GET',
		success: function (json) {
			var count = $('.participant__following').children().first().text();
			if(type=='Follow')
				count++;
			else
				count--;
			$('.participant__following').children().first().text(count);
			current_email = $('#host_email').val();
			$.ajax({
				url: url[0] + "//" + url[2] + '/get_participant_followings_info/'+current_email,
				type: 'GET',
				success: function (json) {
			////console.log(json);
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img class="new--user--icon--login" src="'+json.followings_info[i].profilepic_url+'">';
					followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';					
					followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
				}
				if ($('#participant_email').val() != 'None' && json.followings_num == 0){
					$('#home ul').append('<center><h3 >this user has no followings</h3></center>');
				}else if (json.followings_num != 0) {
					$('#home ul').append(followingList);
				}else{
					$('#home ul').append('<center><h3 id="msg">You are following no one</h3></center>');
				}
			}					
				
		});
		},
		error: function (response) {
			alert('Sorry, something went wrong. Try again later.');		
		}
	});
}

function change_view(view){
	if(view == 'search'){
		$('.participant__general').fadeOut(500);
		setTimeout(function(){
			$('.search__participant').fadeIn(500);
			$('.back__button').fadeIn(500);
		}, 500);
	} else {
		$('.search__participant').fadeOut(500);
		$('.back__button').fadeOut(500);
		setTimeout(function(){
			$('.participant__general').fadeIn(500);
		}, 500);
	}
}


$(document).ready(function(){	
    $('#unfollow-parti').on('click',function(){
        var selected = '';    
        $('#following li input[type=checkbox]').each(function(){
            if (this.checked) {
                selected = $(this).val();          	            																															
				$.ajax({
					url: url[0] + "//" + url[2] + '/remove_following_contact_to_user/'+selected,
					type: 'GET',
					success: function (json) {	
						$('#following li input:checked').parent().fadeOut('slow');
						$('#following center h3').show('slow');
					},
					error: function (response) {
						alert('you have to select a participant that you want stop follow');		
					}
				});
			}		
        }); 
        alert('Has stopped following the participants');  
        var resta = $('#following li input:checked').length;
		var num = parseFloat($('.followingss').text());	
		$('.followingss').empty();	
		$('.followingss').append(num-resta);  
    });         
  
    $('#follow-parti').on('click',function(){
        var selectedfollow = '';   	 
        $('#followers li input[type=checkbox]').each(function(){
            if (this.checked) {
                selectedfollow = $(this).val();                                																																
				$.ajax({
					url: url[0] + "//" + url[2] + '/add_following_contact_to_user/'+selectedfollow,
					type: 'GET',
					success: function (json) {
						
					},
					error: function (response) {
						alert('you have to select a participant that you want follow');		
					}
				});
			}
        }); 
        alert('Participants have been followed');   
        var resta = $('#followers li input:checked').length;
		var num = parseFloat($('.followingss').text());	
		$('.followingss').empty();	
		$('.followingss').append(num+resta); 

		$('#followers li input[type=checkbox]').each(function(){
            if (this.checked) {
                selectedfollow = $(this).val();                                																																
				$.ajax({
					url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+selectedfollow,
					type: 'GET',
					success: function (json) {	
						var folloNew = '';
						folloNew += '<li><input value="'+json.participant_data.id+'" class="checkbox check--followers" type="checkbox" name="check[]">';
						folloNew += '<img class="new--user--icon--login" src="'+json.participant_data.profilepic_url+'">';
						folloNew += '<p><a href="#">'+json.participant_data.username+'</a>';					
						folloNew += '<br>'+json.participant_data.fullname+'</p></li>';			
						$('#home ul').append(folloNew);
						$('#msg').hide();

					}		
				});
			}
        }); 
    });  


});

function isValidEmailAddress(emailAddress) {
	var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
	return pattern.test(emailAddress);
};

function showHideGroups(){
	if($('.sales li').length > 0)
		$('.sales').show();
	if($('.governing li').length > 0)
		$('.governing').show();
	if($('.marketing li').length > 0)
		$('.marketing').show();
	if($('.technical li').length > 0)
		$('.technical').show();
	if($('.human li').length > 0)
		$('.human').show();
}