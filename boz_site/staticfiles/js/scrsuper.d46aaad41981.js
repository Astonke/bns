document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('.button-container');
    const storageKey = 'betSlip';
    let betSlip = JSON.parse(localStorage.getItem(storageKey)) || {};

    containers.forEach(container => {
        const span = container.querySelector('span');
        const buttons = container.querySelectorAll('button');
        const matchName = span.textContent.trim();

        // Set initial state from localStorage
        if (betSlip[matchName]) {
            buttons.forEach(button => {
                if (button.textContent.trim() === betSlip[matchName].odds) {
                    button.classList.add('active');
                }
            });
        }

        // Add click event listener to each button
        buttons.forEach(button => {
            button.addEventListener('click', function () {
                const label = button.previousElementSibling?.textContent.trim() || ''; // Get the previous sibling label, if exists

                // If clicked button is already active, deactivate it
                if (button.classList.contains('active')) {
                    button.classList.remove('active');
                    delete betSlip[matchName];
                } else {
                    // Activate the clicked button and deactivate others
                    buttons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    betSlip[matchName] = {
                        odds: button.textContent.trim(),
                        label: label
                    };
                }
                // Update localStorage
                localStorage.setItem(storageKey, JSON.stringify(betSlip));
            });
        });
    });

    // Function to calculate total odds
    function calculateTotalOdds(betSlipSummary) {
        let totalOdds = 1;
        for (const match in betSlipSummary) {
            totalOdds *= parseFloat(betSlipSummary[match].odds);
        }
        return totalOdds;
    }

    // Function to update the popup content
    function updatePopupContent() {
        const betSlipSummary = JSON.parse(localStorage.getItem(storageKey)) || {};

        // Calculate total odds
        const totalOdds = calculateTotalOdds(betSlipSummary);

        // Update total odds display
        const totalOddsElement = document.getElementById('totalOdds');
        if (totalOddsElement) {
            totalOddsElement.textContent = `${totalOdds.toFixed(2)}`;
        }

        // Update bet slip container
        const betSlipContainer = document.getElementById('betSlipContainer');
        if (betSlipContainer) {
            betSlipContainer.innerHTML = '';
            for (const match in betSlipSummary) {
                const matchContainer = document.createElement('div');
                matchContainer.classList.add('match-container');

                const matchName = document.createElement('span');
                matchName.textContent = match;
                matchContainer.appendChild(matchName);

                const odds = document.createElement('span');
                odds.classList.add('odds_style');
                odds.textContent = `${betSlipSummary[match].odds}`;
                matchContainer.appendChild(odds);


                const label = document.createElement('span');
                label.classList.add('label_style');
                label.textContent = `(${betSlipSummary[match].label})`; // Display the label
                matchContainer.appendChild(label);

                const removeButton = document.createElement('button');
                removeButton.textContent = '-';
                removeButton.classList.add('to_remove');
                removeButton.addEventListener('click', function () {
                    delete betSlipSummary[match];
                    localStorage.setItem(storageKey, JSON.stringify(betSlipSummary));
                    updatePopupContent(); // Update the popup content after removing the selection
                });
                matchContainer.appendChild(removeButton);

                betSlipContainer.appendChild(matchContainer);
            }
        }
    }

    //picks popup handler here 
    //create popup with all data collected
    document.getElementById('checkBetSlip').addEventListener('click', () => {
        const betSlipSummary = JSON.parse(localStorage.getItem(storageKey)) || {};

        // Create the popup HTML dynamically
        const popupHtml = `
        <div id="popup" class="popup">
            <div class="popup-content">
                <br><br>
                <h2>Bet Slip</h2>
                <button id="closePopup" class="minimize">-</button>
                <div id="betSlipContainer" class="bet-slip-container"></div><br>
                <div id="totalOdds">0.00</div><br>
                <input placeholder='$ Amount' id='amount' type='textarea' maxlength='6'><br>
                <label id='ps_label'>win:</label><br>
                <span id="possible">0.00</span>
                <button id="clearBetSlip">Clear Bet Slip</button>
                <button id="place_bet" class="submit-btn" onclick="place_bet()">Place Bet</button>
                <button id="account_amount" class="deposit_check">Balance: $<span id="balance">{{ balanc|safe }}</span></button>
            </div>
            <style>
            body{
                background-color:black;
            }
            main{
                display:none;
            }
            
            </style>
        </div>
        `;
        // Insert the popup HTML into the document body
        document.body.insertAdjacentHTML('beforeend', popupHtml);

        // Show the popup
        const popup = document.getElementById('popup')
        popup.style.display = 'block';

        // Close the popup when the close button is clicked
        document.getElementById('closePopup').addEventListener('click', function () {
            //window.location.reload()
            popup.style.display = 'none';
            document.body.removeChild(popup); // Remove the popup HTML from the DOM

        });

        // Clear the entire bet slip when the clear button is clicked
        document.getElementById('clearBetSlip').addEventListener('click', function () {
            localStorage.removeItem(storageKey);
            document.getElementById('checkBetSlip').click(); // Refresh the popup content
            setTimeout(() => window.location.reload(), 2000);

        });
        //update popup
        updatePopupContent();
    });

    //fast check selections
    // Add event listener for mouseover event on the whole document
    document.addEventListener('mouseover', function () {
        // Execute the script when the mouseover event is triggered
        update_sel_bt()

    });

    document.addEventListener('scroll', function () {
        // Execute the script when the mouseover event is triggered
        update_sel_bt()

    });

//home btnn
const mainButton = document.getElementById('menu');
    const circleMenu = document.getElementById('circleMenu');

    mainButton.addEventListener('click', function () {
        circleMenu.classList.toggle('visible');
    });

    // Hide the menu when the cancel button is clicked
    const cancelButton = circleMenu.querySelector('.cancel-button');
    cancelButton.addEventListener('click', function () {
        circleMenu.classList.remove('visible');
    });

//


    function count_green_Buttons() {
        // Get all buttons in the document
        var buttons = document.querySelectorAll('button');

        // Initialize counter for green buttons
        var greenButtonCount = 0;

        // Loop through each button
        buttons.forEach(function (button) {
            // Get the background color of the button
            var computedStyle = window.getComputedStyle(button);
            var backgroundColor = computedStyle.backgroundColor;

            // Check if the background color is green
            if (backgroundColor === 'rgb(0, 128, 0)') {
                greenButtonCount++;
            }
        });

        return greenButtonCount;
    }


    function update_sel_bt() {
        var selections = count_green_Buttons()
        var slip_button = document.getElementById('checkBetSlip');
        slip_button.textContent = selections;
    }


    function clear_all() {
        localStorage.clear();
        location.reload()
    }

    function unshow() {
        const popup = document.getElementById('popup');
        popup.style.display = 'none';
    }

    // Display random picks in a popup
    function display_pop_up(datax) {
        var popup = document.getElementById('popup');
        var picks = document.getElementById("picks_c");
        picks.textContent = datax;
        popup.style.display = 'block';
    }

})