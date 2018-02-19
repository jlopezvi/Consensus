var url = window.location.href;
url = url.split("/");
var list;
$('.cropme2').simpleCropper();

$(document).ready( function() {
  $('.home--select div').slideUp();
	$('.select--triangle').on('click',function(){
    if( $('.select--options').css('display') == 'block'){
      $('.select--options').slideUp('fast');
      $('.select--triangle').removeClass('active-triangle');
    }
    else {
      $('.select--options').slideDown();
      $('.select--triangle').addClass('active-triangle');
    }
  });
  $('.unselected--option').on('click',function(){
    var current_opt = $('.selected--option').html();
    var type_vote = $(this).children().attr('id');
    $('.selected--option').html('').html($(this).html());
    $(this).html('').html(current_opt);
    $('.select--options').slideUp(100);
    $('.select--triangle').removeClass('active-triangle');
    
    $('#home--proposals').hide();
    $('#today').empty();
    $('#uno').hide();
    $('#lastweek').empty();
    $('#dos').hide();
    $('#thismonth').empty();
    $('#tres').hide();
    $('#older').empty();
    $('#cuatro').hide();
    homeVue.getHomeIdeas(type_vote);
    homeVue.selected_view = type_vote;
  });
  
  /*
  $(document).on('click', '.home--share--button', function(){
    var vote_type = $(this).attr('id');
    var index_idea = $(this).parent().parent().children('input').val();
    var vote_ifvolunteered = false;
    if(vote_type == 'supported-plus'){
      vote_ifvolunteered = true;
      vote_type = 'supported';
    }
    var element = $(this).parent().parent().parent().parent();
      
    var data = {
      'idea_proposal': list[index_idea]['proposal'],
      'vote_ifvolunteered': vote_ifvolunteered,
      'vote_type': vote_type
    };
      
    $.ajax({
      url: url[0] + "//" + url[2] + '/vote_on_idea',
      type: 'POST',
      data: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
      dataType: 'json',
      success: function(json){
        ////console.log(json);
        if(data.vote_type == 'supported' || data.vote_type == 'supported-plus')
          var answer = 'Now you are supporting this idea!';
        else
          var answer = 'Idea rejected successfully!';
        if(json.result == 'OK: User vote was modified'){
          $('#invitation-modal-info h4.modal-title').empty().append('Operation Completed');
          $('#invitation-modal-info p#modal--invitation').empty().append(answer);
          element.fadeOut('slow', function(){ element.remove(); });
        } else if (json.result == 'Wrong: User vote exists of same type'){
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
  });
  */
  
}); 

function loadHomeIdeas(type_vote){
  $('.spinner').show();
  $.ajax({
    url: url[0] + "//" + url[2] + '/ideas_for_home',
    type: 'POST',
    data: JSON.stringify({'vote_type': type_vote}),
    headers: {
      'Content-Type': 'application/json'
    },
    success: function(json){
      ////console.log(json.data);
      list = json.data;
      for(i=0; i<json.data.length;i++){
        showIdeas(json.data[i], i);
      }
      setTimeout(function(){
        $('#home--proposals').show();
        $('.spinner').hide();
      }, 2500);
    },
    error: function(response){
      //console.log('error');
      //console.log(response);
    }
	});
}

function showIdeas(list, index){
  //console.log(list);
  var code = '';
  code += '<div class="col-xs-12 col-sm-6 home--content--proposal">';
  code += '<div class="row home--header">';
  code += '<input type="hidden" class="idea__id" value="'+list.proposal+'">';
  // IF IDEA DOESNT HAVE ANONYMOUS AUTHOR 
  if(list.if_author_public){
  	code += '<div class="col-sm-1" style="padding-left: 0px;">';
  	code += '<div class="home--profile--picture pic--home"><img src="'+list.author_profilepic_url+'"></div></div>';
  	code += '<div class="col-sm-3 home--name"><a href="/participants/'+list.author_email+'">'+list.author_username+'</a></div>';
  	code += '<div class="col-sm-1 newsfeed--duration"><p><img style="width:20px;position:relative;top:-3px;" src="/static/images/clock-icon.png">&nbsp;';
  	code += '<p class="duration--info">&nbsp;'+list.duration+'</p></p></div>';
  } else {
    code += '<div class="col-sm-1 newsfeed--duration"><p><img style="width:20px;position:relative;top:-3px;" src="/static/images/clock-icon.png">&nbsp;';
  	code += '<p class="duration--info">&nbsp;'+list.duration+'</p></p></div>';
    code += '<div class="col-sm-1" style="padding-left: 0px;"></div>';
  	code += '<div class="col-sm-3 home--name"></div>';
  }
	
	var support_percent = (list.supporters_num*100)/list.supporters_goal_num;
  if (list.volunteers_goal_num > 0) {
    code += '<div class="col-sm-3 home--charge"><div class="progress home--progress">';
    code += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+support_percent+'%"></div></div>';
    code += '<div class="progress home--progress2">';
  }else{
    code += '<div class="col-sm-3 home--charge" style="top:22px!important;"><div class="progress home--progress">';
    code += '<div class="progress-bar newsfeed--bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+support_percent+'%"></div></div>';
    code += '<div>';
  }
  
	var volunter_percent = (list.volunteers_num*100)/list.volunteers_goal_num;
	code += '<div class="progress-bar newsfeed--bar2" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width:'+volunter_percent+'%"></div>';
	var _top = '';
  if(((index+1)%2)==0)
    _top = 'margin-top: 1px;';
	if (list.volunteers_goal_num > 0) {
	  code += '</div></div><div class="col-sm-4 newsfeed--goals">';
	  code += '<p>'+list.supporters_num+'/'+list.supporters_goal_num+' supporters<br>';
	  code += '<p>'+list.volunteers_num+'/'+list.volunteers_goal_num+' volunteers<br>';
	  
	  code += '</div></div><div class="row home--proposals--body" style="'+_top+'background-image: url('+list.image_url+');">';
	} else {
	  code += '</div></div><div class="col-sm-4 newsfeed--goals" style="top:16px!important;">';
	  code += '<p>'+list.supporters_num+'/'+list.supporters_goal_num+' supporters<br>';
	  if(list.if_author_public)
	    code += '</div></div><div class="row home--proposals--body" style="height:352px;margin-top: 5px;background-image: url('+list.image_url+');">';
   else
      code += '</div></div><div class="row home--proposals--body" style="height:352px;margin-top: 24px;background-image: url('+list.image_url+');">';
	}
	code += '<div class="col-sm-12"><div class="col-sm-11 newsfeed--problem">'+list.concern+'</div>';
	code += '</div><div class="col-sm-12"><div class="col-sm-11 col-sm-offset-1 newsfeed--proposal">'+list.proposal+'</div></div>';
	code += '</div><div class="row newsfeed--footer">';
	code += '<div class="col-sm-12" style="padding-right: 0px; padding-left: 0px;">';
	code += '<div class="col-sm-9 newsfeed--support" style="padding-right:0;padding-left:30px;">';
	code += '<div class="input--percent"><label>	Support Rate: '+list.support_rate+'%</label></div></div>';
	code += '<div class="col-sm-1 redflag--img"><img class="redflag" src="/static/images/redflag.png"></div>';
	code += '<div class="col-sm-2 neewsfeed--moreinfo" style="float:right;"><input type="button" name="more-info" class="home--button">';
	code += '</div><div id="more--info--modal" hidden><p><h4>  More information about the problem: </h4> '+list.moreinfo_concern+'</br></br><h4> More information about the proposal: </h4>'+list.moreinfo_proposal+'</p></div></div></div>';
	
  code += '<div class="row home--share"><div class="col-sm-8 home--share--icons">';
  code += '<input type="hidden" class="index--idea" value="'+index+'">';
	code += '<div class="col-sm-6" style="padding:10px 8px;">';
	//code += '<img src="/static/images/x-icon.png" class="home--share--button" id="rejected">';
	//code += '<img style="width: 50px;" src="/static/images/check-icon.png" class="home--share--button" id="supported">';
  code += '<div id="rejected" class="home--share--button"></div>';
  code += '<div id="supported" class="home--share--button"></div>';
  if (list.volunteers_goal_num > 0) {
    //code += '<img style="width: 50px;" src="/static/images/checkmark.png" class="home--share--button" id="supported-plus">';
    code += '<div id="supported-plus" class="home--share--button"></div>';
  }
	code += '</div><div class="col-sm-6 home--followers hidden"><i class="fa fa-share-alt"></i><p>Share with: followers</p></div></div></div>';
	
	code += '<div class="row newsfeed--persons" style="left: -20px;width: 106%;"><div class="col-sm-12">';
	code += '<div class="col-sm-1" style="padding:0;"><img style="width:25px;" src="/static/images/check-hover.png"></div>';
	code += '<div class="col-sm-11 newsfeed--likes"><ul>';
	

	if(list.identified_supporters.length > 0){
		for(var f=0; f<list.identified_supporters.length; f++){
			if(list.identified_supporters[f].email != 'user')
				code += '<a href="/participants/'+list.identified_supporters[f].email+'"><li>'+list.identified_supporters[f].username+'</li></a>';
			else
				code += '<a href="/participants"><li>'+list.identified_supporters[f].username+'</li></a>';
		}
	} 
	code += '<a href="#" class="last--liked"><li>'+list.unidentified_supporters_text+'</li></a>';
	
	code += '</ul></div></div><div class="col-sm-12"><div class="col-sm-1" style="padding:0;"><img style="width:25px;" src="/static/images/reject-hover.png"></div>';
	code += '<div class="col-sm-11 newsfeed--likes"><ul>';
	
	if(list.identified_rejectors.length > 0){
		for(var f=0; f<list.identified_rejectors.length; f++){
			if(list.identified_rejectors[f].email != 'user')
				code += '<a href="/participants/'+list.identified_rejectors[f].email+'"><li>'+list.identified_rejectors[f].username+'</li></a>';
			else
				code += '<a href="/participants"><li>'+list.identified_rejectors[f].username+'</li></a>';
		}
	} 
	code += '<a href="#" class="last--liked"><li>'+list.unidentified_rejectors_text+'</li></a>';
	
  code += '</ul></div></div></div>';
	code += '</div>';
	/*
	if (list.vote_duration == '<24h') {
    $('#today').append(code);
  }else
  if (list.vote_duration == '<7days') {
    $('#lastweek').append(code);
  }else
  if (list.vote_duration == '<30days') {
    $('#thismonth').append(code);
  }else{
    $('#older').append(code);
  }
  if($('#today').children().length >0)
    $('#uno').show();
  if($('#lastweek').children().length>0)
    $('#dos').show();
  if($('#thismonth').children().length>0)
    $('#tres').show();
  if($('#older').children().length>0)
    $('#cuatro').show();
  */
}

homeVue = new Vue({
  el: '#homeContainer',
  data: {
    path_get_ideas: url[0] + '//' + url[2] + '/ideas_for_home',
    path_vote_idea: url[0] + "//" + url[2] + '/vote_on_idea',
    day_ideas: [],
    week_ideas: [],
    month_ideas: [],
    older_ideas: [],
    logged_user: '',
    selected_view: 'supported'
  },
  mounted: function(){
      this.getHomeIdeas('supported');
  },
  methods: {
    
    getHomeIdeas: function(vote_type){
      self = this;
      $('#home--proposals').hide();
      $('.spinner').show();
      $.ajax({
        url: self.path_get_ideas,
        type: 'POST',
        data: JSON.stringify({'vote_type': vote_type}),
        headers: {
          'Content-Type': 'application/json'
        },
        success: function(json){
          var ideas = json.data;
          console.log(ideas);
          self.logged_user = $('#host_email').val();
          for(var i=0; i< ideas.length; i++){
            if(ideas[i].vote_duration == '<24h'){
              self.day_ideas.push(ideas[i]);
              $('#uno').show();
            } else if(ideas[i].vote_duration == '<7days'){
              self.week_ideas.push(ideas[i]);
              $('#dos').show();
            } else if(ideas[i].vote_duration == '<30days'){
              self.month_ideas.push(ideas[i]);
              $('#tres').show();
            } else {
              self.older_ideas.push(ideas[i]);
              $('#cuatro').show();
            }
          }
          $('#home--proposals').show();
          $('.spinner').hide();
        }
    	});
    },
        
    showMoreInfoModal: function(index, container){
      $('#'+container).find('.more_info_div[info="'+index+'"]').slideToggle( "slow" );
    },
    
    showRedFlagModal: function(index, container, e){
      e.preventDefault();
      self = this;
      var idea_index = '';
      switch(container){
        case 'today':
          idea_index = self.day_ideas[index].proposal;
          break;
        case 'lastweek':
          idea_index = self.week_ideas[index].proposal;
          break;
        case 'thismonth':
          idea_index = self.month_ideas[index].proposal;
          break;
        case 'older':
          idea_index = self.older_ideas[index].proposal;
          break;
      }
      $('#idea_index').val(idea_index);
      $('#redflag-modal').modal('toggle');
    },
    
    redflagRemoveIdea: function(idea_index){
      this.validateProposalInArray(this.day_ideas, idea_index);
      this.validateProposalInArray(this.week_ideas, idea_index);
      this.validateProposalInArray(this.month_ideas, idea_index);
      this.validateProposalInArray(this.older_ideas, idea_index);
    },
    
    validateProposalInArray: function(array, idea_index){
      if(array.length > 0){
        for(var i=0; i<array.length; i++){
          if(array[i].proposal == idea_index){
            array.splice(i, 1);
          }
        }
      }
    },
    
    voteIdea: function(type, proposal, vote_type, ifvolunteered, idea_type){
      var vote_ifvolunteered = false;
      if(type == 'supported-plus'){
        vote_ifvolunteered = true;
        type = 'supported';
      }
      if((vote_type != type) || ((vote_type == type) && (ifvolunteered != vote_ifvolunteered))){
        self = this;
        var data = {
          'idea_proposal': proposal,
          'vote_ifvolunteered': vote_ifvolunteered,
          'vote_type': type
        };
        
        $.ajax({
          url: self.path_vote_idea,
          type: 'POST',
          data: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          },
          dataType: 'json',
          success: function(json){
            if(self.selected_view != data.vote_type){
              self.validateProposalInArray(self.day_ideas, data.idea_proposal);
              self.validateProposalInArray(self.week_ideas, data.idea_proposal);
              self.validateProposalInArray(self.month_ideas, data.idea_proposal);
              self.validateProposalInArray(self.older_ideas, data.idea_proposal);
            } else {
              self.changeCurrentIdeaData(idea_type, proposal, vote_ifvolunteered);
            }
          },
          error: function(response){
            console.log('error');
            console.log(response);
          }
      	});
      }
    },
    
    showHoverButton: function(vote_type, if_volunteered, plus){
      if((vote_type == 'supported') && if_volunteered && plus)
        return true;
      else if((vote_type == 'supported') && !if_volunteered && !plus)
        return true;
      return false;
    },
    
    changeCurrentIdeaData: function(idea_type, proposal, ifvolunteered){
      switch(idea_type){
        case 'day':
          if(ifvolunteered){
            for(var i=0; i<this.day_ideas.length; i++){
              if(this.day_ideas[i].proposal == proposal){
                this.day_ideas[i].volunteers_num++;
                this.day_ideas[i].vote_ifvolunteered = true;
              }
            }
          } else {
            for(var i=0; i<this.day_ideas.length; i++){
              if(this.day_ideas[i].proposal == proposal){
                this.day_ideas[i].volunteers_num--;
                this.day_ideas[i].vote_ifvolunteered = false;
              }
            }
          }
          break;
        case 'week':
          if(ifvolunteered){
            for(var i=0; i<this.week_ideas.length; i++){
              if(this.week_ideas[i].proposal == proposal){
                this.week_ideas[i].volunteers_num++;
                this.week_ideas[i].vote_ifvolunteered = true;
              }
            }
          } else {
            for(var i=0; i<this.week_ideas.length; i++){
              if(this.week_ideas[i].proposal == proposal){
                this.week_ideas[i].volunteers_num--;
                this.week_ideas[i].vote_ifvolunteered = false;
              }
            }
          }
          break;
        case 'month':
          if(ifvolunteered){
            for(var i=0; i<this.month_ideas.length; i++){
              if(this.month_ideas[i].proposal == proposal){
                this.month_ideas[i].volunteers_num++;
                this.month_ideas[i].vote_ifvolunteered = true;
              }
            }
          } else {
            for(var i=0; i<this.month_ideas.length; i++){
              if(this.month_ideas[i].proposal == proposal){
                this.month_ideas[i].volunteers_num--;
                this.month_ideas[i].vote_ifvolunteered = false;
              }
            }
          }
          break;
        case 'older':
          if(ifvolunteered){
            for(var i=0; i<this.older_ideas.length; i++){
              if(this.older_ideas[i].proposal == proposal){
                this.older_ideas[i].volunteers_num++;
                this.older_ideas[i].vote_ifvolunteered = true;
              }
            }
          } else {
            for(var i=0; i<this.older_ideas.length; i++){
              if(this.older_ideas[i].proposal == proposal){
                this.older_ideas[i].volunteers_num--;
                this.older_ideas[i].vote_ifvolunteered = false;
              }
            }
          }
          break;
      }
    }
    
  },
  delimiters: ["<%","%>"]
});