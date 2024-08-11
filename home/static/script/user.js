import { PORT, TOKEN} from "./secret.js"
let submit = document.getElementById('submit');
submit.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    let username = document.getElementById('username');
    let token = document.getElementById('token');
    if (username.value !== '') {
        localStorage.setItem('username', username.value);
        window.location.href = `${PORT}/user`
    }
    else {
        alert('Username cannot be blank.');
    }
    if (token.value !== '') {
        localStorage.setItem('token', token.value);
    }
    else {
        localStorage.setItem('token', TOKEN)
    }
})