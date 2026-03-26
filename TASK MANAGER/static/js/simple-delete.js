// Simple, working delete function
function deleteTaskSimple(taskId) {
    if (!confirm('Delete task ' + taskId + '?')) {
        return;
    }
    
    // Create a simple form submission
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/ajax/delete/' + taskId + '/';
    
    // Add CSRF token
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
    form.appendChild(csrfInput);
    
    // Submit the form
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}
