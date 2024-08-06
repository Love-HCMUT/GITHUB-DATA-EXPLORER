import {fetchAPI} from '../fetch/fetchUser.js'

const PORT = "http://127.0.0.1:3000"

console.log("HELLO")

// DRAW LINE GRAPH FOR ACTIVITIES IN 3 MONTHS 
async function UserActivityGraph() {
    const activityLine = await fetchAPI(`${PORT}/user/activity`)
    let Months = Object.keys(activityLine)
    let Activity = Object.values(activityLine)
    console.log(Months)
    console.log(Activity)
    const ch = document.getElementById('myChart4');
  
    new Chart(ch, {
      type: 'line',
      data: {
        labels: Months,
        datasets: [{
            label: 'Total activities',
            data: Activity,
            fill: false,
            borderColor: 'rgb(60, 59, 110)',
            tension: 0.3,
            fill: true,
            backgroundColor: 'rgba(60, 59, 110, 0.5)',
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
            text: 'ACTIVITIES IN RECENT 3 MONTHS'
          }
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false
        },
        scales: {
          x: {
            title: {
              display: true,
            }
          },
          y: {
            title: {
              display: true,
              text: 'Total Activities' // Tiêu đề trục Y
            },
            beginAtZero: true
          }
        }
      },
    });
  }
  
  UserActivityGraph()