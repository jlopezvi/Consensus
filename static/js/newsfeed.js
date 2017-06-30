var url = window.location.href;
url = url.split("/");
var list;

$(document).ready(function(){
	$('.home--content').css('background-image','url("")');
	$('#nav--home').css('display', 'none');
	$('#nav--participants').css('display', 'none');
	$('#nav--top_ten').css('display', 'none');
	$('.add--proposal--button').css('display', 'none');
	$('#middle--home--button').on('click', function(e){
      e.preventDefault();
	});

	$.ajax({
    url: url[0] + "//" + url[2] + '/ideas_for_newsfeed',
    type: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    dataType: 'json',
    success: function(json) {
      list = json.data;
      //console.log(list);
      $('#list__id').val(0);
      if(list.length > 1){
        $('.arrow__newsfeed__right').show();
      }
      showContent(0);
      setTimeout(function(){
	      $('#newsfeed__body').show();
	      $('.spinner').hide();
      }, 4000);
    },
    error: function(response){
      if(response.responseText == "redirect to Home"){
        alert("Redirecting to Home");
        window.location = '/home';
      }
    }
  });
  
  $(document).on('click', '.glyphicon', function(){
    var side = $(this).attr('id');
    var id = $('#list__id').val();
    moveFeed(side, id);
  })
});

function showContent(id){
  $('#list__id').val(id);
  console.log(id);
  if(list[id].author_photo_url != ''){
    $('#picture__profile').attr('src', list[id].author_photo_url).show();
    $('#picture__profile').next().hide();
  }
  if(list[id].image_url != '')
    $('.newsfeed--body').css('background-image', 'url('+list[id].image_url+')');
  $('.newsfeed--name a').empty().append(list[id].author_username);
  $('.duration--info').empty().append(list[id].duration);
  var support_percent = (list[id].supporters_num * 100)/ list[id].supporters_goal_num;
  $('.newsfeed--bar').css('width',support_percent+'%');
  var volunter_percent = (list[id].volunteers_num * 100)/ list[id].volunteers_goal_num;
  $('.newsfeed--bar2').css('width',volunter_percent+'%');
  $('.newsfeed--goals p').empty().append(list[id].supporters_num+"/"+list[id].supporters_goal_num+" supporters goals<br>"+list[id].volunteers_num+"/"+list[id].volunteers_goal_num+" volunteers goals");
  $('.newsfeed--problem').empty().append(list[id].concern);
  $('.newsfeed--proposal').empty().append(list[id].proposal);
  var total = ((list[id].supporters.length * 100) / (list[id].supporters.length + list[id].rejectors.length));
  if((list[id].supporters.length + list[id].rejectors.length) == 0)
    total = 0;
  $('.input--percent label').empty().append('Support Rate: '+Math.floor(total)+'%');
  /****************************************** Add Supporters to the Supporters List ****************************************/
  if(list[id].supporters.length > 0){
    for(var i =0; i<=2; i++){
      $('#newsfeed--supporters ul').empty().append("<a href='#'><li>"+list[id].supporters[i].username+"</li></a>");
    }
  }
  if(list[id].supporters.length > 3){
    $('#newsfeed--supporters ul').empty().append("<a href='#' class='last--liked'><li>"+(list[id].supporters.length - 3)+"</li></a>");
  }
  else if(list[id].supporters.length == 0){
    $('#newsfeed--supporters ul').empty().append("<a href='#' class='last--liked'><li>0 people</li></a>");
  }
  /****************************************** Add Supporters to the Supporters List ****************************************/
  if(list[id].supporters.rejectors > 0){
    for(var i =0; i<=2; i++){
      $('#newsfeed--rejectors ul').empty().append("<a href='#'><li>"+list[id].rejectors[i].username+"</li></a>");
    }
  }
  if(list[id].rejectors.length > 3){
    $('#newsfeed--rejectors ul').empty().append("<a href='#' class='last--liked'><li>"+(list[id].rejectors.length - 3)+"</li></a>");
  }
  else if(list[id].rejectors.length == 0){
    $('#newsfeed--rejectors ul').empty().append("<a href='#' class='last--liked'><li>0 people</li></a>");
  }
}

function moveFeed(element, id){
  var intID = parseInt(id);
  if((element == 'left__feed') && (id > 0)){
    $('#newsfeed__body').hide();
    $('.spinner').show();
    
    $('#right__feed').show();
    showContent(intID-1);
    setTimeout(function(){
      $('#newsfeed__body').show();
      $('.spinner').hide();
    }, 2500);
    if(id == 1)
      $('#'+element).hide();
    else
      $('#'+element).show();
  } else if((element == 'right__feed') && (id < (list.length-1))){
    $('#newsfeed__body').hide();
    $('.spinner').show();
    
    $('#left__feed').show();
    showContent(intID+1);
    setTimeout(function(){
      $('#newsfeed__body').show();
      $('.spinner').hide();
    }, 2500);
    
    if(id == (list.length-2))
      $('#'+element).hide();
    else
      $('#'+element).show();
  }
}