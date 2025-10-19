document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const selects = document.querySelectorAll('.status-select');

    selects.forEach(select => {
        select.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const status = this.value;

            fetch(`/tasks/update-status/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: new URLSearchParams({status: status})
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("Помилка оновлення статусу: " + data.error);
                } else {
                    // оновлюємо клас рядка для кольорового підсвічування
                    const row = document.getElementById(`task-row-${taskId}`);
                    row.className = `status-${status}`;
                }
            })
            .catch(error => {
                alert("Помилка AJAX: " + error);
            });
        });
    });
}); 