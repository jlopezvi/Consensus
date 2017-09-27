var url = window.location.href;
url = url.split("/");
$('.cropme2').simpleCropper();

$(document).ready( function() {
    $.ajax({
        url: url[0] + "//" + url[2] + '/get_topten_ideas',
        method: 'GET',
        success: function(data){
            //console.log(data);
            var newTop = '';
            var url_new = url[0] +'//'+ url[2] +'/static/';
            for (var i = 0; i < data.data.length; i++) {                      
                newTop += '<div class="col-sm-6 home--content--proposal" ><div class="row home--header">';
                newTop += '<input type="hidden" class="idea__id" value="'+data.data[i].proposal+'">';
                // IF IDEA DOESNT HAVE ANONYMOUS AUTHOR 
                if(data.data[i].if_author_public){
                    newTop += '<div class="col-sm-1" style="padding-left: 0px;">';
                    newTop += '<div class="home--profile--picture"><img class="img-circle new--user--icon--login" src="'+data.data[i].author_profilepic_url+'"></div></div><div class="col-sm-3 home--name">';
                    if($('#host_email').val() == data.data[i].author_email)
                        newTop += '<a href="/participants">'+data.data[i].author_username+'</a></div>';
                    else
                        newTop += '<a href="/participants/'+data.data[i].author_email+'">'+data.data[i].author_username+'</a></div>';
                    newTop += '<div class="col-sm-1 newsfeed--duration">';
                    newTop += '<p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">&nbsp;';
                    newTop += '<p class="duration--info">&nbsp;'+data.data[i].duration+'</p></p></div>';
                } else {
                    newTop += '<div class="col-sm-1 newsfeed--duration">';
                    newTop += '<p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">&nbsp;';
                    newTop += '<p class="duration--info">&nbsp;'+data.data[i].duration+'</p></p></div>';
                    newTop += '<div class="col-sm-1" style="padding-left: 0px;"></div>';
                    newTop += '<div class="col-sm-3 home--name"></div>';
                }
                
                var supporters_percent = data.data[i].supporters_num*100/data.data[i].supporters_goal_num;
                if(data.data[i].volunteers_goal_num >0){
                    newTop += '<div class="col-sm-3 home--charge"><div class="progress home--progress">';
                    newTop += '<div class="progress-bar newsfeed--bar " role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
                    newTop += '<div class="progress home--progress2">';
                } else {
                    newTop += '<div class="col-sm-3 home--charge one--progress__bar"><div class="progress home--progress">';
                    newTop += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
                    newTop += '<div>';
                }
                var volunteers_percent = data.data[i].volunteers_num*100/data.data[i].volunteers_goal_num;
                newTop += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunteers_percent+'%;"></div></div></div>';
                
                if(data.data[i].volunteers_goal_num >0){
                    newTop += '<div class="col-sm-3 newsfeed--goals newsfeed--goals3"><p>'+data.data[i].supporters_num+'/'+data.data[i].supporters_goal_num+' supporters<br>';
                    newTop += data.data[i].volunteers_num+'/'+data.data[i].volunteers_goal_num+' volunteers<br>';
                    var _top = '';
                    if(((i+1)%2)==0)
                        _top = 'margin-top: 1px;';
                    newTop += '</p></div></div><div class="row home--proposals--body" style="'+_top+'background-image: url('+data.data[i].image_url+');"><div class="col-sm-12 concern__div">';
                } else {
                    newTop += '<div class="col-sm-3 newsfeed--goals newsfeed--goals3" style="top:10px!important;"><p>'+data.data[i].supporters_num+'/'+data.data[i].supporters_goal_num+' supporters<br>';
                    if(data.data[i].if_author_public)
                        newTop += '</p></div></div><div class="row home--proposals--body" style="margin-top: 10px;background-image: url('+data.data[i].image_url+');"><div class="col-sm-12 concern__div">';
                    else
                        newTop += '</p></div></div><div class="row home--proposals--body" style="margin-top: 28px;background-image: url('+data.data[i].image_url+');"><div class="col-sm-12 concern__div">';
                }
                newTop += '<div class="col-sm-11 newsfeed--problem">'+data.data[i].concern+'</div></div><div class="col-sm-12">';
                newTop += '<div class="col-sm-11 col-sm-offset-1 newsfeed--proposal">'+data.data[i].proposal+'</div></div></div> <input type="hidden" value="'+data.data[i].idea_id+'" id="idea__id">';
                newTop += '<div class="row newsfeed--footer"><div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;">';
                newTop += '<div class="col-sm-8 newsfeed--support" style="padding-right:0;padding-left:30px;">';
                var rate = ((data.data[i].supporters_num) * 100 / (data.data[i].supporters_num + data.data[i].rejectors_num));
                if (data.data[i].supporters_num + data.data[i].rejectors_num == 0) {
                    rate = 0
                }
                newTop += '<input type="text" value="'+data.data[i].support_rate+'" id="percent" hidden><div class="input--percent">';
                newTop += '<label> Support Rate: '+data.data[i].support_rate+'% </label></div></div><div class="col-sm-4 neewsfeed--moreinfo" style="float:right;padding: 0px;">';
                newTop += '<input type="hidden" class="id" value="'+data.data[i].proposal+'"><img class="redflag redflag2" src="'+url_new+'images/redflag.png"><input type="button" name="more-info" class="home--button" style="float: right;"></div><div id="more--info--modal" hidden><p><h4>  More information about the problem: </h4> '+data.data[i].moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+data.data[i].moreinfo_proposal+'</p></div></div></div>';
                newTop += '<div class="row newsfeed--persons newsfeed--persons2"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
                newTop += '<img src="'+url_new+'images/check-small.png"></div><div class="col-sm-11 newsfeed--likes">';
                newTop += '<ul class="ul--liked"><a href="#" class="last--liked">';
                if(data.data[i].known_supporters.length > 0){
    				for(var f=0; f<data.data[i].known_supporters.length; f++){
						if(data.data[i].known_supporters[f].email != 'user')
							newTop += '<a href="/participants/'+data.data[i].known_supporters[f].email+'"><li>'+data.data[i].known_supporters[f].username+'</li></a>';
						else
							newTop += '<a href="/participants"><li>'+data.data[i].known_supporters[f].username+'</li></a>';
    				
    				}
    			} if(data.data[i].supporters_num-data.data[i].known_supporters.length > 0) {
    				newTop += '<a href="#" class="last--liked"><li>'+(data.data[i].supporters_num-data.data[i].known_supporters.length)+' people</li></a>';
    			}
    			//
                newTop +='</ul></div></div>';
                newTop += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="'+url_new+'images/x-small.png">';
                newTop += '</div><div class="col-sm-11 newsfeed--likes"><ul class="ul--disliked">';
                if(data.data[i].known_rejectors.length > 0){
					for(var f=0; f<data.data[i].known_rejectors.length; f++){
						if(data.data[i].known_rejectors[f].email != 'user')
							newTop += '<a href="/participants/'+data.data[i].known_rejectors[f].email+'"><li>'+data.data[i].known_rejectors[f].username+'</li></a>';
						else
							newTop += '<a href="/participants"><li>'+data.data[i].known_rejectors[f].username+'</li></a>';
					}
				} if(data.data[i].rejectors_num-data.data[i].known_rejectors.length > 0) {
					newTop += '<a href="#" class="last--liked"><li>'+(data.data[i].rejectors_num-data.data[i].known_rejectors.length)+' people</li></a>';
				}
					
                newTop += '</ul></div></div></div>';
                newTop += '<div class="row home--share"><div class="col-sm-12 home--share--icons">';
                newTop += '<input type="hidden" class="supporters--input" value="'+data.data[i].supporters_num+'">';
                newTop += '<input type="hidden" class="volunteers--input" value="'+data.data[i].volunteers_num+'">';
                newTop += '<input type="hidden" class="rejectors--input" value="'+data.data[i].rejectors_num+'">';
                newTop += '<input type="hidden" class="supporters--goal--input" value="'+data.data[i].supporters_goal_num+'">';
                newTop += '<input type="hidden" class="volunteers--goal--input" value="'+data.data[i].volunteers_goal_num+'">';
                newTop += '<div class="col-sm-6" style="padding:0;width: 100%;"><input type="hidden" class="id" value="'+data.data[i].proposal+'">';
                if($('#host_email').val() == data.data[i].author_email){
					//newTop += '<div class="col-sm-12 idea--action--buttons action--buttons--topten"><div class="col-xs-1"><span class="glyphicon glyphicon-edit edit"></span></div>';
	    			//newTop += '<div class="col-xs-1"><span class="glyphicon glyphicon-trash trash"></span></div></div>';
				}
                newTop += '<img class="icons" src="'+url_new+'images/x-icon.png" id="rejected" hidden><img class="icons" style="width: 50px;" src="'+url_new+'images/check-icon.png" id="supported" hidden><img class="icons" style="width: 48px;" src="'+url_new+'images/checkmark.png" id="support__plus--button" hidden>';
                newTop += '</div><div class="col-sm-6 home--followers hidden" style="width: 100%;">';
                newTop += '</div></div></div></div>';
            }
                $('#topten--proposals').append(newTop);
                
                setTimeout(function(){
                    $('#topten--proposals').show();
                    $('.spinner').hide();
                }, 3000);
                
                $(document).on('click', 'input[name="more-info"]', function(){
                    $(this).parent().next().slideToggle('slow');    
                }); 

            
    },
        error: function(response){
            console.log('error');
            console.log(response);
        }
    });
    
    $(document).on('click', '.trash', function(){
    	$('#delete-idea').modal('toggle');
    	var propuestaid = $(this).parent().parent().parent().children('input').val();
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
			}	
		});

    });
    
    $(document).on('click', '.edit', function(){
    	var propid = $(this).parent().parent().parent().children('input').val();
    	console.log(propid);
    	$.ajax({
    		url: url[0] + "//" + url[2] + '/get_idea_node_data/'+propid,
    		type: 'GET',
    		headers: {
    		'Content-Type': 'application/json'
    		},
    		dataType: 'json',
    		success: function (json) {
    			//console.log(json);
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
		$('#modal_proposal1').find('h4.modal-title').html('Edit Proposal (1/2)');
		$('#modal_proposal3').find('h4.modal-title').html('Edit Proposal (2/2)');
		$('#modal_proposal3').find('.modal-prev > button').attr("onclick", "showModal('modal_proposal2', false)");
    	$('#modal_proposal1').modal('toggle');

    	$('.add--proposal--provisional').hide();
    	$('.edit--proposal--provisional').show();
    	$('.controlss').append('<input type="hidden" id="propoid" value="'+propid+'">');
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
    	
    	dataedit['image'] = null;
    	if($('#cropme_bidea img').attr('src') != "/static/images/fondo-c.png"){
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
                    window.location = '../home';
                    location.reload();
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
    
});