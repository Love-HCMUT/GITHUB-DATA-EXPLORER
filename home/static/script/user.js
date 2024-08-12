import { PORT, TOKEN } from "./secret.js";

document.getElementById('mainForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    let username = document.getElementById('username').value.trim();
    let token = document.getElementById('token').value.trim();

    if(!token) token = TOKEN;
    try {
        const response = await fetch(`https://api.github.com/users/${username}`, {
            headers: {
                'Authorization': `token ${token}`
            }
        });

        if (response.status === 200) {
           // alert(`User "${username.login}" exists and the token is valid.`);
            localStorage.setItem('username', username);
            localStorage.setItem('token', token);  
            window.location.href = `${PORT}/user`
        } else if (response.status === 404) {
            alert('User does not exist.');
        } else if (response.status === 401) {
            alert('Invalid or expired token.');
        } else {
            alert(`An error occurred: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while checking the user and token.');
    }
});
