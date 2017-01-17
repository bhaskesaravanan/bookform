//function loadbook() {
//  var xhttp = new XMLHttpRequest();
//  xhttp.onreadystatechange = function() {
//    if (this.readyState == 4 && this.status == 200) {
//        var book=JSON.parse(this.responseText)
//        document.getElementById("book").innerHTML =book;
//    }
//  };
//  xhttp.open("GET", "is_down()", true);
//  xhttp.send();
//}



$(function() {
        $('#requestbutton').click(function() {
         var bookname=$('#requirebook').val()
         var authorname=$('#authorname'). val()

        $.ajax({
            url: '/bookvalidation',
            data: {'bookname':bookname, 'authorname':authorname},
            type: 'POST',
            success: function(response) {
                console.log(response)
                $('#msg').html(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


$(function() {
        $('#submitbutton').click(function() {
        var book=$('#book').val()

        $.ajax({
            url: '/bookread',
            data: {'book':book},
            type: 'POST',
            success: function(response) {
                console.log(response)
                $('#msg').html(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
