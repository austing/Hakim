


$(function() {

    $( "div#devis" ).hide();
    $( "a#volume-link" ).hide().text("Utiliser ce chiffre");
    $( "a#volume-link" ).click(function() {
        if($( "span#volume-estimate" ).text() != ""){
            $( "input#id_volume" ).val($( "span#volume-estimate" ).text()).trigger('change');
        }
        $(this).hide();
    });
    $( ".meuble-quantite.spinner" ).spinner({ 
        min: 0,
/*        stop: function( event, ui ){
            $( document.activeElement ).blur().focus();
        },*/
        change: function( event, ui ){
            form = $(this).closest("form");
            $.post("/calculate_volume/", form.serialize(), function(data){
                $( "span#volume-estimate" ).text(data.volume);
                $( "div#devis" ).show();
                $( "div#devis-option" ).hide();
                if($( "input#id_volume" ).val() == "0"){
                    $( "input#id_volume" ).val(data.volume);
                }else{
                    $( "a#volume-link" ).show();
                }
            });
        }
    });
    $( ".spinner" ).not(".meuble-quantite").spinner({ 
        min: 0,
    });

    $(document).ready(function(){
            $(".chambre .togglelink").each(function(){ $(this).parent('.chambre').next("li.meubles").toggle();
            if($(this).children("span.toggle-triangle:first").text() == "►"){
                $(this).children("span.toggle-triangle:first").text("▼");
            }else{
                $(this).children("span.toggle-triangle:first").text("►");
            }
            });
    });

    $( ".chambre .togglelink" ).click(function(){
        $(this).parent('.chambre').next("li.meubles").slideToggle();
        if($(this).children("span.toggle-triangle:first").text() == "►"){
            $(this).children("span.toggle-triangle:first").text("▼")
        }else{
            $(this).children("span.toggle-triangle:first").text("►")
        }
    });
});