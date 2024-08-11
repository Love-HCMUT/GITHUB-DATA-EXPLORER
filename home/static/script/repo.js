import { PORT, TOKEN} from "./secret.js"
let submit = document.getElementById('submit');
submit.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    let owner = document.getElementById('owner');
    let repo = document.getElementById('repo');
    let token = document.getElementById('token');
    if (owner.value !== '' && repo.value !== '') {
        localStorage.setItem('owner', owner.value);
        localStorage.setItem('repo', repo.value);
        window.location.href = `${PORT}/repo`
    }
    else {
        alert('Owner name and Repository name cannot be blank.');
    }
    if (token.value !== '') {
        localStorage.setItem('token', token.value);
    }
    else {
        localStorage.setItem('token', TOKEN)
    }
})