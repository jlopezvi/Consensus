//cannot use $('form').serializeArray() or $('form').serialize()
//needs custom made function: serializeObject()
//from  http://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jquery
// http://jsfiddle.net/sxGtM/3/
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(function(){
	$('button').click(function(){
        //var name = $('#txtname').val();
        //var surname = $('#txtsurname').val();
        //var email = $('#txtemail').val();
		//var password = $('#txtpassword').val();
        //var formData= "{ name: "+ name +", surname: "+ surname + ", email: "+email +", password: "+password+"}";
        var formData=JSON.stringify($('form').serializeObject());
        console.log('formData',formData)
        var request = $.ajax({
            type: 'POST',
			url: '/addUser',
			data: formData,
            contentType: 'application/json',
            scriptCharset: 'utf-8',
            dataType: 'json'
			//success: function(response){
            //    console.log(response);
			//},
			//error: function(error){
			//	console.log(error);
			//}
		});

        request.done(function( msg ) {
            console.log( msg );
            //host_email is either an e-mail or the string 'None'
            if (host_email != 'None'){
                console.log('test');
                var current=$('#txtemail').val();
                var newFollowingContact=host_email; 
                var data_2ndrequest = JSON.stringify({current: current, newFollowingContact: newFollowingContact});
		        console.log("test2", data_2ndrequest);
                $.ajax({
                    type: 'POST',
                    url: '/addFollowingContactToUser',
                    data: data_2ndrequest,
                    contentType: 'application/json',
                    scriptCharset: 'utf-8',
                    dataType: 'json',
                    success: function(result){
                        console.log(result);
			        }
                }) ;
            }
        });

	});
});


