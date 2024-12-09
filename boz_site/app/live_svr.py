from http.server import BaseHTTPRequestHandler, HTTPServer
import csv
import urllib.parse
from encron.tools import find_file
from mydb import *
import re


# Function to parse each string and extract required information
def parse_match_data(match_string):
    # Regular expression to extract data
    pattern = re.compile(r"(.+?)(\d+(?:ST|ND|RD|TH) HALF|HALFTIME)(?: • (\d+)')?#(\d+)\+\d+ more(\d)(\d)")

    # Match the pattern against the string
    match = pattern.match(match_string)

    # Extract relevant data
    if match:
        teams_and_status = match.group(1)
        match_time = match.group(3) if match.group(3) else ''  # Time in the match
        unique_id = match.group(4)
        score_1 = match.group(5)
        score_2 = match.group(6)
        
        # Build the list for this particular match
        return [unique_id, f"{teams_and_status}{match.group(2)}{f' • {match_time}' if match_time else ''}", score_1, score_2]
    else:
        # If no match found, return None or handle error
        return None

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        """Set headers to handle CORS."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """Respond to an OPTIONS request."""
        self._set_headers()

    def do_POST(self):
        """Handle POST request."""
        self._set_headers()

        # Get the content length
        content_length = int(self.headers['Content-Length'])

        # Read the data from the request
        post_data = self.rfile.read(content_length)

        # Decode the data
        decoded_data = urllib.parse.unquote(post_data.decode('utf-8'))

        # Parse the data into a list of values
        data_list = decoded_data.split('&')

        # Open the CSV file and write data
        with open(find_file('live_scrap.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_list)
        
        lst=list(get_index_data('live_scrap.csv',0,0).split(','))
        data=lst
        
        # Process each item in the dataset
        parsed_data = [parse_match_data(match) for match in data]

        # Filter out any None values in case of matching errors
        parsed_data = [match for match in parsed_data if match is not None]

        # Output the parsed data
        for match in parsed_data:
            new_match=[match[0],match[1],match[2],match[3]]
            for x in range(len(new_match)):
                mod_list_data('live_data.csv',match[0],x,match[x],match=new_match)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #self.wfile.write(b"Data received and written to CSV.")

# Server setup
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
