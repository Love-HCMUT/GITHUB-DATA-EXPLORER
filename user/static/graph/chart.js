import { fetchAPI } from "../fetch/fetchdata.js"
import {PORT, username} from "../info/info.js"


async function CreateOrgInformation() {
    let data = await fetchAPI(`${PORT}/user/data/${username}`)
    const user = document.querySelector('.org-data')


    user.innerHTML = `
        <div class="part1">           
            <img src="${data.info.avatar_url}" alt="">
        </div>

        <div class="part2">
            <div class="name box">
                <ion-icon name="person-outline"></ion-icon>
                <p><span class="text">Name: </span>${data.info.login}</p>
            </div>

            <div class="email box">
                <ion-icon name="mail-outline"></ion-icon>
                <p><span class="text">Email: </span>${data.info.email}</p>
            </div>

            <div class="location box">
                <ion-icon name="location-outline"></ion-icon>
                <p><span class="text">Location: </span>${data.info.location}</p>
            </div>

            <div class="follower box">
                <ion-icon name="people-outline"></ion-icon>
                <p><span class="text">Followers: </span>${data.info.followers}</p>
            </div>

            <div class="createAt box">
                <ion-icon name="time-outline"></ion-icon>
                <p><span class="text">Create at: </span>${data.info.created_at}</p>
            </div>

            <div class="star box">
                <ion-icon name="star-outline"></ion-icon>
                <p><span class="text">Total stars: </span>${data.totalStars}</p>
            </div>

            <div class="totalPRs box">
                <ion-icon name="git-pull-request-outline"></ion-icon>
                <p><span class="text">PRs: </span>${data.totalPRs}</p>
            </div>
        </div>

        <div class="part3">
             <div class="description box-2">
                <ion-icon name="information-circle-outline"></ion-icon>
                <p><span class="text">Description: </span>${data.info.description}</p>
            </div>

            <div class="totalMergedPRs box-2">
                <ion-icon name="git-merge-outline"></ion-icon>
                <p><span class="text">MergedPRs: </span>${data.totalMergedPRs}</p>
            </div>

            <div class="totalContributions box-2">
                <ion-icon name="logo-github"></ion-icon>
                <p><span class="text">Contributions: </span>${data.totalContributions}</p>
            </div>
            <div class="top3Repos box-2"> 
                <ion-icon name="list-circle-outline"></ion-icon>
                <p><span class="text">Top 3 Repos: </span></p>
                <ul id="top3ReposList"></ul>
            </div>

        </div>
    `;
    const top3ReposList = document.getElementById('top3ReposList');
    data.top3Repos.forEach(repo => {
        const listItem = document.createElement('li');
        listItem.textContent = repo;
        top3ReposList.appendChild(listItem);
    });




    const totalLanguages = data.totalLanguages;
    const totalLines = Object.values(totalLanguages).reduce((a, b) => a + b, 0);
    const diverseBoldColors = [
        "#FF0000", // red
        "#0000FF", // blue
        "#00FF00", // green
        "#FFFF00", // yellow
        "#FF00FF", // magenta
        "#00FFFF", // cyan
        "#800000", // maroon
        "#008000", // green
        "#808000", // olive
        "#800080", // purple
        "#008080", // teal
        "#FFA500", // orange
        "#FFC0CB", // pink
        "#D2691E", // chocolate
        "#DC143C", // crimson
        "#2E8B57", // sea-green
        "#6A5ACD", // slate-blue
    ];
    const ctx = document.getElementById('myChart1');
    
    new Chart(ctx, {
        type: "pie",
    data: {
      labels: Object.keys(totalLanguages),
      datasets: [
        {
          label: "Total Languages",
          data: Object.values(totalLanguages),
          backgroundColor: diverseBoldColors.slice(
            0,
            Object.keys(totalLanguages).length
          ),
          borderColor: diverseBoldColors,
          borderWidth: 1,
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          position: "right",
          labels: {
            color: "black",
            generateLabels: (chart) => {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                return data.labels.map((label, i) => {
                  const value = data.datasets[0].data[i];
                  const total = data.datasets[0].data.reduce(
                    (acc, val) => acc + val,
                    0
                  );
                  const percentage = ((value / total) * 100).toFixed(2) + "%";
                  return {
                    text: `${label}: ${percentage}`,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    strokeStyle: data.datasets[0].borderColor[i],
                    lineWidth: data.datasets[0].borderWidth,
                    hidden: !chart.getDataVisibility(i),
                    index: i,
                  };
                });
              }
              return [];
            },
          },
        },
        title: {
          display: true,
          text: "Total Languages",
          color: "black",
          font: {
            size: 20,
          },
        },
      },
      layout: {
        padding: 20,
      },}
      });

      const repositories = data.repos;

      const tableData = [];

    for (const [repoName, repoInfo] of Object.entries(repositories)) {
        const totalLines = Object.values(repoInfo.languages).reduce((a, b) => a + b, 0);
        const languagePercentages = Object.entries(repoInfo.languages).map(
            ([language, lines]) => `${language}: ${(lines / totalLines * 100).toFixed(2)}%`
        ).join(", ");

        tableData.push([
            repoName,
            repoInfo.contributions,
            languagePercentages || 'N/A',
            repoInfo.stars,
            repoInfo.pullRequests,
            repoInfo.mergedPullRequests
        ]);
    }
    let table = new DataTable('#myTable', {
      // options
      data: tableData,
      pageLength: 4,  
      dom: '<"top"f>rt<"bottom"p><"clear">',
    });
}

async function CreateChartByMonth(){
  let data = await fetchAPI(`${PORT}/user/months/${username}`)
  // Chuyển đổi dữ liệu để phù hợp với định dạng biểu đồ
  const labels = Object.keys(data).reverse(); // Đổi tên tháng từ xa nhất đến gần nhất
  const values = Object.values(data).reverse(); // Giá trị tương ứng

  // Vẽ biểu đồ
  const ctx = document.getElementById('myChart2').getContext('2d'); // Thay 'myChart' bằng ID của canvas

  new Chart(ctx, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [{
              label: 'Contributions by Month',
              data: values,
              backgroundColor: 'rgb(75, 192, 192)', // Màu nền của cột
              borderColor: 'rgb(75, 192, 192)', // Màu viền của cột
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Month',
                      color: 'black'
                  },
                  ticks: {
                      color: 'black'
                  }
              },
              y: {
                  beginAtZero: true,
                  title: {
                      display: true,
                      text: 'Contributions',
                      color: 'black'
                  },
                  ticks: {
                      color: 'black'
                  }
              }
          },
          plugins: {
              legend: {
                display: false
              },
              title: {
                  display: true,
                  text: 'Contributions by Month',
                  color: 'black',
                  font: {
                      size: 20
                  }
              }
          }
      }
  });
}
CreateChartByMonth()
CreateOrgInformation()