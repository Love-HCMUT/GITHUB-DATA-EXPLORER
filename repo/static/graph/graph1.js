import {fetchAPI} from '../fetch/fetch1.js'

const PORT = "http://127.0.0.1:3000"


// DRAW BAR GRAPH FOR CONTRIBUTORS 
async function RepoContributorGraph() {
    const contributors = await fetchAPI(`${PORT}/repo/contributor`)
    let NameContributor = Object.keys(contributors)
    let DataContributor = Object.values(contributors)

    const ctx = document.getElementById('myChart1');
    new Chart(ctx, {
        type: 'bar',
        data: {
          labels: NameContributor,
          datasets: [{
            label: 'TOP 10 CONTRIBUTORS',
            data: DataContributor,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)',
                'rgba(60, 59, 110, 0.2)',
                'rgba(3, 167, 4, 0.2)',
                'rgba(1,88,63,0.2)'
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)',
                'rgb(60, 59, 110)',
                'rgb(3, 167, 4)',
                'rgb(1,88,63)'
              ],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
}
// RepoContributorGraph()


// DRAW LINE GRAPH FOR COMMIT IN 6 MONTHS 
async function RepoCommmitsGraph() {
    const commitLine = await fetchAPI(`${PORT}/repo/commit`)
    let Months = Object.keys(commitLine)
    let Commits = Object.values(commitLine)
    console.log(Months)
    console.log(Commits)
    const char = document.getElementById('myChart1');

    new Chart(char, {
      type: 'line',
      data: {
        labels: Months,
        datasets: [{
            label: 'Total commmits',
            data: Commits,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'COMMITS WITHN RECENT 6 MONTHS'
          }
        }
      },
    });
}

// RepoCommmitsGraph()


// DRAW LINE GRAPH FOR ISSUES IN 6 MONTHS 
async function RepoIssuesGraph() {
  const issuesLine = await fetchAPI(`${PORT}/repo/issues`)
  let Months = Object.keys(issuesLine)
  let Issues = Object.values(issuesLine)
  console.log(Months)
  console.log(Issues)
  const chart = document.getElementById('myChart2');

  new Chart(chart, {
    type: 'line',
    data: {
      labels: Months,
      datasets: [{
          label: 'Total issues',
          data: Issues,
          fill: false,
          borderColor: 'rgb(255, 205, 86)',
          tension: 0.1,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'ISSUES WITHIN RECENT 6 MONTHS'
        }
      }
    },
  });
}

RepoIssuesGraph()