import { PORT, TOKEN} from "./secret.js"
document.getElementById('mainForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const owner = document.getElementById('owner').value.trim();
    const repo = document.getElementById('repo').value.trim();
    let token = document.getElementById('token').value.trim();
    if(!token) token = TOKEN;
    if (!owner || !repo || !token) {
        alert('Owner name, repository name, and token are required.');
        return;
    }

    
    try {
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}`, {
            headers: {
                'Authorization': `token ${token}`
            }
        });

        if (response.status === 200) {
            localStorage.setItem('owner', owner);
            localStorage.setItem('repo', repo);
            localStorage.setItem('token', token);
            window.location.href = `${PORT}/repo`
        } else if (response.status === 404) {
            alert('Repository does not exist.');
        } else if (response.status === 401) {
            alert('Invalid or expired token.');
        } else {
            alert(`An error occurred: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while checking the repository and token.');
    }
});
