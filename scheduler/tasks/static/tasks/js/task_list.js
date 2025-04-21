document.addEventListener('DOMContentLoaded', function() {
    const editableCells = document.querySelectorAll('.editable-cell');
    
    editableCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const displayValue = this.querySelector('.display-value');
            const editInput = this.querySelector('.edit-input');
            
            if (displayValue.style.display !== 'none') {
                displayValue.style.display = 'none';
                editInput.style.display = 'block';
                
                // work_time 필드인 경우 특별 처리
                if (this.dataset.field === 'work_time') {
                    // Save on change for work_time
                    const saveWorkTime = () => {
                        const taskId = this.dataset.taskId;
                        const value = editInput.value;
                        
                        fetch(`/tasks/${taskId}/update_field/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                            },
                            body: JSON.stringify({
                                field: 'work_time',
                                value: value
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                displayValue.textContent = value;
                                displayValue.style.display = 'block';
                                editInput.style.display = 'none';
                            } else {
                                alert('업데이트에 실패했습니다: ' + data.message);
                            }
                        })
                        .catch(error => {
                            alert('오류가 발생했습니다: ' + error);
                        });
                    };
                    
                    editInput.addEventListener('change', saveWorkTime);
                    
                    // Add click event to prevent closing when clicking inside the select
                    editInput.addEventListener('click', function(e) {
                        e.stopPropagation();
                    });
                } else {
                    // 기존의 다른 필드 처리 로직
                    editInput.focus();
                    
                    // manager 필드인 경우 선택된 옵션의 텍스트를 즉시 표시
                    if (this.dataset.field === 'manager') {
                        editInput.addEventListener('change', function() {
                            const selectedOption = this.options[this.selectedIndex];
                            displayValue.textContent = selectedOption.text;
                        });
                    }
                    
                    const saveChanges = () => {
                        const taskId = this.dataset.taskId;
                        const field = this.dataset.field;
                        const value = editInput.value;
                        
                        fetch(`/tasks/${taskId}/update_field/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                            },
                            body: JSON.stringify({
                                field: field,
                                value: value
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                if (field === 'manager') {
                                    const selectedOption = editInput.options[editInput.selectedIndex];
                                    displayValue.textContent = selectedOption.text;
                                } else {
                                    displayValue.textContent = value;
                                }
                                displayValue.style.display = 'block';
                                editInput.style.display = 'none';
                            } else {
                                alert('업데이트에 실패했습니다: ' + data.message);
                            }
                        })
                        .catch(error => {
                            alert('오류가 발생했습니다: ' + error);
                        });
                    };
                    
                    editInput.addEventListener('blur', saveChanges);
                    editInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            saveChanges();
                        }
                    });
                }
            }
        });
    });
}); 