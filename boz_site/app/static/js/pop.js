
function showPopup(message, backgroundColor) {
    // Check if the popup already exists
    let popup = document.getElementById('custom-popup');
    
    // If the popup doesn't exist, create it
    if (!popup) {
        // Create the popup div
        popup = document.createElement('div');
        popup.id = 'custom-popup';
        popup.style.position = 'fixed';
        popup.style.top = '50%';
        popup.style.left = '50%';
        popup.style.transform = 'translate(-50%, -50%)';
        popup.style.padding = '20px';
        popup.style.fontFamily = 'Arial, sans-serif';
        popup.style.fontSize = '16px';
        popup.style.borderRadius = '10px';
        popup.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        popup.style.zIndex = '1000';
        popup.style.opacity = '0';
        popup.style.transition = 'opacity 0.5s ease-in-out';
        popup.style.display = 'none'; // Start hidden

        // Append the popup to the body
        document.body.appendChild(popup);
    }

    // Set the content and background color dynamically
    popup.textContent = message;
    popup.style.backgroundColor = backgroundColor;

    // Show the popup
    popup.style.display = 'block';  
    setTimeout(() => {
            popup.style.display = 'none';
        }, 3000); // Match the transition duration for hiding
}
