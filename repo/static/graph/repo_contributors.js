let chart = document.querySelector('#contributors');

const PORT = "http://127.0.0.1:8000";
let url = `${PORT}/repo/contributors/krahets/hello-algo`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        shuffle(colors);
        let labels = Object.keys(data);
        
        let values = Object.values(data);
        let languages = values.map((item) => Object.keys(item)).flat();
        languages = languages.reduce((result, language) => {
            if (!result.includes(language)) {
                result.push(language);
            }
            return result;
        }, []);

        let datasets = languages.map((language, index) => ({
            label: language,
            backgroundColor: colors[index % colors.length],
            data: values.map((item) => item[language] ? item[language] : 0.0),
        }));

        stackedBarChart(chart, labels, datasets, `Languages of top 3 contributors`);
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

function stackedBarChart(idChart, labels, datasets, title) {
    new Chart(idChart, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            },
            indexAxis: 'y',
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            },
        }
    })
}