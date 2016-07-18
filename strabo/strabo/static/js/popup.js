//flickety object
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
function get_carosel_html(img){
    var html = '<div class="carousel-cell padded-pic">';
    dim  = get_shrunk_dim(img,straboconfig["THUMBNAIL_MAX_SIZE"]);
    html += '<div class="vertical-center">';
    html += '<img style="width:'+dim.width+'px;height:'+dim.height+'px;" src="static/thumbnails/' + img.filename + '"/>';
    html += '</div>';
    html += '</div>';
    return html;
}
function remove_all_carosel_entries(){
    flkty.remove(flkty.getCellElements());
}
//adds all the imag data to the garosel in the odersrc
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
/*
Purpose:
When Flickity cell is clicked, a photoswipe gallery is pulled up.

Details:
On android, there is problem where tapping on flickety cell makes photoswipe flash open for a
second, and close immidiately. Setting closeOnVerticalDrag to false seems to help marginally, but
not fix the problem.

So I fixed the problem by making a delay from when the cell is clicked to when photoswipe is opened,
while making sure that photoswipe is not opened twice.

The delay is the second argument to window.setTimeout in units of milliseconds. This can be played with,
but very small values like 1 do not work very well.
*/
function set_flickety_click(){
    var timeout_sec = 0.1;
    var SECS_PER_MILSEC = 1000;

    var photoswipe_fetched = false;
    flkty.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
        if (cellElement && !photoswipe_fetched) {
            photoswipe_fetched = true;
            window.setTimeout(function(){
                make_photoswipe(cellIndex);
                photoswipe_fetched = false;
            },SECS_PER_MILSEC*timeout_sec);
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
        clickToCloseNonZoomable: false
        //if image loading is too slow try this. It makes switching between images even slower though.
        //preloaderEl: false,
    };

    gallery = new PhotoSwipe(element, PhotoSwipeUI_Default, items, options);

    gallery.init();
}
function set_flickety_img_title(){
    flkty.on( 'cellSelect', function() {
        var img = imgs[flkty.selectedIndex];

        $("#img_description").text(img.description);
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
