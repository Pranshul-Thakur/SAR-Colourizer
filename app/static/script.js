document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', (event) => {
            event.preventDefault();
            
            if (!fileInput.files.length) {
                alert('Please select a file to upload.');
                return;
            }
            
            uploadForm.submit();
        });
    }
});
