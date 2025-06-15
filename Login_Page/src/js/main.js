// This file contains the JavaScript code for handling form submissions and user interactions on the login page.

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');

    if (showRegister) {
        showRegister.addEventListener('click', function(e) {
            e.preventDefault();
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
        });
    }

    if (showLogin) {
        showLogin.addEventListener('click', function(e) {
            e.preventDefault();
            registerForm.style.display = 'none';
            loginForm.style.display = 'block';
        });
    }

    document.querySelector('.form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;

        const res = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, role })
        });
        const data = await res.json();
        alert(data.message);

        // Debug: log values
        console.log('Login response:', res.ok, 'Role:', role);

        if (res.ok && role === 'superAdmin') {
            console.log('Redirecting to main.html as superAdmin');
            window.location.href = 'c:\\Users\\user\\Documents\\FrontEnd Development\\Byte_Battle\\dashboard\\main.html';        
        } else if (res.ok && role === 'student') {
            window.location.href = '../../Student_Side/student-dash.html';
        } else {
            console.log('No redirect: res.ok=', res.ok, 'role=', role);
        }
    });
});