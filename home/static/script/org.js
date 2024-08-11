import { PORT, TOKEN} from "./secret.js"
let submit = document.getElementById('submit');
submit.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    let orgname = document.getElementById('orgname');
    let token = document.getElementById('token');
    if (orgname.value !== '') {
        localStorage.setItem('orgname', orgname.value);
        window.location.href = `${PORT}/org`
    }
    else {
        alert('Organization name cannot be blank.');
    }
    if (token.value !== '') {
        localStorage.setItem('token', token.value);
    }
    else {
        localStorage.setItem('token', TOKEN)
    }
})