//flickety object
var flkty;

function hide_popup(){
    $('.popup').hide();
    $('.container-popup').hide();
}
function show_popup(){
    $('.popup').show();
    $('.container-popup').show();
}

//this function loads the text and images associated
//with a selected interest point
//example output:
// <div class="carousel-cell"><img src= "static/thumbnails/download.jpg"/></div>
function get_carosel_html(filename,descrip){
    var html = '<div class="carousel-cell">';
    html += '<img src="static/thumbnails/' + filename + '"/>';
    html += '<p>' + descrip + '</p>';
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
        var $cellElems = $(get_carosel_html(img.filename,img.description));
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
            var imgs = data.images;
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
        console.log( 'Flickity select ' + cellIndex)
    });
}

function flickety_init(){
    flkty = new Flickity(document.getElementById("carouselholder"),
        {imagesLoaded: true}//doesn't do anything right now
    );
    set_flickety_click();
}
