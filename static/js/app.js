$( "#search_box" ).submit(function( event ) {
    event.preventDefault();
    $.ajax({
        type: "POST",
        url: "/search",
        data: $("#search_form").serialize(),
        success: function(response){
            $("#result").empty()

            let type = typeof response

            if(type == "string"){
                $("#result").append("<p>" + response + "</p>")
            } else {
                let length = response.length
                for(var i = 0; i < length; i++){
                    $("#result").append("<p>" + response[i].artistName + "</p>")
                }
            }
        },
        error: function(){
            $("#result").append("<p> AJAX error. </p>")
        }
    })
});