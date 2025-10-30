const fileHistoryDiv = document.getElementById("fileHistory");
const apiUrl = "http://127.0.0.1:8000/files"; // Your GET /files endpoint [cite: 29]

/**
 * Fetches file metadata from the backend and displays it in a table.
 */
async function loadFileHistory() {
  try {
    // Call the /files endpoint [cite: 32]
    const response = await fetch(apiUrl);
    const data = await response.json(); // Data contains the "files" array

    if (response.ok) {
      const files = data.files; // Retrieve all stored records from the database [cite: 31]

      if (files.length === 0) {
        fileHistoryDiv.innerHTML = "<p>No files have been uploaded yet.</p>";
        return;
      }

      // Build the HTML table
      let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Original Filename</th>
                        <th>File Size (Bytes)</th>
                        <th>Uploaded At (Timestamp)</th>
                        <th>System Filename (Internal ID)</th>
                    </tr>
                </thead>
                <tbody>
        `;

      // Populate table rows with retrieved data [cite: 32]
      files.forEach((file) => {
        const uploadedDate = new Date(file.uploaded_at).toLocaleString();
        tableHTML += `
                <tr>
                    <td>${file.id}</td>
                    <td>${file.original_filename}</td>
                    <td>${file.file_size_bytes}</td>
                    <td>${uploadedDate}</td>
                    <td>${file.system_filename}</td>
                </tr>
            `;
      });

      tableHTML += `
                </tbody>
            </table>
        `;
      fileHistoryDiv.innerHTML = tableHTML;
    } else {
      fileHistoryDiv.innerHTML = `<p style="color: red;">Error fetching data (Status: ${
        response.status
      }). Detail: ${data.detail || "Unknown error"}</p>`;
    }
  } catch (error) {
    fileHistoryDiv.innerHTML = `<p style="color: red;">Network Error: Could not connect to the backend server.</p>`;
    console.error("Fetch error:", error);
  }
}

// Run the function when the page loads [cite: 32]
document.addEventListener("DOMContentLoaded", loadFileHistory);
