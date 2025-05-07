function previewImage(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            const preview = document.getElementById('preview');
            preview.src = reader.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

async function uploadImage() {
    const fileInput = document.getElementById("imageUpload");
    const file = fileInput.files[0];
    const statusMessage = document.getElementById("statusMessage");

    if (!file) {
        statusMessage.textContent = "⚠️ Please select an image first!";
        statusMessage.style.color = "red";
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    statusMessage.textContent = "⏳ Uploading...";
    statusMessage.style.color = "blue";

    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            statusMessage.textContent = "❌ " + data.error;
            statusMessage.style.color = "red";
        } else {
            statusMessage.textContent = "✅ " + data.message;
            statusMessage.style.color = "green";
        }
    } catch (error) {
        console.error("Error:", error);
        statusMessage.textContent = "❌ Failed to upload image. Check backend.";
        statusMessage.style.color = "red";
    }
}
