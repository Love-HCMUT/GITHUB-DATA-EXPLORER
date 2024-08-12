import { PORT, TOKEN } from "./secret.js";

document.getElementById('mainForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    let orgname = document.getElementById('orgname').value.trim();
    let token = document.getElementById('token').value.trim();

    try {
        const response = await fetch(`https://api.github.com/orgs/${orgname}`, {
            headers: {
                'Authorization': `token ${token}`
            }
        });

        if (response.status === 200) {
           // alert(`Organization "${orgData.login}" exists and the token is valid.`);
            localStorage.setItem('orgname', orgname);
            localStorage.setItem('token', token);  // Chuyển hướng đến trang org sau khi xác thực thành công
            window.location.href = `${PORT}/org`
        } else if (response.status === 404) {
            alert('Organization does not exist.');
        } else if (response.status === 401) {
            alert('Invalid or expired token.');
        } else {
            alert(`An error occurred: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while checking the organization and token.');
    }
});
