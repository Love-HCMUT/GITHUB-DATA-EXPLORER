let repoInfo = document.querySelector('.org-data')

const PORT = "http://127.0.0.1:3000";
let url = `${PORT}/repo/info/krahets/hello-algo`;

fetch(url)
    .then(response => response.json())
    .then(data => {
    //     <div class = "stats">
    //     <div class = "repo-stars">
    //         <div class = "title">
    //             <ion-icon name="star-outline"></ion-icon>
    //             <p class="text">Stars: </p>
    //         </div>
    //         <p class = "content">${data["stargazers_count"]}</p>
    //     </div>
    //     <div class = "repo-forks">
    //         <div class = "title">
    //             <ion-icon name="git-network-outline"></ion-icon>
    //             <p class="text">Forks: </p>
    //         </div>
    //         <p class = "content">${data["forks_count"]}</p>
    //     </div>
    //     <div class = "repo-watching">
    //         <div class = "title">
    //             <ion-icon name="eye-outline"></ion-icon>
    //             <p class="text">Watching: </p>
    //         </div>
    //         <p class = "content">${data["watchers_count"]}</p>
    //     </div>
    //     <div class = "repo-branches">
    //         <div class = "title">
    //             <ion-icon name="git-branch-outline"></ion-icon>
    //             <p class="text">Branches: </p>
    //         </div>
    //         <p class = "content">${data["branches"].length}</p>
    //     </div>
    //     <div class = "repo-open-issues">
    //         <div class = "title">
    //             <ion-icon name="trending-down-outline"></ion-icon>
    //             <p class="text">Open issues: </p>
    //         </div>
    //         <p class = "content">${data["open_issues_count"]}</p>
    //     </div>
    // </div>
    // <div class = "repo-description">
    //     <div class = "title">
    //         <p class="text">Description: </p>
    //     </div>
    //     <p>${data["description"]}</p>
    // </div>
        let html = `
            <div class="part1">           
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="">
            </div>

            <div class="part2">
                <div class="name box">
                    <ion-icon name="person-outline"></ion-icon>
                    <p><span class="text">Name: </span>NAME???</p>
                </div>
    
                <div class="start box">
                    <ion-icon name="star-outline"></ion-icon>
                    <p><span class="text">Stars: </span>${data["stargazers_count"]}</p>
                </div>
    
                <div class="fork box">
                    <ion-icon name="git-network-outline"></ion-icon>
                    <p><span class="text">Forks: </span>${data["forks_count"]}</p>
                </div>
    
                <div class="watch box">
                     <ion-icon name="eye-outline"></ion-icon>
                    <p><span class="text">Watches: </span>${data["watchers_count"]}</p>
                </div>
    
                <div class="branch box">
                    <ion-icon name="git-branch-outline"></ion-icon>
                    <p><span class="text">Branchs: </span>${data["branches"].length}</p>
                </div>

                <div class="issues box">
                    <ion-icon name="trending-down-outline"></ion-icon>
                    <p><span class="text">Open issues: </span>${data["open_issues_count"]}</p>
                </div>
               
            </div>
    
            <div class="part3">
                <div class="description box-2">
                    <ion-icon name="information-circle-outline"></ion-icon>
                    <p><span class="text">Description: </span>${data["description"]}</p>
                </div>
    
            </div> 
        `
        repoInfo.innerHTML = html;
    })
    .catch(err => console.log(err))