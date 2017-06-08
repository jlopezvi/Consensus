var url = window.location.href;
url = url.split("/");

$(document).ready( function() {
	$('body').removeClass('container').addClass('container-fluid');

	$(document).on('click', '#send_invitation-btn', function(){
		var guest_email = $('#emails_input').val();
		var host_email = $('#host_email').val();
		$.ajax({
			url: url[0] + "//" + url[2] + '/registration_send_invitation/'+host_email+'/'+guest_email,
			type: 'GET',
			success: function (json) {
				console.log(json);
				if(json.result_msg == 'email sent'){
					$('.modal-title').empty().append('Success!!');
					$('.modal-body p').empty().append('An email with an invitation sent to <strong>'+guest_email+'</strong>');
					$('#invitation-modal-info').modal('toggle');
				}
			},
			error: function(response){
				console.log(response);
			}
		});
	});

	$('#search-input-participant').keydown(function(e){
		var code = e.which;
		if(code == 13){
			e.preventDefault();
			var search = $(this).val();
			seaarch_participant(search);
		}
	});

	$(document).on('click', '.btn__search', function(e){
		e.preventDefault();
		var search = $('#search-input-participant').val();
		seaarch_participant(search);
	});
});

function seaarch_participant(search){
	$.ajax({
		url: url[0] + "//" + url[2] + '/get_participant_data/'+search,
		type: 'GET',
		success: function (json) {
			console.log(json);
		},
		error: function(response){
			console.log(response);
		}
	});
}