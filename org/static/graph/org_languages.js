import {PORT, orgname, TOKEN} from "../info/org_info.js";
let chart = document.querySelector('#languages');

let url = `${PORT}/org/languages/${orgname}/${TOKEN}`;

let xValues = [], yValues = [];

fetch(url)
    .then(response => response.json())
    .then(data => {
        xValues = Object.keys(data);
        yValues = Object.values(data);
        new Chart(chart, {
            type: "pie",
            data: {
                labels: xValues,
                datasets: [{
                    backgroundColor: shuffle(colors),
                    borderColor: shuffle(colors),
                    borderWidth: 1,
                    data: yValues
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            generateLabels: (chart) => {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const percentage = data.datasets[0].data[i].toString() + "%";
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
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: "Languages",
                        color: "black",
                        font: {
                            size: 20,
                        }
                    }
                }
            }
        });
    })
    .catch(err => alert(err))


const colors = [
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

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
    	const j = Math.floor(Math.random() * (i + 1));
    	[array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}