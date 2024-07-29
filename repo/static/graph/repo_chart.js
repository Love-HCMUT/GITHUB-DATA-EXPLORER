import { fetchAPI } from "../fetch/repo_fetch.js";

let chart = document.querySelector('#languages_repo');

const PORT = "http://127.0.0.1:8000";
let url = `${PORT}/repo/test/KietCSE`;

let xValues = [], yValues = [];
try {
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        xValues = Object.keys(data);
        console.log(xValues)
        yValues = Object.values(data);
        console.log(yValues)
        new Chart(chart, {
            type: "pie",
            data: {
              labels: xValues,
              datasets: [{
                backgroundColor: shuffle(colors),
                data: yValues
              }]
            },
            options: {
              title: {
                display: true,
                text: "World Wide Wine Production 2018"
              }
            }
        });
    })
    .catch(err => console.log(err))
}
catch(err) {
    console.log(err)
    xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
    yValues = [55, 49, 44, 24, 15];
    console.log('catch');
}
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

// new Chart(chart, {
//     type: "pie",
//     data: {
//       labels: xValues,
//       datasets: [{
//         backgroundColor: shuffle(colors),
//         data: yValues
//       }]
//     },
//     options: {
//       title: {
//         display: true,
//         text: "World Wide Wine Production 2018"
//       }
//     }
// });

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
    	const j = Math.floor(Math.random() * (i + 1));
    	[array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}