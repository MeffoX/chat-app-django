let options = { year: 'numeric', month: 'short', day: 'numeric' };
let currentDate = new Date().toLocaleDateString('en-US', options);

/**
 * Asynchronously sends a message to the server.
 * It captures the text message from a DOM element, appends it to FormData,
 * and sends a POST request to the server. The response is logged in the console.
 * Also updates the message container with the user's message.
 */
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


/**
 * Retrieves the CSRF token from the DOM.
 * @returns {string} The CSRF token value.
 */
function getCSRFToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}


/**
 * Redirects the user to the logout page.
 */
function logoutUser() {
    window.location.href = '/logout/';
}


/**
 * Validates the login form.
 * Checks if the username and password fields are not empty. Displays an error message if validation fails.
 * @returns {boolean} True if the form is valid, false otherwise.
 */
function validateLoginForm() {
    let username = document.getElementById("login").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("login-error-message");

    if (username === "" || password === "") {
        errorMessage.innerText = "Name or password is invalide!";
        errorMessage.style.display = "block";
        return false;
    }
    errorMessage.style.display = "none";
    return true;
}


/**
 * Validates the password and confirm password fields.
 * Checks if the password and confirm password fields match. Adds or removes validation styles based on the check.
 * @returns {boolean} True if the passwords match, false otherwise.
 */
function validatePassword() {
    let password = document.getElementById("password").value;
    let confirm_password = document.getElementById("confirm_password").value;
    let password_div = document.getElementById("password_div");
    let confirm_div = document.getElementById("confirm_password_div");
    let error_message = document.getElementById("password_error");

    if (password != confirm_password) {
        password_div.classList.add("is-invalid");
        confirm_div.classList.add("is-invalid");
        error_message.style.display = "block";
        return false;
    } else {
        password_div.classList.remove("is-invalid");
        confirm_div.classList.remove("is-invalid");
        error_message.style.display = "none";
        return true;
    }
}