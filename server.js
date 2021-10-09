const express = require("express");
const { exec } = require("child_process");
const log = require("./backend/js/log");
const getWeatherData = require("./backend/js/getWeatherData")

const app = express();
const port = 5000;


app.use(express.static(`${__dirname}/frontend/public`));

app.get("/", (req, res) => {
    res.sendFile(`${__dirname}/frontend/index.html`);
});


app.get("/weather", (req, res) => {
    res.sendFile(`${__dirname}/frontend/weather.html`)
});


app.get("/log", (req, res) => {
    res.sendFile(`${__dirname}/log.txt`);
});

app.get("/get-weatherdata", async (req, res) => {
    graph = await getWeatherData()
    if (graph === "success") {
        res.status(200).send("Graph created successfully")
    } else {
        res.status(500).send("Something went wrong creating graph")
    }
})

app.listen(port, () => log(`Server is listening on port ${port}`));


// Check for new weather data every updateInterval minutes
const updateInterval = 4;
let lastUpdate = -1; // Time of last update in minutes (0-59)

function callWebScraper() {
    exec(`py ./backend/python/ws-weatherdata.py ${lastUpdate}`, (err, stdout, stderr) => {
        log("--- Calling webscraper");

        if (err) log(err);
        if (stdout) {
            stdoutf = stdout.split("\r\n");
            log(stdoutf);
            lastUpdate = stdoutf[0];
        }
        if (stderr) log(stderr);

    });
}

callWebScraper();
setInterval(callWebScraper, 60000 * updateInterval);