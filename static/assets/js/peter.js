$(document).ready(function (){

    $('.btn-name-mdl-create').click(function(){
        name = $(this).attr("data-mdl-name");
        active = $(this).attr("data-mdl-sh");
        for(var i=0; i<100; i++ ){
            $(".sh-" + i).hide();
        }
        $("." + active).show();
        $("." + active + " form").attr("id",active)
        $("#save_modal_create").attr("data-submit-send",active);
        console.log(typeof(name));
        console.log(name);
        if(name !== "undefined"){
            $("#name_modal_create").text(name);
        }else{
            $("#name_modal_create").text("Necesitas agregar al btn el atributo \"data-mdl-name\"");
        }
        xform = $("#modal-without-animation form");
    });


})
