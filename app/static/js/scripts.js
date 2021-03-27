document.addEventListener("DOMContentLoaded", function() {
    console.log("main.js: Document ready");
    var fileToRead = document.getElementById("fileSelect");

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

    var uploadForm = document.getElementById("upload");
    uploadForm.onsubmit = function(event) {
        event.preventDefault();

        var fileSelect = document.getElementById("fileSelect");
        var keyInput = document.getElementById("encryptKey");
        var data = new FormData()
        data.append('files', fileSelect.files[0])
        data.append('key', keyInput.value)
        
        fetch(uploadForm.action, {
          method: 'POST',
          body: data
        })
        .then(response => response.json())
        .then(data => {
            alert("Here you go\r\n\r\nFile ID: " + data.file_id + "\r\nKey: " + keyInput.value)
            window.location.reload();
        })
        .catch((error) => {
            alert('Error:', error);
        });
    }

    function window_focus(){
        window.location.reload();
    }

    var downloadForm = document.getElementById("download");
    downloadForm.onsubmit = function(event) {
        window.addEventListener('focus', window_focus, false);
    }
});
