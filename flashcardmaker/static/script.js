document.addEventListener('DOMContentLoaded', function() {
    const existingGroupedBoxes = JSON.parse(document.getElementById('grouped-boxes-data').textContent || null);

    if (existingGroupedBoxes) {
        displayImage(document.getElementById('uploaded-image').src, existingGroupedBoxes);
    }

function displayImage(src, boxes) {
    const imgContainer = document.querySelector('#image-container');
    const imgElement = document.querySelector('#uploaded-image');

    if (!imgElement) {
        return;
    }

    // Update img element src
    imgElement.src = src;

    imgElement.onload = function () {
        // Get the actual dimensions of the displayed image
        const displayedWidth = imgElement.clientWidth;
        const displayedHeight = imgElement.clientHeight;

        // Get the original dimensions of the image
        const originalImage = new Image();
        originalImage.src = src;
        originalImage.onload = function () {
            const originalWidth = originalImage.width;
            const originalHeight = originalImage.height;

            const scaleX = displayedWidth / originalWidth;
            const scaleY = displayedHeight / originalHeight;

            document.querySelectorAll('.bounding-box').forEach(box => box.remove());

            boxes.forEach((box, index) => {
                const rect = document.createElement('div');
                rect.classList.add('bounding-box');
                rect.style.left = `${box[0][0] * scaleX}px`;
                rect.style.top = `${box[0][1] * scaleY}px`;
                rect.style.width = `${(box[1][0] - box[0][0]) * scaleX}px`;
                rect.style.height = `${(box[1][1] - box[0][1]) * scaleY}px`;
                rect.setAttribute('data-index', index);
                rect.addEventListener('click', function() {
                    rect.classList.toggle('hidden');
                });
                imgContainer.appendChild(rect);
            });


        };
    };
}