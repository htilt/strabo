//flickety object
var flkty;
//photoswipe object
var gallery;
//list of image objects passed from post call in ip_clicked
var imgs;
//heigt of text section (in percent)
var top_height = 49;
//heigt of carousel section (in percent)
var caro_height = 45;
//popup max-width in pixels
var popup_max_width = 700;
//popup max-height in pixels
var popup_max_height = 800;




function hide_popup(){
    $('.popup').hide();
    $('.popup-background').hide();
}
function show_popup(){
    $('.popup').show();
    $('.popup-background').show();
}

function get_thumb_dim(img){
    ratio = Math.min(THUMBNAIL_MAX_SIZE[0]/img.width,THUMBNAIL_MAX_SIZE[1]/img.height)
    return {width:ratio*img.width,height:ratio*img.height}
}
function transform(type,perc){
    return type + ":translateY(" + perc + "%);";
}
function tranform_all(perc){
    var all = transform("transform",perc);
    all += transform("-ms-transform",perc);
    all += transform("-webkit-transform",perc);
    return all;
}
//this function loads the text and images associated
//with a selected interest point
//example output:
// <div class="carousel-cell"><img src= "static/thumbnails/download.jpg"/></div>
function get_carosel_html(img){
    var html = '<div class="carousel-cell padded-pic">';
    dim  = get_thumb_dim(img);
    html += '<div class="vertical-center">'
    //html += '<div style="position:relative;top:' + (top_height+(caro_height/2)) + '%;'+tranform_all(-caro_height/2)+' ">'
    html += '<img style="width:'+dim.width+'px;height:'+dim.height+'px;" src="static/thumbnails/' + img.filename + '"/>';
    //html += '<p>' + img.description + '</p>';
    html += '</div>';
    html += '</div>';
    console.log(html);
    return html;
}
function remove_all_carosel_entries(){
    flkty.remove(flkty.getCellElements());
}
//adds all the imag data to the garosel in the oder
function add_carosel_entries(imgs){
    var carousel_html = "";
    imgs.forEach(function(img){
        var $cellElems = $(get_carosel_html(img));
        flkty.append($cellElems);
    });
}

//brings up popup associated with feature ip
function ip_clicked(db_id) {
    //sends a request to the server tp return the information associated with the
    // database feature id
    $.post(
        "/map/post",
        {db_id:db_id},
        function(data){
            imgs = data.images;
            var ip_descrip = data.description;
            var ip_title = data.title;

            //renders the popup
            show_popup();

            remove_all_carosel_entries();

            add_carosel_entries(imgs);

            $("#ip_description").text(ip_descrip);
            $("#ip_title").text(ip_title);

            // resize after un-hiding Flickity
            flkty.resize();
            flkty.reposition();
        }
    );
}

function set_flickety_click(){
    flkty.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
        if (cellElement) {
            make_photoswipe(cellIndex);
        }
    });
}

function make_photoswipe(pic_index){
    // execute above function
    var element = document.querySelectorAll('.pswp')[0];

    var items = [];
    imgs.forEach(function(img){
        items.push({
            src:'static/uploads/' + img.filename,
            w:img.width,
            h:img.height
        });
    });
    var options = {
        index:pic_index
    };

    gallery = new PhotoSwipe(element, PhotoSwipeUI_Default, items, options);

    gallery.init();
}
function set_popup_sizes(){
    $(".top-section").css("height","" + (top_height) + "%");
    $(".carousel-wrapper").css("height","" + (caro_height) + "%");
    //ar transform_dis =
    //$(".carousel-wrapper").css("transform","translateY(" +  + "px)");
    $("#carouselholder").addClass("vertical-center");
    $("#carouselholder").css("height","" + (100) + "%");
    //$("#carouselholder").css("top","" + (-caro_height/2) + "%");
    /*$("#carouselholder").css("transform","translateY(" + (-caro_height/2) + "%");
    $("#carouselholder").css("-ms-transform","translateY(" + (-caro_height/2) + "%");
    $("#carouselholder").css("-webkit-transform","translateY(" + (-caro_height/2) + "%");*/

    $(".text-section").css("height", "" + (100 - caro_height - top_height) + "%");
    $(".popup-foreground").css("max-height", "" + popup_max_height + "px");
    $(".popup-foreground").css("max-width", "" + popup_max_width + "px");
}
function set_flickety_img_title(){
    flkty.on( 'cellSelect', function() {
        var img = imgs[flkty.selectedIndex];

        $("#img_description").text(img.description);

        var elmts = flkty.getCellElements();
        elmts.forEach(function(elmt){
            elmt.style.background = "Transparent";
        });
        flkty.selectedElement.style.background = "rgba(0,0,0,.5)"
    })
}

function flickety_init(){
    flkty = new Flickity(document.getElementById("carouselholder"),
        {imagesLoaded: true,
        pageDots:false,
        resize: true,
        setGallerySize: false}
    );
    set_flickety_img_title();
    set_flickety_click();
}
