document.getElementById('file-upload').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        var fileReader = new FileReader();

        fileReader.onload = function() {
            var pdfPreview = document.getElementById('pdf-preview');
            var previewContainer = document.getElementById('pdf-preview-container');
            pdfPreview.src = fileReader.result;
            previewContainer.style.display = 'block'; // Show the preview section
        };

        fileReader.readAsDataURL(file); // Read the file content
    } else {
        alert('Please select a valid PDF file.');
    }
});
