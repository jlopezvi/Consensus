var url = window.location.href;
url = url.split("/");
$('.cropme2').simpleCropper();

$(document).ready( function() {
    $.ajax({
        url: url[0] + "//" + url[2] + '/get_topten_ideas',
        method: 'GET',
        success: function(data){
            console.log(data);
            var newTop = '';
            var url_new = url[0] +'//'+ url[2] +'/static/';
            for (var i = 0; i < data.data.length; i++) {                      
                newTop += '<div class="col-sm-6 home--content--proposal" ><div class="row home--header">';
                newTop += '<input type="hidden" class="idea__id" value="'+data.data[i].proposal+'">';
                newTop += '<div class="col-sm-1" style="padding-left: 0px;">';
                newTop += '<div class="home--profile--picture"><img class="img-circle new--user--icon--login" src="'+data.data[i].author_profilepic_url+'"></div></div><div class="col-sm-3 home--name">';
                if($('#host_email').val() == data.data[i].author_email)
                    newTop += '<a href="/participants">'+data.data[i].author_username+'</a></div>';
                else
                    newTop += '<a href="/participants/'+data.data[i].author_email+'">'+data.data[i].author_username+'</a></div>';
                newTop += '<div class="col-sm-1 newsfeed--duration">';
                newTop += '<p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">&nbsp;';
                newTop += '<p class="duration--info">&nbsp;'+data.data[i].duration+'</p></p></div>';
                newTop += '<div class="col-sm-3 home--charge"><div class="progress home--progress">';
                var supporters_percent = data.data[i].supporters_num*100/data.data[i].supporters_goal_num;
                newTop += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
                if(data.data[i].volunteers_goal_num >0)
                    newTop += '<div class="progress home--progress2">';
                else
                    newTop += '<div>';
                var volunteers_percent = data.data[i].volunteers_num*100/data.data[i].volunteers_goal_num;
                newTop += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunteers_percent+'%;"></div></div></div>';
                newTop += '<div class="col-sm-3 newsfeed--goals newsfeed--goals3"><p>'+data.data[i].supporters_num+'/'+data.data[i].supporters_goal_num+' supporters<br>';
                if(data.data[i].volunteers_goal_num >0){
                    newTop += data.data[i].volunteers_num+'/'+data.data[i].volunteers_goal_num+' volunteers<br>';
                    newTop += '</p></div></div><div class="row home--proposals--body" style="background-image: url('+data.data[i].image_url+');"><div class="col-sm-12 concern__div">';
                } else {
                    newTop += '</p></div></div><div class="row home--proposals--body" style="margin-top: 9px;background-image: url('+data.data[i].image_url+');"><div class="col-sm-12 concern__div">';
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
                if(data.data[i].supporters_num > 0){
    				for(var f=0; f<data.data[i].supporters_num; f++){
    					if(f<=3){
    						if(data.data[i].known_supporters[f].email != 'user')
    							newTop += '<a href="/participants/'+data.data[i].known_supporters[f].email+'"><li>'+data.data[i].known_supporters[f].username+'</li></a>';
    						else
    							newTop += '<a href="/participants"><li>'+data.data[i].known_supporters[f].username+'</li></a>';
    					} else {
    						if((data.data[i].supporters_num-4) > 0)
    							newTop += '<a href="#" class="last--liked"><li>'+(data.data[i].supporters_num-4)+' people</li></a>';
    						break;
    					}
    				}
    			} else {
    				newTop += '<a href="#" class="last--liked"><li>'+data.data[i].supporters_num+' people</li></a>';
    			}
    			//
                newTop +='</ul></div></div>';
                newTop += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="'+url_new+'images/x-small.png">';
                newTop += '</div><div class="col-sm-11 newsfeed--likes"><ul class="ul--disliked">';
                if(data.data[i].rejectors_num > 0){
					for(var f=0; f<data.data[i].rejectors_num; f++){
						if(f<=3){
							if(data.data[i].known_rejectors[f].email != 'user')
								newTop += '<a href="/participants/'+data.data[i].known_rejectors[f].email+'"><li>'+data.data[i].known_rejectors[f].username+'</li></a>';
							else
								newTop += '<a href="/participants"><li>'+data.data[i].known_rejectors[f].username+'</li></a>';
						} else {
							if((data.data[i].rejectors_num-4) > 0)
								newTop += '<a href="#" class="last--liked"><li>'+(data.data[i].rejectors_num-4)+' people</li></a>';
							break;
						}
					}
				} else {
					newTop += '<a href="#" class="last--liked"><li>'+data.data[i].rejectors_num+' people</li></a>';
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
					newTop += '<div class="col-sm-12 idea--action--buttons action--buttons--topten"><div class="col-xs-1"><span class="glyphicon glyphicon-edit edit"></span></div>';
	    			newTop += '<div class="col-xs-1"><span class="glyphicon glyphicon-trash trash"></span></div></div>';
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
});