var layer_message;
var icon_message;
var map_message;
var title_message;

function feature_drawn(){
    return shape_drawn;
}
function entered_name(form){
    return form.name.value != ""
}
function selected_layer(form){
    return form.layer.selectedIndex != 0
}
function selected_icon(form){
    return form.icon.selectedIndex != 0
}
function checkForm(form){
    var form_valid = true;
    hide_all();
    if(!feature_drawn()){
        map_message.show();
        form_valid = false;
    }
    if(!entered_name(form)) {
        title_message.show();
        form_valid = false;
    }
    if(!selected_layer(form)){
        layer_message.show();
        form_valid = false;
    }
    if(!selected_icon(form)){
        icon_message.show();
        form_valid = false;
    }
    return form_valid;shape_drawn
}
function hide_all(){
    layer_message.hide();
    icon_message.hide();
    title_message.hide();
    map_message.hide();
}
$(document).ready(function(){
    layer_message = $("#layer-form-issue");
    icon_message = $("#icon-form-issue");
    map_message = $("#map-form-issue");
    title_message = $("#title-form-issue");
});
