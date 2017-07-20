var url = window.location.href;
url = url.split("/");
var current_vote = '';
$('.cropme2').simpleCropper();

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
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_ideas_data_created_by_participant/'+current_email,
		type: 'GET',
		success: function (json) {	
			
			console.log(json);
			var newIdea = '';
			var url_new = url[0] +'//'+ url[2] +'/static/';
			for (var i = 0; i < json.ideas_data.length; i++) {						
				newIdea += '<div class="col-sm-12"><div class="row home--header">';
				newIdea += '<input type="hidden" class="idea__id" value="'+json.ideas_data[i].proposal+'">';
				newIdea += '<div class="col-sm-2" style="padding-left: 0px;margin-left: -15px;">';
				newIdea += '<div class="home--profile--picture"><img class="img-circle new--user--icon--login" src="'+json.ideas_data[i].author_profilepic+'"></div></div><div class="col-sm-1 home--name">';
				newIdea += '<a href="#">'+json.ideas_data[i].author_username+'</a></div><div class="col-sm-2 newsfeed--duration">';
				newIdea += '<p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">&nbsp;'+json.ideas_data[i].duration+'</p>';
				newIdea += '</div><div class="col-sm-3 home--charge"><div class="progress home--progress">';
				var supporters_percent = json.ideas_data[i].supporters_num*100/json.ideas_data[i].supporters_goal_num;
				newIdea += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
				newIdea += '<div class="progress home--progress2">';
				var volunteers_percent = json.ideas_data[i].volunteers_num*100/json.ideas_data[i].volunteers_goal_num;
				newIdea += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunteers_percent+'%;"></div></div></div>';
				newIdea += '<div class="col-sm-4 newsfeed--goals"><p>'+json.ideas_data[i].supporters_num+'/'+json.ideas_data[i].supporters_goal_num+' supporters goals';
				newIdea += '<br>'+json.ideas_data[i].volunteers_num+'/'+json.ideas_data[i].volunteers_goal_num+' volunteers goals</p></div></div>';
				newIdea += '<div class="row home--proposals--body" style="background-image: url('+json.ideas_data[i].image+'); padding-top:47.40%;"><div class="col-sm-12 concern__div">';
				newIdea += '<div class="col-sm-8 newsfeed--problem">'+json.ideas_data[i].concern+'</div></div><div class="col-sm-12" style="position:relative;">';
				newIdea += '<div class="col-sm-8 col-sm-offset-4 newsfeed--proposal">'+json.ideas_data[i].proposal+'</div></div></div> <input type="hidden" value="'+json.ideas_data[i].idea_id+'" id="idea__id">';
				newIdea += '<div class="row newsfeed--footer"><div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;"><div class="col-sm-1 redflag--img"><input type="hidden" class="id" value="'+json.ideas_data[i].proposal+'">';
				newIdea += '<img class="redflag" src="'+url_new+'images/redflag.png"></div><div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
				var rate = ((json.ideas_data[i].supporters_num) * 100 / (json.ideas_data[i].supporters_num + json.ideas_data[i].rejectors.length));
				if (json.ideas_data[i].supporters_num + json.ideas_data[i].rejectors.length == 0) {
					rate = 0
				}
				newIdea += '<input type="text" value="'+Math.floor(rate)+'" id="percent" hidden><div class="input--percent">';
				newIdea += '<label> Support Rate: '+Math.floor(rate)+'% </label></div></div><div class="col-sm-2 neewsfeed--moreinfo" style="float:right;">';
				newIdea += '<input type="button" name="more-info" class="home--button"></div><div id="more--info--modal" hidden><p><h4>  More information about the problem: </h4> '+json.ideas_data[i].moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+json.ideas_data[i].moreinfo_proposal+'</p></div></div></div>';
				newIdea += '<div class="row newsfeed--persons"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
				newIdea += '<img src="'+url_new+'images/check-small.png"></div><div class="col-sm-11 newsfeed--likes">';
				newIdea += '<ul class="ul--liked"><a href="#" class="last--liked"><li>'+json.ideas_data[i].supporters_num+' people</li></a></ul></div></div>';
				newIdea += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="'+url_new+'images/x-small.png">';
				newIdea += '</div><div class="col-sm-11 newsfeed--likes"><ul class="ul--disliked"><a href="#" class="last--liked"><li>'+json.ideas_data[i].rejectors.length+' people</li></a></ul></div></div></div>';
				newIdea += '<div class="row home--share"><div class="col-sm-12 home--share--icons">';
				newIdea += '<input type="hidden" class="supporters--input" value="'+json.ideas_data[i].supporters_num+'">';
				newIdea += '<input type="hidden" class="volunteers--input" value="'+json.ideas_data[i].volunteers_num+'">';
				newIdea += '<input type="hidden" class="rejectors--input" value="'+json.ideas_data[i].rejectors.length+'">';
				newIdea += '<input type="hidden" class="supporters--goal--input" value="'+json.ideas_data[i].supporters_goal_num+'">';
				newIdea += '<input type="hidden" class="volunteers--goal--input" value="'+json.ideas_data[i].volunteers_goal_num+'">';
				newIdea += '<div class="col-sm-6" style="padding:0;width: 100%;"><input type="hidden" class="id" value="'+json.ideas_data[i].proposal+'">';
				newIdea += '<img class="icons" src="'+url_new+'images/x-icon.png" id="rejected" hidden><img class="icons" style="width: 50px;" src="'+url_new+'images/check-icon.png" id="supported" hidden><img class="icons" style="width: 48px;" src="'+url_new+'images/checkmark.png" id="support__plus--button" hidden>';
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
  				if(left == 1){
            		$(this).next('div').show('slow');	
            	left = 0;
            	} else{
            	left = 1;
              		$(this).next('div').hide('slow');
        		}	
   			});	
   			
		}	
	});
	

	//GET ALL INFORMATION OF CURRENT LOGGED USER OR SEARCHED
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+current_email,
		type: 'GET',
		success: function (json) {
			//console.log(json);
			$('.profile--picture img').attr('src', json.participant_data.profilepic);
			$('.participant__name a').append(json.participant_data.username);
			$('.participant__name label').append(json.participant_data.fullname);
			$('.participant__active--p').children().first().append(json.participant_data.ideas_num);
			$('.participant__following').children().first().append(json.participant_data.followings_num);
			$('.participant__followers').children().first().append(json.participant_data.followers_num);
		}	
	});

	//GET ALL FOLLOWERS OF CURRENT LOGGED USER OR SEARCHED
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
		type: 'GET',
		success: function (json) {
				//console.log(json);
				if (json.ifallowed == false) {
					$('#menu1 ul').append('<center><h3 >User private</h3></center>');
				}else{		
				followerList = '';	
				for(var i = 0; i < json.followers_num; i++){
					followerList += '<li><input value="'+json.followers_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followerList += '<img class="new--user--icon--login" src="'+json.followers_info[i].profilepic+'">'
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
			//console.log(json);
				if (json.ifallowed == false){
					$('#home ul').append('<center><h3>User private</h3></center>');
				}else{
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img class="new--user--icon--login" src="'+json.followings_info[i].profilepic+'">';
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
			//console.log(json);
	       	for (var i = 0; i < json.length; i++) {
	       		if_following = '';
	       		if(json[i].if_following)
	       			if_following = 'value="Unfollow"';
	       		else
	       			if_following = 'value="Follow"';
	       		newParti = '';
	       		newParti += '<li><img class="new--user--icon--login" src="'+json[i].profilepic+'"><p>'; 
	       		newParti += '<a href="#">'+json[i].fullname+'</a>';
	       		newParti += '<br><label>'+json[i].position+'</label> | <label>'+json[i].group+'</label></p>';
	       		newParti += '<input type="hidden" value="'+json[i].email+'">';
	       		newParti += '<input class="form-control invite__button" type="button" '+if_following+' id="btn-follow"></li>';
	       		$('#id01').append(newParti);	
	       	}
	       	//console.log(newParti);
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
				console.log(guest_email[i]);
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
			$('.addproposal--step__div ul').find('li.participants__li__private').remove();
			$('#legend__results').remove();
			$('#legend__board').show();
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
    		console.log('Not Allowed');
    	else
    		window.location = '/participants/'+redirect;

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
      			//console.log(data);
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
		        		var support_goal = element.parent().parent().children('input.supporters--goal--input').val();
		        		var volunt_goal = element.parent().parent().children('input.volunteers--goal--input').val();
        				var volunt = parseInt(element.parent().parent().children('input.volunteers--input').val());
        				var rejector = parseInt(element.parent().parent().children('input.rejectors--input').val());
        				var support = parseInt(element.parent().parent().children('input.supporters--input').val());
		        		
		        		if (json.result != 'Wrong: User vote exists of same type'){
		        			if(data_input.vote_type == 'supported'){
		        				var answer = 'Now you are supporting this idea!';
		        				if(vote_ifvolunteered){
		        					volunt++;
		        					element.parent().parent().children('input.volunteers--input').val(volunt);
		        					if(current_vote == 'rejected' || current_vote == 'ignored' || data.result == 'Wrong'){
		        						support++;
			        					element.parent().parent().children('input.supporters--input').val(support);
		        					}
		        				} else {
		        					if(current_vote == 'volunteer'){
		        						volunt--;
		        						element.parent().parent().children('input.volunteers--input').val(volunt);
		        					} else {
			        					support++;
			        					element.parent().parent().children('input.supporters--input').val(support);
		        					}
		        				}
		        				if(current_vote == 'rejected'){
		        					rejector--;
		        					element.parent().parent().children('input.rejectors--input').val(rejector);
		        				}
		        			} else {
		        				var answer = 'Idea rejected successfully!';
		        				rejector++;
	        					element.parent().parent().children('input.rejectors--input').val(rejector);
	        					if(current_vote == 'volunteer'){
	        						volunt--;
		        					element.parent().parent().children('input.volunteers--input').val(volunt);
		        					support--;
		        					element.parent().parent().children('input.supporters--input').val(support);
	        					} else if(current_vote == 'supported'){
	        						support--;
		        					element.parent().parent().children('input.supporters--input').val(support);
	        					}
		        			}
		        			var volunt_percent = ((volunt*100)/volunt_goal)+'%';
			        		var support_percent = ((support*100)/support_goal)+'%';
			        		div_header.children('.home--charge').children('.home--progress2').children('div').attr('style', '').css('width', volunt_percent);
			        		div_header.children('.home--charge').children('.home--progress').children('div').attr('style', '').css('width', support_percent);
			        		div_header.children('.newsfeed--goals').children('p').empty().append(support+'/'+support_goal+' supporters goals<br>'+volunt+'/'+volunt_goal+' volunteers goals');
			        		div_persons.find('.newsfeed--likes ul.ul--liked a.last--liked li').empty().append(support+' people');
			        		div_persons.find('.newsfeed--likes ul.ul--disliked a.last--liked li').empty().append(rejector+' people');
			        		var rate = ((support * 100) / (support + rejector));
			        		if(support + rejector == 0)
			        			rate = 0;
			        		div_footer.find('.input--percent label').empty().append('Support Rate: '+rate+'%');
		        		
			        		$('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
			      			$('#invitation-modal-info p#modal--invitation').empty().append(answer); 
		        		} else {
		        			$('#invitation-modal-info h4.modal-title').empty().append('Error');
			      			$('#invitation-modal-info p#modal--invitation').empty().append('You can not vote the same for this idea.');
		        		}
		        		$('#invitation-modal-info').modal('toggle');
/*		        		
			      		if(data_input.vote_type == 'supported' ){
			      			var answer = 'Now you are supporting this idea!';
			      			if (json.result != 'Wrong: User vote exists of same type'){
			      				var volunt = parseInt(element.parent().parent().children('input.volunteers--input').val());
			      				if(vote_ifvolunteered){
			      					
			      					if(current_vote != 'volunteer')
			      						volunt += 1;
			      					var volunt_percent = ((volunt*100)/volunt_goal)+'%';
			      					div_header.children('.home--charge').children('.home--progress2').children('div').attr('style', '').css('width', volunt_percent);
			      				}
			      				
			      				if(current_vote != 'supported')
			  						
			  					else if(current_vote == 'supported')
			  						var support = parseInt(element.parent().parent().children('input.supporters--input').val());
			  					var support_percent = ((support*100)/support_goal)+'%';
			  					div_header.children('.home--charge').children('.home--progress').children('div').attr('style', '').css('width', support_percent);
			  					div_header.children('.newsfeed--goals').children('p').empty().append(support+'/200 supporters goals<br>'+volunt+'/14 volunteers goals');
			      				div_persons.find('.newsfeed--likes ul.ul--liked a.last--liked li').empty().append(support+' people');
			      				
		      					if(current_vote == 'rejected'){
		      						
		      						div_persons.find('.newsfeed--likes ul.ul--disliked a.last--liked li').empty().append(rejector+' people');
		      					}
			      			}
			      		} else {
			      			
			      			if (json.result != 'Wrong: User vote exists of same type'){
			      				var volunt = parseInt(element.parent().parent().children('input.volunteers--input').val()) + 1;
			      				div_persons.find('.newsfeed--likes ul.ul--disliked a.last--liked li').empty().append(volunt+' people');
			      				if(current_vote == 'supported' || current_vote == 'volunteer'){
			      					var support = parseInt(element.parent().parent().children('input.supporters--input').val()) - 1;
			      					div_persons.find('.newsfeed--likes ul.ul--liked a.last--liked li').empty().append(support+' people');
			      				}
			      			}
			      		}
			    		if(json.result == 'OK: User vote was modified'){
			      			$('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
			      			$('#invitation-modal-info p#modal--invitation').empty().append(answer);       			
			    		} else if (json.result == 'OK: User vote was created'){
			    			$('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
			      			$('#invitation-modal-info p#modal--invitation').empty().append(answer); 
			    		}
			    		else if (json.result == 'Wrong: User vote exists of same type'){
			      			$('#invitation-modal-info h4.modal-title').empty().append('Error');
			      			$('#invitation-modal-info p#modal--invitation').empty().append('You can not vote the same for this idea.');
			    		}
			    		$('#invitation-modal-info').modal('toggle');
*/
			        },
			        error: function(response){
			          console.log('error');
			          console.log(response);
			        }
		        });
			},
			error: function(response){
				console.log('error');
				console.log(response);
			}
		});
    });
});

function seaarch_participant(search){
	var div = $('.addproposal--step__div ul');
	$('#legend__results').remove();
	$('#legend__board').show();
	$('.addproposal--step__div ul').find('li.participants__li__private').remove();
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+search,
		type: 'GET',
		success: function (json) {
			console.log(json);
			if(json.result == 'OK'){
				$('.spinner').show();
				var newAppend = '';
            	newAppend += '<li class="participants__li__private">';
            	newAppend += '<img class="new--user--icon--login" src="'+json.participant_data.profilepic+'"><p>';
            	newAppend += '<a href="#">'+json.participant_data.username+'</a>'; 
            	newAppend += '<br>'+json.participant_data.fullname+'</p>';
            	newAppend += '<input type="hidden" value="'+json.participant_data.id+'">';
                newAppend += '<input class="form-control invite__button" type="button" value="Follow" id="btn-follow"></li>';
                setTimeout(function(){
                	$('.spinner').hide();
					$('.addproposal--step__div ul').find('li.participants__li__private').remove();
					div.append(newAppend);
				}, 2000);
			}
		},
		error: function(response){
			$('.spinner').show();
			$('#legend__board').hide();
			setTimeout(function(){
				$('.spinner').hide();
				div.append('<legend id="legend__results">No results for: '+search+'</legend>');
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
			//console.log(json);
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img class="new--user--icon--login" src="'+json.followings_info[i].profilepic+'">';
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
	console.log();
}

function change_view(view){
	if(view == 'search'){
		$('.participant__general').fadeOut(500);
		setTimeout(function(){
			$('.search__participant').fadeIn(500);
		}, 500);
	} else {
		$('.search__participant').fadeOut(500);
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
						$('#msg').fadeIn('slow');
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
						folloNew += '<img class="new--user--icon--login" src="'+json.participant_data.profilepic+'">';
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


