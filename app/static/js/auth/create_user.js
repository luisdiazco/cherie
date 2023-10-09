// Get references to the form elements
const registrationForm = document.getElementById('registration-form');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const firstNameInput = document.getElementById('first-name');
const lastNameInput = document.getElementById('last-name');

// Add an event listener to the form submission
registrationForm.addEventListener('submit', async (e) => {
  e.preventDefault(); // Prevent the form from submitting via the browser

  // Collect user input data
  const userData = {
    username: usernameInput.value,
    email: emailInput.value,
    password: passwordInput.value,
  };

  // Send a POST request to your server
  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      // Registration successful, you can redirect to another page or show a success message
      console.log('Registration successful');
    } else {
      // Registration failed, handle errors here
      console.error('Registration failed');
    }
  } catch (error) {
    console.error('Error:', error);
  }
});
