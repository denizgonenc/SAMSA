
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

    movieSpeakers = movieChildren[3].children[0].children;

    var speakers = [];
    for (var i = 0; i < movieSpeakers.length; i++) {
        tempSpeaker = movieSpeakers[i].children[0];
        if (tempSpeaker.name !== tempSpeaker.value) {
            var speaker = {
                "old_name": tempSpeaker.name,
                "new_name": tempSpeaker.value
            }
            speakers.push(speaker);
        }
    }

    fetch('/m/' + movieId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "id": movieId,
            "description": movieDescription,
            "speakers": speakers
        })
    })
        .then(response => {
            if (response.status == 404) {
                window.location.href = '/not-found?q=' + searchData;
            } else if (String(response.status).startsWith('2')) {
                response.json()
                    .then(() => {
                        window.location.href = '/database';
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

    fetch('/m/' + movieId, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (response.status == 404) {
                window.location.href = '/not-found?q=' + searchData;
            } else if (String(response.status).startsWith('2')) {
                response.json()
                    .then(() => {
                        window.location.href = '/database';
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
