const searchInput = document.querySelector(".search-input");
const searchButton = document.querySelector(".search-button");


searchButton.addEventListener('click', (event) => {
    var searchData = searchInput.value;
    if (searchData.trim() !== '') {
        fetch('/search?q=' + searchData, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                // console.log('Response from backend:', response);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});