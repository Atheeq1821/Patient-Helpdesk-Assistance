window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) { 
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});


        document.getElementById('chat-form').onsubmit = function(event) {
            event.preventDefault();
            var formData = new FormData(event.target);
            fetch("/assistant/", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
            .then(response => response.json())
            .then(data => {
                const chatWindow = document.getElementById('chat-window');

                const usermessage = document.createElement('div');
                usermessage.classList.add( 'message', 'user');
                usermessage.textContent =data.user;
                chatWindow.appendChild(usermessage);

                // chatWindow.scrollTop = chatWindow.scrollHeight;

                const aimessage = document.createElement('div');
                aimessage.classList.add( "message", 'bot');
                aimessage.textContent= data.model;
                chatWindow.appendChild(aimessage);

                chatWindow.scrollTop = chatWindow.scrollHeight;
                event.target.reset(); 
            });
        };

// function sendMessage() {
//     const inputField = document.getElementById('user-input');
//     const message = inputField.value.trim();

//     if (message) {
//         displayMessage(message, 'user');
//         inputField.value = '';

//         // Here you would send the message to your backend service
//         // For demonstration, we will simulate a response
//         setTimeout(() => {
//             displayMessage(`You said: ${message}`, 'bot');
//         }, 1000);
//     }
// }

// function displayMessage(message, sender) {
//     const chatWindow = document.getElementById('chat-window');
//     const messageElement = document.createElement('div');
//     messageElement.classList.add('message', sender);
//     messageElement.textContent = message;
//     chatWindow.appendChild(messageElement);
//     chatWindow.scrollTop = chatWindow.scrollHeight;
// }
