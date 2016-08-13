var InputField = function(message_identifier,is_valid_cond){
    this.check = function(form){
        return is_valid_cond(form)
    }
    this.hideMessage = function(){
        $(message_identifier).hide();
    }
    this.showMessage = function(){
        $(message_identifier).show();
    }
}
var validators = [
    new InputField("#map-form-issue",function(form){
        return form.geojson.value != "";
    }),
    new InputField("#icon-form-issue",function(form){
        return form.icon.selectedIndex != 0
    }),
    new InputField("#title-form-issue",function(form){
        return form.name.value != ""
    }),
    new InputField("#layer-form-issue",function(form){
        return form.layer.selectedIndex != 0
    })
]

function checkForm(form){
    /*
   :param form: Special builtin form object.
   :returns: Whether the form is vaild or not. If it returns false, then the form is not submitted.
    */
    var is_valid = true;
    validators.forEach(function(validator){
        if(validator.check(form)){
            validator.hideMessage();
        }
        else{
            is_valid = false;
            validator.showMessage();
        }
    })
    return is_valid;
}
function showUploadImg($div,input) {
    /*
    Reads image from input and displays it on the div's preview image element.
    */
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $div.children().children().children('[name="img-preview"]').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
function enable_file_upload_preview($div){
    $div.find('.img-input').change(function(){
        showUploadImg($div,this);
    });
}
function add_new_after($div){
    var $nextdiv = $new_img_div();
    $div.after($nextdiv);
    return $nextdiv;
}
function delete_div($div){
    $div.remove()
}
function activate_add_button($div){
    var $add_button = $div.find("button.add-button");
    $add_button.click(function(){
        add_new_after($div)
    })
}
function activate_del_button($div){
    var $del_button = $div.find("button.del-button");
    $del_button.click(function(){
        delete_div($div)
    })
}
function activate_buttons($div){
    activate_add_button($div)
    activate_del_button($div)
    enable_file_upload_preview($div)
}
function $new_img_div(){
    /*
    Clones a new div from the img-model and turns it into a JQuery that will correctly
    display the image form. Does not add it to the DOM.
    */
    var $retdiv = $("div.img-model").clone(true,true);
    $retdiv.show();
    $retdiv.removeClass("img-model");
    $retdiv.addClass("rootimg");

    //sets today's date as default
    var today = new Date();//today's date
    $retdiv.find('[name="month"]').attr('placeholder',today.getMonth()+1);
    $retdiv.find('[name="year"]').attr('placeholder',today.getFullYear());
    activate_buttons($retdiv);
    return $retdiv;
}
function make_img_div(img,$last_div){
    var $img_div = add_new_after($last_div)
    $img_div.find('[name="month"]').val(img.month);
    $img_div.find('[name="year"]').val(img.year);
    $img_div.find('[name="img-descrip"]').val(img.description);
    $img_div.find('[name="img_id"]').val(img.id);
    $img_div.find('[name="img-preview"]').attr('src',"/static/thumbnails/"+img.filename);
    $img_div.find('[name="file"]').removeAttr('required');
    return $img_div;
}
function initalize_edit_images(){
    var $last_img_div = $("#img-start");
    ip_images.forEach(function(img){
        $last_img_div = make_img_div(img,$last_img_div);
    });
}
$(document).ready(function(){
    $("#root-add-button").click(function(){
        add_new_after($("#img-start"))
    })
    initalize_edit_images();
});
