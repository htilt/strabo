document.getElementById("img-input").onchange = function(e) {
    EXIF.getData(e.target.files[0], function() {
        // alert(EXIF.pretty(this));
        var tags = EXIF.getAllTags(this);
        console.log(tags)
        console.log(tags['Make'])
        var JSONtags = JSON.stringify(tags)
        console.log(JSONtags)
        $.post(
            "/upload_images/exif/", 
            {key: JSONtags},
            function(data) {
              $("#exif-autoComplete").html(data)
            }
        );
        // $.ajax({
        //     type: 'POST',
        //     url: "/upload_images/exif/",
        //     data: { key: JSONtags },
        //     dataType: 'json'
        //     function(data) {
        //       $("#form-wrapper").html(data)
        //     }
        // });
    });
}



// var main = function() {
//   // e = event
//   $("#img-input").onchange(function(e) {
//     EXIF.getData(e.target.files[0], function() {
//         // alert(EXIF.pretty(this));
//         tags = EXIF.getAllTags(this);
//     });
//   });

//   $.post(
//       "/upload_images/post", 
//       {key:tags},
//       function(data) {
//         $("#form-wrapper").html(data)
//       }
//   ); 
// };


// $(document).ready(main);