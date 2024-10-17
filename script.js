document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the form from submitting the default way
    
    const formData = new FormData();
    const fileInput = document.getElementById("pdfFile");

    formData.append("file", fileInput.files[0]); // Add the selected file to the form data

    try {
        const response = await fetch("http://127.0.0.1:8000/upload-pdf/", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            displayResponse(data);
        } else {
            const errorData = await response.json();
            displayResponse(errorData, true);
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        displayResponse({ error: error.message }, true);
    }
});

function displayResponse(data, isError = false) {
    const responseDiv = document.getElementById("response");
    responseDiv.innerHTML = ""; // Clear previous response

    if (isError) {
        responseDiv.innerHTML += `<p style="color: red;">Error: ${data.detail || data.error}</p>`;
    } else {
        responseDiv.innerHTML += `<p>Filename: ${data.filename}</p>`;
        responseDiv.innerHTML += `<p>File Size: ${data.size} bytes</p>`;
        responseDiv.innerHTML += `<p>Message: ${data.message || "Upload successful"}</p>`;
    }
}
