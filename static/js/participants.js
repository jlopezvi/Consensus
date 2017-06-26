var url = window.location.href;
url = url.split("/");

$(window).on('load', function(){
	var current_email = $('#host_email').val();
	
	//GET ALL INFORMATION OF ALL IDEAS CREATED BY PARTICIPANT
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_ideas_data_created_by_participant/'+current_email,
		type: 'GET',
		success: function (json) {		
				var newIdea = '';
			for (var i = 0; i < json.ideas_data.length; i++) {						
				newIdea += '<div class="col-sm-12"><div class="row home--header"><div class="col-sm-2" style="padding-left: 0px;margin-left: -15px;">';
				newIdea += '<div class="home--profile--picture"><img src=""></div></div><div class="col-sm-1 home--name">';
				newIdea += '<a href="#">'+json.ideas_data[i].author_username+'</a></div><div class="col-sm-2 newsfeed--duration">';
				newIdea += '<p><img style="width: 15px;position: relative;top: -3px;" src="static/images/clock-icon.png">&nbsp;'+json.ideas_data[i].duration+'</p>';
				newIdea += '</div><div class="col-sm-3 home--charge"><div class="progress home--progress">';
				newIdea += '<input type="text" value="'+json.ideas_data[i].supporters_num*100/json.ideas_data[i].supporters_goal_num+'" id="supporters--percent" hidden>';
				newIdea += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div></div>';
				newIdea += '<div class="progress home--progress2"><input type="text" value="'+json.ideas_data[i].volunteers_num*100/json.ideas_data[i].volunteers_goal_num+'" id="volunters--percent" hidden>';
				newIdea += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style=""></div></div></div>';
				newIdea += '<div class="col-sm-4 newsfeed--goals"><p>'+json.ideas_data[i].supporters_num/json.ideas_data[i].supporters_goal_num+' supporters goals';
				newIdea += '<br>'+json.ideas_data[i].volunteers_num/json.ideas_data[i].volunteers_goal_num+' volunteers goals</p></div></div>';
				newIdea += '<div class="row home--proposals--body"><div class="col-sm-12">';
				newIdea += '<div class="col-sm-8 newsfeed--problem">'+json.ideas_data[i].concern+'</div></div><div class="col-sm-12" style="margin-top: 180px;">';
				newIdea += '<div class="col-sm-8 col-sm-offset-4 newsfeed--proposal">'+json.ideas_data[i].proposal+'</div></div></div>';
				newIdea += '<div class="row newsfeed--footer"><div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;"><div class="col-sm-1 redflag--img">';
				newIdea += '<img src="static/images/redflag.png"></div><div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
				newIdea += '<input type="text" value="'+json.ideas_data[i].supporters_num*100/json.ideas_data[i].supporters_num+json.ideas_data[i].rejectors+'" id="percent" hidden><div class="input--percent">';
				newIdea += '<label> Support Rate: </label></div></div><div class="col-sm-2 neewsfeed--moreinfo" style="float:right;">';
				newIdea += '<input type="button" name="more-info" class="home--button"></div></div></div>';
				newIdea += '<div class="row newsfeed--persons"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
				newIdea += '<img src=""></div><div class="col-sm-11 newsfeed--likes">';
				newIdea += '<ul><a href="#" class="last--liked"><li>'+json.ideas_data[i].supporters_num+' people</li></a></ul></div></div>';
				newIdea += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="static/images/x-small.png">';
				newIdea += '</div><div class="col-sm-11 newsfeed--likes"><ul><a href="#"><li>'+json.ideas_data[i].rejectors+'</li></a></ul></div></div></div>';
				newIdea += '<div class="row home--share"><div class="col-sm-12 home--share--icons"><div class="col-sm-6" style="padding:0;width: 100%;">';
				newIdea += '<img src="static/images/x-icon.png"><img style="width: 50px;" src="static/images/check-icon.png"><img style="width: 48px;" src="static/images/checkmark.png">';
			    newIdea += '<img style="width: 50px;" src="static/images/ignore-icon.png"></div><div class="col-sm-6 home--followers" style="width: 100%;"><i class="fa fa-share-alt"></i>';
			    newIdea += '<p>Share with: followers</p></div></div></div></div>';
			    }
			$('#newIdea').append(newIdea);		
		}	
	});

	//GET ALL INFORMATION OF CURRENT LOGGED USER OR SEARCHED
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+current_email,
		type: 'GET',
		success: function (json) {
			//console.log(json);
			$('.profile--picture img').attr('src', json.participant_data.profilepic_url);
			$('.participant__name a').append(json.participant_data.username);
			$('.participant__name label').append(json.participant_data.fullname);
			$('.participant__active--p').children().first().append(json.participant_data.ideas_num);
			$('.participant__following').children().first().append(json.participant_data.followers_num);
			$('.participant__followers').children().first().append(json.participant_data.followings_num);
		}	
	});

	//GET ALL FOLLOWERS OF CURRENT LOGGED USER OR SEARCHED
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
		type: 'GET',
		success: function (json) {
			
			if(json.followers_num > 0){
				followerList = '';	
				for(var i = 0; i < json.followers_num; i++){
					followerList += '<li><input value="'+json.followers_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followerList += '<img src="'+json.followers_info[i].profilepic_url+'">'
					followerList += '<p><a href="#">'+json.followers_info[i].username+'</a>';					
					followerList += '<br>'+json.followers_info[i].fullname+'</p></li>';
				}
				$('#home ul').append(followerList);
				
			}
		}	
	});

	//GET ALL FOLLOWINGS OF CURRENT LOGGED USER OR SEARCHED
	
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followings_info/'+current_email,
		type: 'GET',
		success: function (json) {
			//console.log(json);
			if(json.followings_num > 0){
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img src="'+json.followings_info[i].profilepic_url+'">';
					followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';					
					followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
				}
				$('#menu1 ul').append(followingList);
			}
		}	
	});
    
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_all_public_participants',
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
	       		newParti += '<li><img class="new--user--icon--login" src="'+json[i].profilepic_url+'"><p>'; 
	       		newParti += '<a href="#">'+json[i].fullname+'</a>';
	       		newParti += '<br><label>'+json[i].position+'</label> | <label>'+json[i].group+'</label></p>';
	       		newParti += '<input type="hidden" value="'+json[i].email+'">';
	       		newParti += '<input class="form-control invite__button" type="button" '+if_following+' id="btn-follow"></li>';
	       		$('#id01').append(newParti);	
	       	}
	       	//console.log(newParti);
		}
	});

	

});

$(document).ready( function() {
	$('body').removeClass('container').addClass('container-fluid');
	
	$(document).on('click', '#send_invitation-btn', function(){
		$('#send_invitation-btn').prop('disabled', true);
		var guest_email = $('#emails_input').val();
		var host_email = $('#host_email').val();
		$.ajax({
			url: url[0] + "//" + url[2] + '/registration_send_invitation/'+host_email+'/'+guest_email,
			type: 'GET',
			success: function (json) {
				//console.log(json);
				$('#send_invitation-btn').prop('disabled', false);
				if(json.result_msg == 'email sent'){
					$('.modal-title').empty().append('Success!!');
					$('.modal-body p#modal--invitation').empty().append('An email with an invitation sent to <strong>'+guest_email+'</strong>');
					$('#invitation-modal-info').modal('toggle');
				}
			},
			error: function(response){
				$('#send_invitation-btn').prop('disabled', false);
				//console.log(response);
			}
		});
	});

	$('#search-input-participant').on('keydown', function(e){
		var code = e.which;
		if(code == 13){
			e.preventDefault();
		}
	});

	$('#search-input-participant').on('focus', function(){
		change_view('search');
	});

	$(document).on('click', '.btn__search', function(e){
		e.preventDefault();
		change_view('search');
		//var page = $('#page').val();
		//var search = $('#search-input-participant').val();
		//seaarch_participant(search, page);
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

});

function seaarch_participant(search, page){
	var div = $('.addproposal--step__div ul');
	div.empty();
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data_by_email_unrestricted/'+search,
		type: 'GET',
		success: function (json) {
			//console.log(json);
			if(json.result == 'OK'){
				if(page == 'search'){
					$('.spinner').show();
					var newAppend = '<legend>Executive board</legend>';
	            	newAppend += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
	            	newAppend += '<img src="'+json.participant_data.profilepic_url+'"><p>';
	            	newAppend += '<a href="#">'+json.participant_data.username+'</a>'; 
	            	newAppend += '<br>'+json.participant_data.fullname+'</p>';
	            	newAppend += '<input type="hidden" value="'+json.participant_data.id+'">';
	                newAppend += '<input class="form-control invite__button" type="button" value="Follow" id="btn-follow"></li>';
	                setTimeout(function(){
	                	$('.spinner').hide();
						div.append(newAppend);
					}, 2000);
	                
				}
			}
		},
		error: function(response){
			$('.spinner').show();
			setTimeout(function(){
				$('.spinner').hide();
				div.append('<legend>No results for: '+search+'</legend>');
			}, 2000);
			$(document).on('click', '.btn__search', function(){
				//$('.btn__search').on('click', function(){
				$('#does-exist').append('No results for: '+search).show();

			});

		}
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
}

function follow_unfollow_participant(type, user){
	if(type == 'Follow')
		var finalUrl = '/add_following_contact_to_user/'+user;

	else
		var finalUrl = '/remove_following_contact_to_user/'+user;
	$.ajax({
		url: url[0] + "//" + url[2] + finalUrl,
		type: 'GET',
		success: function (json) {
			alert(json.result_msg);	
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
		var current_email = $('#host_email').val();
		$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_followings_info/'+current_email,
		type: 'GET',
		success: function (json) {
			
			
			if(json.followings_num > 0){
				followingList = '';	
				for(var i = 0; i < json.followings_num; i++){
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img src="'+json.followings_info[i].profilepic_url+'">';
					followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';					
					followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
				}
				$('#following').append(followingList);
			}
		}	
		});

    });  

});   


