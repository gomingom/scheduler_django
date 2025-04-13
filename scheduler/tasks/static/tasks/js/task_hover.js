document.addEventListener('DOMContentLoaded', function() {
    const taskLinks = document.querySelectorAll('.calendar-task-link');
    const modal = document.createElement('div');
    modal.className = 'task-hover-modal';
    document.body.appendChild(modal);

    // 모달 스타일 설정
    const style = document.createElement('style');
    style.textContent = `
        .task-hover-modal {
            position: absolute;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            display: none;
            min-width: 300px;
            max-width: 500px;
            border: 1px solid rgb(28, 28, 30);
            pointer-events: none;
        }
        .task-hover-modal.show {
            display: block;
        }
        .task-hover-modal::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0);
            z-index: -1;
        }
        .task-hover-modal h3 {
            margin-top: 0;
            color: #1a202c;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
        }
        .task-hover-modal p {
            margin: 10px 0;
            color: #4a5568;
        }
        .task-hover-modal .close-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #718096;
        }
    `;
    document.head.appendChild(style);

    taskLinks.forEach(link => {
        link.addEventListener('mouseenter', function(e) {
            const hasInquiry = this.dataset.hasInquiry === 'true';
            const shipName = hasInquiry ? this.dataset.inquiryShipName : this.dataset.shipName;
            const blockName = hasInquiry ? this.dataset.inquiryBlockName : this.dataset.blockName;
            const workTime = this.dataset.workTime;
            const manager = this.dataset.manager;
            const description = this.dataset.description;
            
            modal.innerHTML = `
                <button class="close-btn">&times;</button>
                <h3>작업 상세 정보</h3>
                <p><strong>선박명:</strong> ${shipName}</p>
                <p><strong>블록명:</strong> ${blockName}</p>
                <p><strong>작업 시간:</strong> ${workTime}</p>
                <p><strong>담당자:</strong> ${manager}</p>
                <p><strong>설명:</strong> ${description || '없음'}</p>
            `;
            
            // 마우스 위치에서 20px 오른쪽, 20px 아래쪽에 모달 표시
            modal.style.left = (e.pageX + 20) + 'px';
            modal.style.top = (e.pageY + 20) + 'px';
            modal.classList.add('show');
        });

        link.addEventListener('mousemove', function(e) {
            if (modal.classList.contains('show')) {
                modal.style.left = (e.pageX + 20) + 'px';
                modal.style.top = (e.pageY + 20) + 'px';
            }
        });

        link.addEventListener('mouseleave', function() {
            modal.classList.remove('show');
        });
    });

    // 모달 닫기 버튼 이벤트
    modal.addEventListener('click', function(e) {
        if (e.target.classList.contains('close-btn')) {
            modal.classList.remove('show');
        }
    });
});

function getLastValidValue(arr) {
    for (let i = arr.length - 1; i >= 0; i--) {
      if (arr[i] !== "") {
        return arr[i];
      }
    }
    return "";  // 또는 undefined
  }