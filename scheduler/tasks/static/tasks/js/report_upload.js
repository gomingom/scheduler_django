document.addEventListener('DOMContentLoaded', function() {
    // Add click event listeners to all upload buttons
    document.querySelectorAll('.upload-report-btn').forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('.report-upload-form');
            const fileInput = form.querySelector('.report-file-input');
            fileInput.click();
        });
    });

    // Handle file selection
    document.querySelectorAll('.report-file-input').forEach(input => {
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                const form = this.closest('.report-upload-form');
                uploadReport(form);
            }
        });
    });
});

function uploadReport(form) {
    const taskId = form.dataset.taskId;
    const formData = new FormData(form);
    
    fetch(`/tasks/${taskId}/upload_report/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Reload the page to show the updated report
            window.location.reload();
        } else {
            alert('리포트 업로드에 실패했습니다: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('리포트 업로드 중 오류가 발생했습니다.');
    });
} 