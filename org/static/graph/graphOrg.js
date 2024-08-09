import { fetchAPI } from "../fetch/fetchOrg.js"
import {PORT, orgname} from "../info/org_info.js"

async function CreateOrgInformation() {
    let data = await fetchAPI(`${PORT}/org/infor/${orgname}`)
    const org = document.querySelector('.org-data')
    org.innerHTML = `
        <div class="part1">           
            <img src="${data.avatar_url}"  alt="">
        </div>

        <div class="part2">
            <div class="name box">
                <ion-icon name="person-outline"></ion-icon>
                <p><span class="text">Name: </span>${data.login}</p>
            </div>

            <div class="email box">
                <ion-icon name="mail-outline"></ion-icon>
                <p><span class="text">Email: </span>${data.email}</p>
            </div>

            <div class="location box">
                <ion-icon name="location-outline"></ion-icon>
                <p><span class="text">Location: </span>${data.location}</p>
            </div>

            <div class="follower box">
                <ion-icon name="people-outline"></ion-icon>
                <p><span class="text">Followers: </span>${data.followers}</p>
            </div>

            <div class="createAt box">
                <ion-icon name="time-outline"></ion-icon>
                <p><span class="text">Create at: </span>${data.created_at}</p>
            </div>

            <div class="description box">
                <ion-icon name="information-circle-outline"></ion-icon>
                <p><span class="text">Description: </span>${data.description}</p>
            </div>

            <div class="memeber box">
                <ion-icon name="people-outline"></ion-icon>
                <p><span class="text">Members: </span>${data.members}</p>
            </div>
        </div>
    `
}

CreateOrgInformation()