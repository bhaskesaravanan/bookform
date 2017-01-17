
$(document).ready(function() {
    $('#submit').click(function() {
        var bookname = $('#bookname').val();
        var genre = $('#bookgenre').val();
        var authorname = $('#authorname').val();
        $.ajax({
            url: '/addingbook',
            data: {"bookname": bookname, "authorname": authorname, "genre": genre},
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
});