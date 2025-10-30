// client/script.js

const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const statusArea = document.getElementById('statusArea');
// Ensure the API URL points to your running backend
const apiUrl = 'http://127.0.0.1:8000/upload-document'; 

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Stop the browser from submitting the form normally

    const file = fileInput.files[0];
    if (!file) {
        statusArea.innerHTML = '<span style="color: red;">Please select a file to upload.</span>';
        return;
    }

    // Display a loading message
    statusArea.innerHTML = '<span style="color: blue;">Uploading... Please wait.</span>';

    // Use FormData to correctly package the file for the multipart/form-data request
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Send the file data to the POST /upload-document API endpoint [cite: 25]
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            // Success response (200)
            statusArea.innerHTML = `
                <span style="color: green; font-weight: bold;">File Uploaded Successfully!</span>
                <br><br>
                <strong>Database ID:</strong> ${result.id}
                <br>
                <strong>Original Name:</strong> ${result.original_filename}
                <br>
                <strong>System ID:</strong> ${result.system_filename}
                <br>
                <strong>Size:</strong> ${result.file_size_bytes} bytes
                <br>
                <strong>Uploaded At:</strong> ${new Date(result.uploaded_at).toLocaleString()}
            `;
            // Clear the file input after successful upload
            form.reset();
        } else {
            // Error response (e.g., 500)
            statusArea.innerHTML = `
                <span style="color: red; font-weight: bold;">Upload Failed (Status ${response.status})</span>
                <br><br>
                <strong>Detail:</strong> ${result.detail || 'An unknown error occurred.'}
            `;
        }
    } catch (error) {
        // Network or other fatal error
        statusArea.innerHTML = `
            <span style="color: red; font-weight: bold;">Network Error:</span>
            <br>
            Could not connect to the server. Check if your backend is running at http://127.0.0.1:8000.
        `;
        console.error('Fetch error:', error);
    }
});