document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const chatContainer = document.getElementById('chatContainer');
    const documentContent = document.getElementById('documentContent');
    const taskInput = document.getElementById('taskInput');
    const classInput = document.getElementById('classInput');
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const responseContainer = document.getElementById('responseContainer');
    const valueToCopy = document.getElementsByTagName('div');

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // Show loading indicator
        // chatContainer.innerHTML = '<p>Loading...</p>';

        console.log('Sending file to server...');

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Received response from server');
            return response.json();
        })
        .then(data => {
            console.log('Parsed response data:', data);
            if (data.success) {
                console.log('File processed successfully');
                documentContent.value = data.text;
                // chatContainer.innerHTML = ''; // Clear loading indicator
                console.log('Chat container updated');
            } else {
                throw new Error(data.error ||  'An error occurred while processing the file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        });
    });
    
    generateBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const taskInputValue = taskInput.value;
        const classInputValue = classInput.value;
        const context = documentContent.value;
        
        if (!taskInputValue.trim() || !classInputValue.trim()) {
            alert('Please enter a question.');
            return;
        }
        

        chatContainer.style.display = 'flex';
        chatContainer.appendChild(responseContainer);
        chatContainer.appendChild(copyBtn);

    
        // Show loading indicator
        responseContainer.innerHTML = '<p>Loading...</p>';

        console.log('Sending question to server...');

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                taskInputValue: taskInputValue,
                classInputValue: classInputValue,
                context: context
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received response from server:', data);
            if (data.response) {
                responseContainer.innerHTML = marked.parse(data.response);
            } else {
                throw new Error(data.error || 'An error occurred while processing your question.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            responseContainer.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
    
    copyBtn.addEventListener('click', function(e) {
        e.preventDefault();
        navigator.clipboard.writeText(valueToCopy[5].textContent);
        copyBtn.innerHTML = 'Copied';
        setTimeout(() => {
            copyBtn.innerHTML = 'Copy as text';
        }, 2000);
    });
});

