from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import csv
import urllib.parse
import re
from encron.tools import find_file
from app.mydb import mod_list_data, get_index_data, find, check_add

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

from .auto import execute_bash

def fill_result():
    try:
        live_scrap_path = find_file('live_scrap.csv')
    except FileNotFoundError:
        return HttpResponse("File 'live_scrap.csv' not found.", status=404)

    lst = list(get_index_data(live_scrap_path, 0, 0).split(','))
    data = lst
    
    # Process each item in the dataset
    parsed_data = [parse_match_data(match) for match in data]

    # Filter out any None values in case of matching errors
    parsed_data = [match for match in parsed_data if match is not None]
    
    print(f'parsed data: {parsed_data}')
    try:
        live_data_path = find_file('live_data.csv')
        execute_bash("echo '' > {live_data_path}")
    except FileNotFoundError:
        return HttpResponse("File 'live_data.csv' not found.", status=404)

    for match in parsed_data:
        new_match = [match[0], match[1], match[2], match[3]]
        
        if find(live_data_path, match[0], 0) == []:
            print(f'id not found appending data for {match[0]}')
            id_file = find_file('media/shell_scripts/ids.txt')
            with open(id_file, 'r') as f:
                ids = f.read().splitlines()  # makes list of file
            if match[0] in ids:
                print(f'id found appending data for {match[0]}')
                try:
                    mod_list_data(live_data_path, match[0], 2, match[2])
                    mod_list_data(live_data_path, match[0], 3, match[3])
                except:
                    check_add(live_data_path, new_match)
                print('append success..')
            else:
                print(f'id {match[0]} not associated.')
                pass
        else:
            try:
                    mod_list_data(live_data_path, match[0], 2, match[2])
                    mod_list_data(live_data_path, match[0], 3, match[3])
            except:
                    check_add(live_data_path, new_match)
                    print('append success..')
            print('mod success..')

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for this view
class LiveScrapView(View):

    @method_decorator(require_http_methods(["OPTIONS", "POST"]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get the content length
        content_length = int(request.headers.get('Content-Length', 0))

        # Read the data from the request
        post_data = request.body.decode('utf-8')

        # Decode the data
        decoded_data = urllib.parse.unquote(post_data)

        # Parse the data into a list of values
        data_list = decoded_data.split('&')

        # Find the file path for 'live_scrap.csv'
        try:
            live_scrap_path = find_file('live_scrap.csv')
        except FileNotFoundError:
            return HttpResponse("File 'live_scrap.csv' not found.", status=404)

        # Open the CSV file and write data
        with open(live_scrap_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_list)
        
        # Call the fill_result function to handle parsing and modification
        response = fill_result()

        if isinstance(response, HttpResponse):
            return response

        # Send response
        response = HttpResponse("Data received and written to CSV.", status=200)
        response['Access-Control-Allow-Origin'] = '*'  # Allow all origins
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    # Handle OPTIONS request for CORS preflight
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # Adjust as per your requirements
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
