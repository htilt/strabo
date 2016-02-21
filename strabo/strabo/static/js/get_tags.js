// This function and its methods come from the EXIF.js project
// The function gets EXIF tags from the image once it has been 
// uploaded and posts those tags to the server so that the tags
// will be substituted into the image upload form.
document.getElementById("img-input").onchange = function(e) {
    EXIF.getData(e.target.files[0], function() {
        var tags = EXIF.getAllTags(this);
        var JSONtags = JSON.stringify(tags)
        $.post(
            "/admin/upload_images/exif/", 
            {key: JSONtags},
            function(data) {
              $("#exif-autoComplete").html(data)
            }
        );
    });
}

