/*todo.js*/
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('todoForm');
    const taskInput = document.getElementById('taskInput');
    const taskList = document.getElementById('taskList');

    // Load tasks from sessionStorage (not localStorage because we wanna clear tasks when session is gone) and display
    function loadTasks() {
        const tasks = JSON.parse(sessionStorage.getItem('tasks')) || [];
        taskList.innerHTML = '';
        tasks.forEach((task, index) => {
            if(task && task.name) { // so task and task.name are defined
                taskList.innerHTML += `
                    <li>
                        <input type="checkbox" id="task_${index}" ${task.completed ? 'checked' : ''} onchange="toggleTaskCompleted(${index})">
                        <label for="task_${index}">${task.name}</label>
                    </li>
                `;
            }
        });
    }

    // Toggle task completion status
    window.toggleTaskCompleted = function(index) {
        const tasks = JSON.parse(sessionStorage.getItem('tasks')) || [];
        tasks[index].completed = !tasks[index].completed;
        sessionStorage.setItem('tasks', JSON.stringify(tasks));
        loadTasks(); // Refresh the list to reflect changes
    };

    // Save new task
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const taskName = taskInput.value.trim();
        if (!taskName) return; // so undefined tasks don't get displayed
        const tasks = JSON.parse(sessionStorage.getItem('tasks')) || [];
        tasks.push({ name: taskName, completed: false }); // Add task as an object
        sessionStorage.setItem('tasks', JSON.stringify(tasks));
        taskInput.value = '';
        loadTasks(); // Refresh the list
    });

    loadTasks(); // Initial load of tasks
});
