document.addEventListener('DOMContentLoaded', function() {
  const taskForm = document.getElementById('taskCreationForm');
  const showBtn = document.getElementById('showTaskFormBtn');
  const closeBtn = document.getElementById('closeTaskFormBtn');
  const cancelBtn = document.getElementById('cancelTaskFormBtn');
  const content = document.querySelector('.content');

  showBtn.addEventListener('click', function() {
    taskForm.classList.add('show');
    content.classList.add('form-shown');
  });

  closeBtn.addEventListener('click', function() {
    taskForm.classList.remove('show');
    content.classList.remove('form-shown');
  });

  cancelBtn.addEventListener('click', function() {
    taskForm.classList.remove('show');
    content.classList.remove('form-shown');
  });
}); 