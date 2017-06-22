var ctx = $("#hourLineChart");
    var arr={{hourlyarr|safe}};
    var timeArr=[];
    var tempArr=[];
    var arr2={{hourlyarr|safe}}
    for (var i = 0; i < 25; i++) {
        var temp = new Date(arr[i].time*1000).toLocaleTimeString();
        //var temp2 = new Date(arr[i].time*1000).getMinutes();
        timeArr[i]=temp
        console.log(tempArr);
        tempArr[i]=arr[i].temperature

    }
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeArr,
            datasets: [{
                label: '°F',
                data: tempArr,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:false
                    }
                }]
            }
        }
    });
