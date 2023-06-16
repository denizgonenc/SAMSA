let xhr = null;

const dropArea = document.querySelector(".dnd");
const fileInput = document.querySelector(".audio-input");

const form = document.getElementById("form1");

const fileName = document.createElement("p");
fileName.id = "fileName1";
const progressBar = document.createElement("progress");
progressBar.value = "0";
progressBar.max = "100";

const uploadButton = document.createElement("input");
uploadButton.classList.add("submit-button");
uploadButton.type = "submit";
uploadButton.id = "submit-button1";
uploadButton.value = "Upload";

const cancelButton = document.createElement("button");
cancelButton.classList.add("cancel-button");
cancelButton.id = "cancel-button1";
cancelButton.innerHTML = "Cancel"

const buttons = document.createElement("div");
buttons.classList.add("buttons");
buttons.appendChild(uploadButton);
buttons.appendChild(cancelButton);


const uploadedFileDiv = document.createElement("div");
uploadedFileDiv.classList.add("uploaded-file");
uploadedFileDiv.style.display = "none";
uploadedFileDiv.appendChild(fileName);
uploadedFileDiv.appendChild(progressBar);
uploadedFileDiv.appendChild(buttons);

const errorBox = document.createElement("div")
errorBox.classList.add("box-input-error")
errorBox.style.display = "none";

const boxInput = document.getElementsByClassName("box-input")[0]
boxInput.appendChild(uploadedFileDiv);
uploadedFileDiv.appendChild(errorBox);

let file;

/* Directly selecting file from file explorer.*/
fileInput.addEventListener("change", (event) => {
    file = event.target.files[0];
    showFile();
    console.log(file);
});

/* Draging file on the top of drag area. */
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add("hover");
});

/* Canceling the dragging operation. */
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("hover");
});

/* Dropping the selected file to the drop area. */
dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];

    // Now let's create a DataTransfer to get a FileList
    let dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;

    showFile();
    dropArea.classList.remove("hover");
});

/* After selecting the file, it will shows the name of the file and a cancel button to cancel it. */
function showFile() {

    fileName.innerHTML = file.name;
    uploadedFileDiv.style.display = "flex";
}

/* By clicking the cancel button that appears in the webpage,
 removing the selected file so new file can be selected. */
cancelButton.addEventListener('click', (event) => {
    event.preventDefault();
    file = null;
    fileName.innerHTML = "";
    uploadedFileDiv.style.display = "none";
    if (xhr) {
        xhr.abort();
        progressBar.value = "0";
        xhr = null;
    }
});

/* Uploading the selected file to the fastapi. */
function upload(event) {
    let uploadedFile = event.dataTransfer.files[0];
    console.log(uploadedFile);
}

uploadButton.addEventListener('click', (event) => {
    if (xhr == null) {
        event.preventDefault();
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                try {
                    if (xhr.status === 200) {
                        errorBox.style.display = 'none';
                    } else {    // Warning, error or internal server errors.
                        event.preventDefault();
                        errorMessage = JSON.parse(JSON.parse(xhr.response));
                        errorBox.innerHTML = "<i class=\"fa fa-close\" style=\"font-size: 32px; color:red\"></i>" +
                            "<strong style=\"margin: 0 8px 0 8px;\">ERROR: </strong> " + errorMessage.error
                        errorBox.style.display = 'flex';
                    }
                } catch (e) {
                    console.error(e);
                }
            }
        };

        xhr.upload.onprogress = function (event) {
            if (event.lengthComputable) {
                let percentComplete = (event.loaded / event.total) * 100;
                progressBar.value = percentComplete;
                if (percentComplete != 100) {
                    fileName.innerHTML = file.name + '<span style="font-weight: 400;">: - Loading ... ' + Math.floor(percentComplete) + '% </span>';
                } else {
                    fileName.innerHTML = file.name + '<span style="font-weight: 400;">: - Finished. </span>';
                }
            }
        }

        xhr.send(new FormData(form));

    } else {
        event.preventDefault();
        return;
    }

});