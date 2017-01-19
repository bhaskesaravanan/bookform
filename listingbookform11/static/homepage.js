var modal = document.getElementById('id01');
var modal= document.getElementById('id02');
var modal= document.getElementById('id03');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function Validate() {
        var password = document.getElementById("pswd").value;
        var confirmPassword = document.getElementById("rpswd").value;
        if (password != confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        return true;
    }





$(document).ready(function() {
        $('#buttonlogin').click(function() {
         var emailid=$('#uemail').val()
         var password=$('#psw'). val()

        $.ajax({
            url: '/loginpage',
            data: {'emailid':emailid, 'password':password},
            type: 'POST',
            success: function(response) {
                if (response.result === '') {
                    console.log(response)
                    window.location = '/userpage';
                    }
                else
                {   console.log(response);
                    $("#flash").html(response.result);

                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


$(function() {
        $('#adminbutton').click(function() {
         var emailid=$('#admin_mail').val()
         var password=$('#admin_password'). val()

        $.ajax({
            url: '/admin',
            data: {'emailid':emailid, 'password':password},
            type: 'POST',
            success: function(response) {
                console.log(response)
                if (response.result === '') {
                    window.location = '/adminpage';
                    }
                else
                {   console.log(response);
                    $("#adminflash").html(response.result);

                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});



$(document).ready(function() {
        $('#signupbutton').click(function() {
         var username=$('#uname').val()
         var emailid=$('#email').val()
         var password=$('#spsw'). val()
         var repassword=$('#repsw').val()
        if(password == repassword){
        $.ajax({
            url: '/signup',
            data: {'username':username,'emailid':emailid,'password':password},
            type: 'POST',
            success: function(response) {
                console.log(response)
                $('#signupflash').html(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
        }
        else
            alert("Passwords do not match.");

    });
});
