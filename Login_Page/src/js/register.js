document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Match backend field names!
    const fullname = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    const role = document.getElementById('reg-role').value;

    const messageDiv = document.getElementById('message');
    messageDiv.textContent = '';
    messageDiv.style.color = '';

    try {
        const res = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fullname, email, password, role })
        });
        const data = await res.json();
        if (res.ok) {
            messageDiv.textContent = 'Registration successful! You can now log in.';
            messageDiv.style.color = 'green';
            setTimeout(() => {
                window.location.href = 'User_login.html';
            }, 1500);
        } else {
            messageDiv.textContent = data.message || 'Registration failed.';
            messageDiv.style.color = 'red';
        }
    } catch (err) {
        messageDiv.textContent = 'Server error. Please try again later.';
        messageDiv.style.color = 'red';
    }
});