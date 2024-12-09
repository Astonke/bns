// script.js

document.addEventListener('DOMContentLoaded', function () {
    const mainButton = document.getElementById('mainButton');
    const circleMenu = document.getElementById('circleMenu');

    mainButton.addEventListener('click', function () {
        circleMenu.classList.toggle('visible');
    });

    // Hide the menu when the cancel button is clicked
    const cancelButton = circleMenu.querySelector('.cancel-button');
    cancelButton.addEventListener('click', function () {
        circleMenu.classList.remove('visible');
    });
});
