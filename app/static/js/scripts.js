function updateStorageBar() {
    var storageBar = document.getElementById("storageBar");
    var storageBarText = document.getElementById("storageBarText");

    fetch("/metrics/space", {
        method: 'GET'
      })
      .then(response => {
          if (response.status === 200) {
              return response;
          } else {
              throw new Error(response);
          }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
            storageBar.style.width =  data.percent_remaining + "%";
            storageBarText.innerText = data.bytes_remaining + " / " + data.bytes_allocated;
          }
      })
      .catch((error) => {
          console.log(error);
      });
}

function clearUploadInput() {
    var fileSelect = document.getElementById("fileSelect");
    fileSelect.value = null;
}

function clearDownloadInputs() {
    var downloadId = document.getElementById("downloadFileId");
    var downloadKey = document.getElementById("downloadFileKey");
    downloadId.value = "";
    downloadKey.value = "";
}

document.addEventListener("DOMContentLoaded", function() {
    updateStorageBar();
    clearUploadInput();
    clearDownloadInputs();

    var uploadForm = document.getElementById("upload");
    uploadForm.onsubmit = function(event) {
        event.preventDefault();

        document.getElementById("uploadButton").disabled = true;

        // Clear status texts
        var errorElement = document.getElementById("errorResponse");
        errorElement.innerText = "";
        var fileIdLabel = document.getElementById("uploadFileIdLabel");
        fileIdLabel.innerText = "";
        var fileIdElement = document.getElementById("uploadedFileId");
        fileIdElement.innerText = "";
        var fileKeyLabel = document.getElementById("uploadFileKeyLabel");
        fileKeyLabel.innerText = "";
        var fileKeyElement = document.getElementById("uploadedFileKey");
        fileKeyElement.innerText = "";

        var fileSelect = document.getElementById("fileSelect");

        // Handle no file selected
        if (fileSelect.files.length === 0) {
            errorElement.innerText = "No file selected";
            document.getElementById("uploadButton").disabled = false;
            return;
        }

        var data = new FormData()
        data.append('files', fileSelect.files[0])
        
        fetch(uploadForm.action, {
          method: 'POST',
          body: data
        })
        .then(response => {
            if (response.status === 200) {
                return response;
            } else {
                throw new Error(response.statusText);
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fileIdLabel.innerText = "File ID";
                fileIdElement.innerText = data.file_id;
                fileKeyLabel.innerText = "Decrypt Key";
                fileKeyElement.innerText = data.decrypt_key;
            } else {
                errorElement.innerText = "Error: " + data.message;
            }

            document.getElementById("uploadButton").disabled = false;
            clearUploadInput();
            updateStorageBar();
        })
        .catch((error) => {
            errorElement.innerText = error;

            document.getElementById("uploadButton").disabled = false;
            clearUploadInput();
            updateStorageBar();
        });
    }

    function window_focus() {
        document.getElementById("downloadButton").disabled = false;
        updateStorageBar();
    }

    var downloadForm = document.getElementById("download");
    downloadForm.onsubmit = function(event) {
        document.getElementById("downloadButton").disabled = true;
        window.addEventListener('focus', window_focus, false);
    }
});
