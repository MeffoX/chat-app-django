let options = { year: 'numeric', month: 'short', day: 'numeric' };
let currentDate = new Date().toLocaleDateString('en-US', options);

async function sendMessage() {
  let fd = new FormData();
  fd.append('textmessage', document.getElementById('messageField').value);
  fd.append('csrfmiddlewaretoken', getCSRFToken());

  messageContainer.innerHTML += `<div class="my-message"><b>${userName}:</b> (${currentDate})<br> ${document.getElementById('messageField').value}</div>`;
  document.getElementById('messageField').value = '';

  try {
      let response = await fetch('/chat/', { method: 'POST', body: fd });
      console.log('JSON is', await response.json());
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