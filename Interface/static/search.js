
const searchInput = document.querySelector(".search-input");
const searchButton = document.querySelector(".search-button");

searchButton.addEventListener('click', (event) => {
    var searchData = searchInput.value;
    if (searchData.trim() !== '') {
        fetch('/search?q=' + searchData, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (response.status == 404) {
                    window.location.href = '/not-found?q=' + searchData;
                } else if (String(response.status).startsWith('2')) {
                    response.json()
                        .then((json) => {
                            movieUrl = '/movies/' + String(json[0].id);
                            window.location.href = movieUrl;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});


// It is used to trigger searchButton when `enter` key pressed.
searchInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        searchButton.click();
    }
});

// IT IS NOT USED.
function showCloseSearchList(results, open = false) {
    searchListOpened = searchInput.getAttribute("aria-haspopup");
    if (searchListOpened == false && open == true) {
        searchInput.getAttribute("aria-haspopup") = true;
        // TODO add results.
    } else if (searchListOpened == true && open == false) {
        searchInput.getAttribute("aria-haspopup") = false;
        // TODO add results.
    } else { }
}