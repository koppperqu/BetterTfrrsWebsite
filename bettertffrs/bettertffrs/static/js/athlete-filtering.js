document.addEventListener('DOMContentLoaded', function () {
    var searchBox = document.getElementById('athlete-search-box')
    var athleteContainer = document.getElementById('athlete-container')
    var athleteDivs = athleteContainer.getElementsByClassName('athlete')
    var noAthletesDiv = document.getElementById("no-matching-athletes")

    searchBox.addEventListener('input', function () {
        var matches = 0
        var searchTerm = searchBox.value.toLowerCase()
        for (var i = 0; i < athleteDivs.length; i++) {
            var athleteName = athleteDivs[i].getElementsByTagName("a")[0].textContent.toLowerCase()
            if (athleteName.includes(searchTerm)) {
                athleteDivs[i].classList.remove('d-none')
                athleteDivs[i].getElementsByTagName("a")[0].classList.remove('d-none')
                matches++
            } else {
                athleteDivs[i].classList.add('d-none')
                athleteDivs[i].getElementsByTagName("a")[0].classList.add('d-none')
            }
        }
        if (matches==0) {
            noAthletesDiv.innerHTML = "<h2>There are no matching athletes</h2>"
        }
        else {
            noAthletesDiv.innerHTML = ""
        }
    });
});
