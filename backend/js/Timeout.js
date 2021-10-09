
module.exports = function* Timeout(interval) { // Calculates times along given interval for consistent loops
    let iteration = 1;
    let startTime = Date.now();

    let nextTime = startTime + (interval * iteration);

    while (true) {
        yield nextTime;
        iteration++;
        nextTime = startTime + (interval * iteration);
    }
}