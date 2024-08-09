import {PORT, orgname} from "../info/org_info.js";
let chart_contributions = document.querySelector('#contributions');

let url = `${PORT}/org/contributions/${orgname}`;

let xValues = [], yValues = [];

fetch(url)
    .then(response => response.json())
    .then(data => {
        xValues = Object.keys(data);
        yValues = Object.values(data);
        new Chart(chart_contributions, {
            type: "bar",
            data: {
                labels: xValues,
                datasets: [{
                    backgroundColor: shuffle(colors),
                    data: yValues
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: "Contributions"
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