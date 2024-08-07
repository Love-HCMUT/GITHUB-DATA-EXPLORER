const PORT = "http://127.0.0.1:3000";
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
        alert('Owner và Repo không được để trống.');
    }
    localStorage.setItem('token', token.value);
})