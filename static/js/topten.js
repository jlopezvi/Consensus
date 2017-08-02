var url = window.location.href;
url = url.split("/");
$('.cropme2').simpleCropper();

$(document).ready( function() {
    $.ajax({
        url: url[0] + "//" + url[2] + '/get_topten_ideas',
        method: 'GET',
        success: function(data){
            var newTop = '';
            var url_new = url[0] +'//'+ url[2] +'/static/';
            for (var i = 0; i < data.data.length; i++) {                      
                newTop += '<div class="col-sm-6 home--content--proposal" ><div class="row home--header">';
                newTop += '<input type="hidden" class="idea__id" value="'+data.data[i].proposal+'">';
                newTop += '<div class="col-sm-2" style="padding-left: 0px;margin-left: -15px;">';
                newTop += '<div class="home--profile--picture"><img class="img-circle new--user--icon--login" src="'+data.data[i].author_profilepic+'"></div></div><div class="col-sm-1 home--name">';
                newTop += '<a href="#">'+data.data[i].author_username+'</a></div><div class="col-sm-2 newsfeed--duration">';
                newTop += '<p><img style="width: 15px;position: relative;top: -3px;" src="'+url_new+'images/clock-icon.png">&nbsp;'+data.data[i].duration+'</p>';
                newTop += '</div><div class="col-sm-3 home--charge"><div class="progress home--progress">';
                var supporters_percent = data.data[i].supporters_num*100/data.data[i].supporters_goal_num;
                newTop += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+supporters_percent+'%;"></div></div>';
                newTop += '<div class="progress home--progress2">';
                var volunteers_percent = data.data[i].volunteers_num*100/data.data[i].volunteers_goal_num;
                newTop += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunteers_percent+'%;"></div></div></div>';
                newTop += '<div class="col-sm-4 newsfeed--goals"><p>'+data.data[i].supporters_num+'/'+data.data[i].supporters_goal_num+' supporters';
                newTop += '<br>'+data.data[i].volunteers_num+'/'+data.data[i].volunteers_goal_num+' volunteers</p></div></div>';
                newTop += '<div class="row home--proposals--body" style="background-image: url('+data.data[i].image+'); padding-top:47.40%;"><div class="col-sm-12 concern__div">';
                newTop += '<div class="col-sm-8 newsfeed--problem">'+data.data[i].concern+'</div></div><div class="col-sm-12" style="position:relative;">';
                newTop += '<div class="col-sm-8 col-sm-offset-4 newsfeed--proposal">'+data.data[i].proposal+'</div></div></div> <input type="hidden" value="'+data.data[i].idea_id+'" id="idea__id">';
                newTop += '<div class="row newsfeed--footer"><div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;"><div class="col-sm-1 redflag--img"><input type="hidden" class="id" value="'+data.data[i].proposal+'">';
                newTop += '<img class="redflag" src="'+url_new+'images/redflag.png"></div><div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
                var rate = ((data.data[i].supporters_num) * 100 / (data.data[i].supporters_num + data.data[i].rejectors.length));
                if (data.data[i].supporters_num + data.data[i].rejectors.length == 0) {
                    rate = 0
                }
                newTop += '<input type="text" value="'+data.data[i].support_rate+'" id="percent" hidden><div class="input--percent">';
                newTop += '<label> Support Rate: '+data.data[i].support_rate+'% </label></div></div><div class="col-sm-2 neewsfeed--moreinfo" style="float:right;">';
                newTop += '<input type="button" name="more-info" class="home--button"></div><div id="more--info--modal" hidden><p><h4>  More information about the problem: </h4> '+data.data[i].moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+data.data[i].moreinfo_proposal+'</p></div></div></div>';
                newTop += '<div class="row newsfeed--persons"><div class="col-sm-12"><div class="col-sm-1" style="padding:0;">';
                newTop += '<img src="'+url_new+'images/check-small.png"></div><div class="col-sm-11 newsfeed--likes">';
                newTop += '<ul class="ul--liked"><a href="#" class="last--liked"><li>'+data.data[i].supporters_num+' people</li></a></ul></div></div>';
                newTop += '<div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img src="'+url_new+'images/x-small.png">';
                newTop += '</div><div class="col-sm-11 newsfeed--likes"><ul class="ul--disliked"><a href="#" class="last--liked"><li>'+data.data[i].rejectors.length+' people</li></a></ul></div></div></div>';
                newTop += '<div class="row home--share"><div class="col-sm-12 home--share--icons">';
                newTop += '<input type="hidden" class="supporters--input" value="'+data.data[i].supporters_num+'">';
                newTop += '<input type="hidden" class="volunteers--input" value="'+data.data[i].volunteers_num+'">';
                newTop += '<input type="hidden" class="rejectors--input" value="'+data.data[i].rejectors.length+'">';
                newTop += '<input type="hidden" class="supporters--goal--input" value="'+data.data[i].supporters_goal_num+'">';
                newTop += '<input type="hidden" class="volunteers--goal--input" value="'+data.data[i].volunteers_goal_num+'">';
                newTop += '<div class="col-sm-6" style="padding:0;width: 100%;"><input type="hidden" class="id" value="'+data.data[i].proposal+'">';
                newTop += '<img class="icons" src="'+url_new+'images/x-icon.png" id="rejected" hidden><img class="icons" style="width: 50px;" src="'+url_new+'images/check-icon.png" id="supported" hidden><img class="icons" style="width: 48px;" src="'+url_new+'images/checkmark.png" id="support__plus--button" hidden>';
                newTop += '</div><div class="col-sm-6 home--followers hidden" style="width: 100%;">';
                newTop += '</div></div></div></div>';
            }
                $('#topten--proposals').append(newTop);
                
                setTimeout(function(){
                    $('#topten--proposals').show();
                    $('.spinner').hide();
                }, 3000);
                
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

            
    },
        error: function(response){
            console.log('error');
            console.log(response);
        }
    });
});