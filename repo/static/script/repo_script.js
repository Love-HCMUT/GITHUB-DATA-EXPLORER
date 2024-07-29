let repoInfo = document.querySelector('.repo-info')

const PORT = "http://127.0.0.1:8000";
let url = `${PORT}/repo/test/krahets/hello-algo`;

fetch(url)
.then(response => response.json())
.then(data => {
    console.log(data)
    let html = `
    <div class = "repo-stars">
        <ion-icon name="star-outline"></ion-icon>
        <p><span class="text">Stars: </span>${data["stargazers_count"]}</p>
    </div>
    <div class = "repo-forks">
        <ion-icon name="git-network-outline"></ion-icon>
        <p><span class="text">Forks: </span>${data["forks_count"]}</p>
    </div>
    <div class = "repo-watching">
        <ion-icon name="eye-outline"></ion-icon>
        <p><span class="text">Watching: </span>${data["watchers_count"]}</p>
    </div>
    <div class = "repo-branches">
        <ion-icon name="git-branch-outline"></ion-icon>
        <p><span class="text">Branches: </span>${data["branches"].length}</p>
    </div>
    <div class = "repo-open-issues">
        <ion-icon name="trending-down-outline"></ion-icon>
        <p><span class="text">Open issues: </span>${data["open_issues_count"]}</p>
    </div>
    <div class = "repo-description">
        <ion-icon name="reader-outline"></ion-icon>
        <p>Description: ${data["description"]}</p>
    </div>
    `
    repoInfo.innerHTML = html;
})
.catch(err => console.log(err))