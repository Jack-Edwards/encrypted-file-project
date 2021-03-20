document.addEventListener("DOMContentLoaded", function() {
    console.log("main.js: Document ready");
    var fileToRead = document.getElementById("file-upload");

    fileToRead.addEventListener("change", function(event) {
        var files = fileToRead.files;
        var len = files.length;
        // we should read just one file
        if (len) {
            var pFileName = document.getElementById("upload-file-name");
            pFileName.innerHTML = files[0].name;

            var pFileType = document.getElementById("upload-file-type");
            pFileType.innerHTML = files[0].type;

            var pFileSize = document.getElementById("upload-file-size");
            pFileSize.innerHTML = files[0].size;

            var container = document.getElementById("file-details-container");
            container.style.display = "block";
        }

    }, false);
    console.log("main.js: fileToRead listener ready");



});



