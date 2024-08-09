import {fetchAPI} from '../fetch/fetchUser.js'
import {PORT, username} from "../info/user_info.js";

// DRAW LINE GRAPH FOR ACTIVITIES IN 3 MONTHS 
async function UserActivityGraph() {
    const activityLine = await fetchAPI(`${PORT}/user/activity/${username}`)
    let Months = Object.keys(activityLine)
    let Activity = Object.values(activityLine)
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