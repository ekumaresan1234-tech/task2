// Simple working delete function
function deleteTaskWorking(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return false;
    }
    
    console.log('Starting delete for task:', taskId);
    
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) {
        console.error('CSRF token not found');
        alert('Error: Security token not found');
        return false;
    }
    
    console.log('CSRF token found:', csrfToken.value.substring(0, 10) + '...');
    
    // Create form data
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken.value);
    
    // Send delete request
    fetch('/ajax/delete/' + taskId + '/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Delete response received:', response.status);
        if (!response.ok) {
            throw new Error('Server error: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Delete response data:', data);
        if (data.success) {
            alert('Task deleted successfully!');
            window.location.reload();
        } else {
            alert('Delete failed: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Delete error:', error);
        alert('Delete error: ' + error.message);
    });
    
    return false;
}

// Alternative simple form submission
function deleteTaskForm(taskId) {
    if (!confirm('Delete this task?')) {
        return false;
    }
    
    // Create and submit form
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/ajax/delete/' + taskId + '/';
    
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
    form.appendChild(csrfInput);
    
    document.body.appendChild(form);
    form.submit();
    
    return false;
}
