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
function get_thumb_dim(img){
    max_dim  = straboconfig["THUMBNAIL_MAX_SIZE"]
    ratio = Math.min(max_dim[0]/img.width,max_dim[1]/img.height);
    return {width:ratio*img.width,height:ratio*img.height};
}
//this function generates the flickity cell corresponding to
//the specific image object passed in
function get_carosel_html(img){
    var html = '<div class="carousel-cell padded-pic">';
    dim  = get_thumb_dim(img);
    html += '<div class="vertical-center">';
    html += '<img style="width:'+dim.width+'px;height:'+dim.height+'px;" src="static/thumbnails/' + img.filename + '"/>';
    html += '</div>';
    html += '</div>';
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
    var photoswipe_fetched = false;
    flkty.on( 'staticClick', function( event, pointer, cellElement, cellIndex ) {
        if (cellElement && !photoswipe_fetched) {
            photoswipe_fetched = true;
            window.setTimeout(function(){
                make_photoswipe(cellIndex);
                photoswipe_fetched = false;
            },100);
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
        index:pic_index,
        loop:false,
        closeOnVerticalDrag:false,
        clickToCloseNonZoomable: true,
        pinchToClose:false,
        closeOnScroll:false
    };

    gallery = new PhotoSwipe(element, PhotoSwipeUI_Default, items, options);

    gallery.init();
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
