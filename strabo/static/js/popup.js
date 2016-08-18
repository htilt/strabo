//flickity object
var flkty;
//photoswipe object
var gallery;
//list of image objects passed from post call in ip_clicked
var imgs;

function hide_popup(){
    $('.popup').hide();
    $('.popup-background').hide();
}
function show_popup(){
    $('.popup').show();
    $('.popup-background').show();
}
//calculates thumbnail size from the full size image size passed in
function get_shrunk_dim(img,max_dim){
    ratio = Math.min(max_dim[0]/img.width,max_dim[1]/img.height);
    shrink_ratio = Math.min(ratio,1.0)
    return {
        width:shrink_ratio*img.width,
        height:shrink_ratio*img.height
    };
}
//this function generates the flickity cell corresponding to
//the specific image object passed in
function get_carousel_html(img){
    var html = '<div class="carousel-cell padded-pic">';
    dim  = get_shrunk_dim(img,straboconfig["THUMBNAIL_MAX_SIZE"]);
    html += '<div class="vertical-center">';
    html += '<img style="width:'+dim.width+'px;height:'+dim.height+'px;" src="/static/thumbnails/' + img.filename + '"/>';
    html += '</div>';
    html += '</div>';
    return html;
}
function remove_all_carousel_entries(){
    flkty.remove(flkty.getCellElements());
}
//adds all the image data to the carousel
function add_carousel_entries(imgs){
    var carousel_html = "";
    imgs.forEach(function(img){
        var $cellElems = $(get_carousel_html(img));
        flkty.append($cellElems);
    });
}
/////////////////////////////////////////////////////////////////////////////////////////////////
//brings up popup associated with feature ip
function ip_clicked(db_id) {
    //sends a request to the server to return the information associated with the
    // database feature id
    $.post(
        "/map/post",
        {db_id:db_id},
        function(data){
            imgs = data.images;
            var ip_descrip = data.description;
            var ip_title = data.title;
            if (data.images.length != 0){
            //renders the popup
            show_popup();
            remove_all_carousel_entries();

            add_carousel_entries(imgs);

            $("#ip_description").text(ip_descrip);
            $("#ip_title").text(ip_title);

            // resize after un-hiding Flickity
            flkty.resize();
            flkty.reposition();
        }
        }
    );

}
//////////////////////////////////////////////////////////////////////////////////////////////

function set_flickity_click(){ 
    /*
    Purpose:
    When Flickity cell is clicked, a photoswipe gallery is pulled up displaying a larger version of the same image.

    Details:
    On android, there is problem where tapping on flickity cell makes photoswipe flash open for a
    second, and close immidiately, making the photoswipe feature useless. Setting closeOnVerticalDrag to false
    seems to help marginally, but does not fix the problem.

    I fixed the problem by adding a delay between when the cell is clicked to when photoswipe is opened.
    I also ensure that photoswipe is not opened twice. I don't know why it works, but it does.

    Note that smaller values of timeout_seconds do not work as well.
    */
    var timeout_seconds = 0.1;
    var SECS_PER_MILSEC = 1000;

    var photoswipe_fetched = false;


    flkty.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
        if (cellElement && !photoswipe_fetched) {
            photoswipe_fetched = true;
            window.setTimeout(function(){
                make_photoswipe(cellIndex);
                photoswipe_fetched = false;
            },SECS_PER_MILSEC*timeout_seconds);
        }
    });
}


function make_photoswipe(pic_index){
    // execute above function
    var element = document.querySelectorAll('.pswp')[0];

    var items = [];
    imgs.forEach(function(img){
        /*currently serves only images with size maxed out by MOBILE_SERV_MAX_SIZE
        This means that the original, maximum size images never get seen at all.
        In order to get them seen, perhaps on larger screens, you will need to look
        at the size of the screenand add image sources and sizes depending on the size
        of the screen. PhotoSwipe has an unnecessarily complicated example of how to do this
        at http://photoswipe.com/documentation/responsive-images.html */
        mobile_dim = get_shrunk_dim(img,straboconfig['MOBILE_SERV_MAX_SIZE'])
        items.push({
            src:straboconfig['MOBILE_IM_DIR_RELPATH'] + img.filename,
            w:mobile_dim.width,
            h:mobile_dim.height
        });
    });
    var options = {
        index:pic_index,
        //flickty does not loop, so neither does this
        loop:false,
        //on android, "true" will cause this to close when you wouldn't want it to
        closeOnVerticalDrag:false,
        //I don't think drastically differnt interfaces between small and large pictures is a good idea.
        clickToCloseNonZoomable: false,
        //if image loading is too slow try this. It makes switching between images even slower though.
        //preloaderEl: false,
        escKey: false
    };

    gallery = new PhotoSwipe(element, PhotoSwipeUI_Default, items, options);

    gallery.init();
}
function linear_text_width(text){
    /*Returns width of text (in pixels) if it never wraps, assuming a font size of a
    single pixel.*/

    //adds a really wide temporary div to screen to allow for measurement of long text
    var $meas_space = $('<div class="img-description text-measure"></div>')
    $("body").append($meas_space);
    //adds text to div for measurement.
    var $span = $("<p>"+text+"</p>");
    $meas_space.append($span);

    var width = $span.width();

    $meas_space.remove()
    //.text-measure css class is 10px because really small text renders differently.
    //and so this is more accurate.
    var measured_width = 10.0;
    //gives room for 10% error in text size calculation
    var measured_error = 1.1;
    return (width*measured_error) / measured_width;
}
function get_img_desc_font_size(imgdescr){
    var $container = $("#img-text-section")

    var text_width_max = $container.width() / linear_text_width(imgdescr);
    //makes sure bottom of text is not cut off
    var text_height_max = $container.height() / 1.25;

    return Math.min(text_width_max, text_height_max);
}
function set_flickity_img_title(){
    flkty.on( 'cellSelect', function() {
        var img = imgs[flkty.selectedIndex];

        var img_desc = document.getElementById("img-desc");
        //sets font size of the text to the max size that can fit in the area.
        var font_size = get_img_desc_font_size(img.description);
        img_desc.style.fontSize = font_size+"px";
        //sets the text.
        img_desc.innerHTML = img.description;
    })
}



function flickity_init(){
    flkty = new Flickity(document.getElementById("carouselholder"),
        {imagesLoaded: true,
        pageDots:false,
        setGallerySize: false}
    );
    set_flickity_img_title();
    set_flickity_click();
}




$(document).keyup(function(e) {
    if (e.keyCode==27) { //if ESC key is hit
        hide_popup();
        if (gallery){
            gallery.close();
        }
    }
});

$(document).mouseup(function(e){
        var popup = $(".popup");
        if (popup.is(e.target)){
            hide_popup();
        }
});
