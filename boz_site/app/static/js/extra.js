
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
    
    // Fade in the popup
    setTimeout(() => {
        popup.style.opacity = '1';
    }, 100); // small delay for the fade-in effect

    // Hide the popup after 2.5 seconds
    setTimeout(() => {
        popup.style.opacity = '0';

        // After the fade-out transition ends, hide the popup
        setTimeout(() => {
            popup.style.display = 'none';
        }, 500); // Match the transition duration for hiding
    }, 2500); // Delay for showing the popup (2.5 seconds)
}



function clear_all() {
    localStorage.clear();
    location.reload();
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

function post_home(datas) {
    fetch('/home/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Include CSRF token in header
        },
        body: JSON.stringify(datas)
    });
}


function register() {
    var name = document.getElementById('id_name').value;
    var email = document.getElementById('id_email').value;
    var psk = document.getElementById('psk_log').value; // Semicolon added
    var psk2 = document.getElementById('psk_log2').value;
    var mobile = document.getElementById('m_number').value;

    if (name === "" || email === "" || psk === "" || mobile === "") {
        showPopup("All fields must be filled out",'red');
        return false;
    } else if (psk !== psk2) {
        showPopup('Passwords do not match','red');
    } else {
        var passwd = psk;
        // Create the JSON data object
        var j_feed = {
            'name': name,
            'email': email,
            'psk': passwd, // Use the declared passwd variable
            'mobile': mobile
        };

        // Send the JSON data using fetch or similar
        send_json(j_feed, "http://localhost:8000/register/");
    }
}

function log_in() {
    var mobile = document.getElementById('id_name').value;
    var psk = document.getElementById('psk_log').value;
    if (psk === "" || mobile === "") {
        alert("All fields must be filled out");
        location.reload();
    } else {
        var j_feed = {
            'psk': psk,
            'mobile': mobile
        };
        send_json(j_feed, "http://localhost:8000/login/");
    }
}

function export_data(file, export_data) {
    const targetUrl = `${file}?data=` + encodeURIComponent(export_data);
    window.location.href = targetUrl;
}

function get_export() {
    var urldata = new URLSearchParams(window.location.search);
    var rcd = urldata.get('data');
    alert(rcd);
}

function revo_hid() {
    var h_cont = document.getElementById('hid_cont');
    if (h_cont.style.display === "none") {
        h_cont.style.display = "block";
    } else {
        h_cont.style.display = "none";
    }
}




//var local_net='http://192.168.0.14:8000/'

function page(page_path) {
    //var dev_url = surl;function redirectToPending() {
    // Get the current URL
    const currentUrl = window.location.href;

    // Extract the encrypted text from the URL
    // Assuming the encrypted text is after the last slash
    const parts = currentUrl.split('/');
    const encryptedText = parts[parts.length - 2]; // Adjust based on URL structure

    // Construct the new URL for redirection
    const baseUrl = window.location.origin; // Get the base URL (e.g., http://192.168.0.108:8080)
    const newUrl = `${baseUrl}/pending/${encryptedText}`;

    // Redirect to the new URL
    window.location.href = newUrl;
}



function persistInputValue(id) {
    var inputElement = document.getElementById(id);
    if (!inputElement) {
        console.error(`Element with ID ${id} not found.`);
        alert('you session has expired')
        window.location.href = '/login_page/';
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

// Example usagexxxx
//persistInputValue('usrdata');xx
function syncValues(hiddenInputId, spanId) {
    const hiddenInput = document.getElementById(hiddenInputId);

    if (!hiddenInput) {
        console.error('Hidden input element was not found.');
        //return;
    }

    function updateSpan() {
        const span = document.getElementById(spanId);
        if (span) {
            if (span.textContent !== hiddenInput.value) {
                span.textContent = hiddenInput.value;
            }
        }
    }

    function updateHiddenInput() {
        const span = document.getElementById(spanId);
        if (span) {
            if (hiddenInput.value !== span.textContent) {
                hiddenInput.value = span.textContent;
            }
        }
    }

    // Sync when hidden input value changes
    hiddenInput.addEventListener('input', updateSpan);

    // Sync when span is created or updated
    const observer = new MutationObserver(() => {
        updateSpan();
        const span = document.getElementById(spanId);
        if (span) {
            span.addEventListener('input', updateHiddenInput);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Initial sync
    updateSpan();
};


function set_input_value(id, newValue) {
    let inputElement = document.getElementById(id);
    if (inputElement) {
        inputElement.value = newValue;
    } else {
        console.error(`Element with ID ${id} not found.`);
    }
}

function set_v(obj,val){
    obj.value=val;
}

function send_json(datas, urlp){
    const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value; // Get CSRF token from form
    fetch(urlp, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Include CSRF token in header
        },
        body: JSON.stringify(datas)
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            //console.log(data)
            //alert(JSON.stringify(data))
            if (data.info === 'verified') {
                showPopup('Verified','green')
                window.location.href = `/home/${data.ckey}/`;
            }
            if (data.info === 'reload') {
                window.location.reload();
            }
            if (data.info === 'rej_depo') {
                showPopup('minimum deposit kes10..','red')
            }
            if (data.info === 'wait_depo') {
                showPopup('check your device for prompt','green')
            }
            
            if (data.info === 'rec') {
                showPopup('Bet received success','green')
                window.location.reload();
            }
            if (data.info === 'deny') {
                showPopup('insufficient balance','red')
                window.location.reload();
            }
            if (data.info === 'user already exists') {
                showPopup('User already exists.','red');
                window.location.href = "/login_page/";
            }
            if (data.info === 'Account_created') {
                showPopup('Account has been created, now login.','green');
                window.location.href = '/login_page/';
            }
            if (data.info === 'invalid') {
                showPopup('Invalid credentials','red');
                window.location.href = '/login_page/';
            }
        } else {
            alert('No connection..');
        }
    })
    .catch(error => {
        showPopup('No connection..','red');
        console.log('Error:', error);
    });
}

function toggleBet(button) {
    // Add toggle functionality here
    button.classList.toggle('active');
    // You may need to adjust the class or other functionality depending on your requirements
}

document.querySelectorAll('.hid_g').forEach(button => {
    button.addEventListener('click', function() {
        // Toggle 'active' class on click
        button.classList.toggle('active');
        
        // Check if the button is active
        //console.log(`Button ${button.id} is ${button.classList.contains('active') ? 'active' : 'inactive'}`);
    });
});


//get the id 
// Function to extract ID from a string like "home_odd_5615"
function extractIdFromString(inputString) {
    let parts = inputString.split("_");
    let id = parseInt(parts[parts.length - 1]);
    return id;
}

function place_bet() {
    const storageKey = 'betSlip';
    const odds = document.getElementById('totalOdds').innerText;
    const mobile = document.getElementById('usrdata').value;
    const balance = document.getElementById('balance').textContent;
    const amount = document.getElementById('amount').value;
    const possible = document.getElementById('possible').innerText;

    // Retrieve the picks from localStorage
    var picks = JSON.parse(localStorage.getItem(storageKey)) || {};

    // Create a new object to store the picks with IDs
    var picksWithId = {};

    // Initialize a variable to store the latest time in epoch
    let latestTimeEpoch = 0;

    // Loop through the picks to extract the ID and concatenate with the match name
    let matchIds = [];  
    var matchNames = [];

    // Set to store unique match IDs and names
    let matchIdsSet = new Set();
    let matchNamesSet = new Set();

    for (const matchName in picks) {
        const buttons = document.querySelectorAll('button');
        //let matchNames = [];
        let matchId = null;
        //let matchTime = null;

        buttons.forEach(button => {
            if (button.classList.contains('active')) {
                matchId = extractIdFromString(button.id);
                matchIds.push(matchId);

                if (matchId) {
                    // Store unique match IDs and names
                    matchIdsSet.add(matchId);
                    matchNamesSet.add(matchName);

                // Extract the match time from the parent container
                const matchContainer = button.closest('.button-container');
                const timeElement = matchContainer.querySelector('tm');
                if (timeElement) {
                    const timeText = timeElement.textContent.trim().split(':')[1]; // Extract "22:00"
                    const tm = `${timeText}:${timeElement.textContent.trim().split(':')[2]}`
                    console.log(tm)
                    
                    // Convert time to epoch assuming it's in the future
                    const [hours, minutes] = tm.split(':').map(Number);
                    const now = new Date();
                    
                    // Create a Date object for the match time
                    let matchDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, 0);
                    
                    // If the match time has already passed today, assume it's the next day
                    if (matchDate.getTime() < now.getTime()) {
                        matchDate.setDate(now.getDate() + 1); // Move to the next day
                    }

                    const matchTimeEpoch = Math.floor(matchDate.getTime() / 1000);

                    // Debugging output
                    //console.log(Match: ${matchName}, Match ID: ${matchId}, Match Time Epoch: ${matchTimeEpoch});

                    // Update the latestTimeEpoch if this match is later
                    if (matchTimeEpoch > latestTimeEpoch) {
                        latestTimeEpoch = matchTimeEpoch;
                    }
                }

                
            }
            //if (matchId !== null) {
            
                //const key = `${matchId}_${matchName}`;
                //if (!picksWithId[key] && picks[matchName]) {
                    //picksWithId[key] = picks[matchName];
                    //console.log(`Added to picksWithId: ${key} ->`, picks[matchName]);
                   // }
                }//}
        });
       
       
    }

     // Log unique match IDs and names
     //console.log("Unique Match IDs:", Array.from(matchIdsSet));
     //console.log("Unique Match Names:", Array.from(matchNamesSet));
 
     // Convert sets to arrays for iteration
     const matchIdsArray = Array.from(matchIdsSet);
     const matchNamesArray = Array.from(matchNamesSet);
 
     // Ensure both arrays have the same length
     if (matchIdsArray.length !== matchNamesArray.length) {
         console.error("Mismatch between match IDs and names length.");
         return;
     }
 
     // Combine unique IDs and names
     let combinedPicks = {};
     matchIdsArray.forEach((matchId, index) => {
         const matchName = matchNamesArray[index];
         const key = `${matchId}_${matchName}`;
         if (picks[matchName]) {
             // Only add the pick if the match ID and name combination is valid
             const pick = picks[matchName];
             if (pick) {
                 combinedPicks[key] = pick;
             }
         }
     });
 
     // Debugging logs
     //console.log("combinedPicks:", combinedPicks);
    

    // Calculate max_time by adding 2 hours (7200 seconds) to the latest time in epoch
    const maxTime = latestTimeEpoch + 7200; // Add 2 hours

    // Debugging logs
    //console.log("latestTimeEpoch:", latestTimeEpoch);
    //console.log("maxTime:", maxTime);

    // Alert showing the picks with IDs (for debugging purposes)
    //alert(JSON.stringify(combinedPicks)); // Optional: Remove this line in production

    // Continue with your existing logic
    if (odds === '1.00') {
        showPopup("No selections made ..");
        setTimeout(window.location.reload(),2000);
    } else if (parseFloat(balance) < amount) {
        //alert(`${balance}` < `${amount}`);
        showPopup("Insufficient balance",'red');
        window.location.reload();
    } else if (amount < 2) {
        showPopup("Amount should be at least KES 2.0",'red');
        location.reload();
    } else if (parseFloat(possible) > 2000000) {
        set_input_value('possible', '2000000');
        set_input_value('totalOdds', 'infinity');
        showPopup("Maximum bet limit reached",'gray');
    } else {
        var j_feed = {
            'picks': JSON.stringify(combinedPicks),
            'odds': odds,
            'mobile': mobile,
            'possible': possible,
            'bet_amount': amount,
            'max_time': maxTime // Include max_time in the JSON payload
        };

        // Debugging log
        //console.log("j_feed:", j_feed);

        send_json(j_feed, "/slip/");
    }
}

//up 3

    


