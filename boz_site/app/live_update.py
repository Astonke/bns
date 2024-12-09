from auto import *
from time import sleep
from mydb import get_index_data, count_rows,remove_if_started,update_pending_slips

def init_odi():
    init(background=False)
    go('https://odibets.com/live/')
    find_click('//*[@id="menu-list"]/li[2]/a')

def inject_js():
    script = """
    // Select all elements with the class name 'info'
    var elements = document.querySelectorAll('.info');

    var sdata = [];

    // Iterate over the NodeList and push each element's content to the array
    elements.forEach(function(element) {
        sdata.push(element.textContent);
    });

    // Function to send data to server
    function sendDataToServer(data) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://bozbet.xyz', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        // Handle the response
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log('Data sent successfully:', xhr.responseText);
                } else {
                    console.log('Failed to send data:', xhr.status, xhr.statusText);
                }
            }
        };

        xhr.send('data=' + encodeURIComponent(JSON.stringify(data)));
    }

    // Send the collected data to the server
    sendDataToServer(sdata);
    """
    exec(script)

while True:
    try:
        # Start first instance
        init_odi()
        # Inject JavaScript
        inject_js()
        # Reload the page and wait for it to load
        refresh()
        sleep(5)
        # Inject JavaScript again after the page reload
        inject_js()
        # Next update should be made after 5 seconds
        sleep(5)
        #remove_if_started()
        update_pending_slips()
    except Exception as e:
        print(f"An error occurred: {e}")
        sleep(10)  # Wait before retrying
