from http.server import BaseHTTPRequestHandler, HTTPServer
import csv
import urllib.parse
from encron.tools import find_file

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
        with open(find_file('live_data.csv'), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_list)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Data received and written to CSV.")

# Server setup
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
