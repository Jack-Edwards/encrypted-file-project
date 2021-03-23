document.addEventListener("DOMContentLoaded", function() {
    console.log("main.js: Document ready");
    var fileToRead = document.getElementById("fileUpload");

    fileToRead.addEventListener("change", function(event) {
        var files = fileToRead.files;
        var len = files.length;
        if (len > 0) {
            var pFileName = document.getElementById("uploadFileName");
            pFileName.innerHTML = files[0].name;

            var pFileType = document.getElementById("uploadFileType");
            pFileType.innerHTML = files[0].type;

            var pFileSize = document.getElementById("uploadFileSize");
            pFileSize.innerHTML = files[0].size;
        }

    }, false);
    console.log("main.js: fileToRead listener ready");
});
