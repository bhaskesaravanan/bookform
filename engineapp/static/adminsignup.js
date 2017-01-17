
$(document).ready(function() {
    $('#signup').click(function() {
        var password = $('#password').val();
        var cpassword = $('#cpassword').val();
        if (password === cpassword) {
            $.ajax({
            url: '/signedup',
            data: {"password": password},
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location="/userpage"
                $("#adminrequest").html(response.result);
                alert(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
        }
        else {
            alert('Passwords do not match.')
        }
    });
});