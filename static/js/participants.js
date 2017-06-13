var url = window.location.href;
url = url.split("/");

$(window).on('load', function() {
	var page = $('#page').val();
	var current_email = $('#host_email').val();
	if(page == 'participant'){
		
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
				$('.participant__followers').children().first().append(json.participant_data.followers_num);
				$('.participant__following').children().first().append(json.participant_data.followings_num);
			}	
		});

		//GET ALL FOLLOWERS OF CURRENT LOGGED USER OR SEARCHED
		$.ajax({
			url: url[0] + "//" + url[2] + '/get_participant_followers_info/'+current_email,
			type: 'GET',
			success: function (json) {
				//console.log(json);
				if(json.followers_num > 0){
					followerList = '';	
					for(var i = 0; i < json.followers_num; i++){
						followerList += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
						followerList += '<img src="/static/assets/profile/perfil-mediano.png">'
						followerList += '<p><a href="#">'+json.followers_info[i].username+'</a>';
						followerList += '<br>'+json.followers_info[i].fullname+'</p></li>';
					}
					$('#menu1 ul').append(followerList);
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
						followingList += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
						followingList += '<img src="/static/assets/profile/perfil-mediano.png">'
						followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';
						followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
					}
					$('#home ul').append(followingList);
				}
			}	
		});
		
	} else { //else que valida el template en que le estamos (search_participants.html)
		//Moví la funcion para aca, porque aqui carga antes de que cargue el HTML 
		//Aparte, aqui tengo una validacion de los templates, search_participants 
		//y participants, entonces, tener la informacion de todos los participantes
		//precaragas en el template pparticipants, no es necesario.
		$.ajax({
		url: url[0] + "//" + url[2] + '/get_all_public_participants',
		type: 'GET',
		headers: {
		'Content-Type': 'application/json'
		},
		dataType: 'json',
		success: function(json) {
	       	for (var i = 0; i < json.length; i++) {
	       		newParti = '';
	       		newParti += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
	       		newParti += '<img src="'+json[i].profilepic_url+'"><p>'; 
	       		newParti += '<a href="#">'+json[i].fullname+'</a>';
	       		newParti += '<br>'+json[i].email+'  |  '+json[i].position+'  |  '+json[i].group+'</p>';
	       		newParti += '<input type="hidden" value="'+json[i].email+'">';
	       		newParti += '<input class="form-control invite__button" type="button" value="Follow" id="btn-follow"></li>';
	       		$('.addproposal--step2').append(newParti);	
	       	}
	       	console.log(newParti);
		}
	});
	}
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
					$('.modal-body p').empty().append('An email with an invitation sent to <strong>'+guest_email+'</strong>');
					$('#invitation-modal-info').modal('toggle');
				}
			},
			error: function(response){
				$('#send_invitation-btn').prop('disabled', false);
				//console.log(response);
			}
		});
	});

	$('#search-input-participant').keydown(function(e){
		var code = e.which;
		var page = $('#page').val();
		if(code == 13){
			e.preventDefault();
			var search = $(this).val();
			seaarch_participant(search, page);
		}
	});

	$(document).on('click', '.btn__search', function(e){
		e.preventDefault();
		var page = $('#page').val();
		var search = $('#search-input-participant').val();
		seaarch_participant(search, page);
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