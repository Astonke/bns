# Script Execution
from auto import *
from time import sleep
from mydb import get_index_data, count_rows


def init_odi():
    init(background=True)
    go('https://odibets.com/live/')
    #find_click('//*[@id="menu-list"]/li[2]/a')

#start first instance
init_odi()    

def console():
    script = """
// Select all elements with the class name 'info'
var elements = document.querySelectorAll('.info');

var sdata=[]

// Iterate over the NodeList and log each element's content
elements.forEach(function(element) {
    sdata.push(element.textContent);
    //console.log(element.textContent);  // Log the text content of each element
});


// Function to send data to server
function sendDataToServer(data) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://bozbet.xyz/api/live-scrap/', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Handle the responsex
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log('Data sent successfully:', xhr.responseText);
            } else {
                console.log('Failed to send data:', xhr.status, xhr.statusText);
            }
        }
    };

    xhr.send(data);
}

// Send the collected data to the server
sendDataToServer(sdata);
"""
    exec(script)
    #print('data sent to server success')
# (Optional) Get data returned by the script
    #result = driver.execute_script("return Array.from(document.querySelectorAll('.info')).map(el => el.textContent)")

    #print(result)
    
    sleep(3)
    
'''    
i = 2
f_len = count_rows('today.csv')
for val in range(0,f_len-3):
    try:
        gid = get_index_data('today.csv', 0, i)
        
            
    except IndexError:
        print("gap")
    i += 1

'''
console()
