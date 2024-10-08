document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const chatContainer = document.getElementById('chatContainer');
    const documentContent = document.getElementById('documentContent');
    const questionInput = document.getElementById('questionInput');
    const askButton = document.getElementById('askButton');
    const responseContainer = document.getElementById('responseContainer');

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // Show loading indicator
        chatContainer.innerHTML = '<p>Loading...</p>';
        chatContainer.style.display = 'block';

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
                chatContainer.innerHTML = ''; // Clear loading indicator
                chatContainer.appendChild(documentContent);
                chatContainer.appendChild(questionInput);
                chatContainer.appendChild(askButton);
                chatContainer.appendChild(responseContainer);
                console.log('Chat container updated');
            } else {
                throw new Error(data.error || 'An error occurred while processing the file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            chatContainer.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });

    askButton.addEventListener('click', function() {
        const question = questionInput.value;
        const context = documentContent.value;

        if (!question.trim()) {
            alert('Please enter a question.');
            return;
        }

        // Show loading indicator
        responseContainer.innerHTML = '<p>Loading...</p>';

        console.log('Sending question to server...');

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({question: question, context: context})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received response from server:', data);
            if (data.response) {
                responseContainer.innerHTML = `<p><strong>Q:</strong> ${question}</p><p><strong>A:</strong> ${data.response}</p>`;
                questionInput.value = '';
            } else {
                throw new Error(data.error || 'An error occurred while processing your question.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            responseContainer.innerHTML = `<p>Error: ${error.message}</p>`;
        });
    });
});