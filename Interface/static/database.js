
const saveButtons = document.getElementsByClassName('movie-btn green');
const deleteButtons = document.getElementsByClassName('movie-btn red');


for (var i = 0; i < saveButtons.length; i++) {
    saveButtons.item(i).addEventListener('click', save_);
}

for (var i = 0; i < deleteButtons.length; i++) {
    deleteButtons.item(i).addEventListener('click', delete_);
}


function save_(event) {
    movieRow = event.target.closest('tr');
    movieChildren = movieRow.children;

    movieId = movieChildren[0].innerHTML;
    movieDescription = movieChildren[2].children[0].value;

    // TODO: Don't forget to add the speaker changing parts.

    a = JSON.stringify({
        "movie": {
            "id": movieId,
            "description": movieDescription
        }
    });
    console.log(a);

    fetch('/m/' + movieId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "id": movieId,
            "description": movieDescription
        })
    })
        .then(response => {
            if (response.status == 404) {
                window.location.href = '/not-found?q=' + searchData;
            } else if (String(response.status).startsWith('2')) {
                response.json()
                    .then((json) => {
                        console.log(json);
                        // window.location.href = '/database';
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

function delete_(event) {
    movieRow = event.target.closest('tr');
    movieChildren = movieRow.children;

    movieId = movieChildren[0].innerHTML;

    // fetch('/m/' + movieId, {
    //     method: 'DELETE',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // })
    //     .then(response => {
    //         if (response.status == 404) {
    //             window.location.href = '/not-found?q=' + searchData;
    //         } else if (String(response.status).startsWith('2')) {
    //             response.json()
    //                 .then(() => {
    //                     window.location.href = '/database';
    //                 })
    //                 .catch((error) => {
    //                     console.error(error);
    //                 });
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //     });
}
