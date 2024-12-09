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
                if (button.textContent.trim() === betSlip[matchName]) {
                    button.classList.add('active');
                }
            });
        }

        // Add click event listener to each button
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                // If clicked button is already active, deactivate it
                if (button.classList.contains('active')) {
                    button.classList.remove('active');
                    delete betSlip[matchName];
                } else {
                    // Activate the clicked button and deactivate others
                    buttons.forEach(btn => btn.classList.remove('active'));
                    button.classList.add('active');
                    betSlip[matchName] = button.textContent.trim();
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
        totalOdds *= parseFloat(betSlipSummary[match]);
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
            odds.classList.add('odds_style')
            odds.textContent = `${betSlipSummary[match]}`;
            matchContainer.appendChild(odds);

            const removeButton = document.createElement('button');
            removeButton.textContent = '-';
            removeButton.classList.add('to_remove');
            removeButton.addEventListener('click', function() {
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
document.getElementById('checkBetSlip').addEventListener('click', ()=>{
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
           <lal  id='ps_label'>win:</lal><br>
           <span id="possible">0.00</span>
           <button id="clearBetSlip">Clear Bet Slip</button>
           <button id="place_bet" class="submit-btn" onclick="place_bet()">Place Bet</button>
           <button id="account_amount" class="deposit_check">Balance: $<span id="balance">0.00</span></button>
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
    const popup =document.getElementById('popup')
    popup.style.display = 'block';

    // Close the popup when the close button is clicked
    document.getElementById('closePopup').addEventListener('click', function() {
        window.location.reload()
        popup.style.display = 'none';
        document.body.removeChild(popup); // Remove the popup HTML from the DOM
        
    });

    // Clear the entire bet slip when the clear button is clicked
    document.getElementById('clearBetSlip').addEventListener('click', function() {
        localStorage.removeItem(storageKey);
        document.getElementById('checkBetSlip').click(); // Refresh the popup content
    });
    //update popup
    updatePopupContent();
});


  
    //fast check selections
    // Add event listener for mouseover event on the whole document
  document.addEventListener('mouseover', function() {
    // Execute the script when the mouseover event is triggered
    update_sel_bt()

  });

  document.addEventListener('scroll', function() {
    // Execute the script when the mouseover event is triggered
    update_sel_bt()

  });


function count_green_Buttons() {
    // Get all buttons in the document
    var buttons = document.querySelectorAll('button');
    
    // Initialize counter for green buttons
    var greenButtonCount = 0;
    
    // Loop through each button
    buttons.forEach(function(button) {
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
  
  
  function update_sel_bt(){
    var selections=count_green_Buttons()-1
    var slip_button=document.getElementById('checkBetSlip');
    slip_button.textContent=selections;
  }


function clear_all() {
    localStorage.clear();
    location.reload()
}

function unshow(){
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
    }

 // Display random picks in a popup
 function display_pop_up(datax) {
    var popup = document.getElementById('popup');
    var picks = document.getElementById( "picks_c" );
    picks.textContent = datax;
    popup.style.display = 'block';
}

function post_home(datas){
    fetch('/home/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Include CSRF token in header
        },
        body: JSON.stringify(datas)
    })
    
}

  function register() {
    var name = document.getElementById('id_name').value;
    var email = document.getElementById('id_email').value;
    var psk = document.getElementById('psk_log').value; // Semicolon added
    var psk2 = document.getElementById('psk_log2').value;
    var mobile = document.getElementById('m_number').value;
    
    if (name == "" || email == "" || psk == "" || mobile == "") {
      alert("All fields must be filled out");
      return false;
    } else if (psk != psk2) {
      alert('Passwords do not match');
    } else {  
    if (psk === psk2) {
      console.log('password_match..');
      var passwd = psk;
    // Create the JSON data object
    var j_feed = {
        'name': name,
        'email': email,
        'psk': passwd, // Use the declared passwd variable
        'mobile': mobile
      };
    
      // Alert or send the JSON data using fetch or similar
      // (Security reminder: Hash passwords before sending)
      //alert(JSON.stringify(j_feed));
      send_json(j_feed,"http://localhost:8000/register/")

    } else {
      alert('passwords don\'t match');
      location.reload()
    };}
  }

  function log_in(){
    var mobile = document.getElementById('id_name').value;
    var psk = document.getElementById('psk_log').value;
    if (psk == "" || mobile == "") {
        alert("All fields must be filled out");
        location.reload()
    }
    else{
        // Send the JSON data to server for authentication
        // and get back a response in JSON format
        var j_feed = {
            'psk': psk, // Use the declared passwd variable
            'mobile': mobile
          };
          send_json(j_feed,"http://localhost:8000/login/") 
    }
  }

function export_data(file,export_data) {
    const dataToSend = export_data; // Replace with your actual data
    const targetUrl = `${file}?data=`+ encodeURIComponent(dataToSend);
    window.location.href = targetUrl;
  }

function get_export(){
     //get exported data
     var urldata = new URLSearchParams(window.location.search);
     var rcd = urldata.get('data');
     alert(rcd)
}


function revo_hid(){
    var h_cont=this.getElementById('hid_cont');
    if(h_cont.style.display=="none"){
        h_cont.style.display="block";
    }else{
        h_cont.style.display="none"
    }
}
  
function rev_hid(clickedContainer) {
    // Get the hidden element with ID "hid_cont" within the clicked container
    const hiddenElement = clickedContainer.querySelector("#hid_cont");
  
    // Check if the hidden element exists
    if (hiddenElement) {
      // Toggle the visibility of the hidden element (show if hidden, hide if visible)
      hiddenElement.classList.toggle("hid_cont"); // Assuming "hid_cont" class hides the element
    } else {
      console.log("No element with ID 'hid_cont' found within clicked container.");
    }
  }
  
  

  function page(page_path) {
    // Define dev_url within the function
    var dev_url = 'http://127.0.0.1:8000/';
  
    // Check if page_path is valid (optional)
    if (!page_path || typeof page_path !== 'string') {
      console.error('Invalid page path provided');
      return;
    }else{
        window.location.href = dev_url + page_path;
    }
}
function persistInputValue(id) {
    let inputElement = document.getElementById(id);
    if (!inputElement) {
        console.error(`Element with ID ${id} not found.`);
        return;
    }

    // Function to update the input value in localStorage
    function updateLocalStorage() {
        if (inputElement.value) {  // Only update if the input value is not empty
            localStorage.setItem(id, inputElement.value);
        }
    }

    // Load the saved value from localStorage
    let savedValue = localStorage.getItem(id);
    if (savedValue !== null) {
        inputElement.value = savedValue;
    }

    // Event listener to update localStorage whenever the input value changes
    inputElement.addEventListener('input', updateLocalStorage);

    // Ensure the input value is not empty, otherwise load the last saved value
    window.addEventListener('load', () => {
        if (!inputElement.value && savedValue !== null) {
            inputElement.value = savedValue;
        }
    });
}

// Example usage
persistInputValue('usrdata');

function set_input_value(id, newValue) {
    let inputElement = document.getElementById(id);
    if (inputElement) {
        inputElement.value = newValue;
    } else {
        console.error(`Element with ID ${id} not found.`);
    }
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
        odds.classList.add('odds_style')
        odds.textContent = `${betSlipSummary[match]}`;
        matchContainer.appendChild(odds);

        const removeButton = document.createElement('button');
        removeButton.textContent = '-';
        removeButton.classList.add('to_remove');
        removeButton.addEventListener('click', function() {
            delete betSlipSummary[match];
            localStorage.setItem(storageKey, JSON.stringify(betSlipSummary));
            updatePopupContent(); // Update the popup content after removing the selection
        });
        matchContainer.appendChild(removeButton);

        betSlipContainer.appendChild(matchContainer);
    }
}

});
