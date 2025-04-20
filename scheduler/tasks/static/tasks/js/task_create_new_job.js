function showNewTaskForm() {
  console.log(document.getElementById('new-task-form'));
  document.getElementById('new-task-form').style.display = 'table-row';
}

function hideNewTaskForm() {
  document.getElementById('new-task-form').style.display = 'none';
}

function formatTime(timeStr) {
  // 시간 문자열이 HH:00 형식인지 확인
  if (!timeStr.endsWith(':00')) {
    timeStr = timeStr.split(':')[0] + ':00';
  }
  
  const [hours, minutes] = timeStr.split(':');
  const hour = parseInt(hours);
  const period = hour < 12 ? '오전' : '오후';
  const formattedHour = hour <= 12 ? hour : hour - 12;
  return `${period} ${formattedHour}시`;
}

function submitNewTask() {
  const shipName = document.getElementById('ship-name').value;
  const blockName = document.getElementById('block-name').value;
  const managerId = document.getElementById('manager').value;
  const workDate = document.getElementById('work-date').value;
  const workTime = formatTime(document.getElementById('work-time').value);
  const description = document.getElementById('description').value;

  // CSRF 토큰 가져오기
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // API 요청 보내기
  fetch('/tasks/create_inline/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
      ship_name: shipName,
      block_name: blockName,
      manager: managerId,
      work_date: workDate,
      work_time: workTime,
      description: description
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // 페이지 새로고침
      window.location.reload();
    } else {
      alert('작업 추가에 실패했습니다: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('작업 추가 중 오류가 발생했습니다.');
  });
} 