const PORT = "http://127.0.0.1:3000";
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
    localStorage.setItem('token', token.value);
})