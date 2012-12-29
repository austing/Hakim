

$(function() {
    $( "a#volume-link" ).hide().text("Click to use calculated volume").insertAfter( "input#id_volume" );
    $( "a#volume-link" ).click(function() {
        if($( "span#volume-estimate" ).text() != ""){
            $( "input#id_volume" ).val($( "span#volume-estimate" ).text());
        }
        $(this).hide();
    });
    $( ".spinner" ).spinner({ 
        min: 0,
        change: function( event, ui ){
            form = $(this).closest("form");
            $.post("/calculate_volume/", form.serialize(), function(data){
                $( "span#volume-estimate" ).text(data.volume);
                if($( "input#id_volume" ).val() == "0"){
                    $( "input#id_volume" ).val(data.volume);
                }else{
                    $( "a#volume-link" ).show();
                }
            });
        }
    });

});