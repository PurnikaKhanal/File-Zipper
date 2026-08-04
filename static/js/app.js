async function uploadFile(endpoint, resultPanelId) {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    const panel = document.getElementById(resultPanelId);

    if (!data.success) {
      panel.innerHTML = `<p style="color:red;">${data.error}</p>`;
      return;
    }

    // Show correct panel content
    if (endpoint.includes("compress")) {
      panel.innerHTML = `
        <h3>Compression Result</h3>
        <p>Original size: ${data.original_size} bytes</p>
        <p>Compressed size: ${data.compressed_size} bytes</p>
        <a href="/download/${data.output_file}" download>Download Compressed File</a>
      `;
    } else {
      panel.innerHTML = `
        <h3>Decompression Result</h3>
        <p>Original size: ${data.original_size} bytes</p>
        <p>Recovered size: ${data.recovered_size} bytes</p>
        <a href="/download/${data.output_file}" download>Download Decompressed File</a>
      `;
    }
  } catch (err) {
    const panel = document.getElementById(resultPanelId);
    panel.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
}

// Attach button listeners
document.getElementById('compressBtn').addEventListener('click', () => {
  uploadFile('/api/compress', 'compressResult');
});

document.getElementById('decompressBtn').addEventListener('click', () => {
  uploadFile('/api/decompress', 'decompressResult');
});
