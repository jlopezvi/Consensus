var url = window.location.href;
url = url.split("/");
var list;
$('.cropme2').simpleCropper();

$(document).ready( function() {
    $.ajax({
        url: url[0] + "//" + url[2] + '/get_topten_ideas',
        method: 'GET',
        success: function(data){
            console.log(data);
        },
        error: function(response){
            console.log('error');
            console.log(response);
        }
    });
});