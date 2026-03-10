document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const taskForm = document.getElementById('task-form');
    const taskTitle = document.getElementById('task-title');
    const taskDesc = document.getElementById('task-desc');
    const taskList = document.getElementById('task-list');
    const toggleDescBtn = document.getElementById('toggle-desc-btn');
    const descGroup = document.getElementById('desc-group');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const emptyState = document.getElementById('empty-state');
    const loader = document.getElementById('loader');
    const toastContainer = document.getElementById('toast-container');

    // State
    let tasks = [];
    let currentFilter = 'all';

    // API Base URL
    const API_URL = '/tasks/';

    // Initialize
    fetchTasks();

    // Event Listeners
    taskForm.addEventListener('submit', handleTaskSubmit);
    
    toggleDescBtn.addEventListener('click', () => {
        descGroup.classList.toggle('hidden');
        if (descGroup.classList.contains('hidden')) {
            toggleDescBtn.innerHTML = '<i class="fa-solid fa-align-left"></i> Add Details';
        } else {
            toggleDescBtn.innerHTML = '<i class="fa-solid fa-chevron-up"></i> Hide Details';
            taskDesc.focus();
        }
    });

    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            // Set filter and render
            currentFilter = e.target.dataset.filter;
            renderTasks();
        });
    });

    // Functions
    async function fetchTasks() {
        showLoader(true);
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Failed to fetch tasks');
            
            tasks = await response.json();
            renderTasks();
        } catch (error) {
            console.error('Error fetching tasks:', error);
            showToast('Failed to load tasks', 'error');
        } finally {
            showLoader(false);
        }
    }

    async function handleTaskSubmit(e) {
        e.preventDefault();
        
        const title = taskTitle.value.trim();
        const description = taskDesc.value.trim();
        
        if (!title) return;
        
        // Disable form while submitting
        const submitBtn = taskForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';
        
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, description })
            });
            
            if (!response.ok) throw new Error('Failed to add task');
            
            const newTask = await response.json();
            
            // Add to state and re-render
            tasks.unshift(newTask); // Add to beginning
            renderTasks();
            
            // Reset form
            taskForm.reset();
            taskTitle.focus();
            
            showToast('Task added successfully!', 'success');
        } catch (error) {
            console.error('Error adding task:', error);
            showToast('Failed to add task', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Add Task <i class="fa-solid fa-plus"></i>';
        }
    }

    async function toggleTaskStatus(id, currentStatus) {
        const newStatus = currentStatus === 'pending' ? 'completed' : 'pending';
        
        // Optimistic UI update
        const taskIndex = tasks.findIndex(t => t.id === id);
        if (taskIndex !== -1) {
            tasks[taskIndex].status = newStatus;
            renderTasks(); // Re-render to show immediate feedback
        }
        
        try {
            const response = await fetch(`${API_URL}${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: newStatus })
            });
            
            if (!response.ok) {
                // Revert optimistic update on failure
                throw new Error('Failed to update task');
            }
            
            const updatedTask = await response.json();
            tasks[taskIndex] = updatedTask; // Ensure state matches server exactly
            
            const statusMsg = newStatus === 'completed' ? 'Task completed!' : 'Task marked as pending';
            showToast(statusMsg, 'success');
        } catch (error) {
            console.error('Error updating task:', error);
            // Revert optimistic update
            tasks[taskIndex].status = currentStatus;
            renderTasks();
            showToast('Failed to update task', 'error');
        }
    }

    async function deleteTask(id, element) {
        // Add removing animation class
        element.classList.add('removing');
        
        try {
            const response = await fetch(`${API_URL}${id}/`, {
                method: 'DELETE'
            });
            
            if (!response.ok) throw new Error('Failed to delete task');
            
            // Wait for animation to finish before updating state/DOM
            setTimeout(() => {
                tasks = tasks.filter(t => t.id !== id);
                renderTasks();
                showToast('Task deleted', 'success');
            }, 300);
            
        } catch (error) {
            console.error('Error deleting task:', error);
            element.classList.remove('removing');
            showToast('Failed to delete task', 'error');
        }
    }

    function renderTasks() {
        taskList.innerHTML = '';
        
        const filteredTasks = tasks.filter(task => {
            if (currentFilter === 'all') return true;
            return task.status === currentFilter;
        });
        
        if (filteredTasks.length === 0) {
            emptyState.classList.remove('hidden');
            return;
        }
        
        emptyState.classList.add('hidden');
        
        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.status === 'completed' ? 'completed' : ''}`;
            li.dataset.id = task.id;
            
            // Format date nicely
            const dateObj = new Date(task.created_date + 'Z'); // Appending Z to interpret as UTC from SQLite default
            const dateStr = dateObj.toLocaleDateString(undefined, { 
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            li.innerHTML = `
                <div class="task-checkbox-container">
                    <button class="custom-checkbox" aria-label="Toggle status" title="Mark as ${task.status === 'pending' ? 'completed' : 'pending'}">
                        <i class="fa-solid fa-check"></i>
                    </button>
                </div>
                <div class="task-content">
                    <div class="task-title">${escapeHTML(task.title)}</div>
                    ${task.description ? `<div class="task-desc">${escapeHTML(task.description)}</div>` : ''}
                    <div class="task-meta">
                        <i class="fa-regular fa-clock"></i>
                        <span>Added ${dateStr}</span>
                    </div>
                </div>
                <div class="task-actions">
                    <button class="expand-btn" aria-label="Toggle questions" title="Show Questions">
                        <i class="fa-solid fa-chevron-down"></i>
                    </button>
                    <button class="delete-btn" aria-label="Delete task" title="Delete task">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            `;
            
            // Generate Questions HTML
            const questionsContainer = document.createElement('div');
            questionsContainer.className = 'questions-section hidden';
            
            // Sort questions to always display in the same order
            const sortedQuestions = (task.questions || []).sort((a,b) => a.id - b.id);
            
            let questionsHTML = `<ul class="questions-list">`;
            sortedQuestions.forEach((q, index) => {
                questionsHTML += `
                    <li class="question-item ${q.is_completed ? 'completed' : ''}" data-qid="${q.id}">
                        <div class="task-checkbox-container">
                             <button class="custom-checkbox q-checkbox" aria-label="Toggle question status" title="Mark as ${q.is_completed ? 'pending' : 'completed'}">
                                 <i class="fa-solid fa-check"></i>
                             </button>
                        </div>
                        <div class="question-content">
                            <div class="question-text">${escapeHTML(q.text)}</div>
                            <input type="text" class="question-answer" placeholder="Type your answer here..." value="${escapeHTML(q.answer || '')}" ${q.is_completed ? 'readonly' : ''}>
                        </div>
                        <button class="btn-text delete-q-btn" style="color:var(--danger-color)" title="Remove question"><i class="fa-solid fa-xmark"></i></button>
                    </li>
                `;
            });
            questionsHTML += `</ul>`;
            
            if (sortedQuestions.length < 5) {
                questionsHTML += `
                    <form class="add-question-form" data-task-id="${task.id}">
                        <input type="text" placeholder="Add a new question/sub-task (max 5)" required>
                        <button type="submit" class="btn-primary btn-small"><i class="fa-solid fa-plus"></i> Add</button>
                    </form>
                `;
            } else {
                questionsHTML += `<div style="font-size:0.8rem; color:var(--text-muted); text-align:center;">Maximum of 5 questions reached.</div>`;
            }
            
            questionsContainer.innerHTML = questionsHTML;
            li.appendChild(questionsContainer);
            
            // Add event listeners right after creating elements
            const checkboxBtn = li.querySelector('.custom-checkbox:not(.q-checkbox)');
            checkboxBtn.addEventListener('click', () => toggleTaskStatus(task.id, task.status));
            
            const deleteBtn = li.querySelector('.delete-btn');
            deleteBtn.addEventListener('click', () => {
                if(confirm('Are you sure you want to delete this task?')) {
                    deleteTask(task.id, li);
                }
            });

            // Expand Button functionality
            const expandBtn = li.querySelector('.expand-btn');
            expandBtn.addEventListener('click', () => {
                questionsContainer.classList.toggle('hidden');
                expandBtn.classList.toggle('open');
            });

            // Question Interactions
            const addQForm = li.querySelector('.add-question-form');
            if (addQForm) {
                addQForm.addEventListener('submit', (e) => handleAddQuestion(e, task.id, li));
            }
            
            // Attach specific question listeners
            const qItems = li.querySelectorAll('.question-item');
            qItems.forEach(qItem => {
                const qId = qItem.dataset.qid;
                const qCheck = qItem.querySelector('.q-checkbox');
                const qInput = qItem.querySelector('.question-answer');
                const qDel = qItem.querySelector('.delete-q-btn');
                
                qCheck.addEventListener('click', () => toggleQuestionStatus(qId, task.id));
                qDel.addEventListener('click', () => deleteQuestion(qId, task.id));
                
                // Save answer when focus leaves the input
                qInput.addEventListener('change', (e) => updateQuestionAnswer(qId, e.target.value, task.id));
            });
            
            taskList.appendChild(li);
        });
    }

    function showLoader(show) {
        if (show) {
            loader.classList.remove('hidden');
            taskList.classList.add('hidden');
        } else {
            loader.classList.add('hidden');
            taskList.classList.remove('hidden');
        }
    }

    // --- Question Handlers ---
    async function handleAddQuestion(e, taskId, liElement) {
        e.preventDefault();
        const inputStr = e.target.querySelector('input').value.trim();
        if (!inputStr) return;
        
        try {
            const response = await fetch(`${API_URL}${taskId}/questions/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: inputStr })
            });
            
            if (!response.ok) throw new Error('Failed to add question');
            
            // Re-fetch everything to ensure strict state sync
            fetchTasks();
            showToast('Question added', 'success');
        } catch(err) {
            console.error(err);
            showToast(err.message || 'Could not add question', 'error');
        }
    }

    async function toggleQuestionStatus(questionId, taskId) {
        // Find task and question state natively
        const task = tasks.find(t => t.id === taskId);
        const question = task.questions.find(q => q.id === parseInt(questionId));
        const newStatus = !question.is_completed;

        try {
            const response = await fetch(`/questions/${questionId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_completed: newStatus })
            });
            
            if (!response.ok) throw new Error('Failed to update status');
            fetchTasks(); // refresh UI
        } catch(err) {
            console.error(err);
            showToast('Failed to update question status', 'error');
        }
    }

    async function updateQuestionAnswer(questionId, answerValue, taskId) {
        try {
            const response = await fetch(`/questions/${questionId}/`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answer: answerValue })
            });
            if (!response.ok) throw new Error('Failed to save answer');
            
            // Silently sync local array so a full refetch flash doesn't occur constantly when typing
            const task = tasks.find(t => t.id === taskId);
            const question = task.questions.find(q => q.id === parseInt(questionId));
            if(question) { question.answer = answerValue; }
            
            showToast('Answer Auto-Saved!', 'success');
        } catch(err) {
            console.error(err);
            showToast('Failed to save answer', 'error');
        }
    }

    async function deleteQuestion(questionId, taskId) {
        if(!confirm('Delete this question?')) return;
        try {
            const response = await fetch(`/questions/${questionId}/`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete question');
            fetchTasks();
            showToast('Question Removed', 'success');
        } catch(err) {
             console.error(err);
             showToast('Failed to delete question', 'error');
        }
    }

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
        
        toast.innerHTML = `
            <i class="fa-solid ${icon}"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        
        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Utility to prevent XSS
    function escapeHTML(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
