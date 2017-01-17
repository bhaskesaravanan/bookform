

$(document).ready(function() {
    $('#request').click(function() {
        var name = $('#requirebook').val();
        var author = $('#authorname').val();
        $.ajax({
            url: '/bookrequest',
            data: JSON.stringify({"name": name, "author": author}),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $("#flash").html(response.result);
//                alert(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#readbook').click(function() {
        var name = $('#bookname').val();
        if (name === '') {
            $('#flash').html('Please select a book to submit')
        }
        else {
            $.ajax({
            url: '/bookread',
            data: JSON.stringify({"name": name}),
            type: 'POST',
            success: function(response) {
                console.log(response);
                $("#flash").html(response.result);
//                alert(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
        }

    });

    $('#admin').click(function(event) {
        $.ajax({
            url: '/adminsignup',
            type: 'GET',
            success: function(response) {
                if (response.result === '') {
                    console.log(response);
                    window.location="/admin_signup_page";
                }
                else {
                    console.log(response);
                    $("#adminrequest").html(response.result)
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
        event.preventDefault();
    });
});