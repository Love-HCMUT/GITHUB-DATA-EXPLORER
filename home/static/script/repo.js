const PORT = "http://127.0.0.1:3000";
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
        alert('Owner và Repo không được để trống.');
    }
    localStorage.setItem('token', token.value);
})