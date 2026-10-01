const imageInput = document.getElementById("imageInput");
const browseBtn = document.getElementById("browseBtn");
const dropZone = document.getElementById("dropZone");

const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");

const removeBtn = document.getElementById("removeBtn");
const inspectBtn = document.getElementById("inspectBtn");

let selectedFile = null;


// Browse button
browseBtn.addEventListener("click", function () {
    imageInput.click();
});


// Select image
imageInput.addEventListener("change", function () {

    if (imageInput.files.length === 0) {
        return;
    }

    selectImage(imageInput.files[0]);
});


// Select image function
function selectImage(file) {

    if (!file.type.startsWith("image/")) {
        alert("Please select an image.");
        return;
    }

    selectedFile = file;

    const reader = new FileReader();

    reader.onload = function (event) {

        imagePreview.src = event.target.result;

        previewContainer.hidden = false;

        inspectBtn.disabled = false;
    };

    reader.readAsDataURL(file);
}


// Remove image
removeBtn.addEventListener("click", function () {

    selectedFile = null;

    imageInput.value = "";

    imagePreview.src = "";

    previewContainer.hidden = true;

    inspectBtn.disabled = true;
});


// Drag and drop
dropZone.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropZone.classList.add("dragover");
});


dropZone.addEventListener("dragleave", function () {

    dropZone.classList.remove("dragover");
});


dropZone.addEventListener("drop", function (event) {

    event.preventDefault();

    dropZone.classList.remove("dragover");

    const file = event.dataTransfer.files[0];

    if (file) {
        selectImage(file);
    }
});