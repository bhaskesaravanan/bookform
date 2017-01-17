// Get the modal
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
        var password = document.getElementById("psw").value;
        var confirmPassword = document.getElementById("cpsw").value;
        if (password != confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        return true;
    }


$(document).ready(function() {
    $('#loginbutton').click(function() {
        var name = $('#username').val();
        var password = $('#userpassword').val();
        $.ajax({
            url: '/loginpage',
            data: {"name": name, "password": password},
            type: 'POST',
//            async: true,
            success: function(response) {
                if (response.result == '') {
                      window.location="/userpage";
                }
                else {
                    console.log(response);
                $("#loginflash").html(response.result);

                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#adminbutton').click(function() {
        var adminname = $('#adminname').val();
        var password = $('#password').val();
        $.ajax({
            url: '/admin',
            data: {"adminname": adminname, "password": password},
            type: 'POST',
            async: true,
            success: function(response) {
                if (response.result == '') {
                      window.location="/adminpage";
                }
                else {
                    console.log(response);
                $("#adminflash").html(response.result);

                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });


    $('#signupbutton').click(function() {
        var uname = $('#uname').val();
        var umail = $('#umail').val();
        var psw = $('#psw').val();
        var cpsw = $("#cpsw").val();
        if (psw === cpsw) {
            $.ajax({
            url: '/signup',
            data: {"uname": uname, "umail": umail, "psw": psw},
            type: 'POST',
            async: true,
            success: function(response) {
                console.log(response);
                $("#signupflash").html(response.result);

            },
            error: function(error) {
                console.log(error);
            }
        });
        }
        else {
            alert('Passwords do not match.');
        }
    });

});