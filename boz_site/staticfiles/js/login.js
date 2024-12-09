function send_json(datas, urlp) {
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
                //console.log(data);
                //alert(JSON.stringify(data));
                if (data.info === 'verified') {
                    alert('Verified')
                    window.location.href = `/home/${data.ckey}/`;
                }
                if (data.info === 'user already exists') {
                    alert('User already exists.');
                    window.location.href = "/login_page/";
                }
                if (data.info === 'Account_created') {
                    alert('Account has been created, now login.');
                    window.location.href = '/login_page/';
                }
                if (data.info === 'invalid') {
                    alert('Invalid credentials');
                    window.location.href = '/login_page/';
                }
            } else {
                alert('No connection.');
            }
        })
        .catch(error => {
            alert('No connection.');
            console.log('Error:', error);
        });
}



function log_in(surl) {
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
        send_json(j_feed, surl+"login/");
    }
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
        alert("All fields must be filled out");
        return false;
    } else if (psk !== psk2) {
        alert('Passwords do not match');
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
        send_json(j_feed, surl+"register/");
    }
}