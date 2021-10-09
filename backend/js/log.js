const fs = require("fs");

module.exports = function log(message) {

    console.log(message);

    if (typeof message === "string") {
        const stream = fs.createWriteStream("./log.txt", {flags: "a"});
        stream.write(`[${new Date().toLocaleString()}] - " ${message} "\n`);
        stream.end();
    } 
    else if (Array.isArray(message)) {
        let text = "[ ";
        message.forEach((v, i) => {
            if (i != message.length -1) text += `${v}, `;
            else text += `${v} ]`;
        });

        const stream = fs.createWriteStream("./log.txt", {flags: "a"});
        stream.write(`[${new Date().toLocaleString()}] - " ${text} "\n`);
        stream.end();
    }
}