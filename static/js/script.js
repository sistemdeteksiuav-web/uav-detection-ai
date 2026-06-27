// =====================================================
// UAV Detection AI
// script.js
// =====================================================

// =========================
// ELEMENT
// =========================

const dropArea = document.getElementById("drop-area");
const chooseBtn = document.getElementById("chooseBtn");
const imageInput = document.getElementById("imageInput");

const previewImage = document.getElementById("previewImage");

const statusText = document.getElementById("status");
const confidenceText = document.getElementById("confidence");
const distanceText = document.getElementById("distance");

// =========================
// PILIH GAMBAR
// =========================

chooseBtn.addEventListener("click", function (e) {

    e.preventDefault();

    e.stopPropagation();

    imageInput.click();

});

dropArea.addEventListener("click", function () {

    imageInput.click();

});

// =========================
// FILE DIPILIH
// =========================

imageInput.addEventListener("change", function () {

    if (!this.files || this.files.length === 0) {

        return;

    }

    uploadImage(this.files[0]);

    // supaya file yang sama bisa dipilih lagi
    this.value = "";

});

// =========================
// DRAG OVER
// =========================

dropArea.addEventListener("dragover", function (e) {

    e.preventDefault();

    dropArea.style.borderColor = "#2563eb";

    dropArea.style.backgroundColor = "#eef6ff";

});

// =========================
// DRAG LEAVE
// =========================

dropArea.addEventListener("dragleave", function () {

    dropArea.style.borderColor = "#cbd5e1";

    dropArea.style.backgroundColor = "#ffffff";

});

// =========================
// DROP
// =========================

dropArea.addEventListener("drop", function (e) {

    e.preventDefault();

    dropArea.style.borderColor = "#cbd5e1";

    dropArea.style.backgroundColor = "#ffffff";

    if (!e.dataTransfer.files || e.dataTransfer.files.length === 0) {

        return;

    }

    uploadImage(e.dataTransfer.files[0]);

});

// =========================
// UPLOAD KE SERVER
// =========================

function uploadImage(file) {

    // Preview gambar

    previewImage.src = URL.createObjectURL(file);

    // Loading

    statusText.innerHTML = "Processing...";

    confidenceText.innerHTML = "...";

    distanceText.innerHTML = "...";

    // FormData

    const formData = new FormData();

    formData.append("image", file);

    fetch("/predict", {

        method: "POST",

        body: formData,

        cache: "no-cache"

    })

    .then(function(response){

        if(!response.ok){

            throw new Error("Server Error");

        }

        return response.json();

    })

    .then(function(data){

        console.log("Response :", data);

        if(data.success === false){

            alert(data.message);

            statusText.innerHTML = "-";

            confidenceText.innerHTML = "-";

            distanceText.innerHTML = "-";

            return;

        }

        // Status

        statusText.innerHTML = data.label;

        // Confidence

        confidenceText.innerHTML = data.confidence + " %";

        // Distance

        if(data.distance === null){

            distanceText.innerHTML = "-";

        }

        else{

            distanceText.innerHTML = data.distance + " meter";

        }

    })

    .catch(function(error){

        console.error(error);

        alert("Terjadi kesalahan saat menghubungkan ke server.");

        statusText.innerHTML = "-";

        confidenceText.innerHTML = "-";

        distanceText.innerHTML = "-";

    });

}