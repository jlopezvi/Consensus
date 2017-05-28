
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

    $.ajax({
      url: url[0] + "//" + url[2] + '/add_idea_to_user',
      type: 'POST',
      data: fData,
      processData: false,
      contentType: false,
      success: function (json) {
        //console.log(json);
        if(json.result != 'OK'){
          alert(json.result_msg);
        } else {
          alert(json.result_msg);
        }
      },
      error: function(response){
        console.log(response);
      }
    });
  });
});
function showModal(id) {
    $('.modal').modal('hide');
    $("#" + id).modal();

  }