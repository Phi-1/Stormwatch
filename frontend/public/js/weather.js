let temp_day_data_el = document.querySelector("#temp_day_data")
let data_list_el = document.querySelector("#data_list")
let temp_day_data = JSON.parse(temp_day_data_el.innerHTML)
console.log(temp_day_data)
// data_list_el.removeChild(data_list_el)

let ctx = document.querySelector('#temp_day_chart').getContext('2d')

let temp_day_chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Object.keys(temp_day_data),
        datasets: [{
            label: 'Temperature',
            data: Object.values(temp_day_data),
            backgroundColor: "rgba(100, 100, 120, 1)",
            borderColor: "rgba(70, 255, 200, .9)",
            borderWidth: 2
        }]
    },
    options: {
        responsive: false
    }
})