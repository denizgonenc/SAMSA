const popupImage = document.querySelector(".popup-image");
const graphs = document.getElementsByClassName("graph");

popupImage.addEventListener('click', closePopup);

for (var i = 0; i < graphs.length; i++) {
    graphs.item(i).addEventListener('click', popupGraph);
    graphs.item(i).addEventListener("dragstart", function (event) { event.preventDefault(); })

}

function popupGraph(event) {
    var graph = event.target.closest('img');
    popupImage.src = graph.src;
    popupImage.style.display = 'block';
}

function closePopup() {
    popupImage.style.display = 'none';
    popupImage.src = '';
}
