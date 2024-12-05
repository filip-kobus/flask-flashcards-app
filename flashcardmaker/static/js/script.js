document.addEventListener('DOMContentLoaded', function() {
    const groupedBoxesDataElement = document.getElementById('grouped-boxes-data');
    const uploadedImage = document.getElementById('uploaded-image');
    const imageContainer = document.querySelector('#image-container');

    if (!groupedBoxesDataElement || !uploadedImage || !imageContainer) {
        console.error('Required elements not found.');
        return;
    }

    const existingGroupedBoxes = JSON.parse(groupedBoxesDataElement.textContent || '[]');

    if (existingGroupedBoxes.length > 0) {
        displayImage(uploadedImage.src, existingGroupedBoxes);
    }

    function displayImage(src, boxes) {
        uploadedImage.src = src;

        uploadedImage.onload = function () {
            const displayedWidth = uploadedImage.clientWidth;
            const displayedHeight = uploadedImage.clientHeight;

            const originalImage = new Image();
            originalImage.src = src;

            originalImage.onload = function () {
                const originalWidth = originalImage.width;
                const originalHeight = originalImage.height;

                const scaleX = displayedWidth / originalWidth;
                const scaleY = displayedHeight / originalHeight;

                document.querySelectorAll('.bounding-box').forEach(box => box.remove());

                boxes.forEach((box, index) => {
                    createBoundingBox(imageContainer, box, scaleX, scaleY, index);
                });
            };
        };
    }

    function createBoundingBox(container, box, scaleX, scaleY, index) {
        const rect = document.createElement('div');
        rect.classList.add('bounding-box');
        rect.style.left = `${box[0][0] * scaleX}px`;
        rect.style.top = `${box[0][1] * scaleY}px`;
        rect.style.width = `${(box[1][0] - box[0][0]) * scaleX}px`;
        rect.style.height = `${(box[1][1] - box[0][1]) * scaleY}px`;
        rect.setAttribute('data-index', index);

        rect.addEventListener('click', function () {
            rect.classList.toggle('hidden');
        });

        container.appendChild(rect);
    }
});
