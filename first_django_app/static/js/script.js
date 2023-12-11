async function sendMessage() {
    let fd = new FormData();
    let token = getCSRFToken();
    let messageText = document.getElementById('messageField').value;
  
    let messageClass = userName === "{{ request.user.first_name }}" ? "my-message" : "other-message";
  
    messageContainer.innerHTML += `
      <div class="${messageClass}"><b>${userName}:</b> ${messageText}</div>
    `;
  
    document.getElementById('messageField').value = '';
  
    fd.append('textmessage', messageText);
    fd.append('csrfmiddlewaretoken', token);
  
    try {
      let response = await fetch('/chat/', {
        method: 'POST',
        body: fd
      });
      let json = await response.json();
      console.log('JSON is', json);
    } catch(e) {
      console.error('Error', e);
    }
  }

function getCSRFToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}

function logoutUser() {
    window.location.href = '/logout/';
}