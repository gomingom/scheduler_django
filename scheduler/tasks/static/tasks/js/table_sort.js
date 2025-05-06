document.addEventListener('DOMContentLoaded', function() {
    console.log("table_sort.js loaded");
    const sortableHeaders = document.querySelectorAll('.sortable');
    let currentSort = {
        column: null,
        direction: 'asc'
    };

    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const sortField = this.dataset.sort;
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            // 정렬 방향 결정
            if (currentSort.column === sortField) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = sortField;
                currentSort.direction = 'asc';
            }

            // 정렬 아이콘 업데이트
            sortableHeaders.forEach(h => {
                h.classList.remove('asc', 'desc');
            });
            this.classList.add(currentSort.direction);

            // 행 정렬
            rows.sort((a, b) => {
                let aValue = getCellValue(a, sortField);
                let bValue = getCellValue(b, sortField);

                // 날짜 형식 처리
                if (sortField === 'work_date') {
                    aValue = new Date(aValue);
                    bValue = new Date(bValue);
                }

                if (currentSort.direction === 'asc') {
                    return aValue > bValue ? 1 : -1;
                } else {
                    return aValue < bValue ? 1 : -1;
                }
            });

            // 정렬된 행을 테이블에 다시 추가
            rows.forEach(row => tbody.appendChild(row));
        });
    });

    function getCellValue(row, field) {
        const cell = row.querySelector(`td:nth-child(${getColumnIndex(field)})`);
        if (!cell) return '';

        // 편집 가능한 셀인 경우
        const editableCell = cell.querySelector('.editable-cell');
        if (editableCell) {
            const displayValue = editableCell.querySelector('.display-value');
            return displayValue ? displayValue.textContent.trim() : '';
        }

        // 일반 셀인 경우
        return cell.textContent.trim();
    }

    function getColumnIndex(field) {
        const fieldMap = {
            'ship_name': 1,
            'manager': 2,
            'work_date': 3,
            'work_time': 4,
            'description': 5
        };
        return fieldMap[field] || 1;
    }
}); 