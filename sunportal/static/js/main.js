let ctx = document.getElementById("chartPower").getContext('2d');
let chartBottom = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Wh',
            data: [],
            backgroundColor: 'rgba(227,6,19,0.3)',
            borderColor: 'rgba(227,6,19,1)',
            borderWidth: 1,
            pointRadius: 0
        }]
    },
    options: {
        animation: {
            duration: 0
        },
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    fontColor: 'rgba(255,255,255,1)',
                    fontSize: 14
                }
            }],
            xAxes: [{
                display: false,
                type: 'time',
                ticks: {
                    fontColor: 'rgba(255,255,255,1)'
                }
            }]
        },
        legend: {
            labels: {
                fontColor: 'rgba(255,255,255,1)'
            }
        }
    }
});

let giga = Math.pow(10, 9);
let mega = Math.pow(10, 6);
let kilo = Math.pow(10, 3);

let Giga = "G";
let Mega = "M";
let Kilo = "k";

let maxDecimals = 2;

let reloadTime = 60000;

let lastDataSetLength = 0;

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function setDataPoints(dataPoints, chart) {
    for (let i = 0; i < dataPoints.length; i++) {
        addData(chart, dataPoints[i].time, dataPoints[i].power);
    }
}

function removeAllData(amount, chart) {
    for (let i = 0; i < amount; i++) {
        removeData(chart);
    }
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

function roundToDec(toRound, amount_of_decimals) {
    return Math.round(toRound*(Math.pow(10, amount_of_decimals))) / (Math.pow(10, amount_of_decimals));
}

function addPrefix(number) {
    if (number > giga) {
        return (roundToDec(number/giga, maxDecimals)) + " " + Giga;
    }
    else if (number > mega) {
        return (roundToDec(number/mega, maxDecimals)) + " " + Mega;
    }
    else if (number > kilo) {
        return (roundToDec(number/kilo, maxDecimals)) + " " + Kilo;
    }
    else {
        return roundToDec(number, maxDecimals) + " ";
    }
}

function loadData() {
    $.ajax({type: 'post', dataType: "json", url: 'http://sunportal.nl/updateData.php', success: function(response) {
        $('#dayTotal').html(addPrefix(response.dayTotal) + "Wh");
        $('#total').html(addPrefix(response.total*1000) + "Wh");
        $('#co2').html(addPrefix(response.co2) + "t");

        removeAllData(lastDataSetLength, chartBottom);
        setDataPoints(response.last24h, chartBottom);

        lastDataSetLength = response.last24h.length;
    }
    });
}

loadData();
window.setInterval(loadData, reloadTime);