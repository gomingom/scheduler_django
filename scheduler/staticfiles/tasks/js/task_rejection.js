function showRejectModal() {
    document.getElementById('rejectModal').style.display = 'block';
}

function closeRejectModal() {
    document.getElementById('rejectModal').style.display = 'none';
}

function submitRejection() {
    const rejectionReason = document.getElementById('rejectionReason').value;
    const inquiryId = document.querySelector('select[name="inquiry"]').value;
    
    if (!rejectionReason) {
        alert('반려 사유를 입력해주세요.');
        return;
    }

    fetch('/tasks/reject/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            inquiry_id: inquiryId,
            rejection_reason: rejectionReason
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('반려 처리에 실패했습니다: ' + data.message);
        }
    })
    .catch(error => {
        alert('오류가 발생했습니다: ' + error);
    });
} 