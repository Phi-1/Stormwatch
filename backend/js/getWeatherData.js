const { exec } = require("child_process");
const log = require("./log")

module.exports = function getWeatherData() {
    return new Promise((resolve, reject) => {

        exec(`py ./backend/python/graph-weatherdata.py`, (err, stdout, stderr) => {
    
            if (err) reject(err)
            if (stdout) {
                if (stdout === "1") resolve("success")
            }
            if (stderr) reject(stderr)
    
        })

    })
}