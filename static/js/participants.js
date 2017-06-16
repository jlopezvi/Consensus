var url = window.location.href;
url = url.split("/");

$(window).on('load', function() {
	var current_email = $('#host_email').val();
	
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
			
			if(json.followers_num > 0){
				followerList = '';	
				for(var i = 0; i < json.followers_num; i++){
					followerList += '<li><input value="'+json.followers_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followerList += '<img src="'+json.followers_info[i].profilepic_url+'">'
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
					followingList += '<li><input value="'+json.followings_info[i].email+'" class="checkbox check--followers" type="checkbox" name="check[]">';
					followingList += '<img src="'+json.followings_info[i].profilepic_url+'">'
					followingList += '<p><a href="#">'+json.followings_info[i].username+'</a>';					
					followingList += '<br>'+json.followings_info[i].fullname+'</p></li>';
				}
				$('#home ul').append(followingList);
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
	       		newParti += '<li><input class="checkbox check--followers" type="checkbox" name="check[]">';
	       		newParti += '<img src="'+json[i].profilepic_url+'"><p>'; 
	       		newParti += '<a href="#">'+json[i].fullname+'</a>';
	       		newParti += '<br><label>'+json[i].email+'</label>|<label>'+json[i].position+'</label>|<label>'+json[i].group+'</label></p>';
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
});




$(document).ready(function(){	
$('#follow-parti').on('click', function(){	
	var lista = [$('#following li input:checked').val()];			
			for (var i = 0; i < lista.length; i++) {					
					var listaC ='';
					listaC += lista[i];																								
			//console.log(listaC);			
			if (listaC > 0) {
				var Url =  '/add_following_contact_to_user/'+listaC;
			}else{
				$.ajax({
				url: url[0] + "//" + url[2] + '/add_following_contact_to_user/'+listaC,
				type: 'GET',
					success: function (json) {
						alert(json.result_msg);

					},
					error: function (response) {
						alert('Sorry, something went wrong. Try again later.');		
					}
				});
			}
		}		
	});
});

$(document).ready(function(){	
$('#unfollow-parti').on('click', function(){	
	var lista = [$('#followers li input:checked').val()];			
			for (var i = 0; i < lista.length; i++) {					
					var listaC ='';
					listaC += lista[i];																								
			//console.log(listaC);			
			if (listaC > 0) {
				var Url =  '/remove_following_contact_to_user/'+listaC;
			}else{
				$.ajax({
				url: url[0] + "//" + url[2] + '/remove_following_contact_to_user/'+listaC,
				type: 'GET',
					success: function (json) {
						alert(json.result_msg);

					},
					error: function (response) {
						alert('Sorry, something went wrong. Try again later.');		
					}
				});
			}
		}		
	});
});

