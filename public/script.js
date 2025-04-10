let voteCounts = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0
};

let savedVotes = localStorage.getItem("votes");
if (savedVotes) {
    voteCounts = JSON.parse(savedVotes);
    updateCounters();
}

function vote(option) {

    ++voteCounts[option];
    document.getElementById("counter" + option).textContent = voteCounts[option];
    localStorage.setItem("votes", JSON.stringify(voteCounts));
}

function updateCounters() {
    for (let option in voteCounts) {
        let el = document.getElementById("counter" + option);
        if (el) {
            el.textContent = voteCounts[option];
        }
    }
}

function resetVotes() {
    for (let option in voteCounts) {
        voteCounts[option] = 0;
    }

    updateCounters();

    localStorage.removeItem("votes");
}