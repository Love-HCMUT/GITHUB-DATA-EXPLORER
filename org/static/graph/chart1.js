import { fetchAPI } from "../fetch/fetchdata1.js";

const PORT = "http://127.0.0.1:3000";

async function CreateOrgInformation() {
    // Fetch data from the API
    let data = await fetchAPI(`${PORT}/org/data/`);

    let NameContributor = Object.keys(data.top10)
    let DataContributor = Object.values(data.top10)

    const ctx = document.getElementById('myChart1');
    new Chart(ctx, {
        type: 'bar',
        data: {
          labels: NameContributor,
          datasets: [{
            data: DataContributor,
            backgroundColor: [
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
          },
          plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: "Top Members Commit",
                color: "black",
                font: {
                    size: 20,
                },
            },
        },
    },
});
}

CreateOrgInformation();