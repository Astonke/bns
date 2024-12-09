import csv
import os
from encron.tools import find_file
import json
from .my_func import generate_odd

def cap_odd(value,max_threshold):
    """
    Returns the float value if it is less than the max_threshold.
    Otherwise, returns the max_threshold.

    Args:
        value (float): The input float value to be capped.
        max_threshold (float): The maximum allowable threshold.

    Returns:
        float: The capped value.
    """
    return value if value <= max_threshold else generate_odd(1.15,max_threshold)


def cap_float(value,max_threshold):
    """
    Returns the float value if it is less than the max_threshold.
    Otherwise, returns the max_threshold.

    Args:
        value (float): The input float value to be capped.
        max_threshold (float): The maximum allowable threshold.

    Returns:
        float: The capped value.
    """
    return value if value <= max_threshold else max_threshold

client_file=find_file('clients.csv')
"""
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)"""


def write_csv(file_path, data):
    """
    Write data to a CSV file.
    :param file_path: Path to the target CSV file
    :param data: List of lists representing rows in the CSV
    """
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)  # Write all rows from the list `data`

"""
def read(file_path):
    # Open the file and read the contents
    if not isinstance(file_path, str):
        raise ValueError("Expected file path to be a string")

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data"""

import sys

# Set the field size limit to a higher value
#csv.field_size_limit()

def read(file_path):
    if not isinstance(file_path, str):
        raise ValueError("Expected file path to be a string")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data
#x

def insert(filename, data):
    with open(filename, 'a', newline='') as csvfile:  # Changed 'w' to 'a' to append data
        writer = csv.writer(csvfile)
        for d in data:
            writer.writerow(d)

def wipe(file_path):
    os.remove(file_path)

def find(file, search_term, column_index=0):
    matching_rows = []
    for row in read(file):
        if 0 <= column_index < len(row) and row[column_index] == search_term:
            matching_rows.append(row)
    return matching_rows

def add_list(file, lst):
    with open(file, "a", newline="") as csvfile:  # Changed 'w' to 'a' to append data
        writer = csv.writer(csvfile)
        for l in lst:
            writer.writerow(l)

def replace_data(file, old_data, new_data):
    data = read(file)
    for row in data:
        if row == old_data:
            data[data.index(row)] = new_data
    wipe(file)
    write_csv(file, data[0])  # Add headers back
    add_list(file, data[1:])  # Append the rest of the data

# Create your tests here.
# from mydb1 import *

def add_to_db(file, data):
    insert(file, [data])  # Wrapping data in a list to make it a list of lists

def auth_user(mobile_no, password):
    m_list = find(client_file, mobile_no, column_index=3)  # Mobile is in the 4th column
    if m_list:
        return m_list[0][2] == password  # Password is in the 3rd column
    else:
        return False

def check_add(file, data):
    if not isinstance(file, str):
        raise ValueError("Expected file path to be a string")

    #print(f"Checking file: {file}")
    #print(f"Data to check: {data}")

    file_data = read(file)
    match = False
    for d in file_data:
        if d == data:
            match = True
            break

    if not match:
        #print(f"Data not found, adding to database.")
        add_to_db(file, data)
    else:
        print(f"Data already exists.")


def get_balance(mobile_no):
    with open(client_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == mobile_no:  # Assuming mobile_no is in the 4th column
                return row[4]  # Assuming balance is in the 5th column
    return None  # Return None if no matching mobile number is found



slips_file=find_file('pending_slips.csv')

def update_balance(mobile, new_balance=None, diff=None):
    # Read the CSV data
    with open(client_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    updated = False
    
    # Iterate over each row in the CSV
    for row in data:
        if row[3] == mobile:  # Check if the mobile number matches
            #print(f"Original row: {row}")  # Debug: print the original row

            # If diff is provided, calculate the new balance
            if diff is not None:
                current_balance = float(row[4])  # Current balance
                new_balance = current_balance - diff
                row[4] = str(new_balance)  # Update the balance in the row
                updated = True
            # If new_balance is provided, set it directly
            elif new_balance is not None:
                row[4] = str(float(new_balance))
                updated = True

            #print(f"Updated row: {row}")  # Debug: print the updated row
            break

    # If an update was made, write back to the CSV
    if updated:
        with open(client_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        #print(f"Balance updated successfully for mobile number {mobile}.")
    else:
        print(f"Mobile number {mobile} not found.")

# Example usage:
#update_balance('0702162058', diff=15)  # Deduct 15 from the current balance
# update_balance('0702162058', new_balance='85.0')  # Set balance to 85 directly

import csv
import json

def get_client_slips(mobile, db_file=slips_file):
    with open(db_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        slips = []
        for row in reader:
            if row[0] == mobile:
                # row format: mobile, possible_win, matches, total_odds
                possible_win = row[1]
                matches = json.loads(row[2])
                total_odds = row[3]
                f_status=row[-1]
                slip = {
                    'possible_win': possible_win,
                    'total_odds': total_odds,
                    'final':f_status,
                    'matches': [
                        {
                            'match': match,
                            'odds': details['odds'],
                            'label': details['label'],
                            'status': details.get('status', 'pending')  # Ensure default 'pending' if not present
                        } for match, details in matches.items()
                    ]
                }
                slips.append(slip)

    return slips 


def mod_list_data(file_name, search_term, index, new_data):
    f_path = find_file(file_name)
    # Read the CSV data
    with open(f_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    updated = False
    
    # Find all matching rows with the given ID in column 0
    for row in data:
        if len(row) > 0 and row[0] == search_term:  # Check if the ID matches
            row[index] = new_data  # Update the specified column with new data
            updated = True
            break

    # If an update was made, write back to the CSV
    if updated:
        with open(f_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    else:
        print(f"list not found for search term {search_term} in column {index}.")
        return 'not_found'

def get_index_data(file, d_index, iteration):
    f_path = find_file(file)
    # Read the CSV data
    with open(f_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data[iteration][d_index]

def count_rows(file):
    f_path = find_file(file)
    # Read the CSV data
    with open(f_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        
    return len(data)  # Total rows in the CSV file
            

#update slip
import csv

def update_selection_status(mobile, match_name, status, db_file=slips_file):
    rows = []
    with open(db_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == mobile:
                matches = json.loads(row[2])
                if match_name in matches:
                    matches[match_name]['status'] = status
                    row[2] = json.dumps(matches)
            rows.append(row)

    with open(db_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

#update_selection_status('0702162058', '3997_Malaysia - Philippines', 'false', db_file=slips_file)



source_file = find_file('live_data.csv')  # Replace with the path to your source CSV file
target_file = find_file('logic.csv')  # Replace with the path to your target CSV file
slips_file = find_file('pending_slips.csv')

'''
def create_logic(source_file=source_file, target_file=target_file):
    # Read the data from source and target files
    source_data = read(source_file)  # Source data containing live match data
    header = ['id', 'home_win', 'away_win', 'draw', 'gg', 'ngg', 'o1.5', 'u1.5', 'o2.5', 'u2.5']
    
    # Ensure the header is present in the target file
    check_add(target_file, header)
    
    # Read existing logic data from the target file
    existing_rows = read(target_file)
    
    # Create a dictionary of existing rows for easy lookups and updates
    existing_data_dict = {row[0]: row for row in existing_rows[1:]}  # Skip the header row
    
    updated_rows = []
    
    # Process each row from the source data (live match data)
    for lst in source_data:
        match_id = str(lst[0])  # Assuming the first column in source is the match ID
        home_score = int(lst[2])
        away_score = int(lst[3])
        
        # Initialize win/draw status
        home_win = 1 if home_score > away_score else 0
        away_win = 1 if away_score > home_score else 0
        draw = 1 if home_score == away_score else 0
        
        # Calculate GG/NGG and over/under scores
        gg = 1 if home_score > 0 and away_score > 0 else 0
        ngg = 1 if gg == 0 else 0
        
        o15 = 1 if (home_score + away_score) > 1 else 0
        u15 = 1 if o15 == 0 else 0
        
        o25 = 1 if (home_score + away_score) > 2 else 0
        u25 = 1 if o25 == 0 else 0
        
        # Create the new row for the target file as a list of values
        new_row = [match_id, str(home_win), str(away_win), str(draw), str(gg), str(ngg), str(o15), str(u15), str(o25), str(u25)]
        
        # Check if the match_id already exists in the target file
        if match_id in existing_data_dict:
            # Update the existing entry in the dictionary
            existing_data_dict[match_id] = new_row
        else:
            # Append new rows for matches that do not exist
            existing_data_dict[match_id] = new_row
    
    # Combine the header with updated data
    final_rows = [header] + list(existing_data_dict.values())
    
    # Write the final updated data back to the target file
    write_csv(target_file, final_rows)
'''

def create_logic(source_file=source_file, target_file=target_file):
    """
    Processes live match data from the source file and updates logic data in the target file.
    Ensures robust handling of missing or empty files.

    Args:
        source_file (str): Path to the source file containing live match data.
        target_file (str): Path to the target file where logic data will be updated.
    """
    import os

    # Validate source file exists and is not empty
    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        return 'empty'
    
    source_data = read(source_file)  # Read source data
    
    if not source_data:  # Check if source file is empty
        print(f"Source file is empty: {source_file}")
        return 'empty'

    # Define the header for the target file
    header = ['id', 'home_win', 'away_win', 'draw', 'gg', 'ngg', 'o1.5', 'u1.5', 'o2.5', 'u2.5']
    
    # Ensure the header exists in the target file
    if not os.path.exists(target_file) or os.stat(target_file).st_size == 0:
        # If the target file does not exist or is empty, initialize it with the header
        write_csv(target_file, [header])
        print(f"Initialized target file with header: {target_file}")

    # Read existing logic data from the target file
    existing_rows = read(target_file)
    if not existing_rows:  # Check if the target file has no rows
        existing_rows = [header]

    # Create a dictionary of existing rows for easy lookup and updates
    existing_data_dict = {row[0]: row for row in existing_rows[1:]}  # Skip the header row

    # Process each row from the source data
    for line_number, lst in enumerate(source_data, start=1):
        try:
            # Ensure the source row has enough data
            if len(lst) < 4:
                print(f"Skipping malformed row {line_number} in source file: {lst}")
                continue

            match_id = str(lst[0])  # Assuming the first column in source is the match ID
            home_score = int(lst[2])
            away_score = int(lst[3])

            # Calculate outcomes
            home_win = 1 if home_score > away_score else 0
            away_win = 1 if away_score > home_score else 0
            draw = 1 if home_score == away_score else 0
            gg = 1 if home_score > 0 and away_score > 0 else 0
            ngg = 1 if gg == 0 else 0
            o15 = 1 if (home_score + away_score) > 1 else 0
            u15 = 1 if o15 == 0 else 0
            o25 = 1 if (home_score + away_score) > 2 else 0
            u25 = 1 if o25 == 0 else 0

            # Create the new row for the target file
            new_row = [match_id, str(home_win), str(away_win), str(draw), str(gg), str(ngg), str(o15), str(u15), str(o25), str(u25)]

            # Update or add the match data in the dictionary
            existing_data_dict[match_id] = new_row

        except (ValueError, IndexError) as e:
            print(f"Error processing row {line_number} in source file: {lst}, Error: {e}")
            continue

    # Combine the header with updated data
    final_rows = [header] + list(existing_data_dict.values())

    # Write the updated data back to the target file
    write_csv(target_file, final_rows)
    print(f"Logic data successfully updated in: {target_file}")


# Constants for URL paths
#from app.conf_base_url import base_url
BASE_URL = 'https://bozbet.xyz'
SUCCESS_URL = f"{BASE_URL}/success"
FAILURE_URL = f"{BASE_URL}/fail"



def check_slip_status(slip_id):
    with open(slips_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == slip_id:
                # Parse the JSON data from the slip
                selections = json.loads(row[2].replace('""', '"'))
                statuses = [details["status"] for details in selections.values()]

                if 'false' in statuses:
                    print(f"Slip fail: {slip_id}, selections:{selections}")
                    #mod_list_data(slips_file, slip_id, 5, 'fail')
                elif all(status == "true" for status in statuses):
                    print(f"slip win: {slip_id}, selections:{selections}")
                    #mod_list_data(slips_file, slip_id, 5, 'win')
                elif any(status == "pending" for status in statuses):
                    pass  # Still pending, so no action

#check_slip_status("0702162058")
def win(mobile, win_amount):
    url = f"{BASE_URL}/success?mobile={mobile}&win_amount={win_amount}"
    
    # Send a GET request to the Django view
    response = requests.get(url)
    
    # Check the response status
    if response.status_code == 200:
        print(f"Win data sent successfully for mobile {mobile}.")
    else:
        print(f"Failed to send data for mobile {mobile}, status code: {response.status_code}")

import requests

def fail(mobile, loss_amount):
    url = f"{BASE_URL}/fail?mobile={mobile}&win_amount={loss_amount}"
    
    # Send a GET request to the Django view
    response = requests.get(url)
    
    # Check the response status
    if response.status_code == 200:
        print(f"loss data sent successfully for mobile {mobile}.")
    else:
        print(f"Failed to send data for mobile {mobile}, status code: {response.status_code}")



def update_slip_final_status(slip_id):
    updated_rows = []
    
    # Read the CSV and process each row
    with open(slips_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == slip_id:
                # Parse the JSON data for the selections
                selections = json.loads(row[2].replace('""', '"'))
                statuses = [details["status"] for details in selections.values()]
                
                # Determine if the slip is a win or fail based on statuses
                if all(status == "true" for status in statuses):
                    row[-1] = "win"  # Update the final item to 'win'
                    win(row[0], row[1])
                elif 'false' in statuses:
                    row[-1] = "fail"  # Update the final item to 'fail'
                    los_amnt=str((float(row[1]))/float(row[3]))
                    fail(row[0], los_amnt)
                else:
                    #row[-1] = "pending"  # Update the final item to 'pending'
                    pass
                #print(f"Slip {slip_id} status updated to {row[-1]}.")

            updated_rows.append(row)
    
    # Write the updated rows back to the CSV file
    with open(slips_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

# Example usage
#update_slip_final_status("0702162058")

import datetime ,time

def update_pending_slips(pending_file=slips_file, logic_file=target_file):
    # Update logic
    create_logic()
    if create_logic()=='empty':
        return ''

    # Load logic data from CSV as a dictionary
    logic_data = {}
    with open(logic_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            logic_data[row['id']] = row  # Store each row using 'id' as the key
    
    # Get the current epoch time
    current_epoch = int(time.time())

    updated_slips = []
    send_success = False
    send_failure = False

    # Process pending slips
    with open(pending_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            mobile = row[0]
            bet_data = json.loads(row[2])  # Parse the bet data
            slip_epoch = int(row[4])  # Parse the slip epoch time

            if slip_epoch < current_epoch:  # Only process if the bet has ended
                #print(f'bet ended: {slip_epoch}')
                
                # Iterate over each match in the bet data
                for match_name, match_info in bet_data.items():
                    match_id = match_name.split('_')[0]  # Extract match ID
                    #print(match_id, logic_data)

                    # Check if the match_id exists in the logic_data
                    if match_id in logic_data:
                        logic = logic_data[match_id]  # Get logic for the current match
                        
                        # Extract logic values and convert them to integers
                        home_win = int(logic['home_win'])
                        away_win = int(logic['away_win'])
                        draw = int(logic['draw'])
                        gg = int(logic['gg'])
                        ngg = int(logic['ngg'])
                        o1_5 = int(logic['o1.5'])
                        u1_5 = int(logic['u1.5'])
                        o2_5 = int(logic['o2.5'])
                        u2_5 = int(logic['u2.5'])
                        
                        # Determine the expected result based on the bet label
                        bet_label = (match_info['label']).lower()
                        bet_status = match_info['status']  # Might need to check how this is used

                        if bet_label == '1':
                            expected = home_win
                        elif bet_label == '2':
                            expected = away_win
                        elif bet_label == 'x':
                            expected = draw
                        elif bet_label == 'gg':
                            expected = gg
                        elif bet_label == 'ngg':
                            expected = ngg
                        elif bet_label == 'ov1.5':
                            expected = o1_5
                        elif bet_label == 'und1.5':
                            expected = u1_5
                        elif bet_label == 'ov2.5':
                            expected = o2_5
                        elif bet_label == 'und2.5':
                            expected = u2_5
                        else:
                            expected = 0  # Default to 0 if no match is found
                        
                        # Mark selections based on the expected result
                        if expected == 1:
                            update_selection_status(mobile, match_name, 'true', slips_file)
                        elif expected == 0:
                            update_selection_status(mobile, match_name, 'false', slips_file)
                        else:
                            continue

                # Update final slip status after processing all matches for the slip
                update_slip_final_status(mobile)

import csv
import json
import time


def update_pending_slip(pending_file=slips_file, logic_file=target_file):
    """
    Processes pending slips by matching against logic data and updating their statuses.
    Handles malformed rows gracefully.

    Args:
        pending_file (str): Path to the CSV file containing pending slips.
        logic_file (str): Path to the CSV file containing logic data.
    """
    # Load logic data from CSV as a dictionary
    logic_data = {}
    with open(logic_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'id' in row:
                logic_data[row['id']] = row  # Store each row using 'id' as the key
    
    # Get the current epoch time
    current_epoch = int(time.time())

    with open(pending_file, 'r') as file:
        reader = csv.reader(file)
        for line_number, row in enumerate(reader, start=1):
            # Ensure the row has enough columns
            if len(row) < 6:
                print(f"Skipping malformed row {line_number}: {row}")
                continue

            try:
                mobile = row[0]
                bet_data = json.loads(row[2])  # Parse the bet data JSON
                slip_epoch = int(row[4])      # Parse the slip epoch time
                slip_status = row[5]          # Current slip status

                # Skip slips that are not yet due for processing
                if slip_epoch > current_epoch:
                    continue

                # Process each match in the bet data
                for match_name, match_info in bet_data.items():
                    match_id = match_name.split('_')[0]  # Extract match ID
                    if match_id not in logic_data:
                        print(f"Match ID {match_id} not found in logic data for row {line_number}.")
                        continue

                    # Get logic data for the current match
                    logic = logic_data[match_id]

                    # Safely extract logic values, defaulting to 0 if missing
                    home_win = int(logic.get('home_win', 0))
                    away_win = int(logic.get('away_win', 0))
                    draw = int(logic.get('draw', 0))
                    gg = int(logic.get('gg', 0))
                    ngg = int(logic.get('ngg', 0))
                    o1_5 = int(logic.get('o1.5', 0))
                    u1_5 = int(logic.get('u1.5', 0))
                    o2_5 = int(logic.get('o2.5', 0))
                    u2_5 = int(logic.get('u2.5', 0))

                    # Determine the expected result based on the bet label
                    bet_label = (match_info['label']).lower()
                    if bet_label == '1':
                        expected = home_win
                    elif bet_label == '2':
                        expected = away_win
                    elif bet_label == 'x':
                        expected = draw
                    elif bet_label == 'gg':
                        expected = gg
                    elif bet_label == 'ngg':
                        expected = ngg
                    elif bet_label == 'ov1.5':
                        expected = o1_5
                    elif bet_label == 'und1.5':
                        expected = u1_5
                    elif bet_label == 'ov2.5':
                        expected = o2_5
                    elif bet_label == 'und2.5':
                        expected = u2_5
                    else:
                        expected = 0  # Default to 0 if no match is found

                    # Update the status of the bet based on the expected result
                    if expected == 1:
                        match_info['status'] = 'true'
                    elif expected == 0:
                        match_info['status'] = 'false'

                # Update the final slip status
                final_status = all(match_info['status'] == 'true' for match_info in bet_data.values())
                new_status = 'win' if final_status else 'lose'
                print(f"Slip {mobile} updated to status: {new_status}")

            except (ValueError, json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"Error processing row {line_number}: {e}")
                continue

#from my_func import generate_odd
#print(type(generate_odd))
def generate_match_data_from_csv(file_path):
    new_page = ""

    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        # Use csv.DictReader to read the CSV file into dictionaries
        csv_reader = read(file_path)
        
        # Extract headers to verify
        headers =['Game_id','match','home_odd','draw_odd','away_odd','gg','ngg','o1.5','u1.5','o2.5','u2.5','date']#csv_reader.fieldnames
        #print("CSV Headers:", headers)
        
        # Ensure the expected headers are present
        if headers != ['Game_id','match','home_odd','draw_odd','away_odd','gg','ngg','o1.5','u1.5','o2.5','u2.5','date']:
            raise ValueError(f"Unexpected headers in CSV: {headers}")

        # Loop through each row in the CSV
        for row in csv_reader:
            #print(row)
            # Check if the required fields are not empty
            if row != [] and row != ['Game_id','match','home_odd','draw_odd','away_odd','gg','ngg','o1.5','u1.5','o2.5','u2.5','date']:
                # Extract data from the row
                #print(row)
                game_id = row[0]
                game = row[1]
                home_odd= row[3]#ok
                draw_odd = row[4]#ok
                away_odd = cap_odd(float(row[2]),2.40)#
                gg_odd = row[5]
                ngg_odd = row[6]
                over_one_odd = row[7]
                under_one_odd = row[8]
                over_two_odd = row[9]
                under_two_odd = row[10]
                date = row[11] # Default to 'N/A' if no date provided
                
                # Construct match data
                match_data = f'''
                    <div class='button-container' id='id{game_id}' onclick='rev_hid(this)'>
    <tm>time:{date}</tm>
    <span>{game}</span>
    <h3>1 X 2</h3>
    <label for="home_odd_{game_id}" class='hidx'>1</label>
    <button id='home_odd_{game_id}'>{home_odd}</button>
    <label for="draw_{game_id}" class='hidx'>X</label>
    <button id='draw_{game_id}'>{draw_odd}</button>
    <label for="away_odd_{game_id}" class='hidx'>2</label>
    <button id='away_odd_{game_id}'>{away_odd}</button>
    <br><br>

    <div class='hid_cont'>
        <table class='odds-table'>
            <!-- GG Section -->
            <tr>
                <th>GG</th>
                <th>NGG</th>
            </tr>
            <tr>
                <td><button id='gg_{game_id}' class='hid_g'>{gg_odd}</button></td>
                <td><button id='ngg_{game_id}' class='hid_g'>{ngg_odd}</button></td>
            </tr>

            <!-- Over 1.5 Section -->
            <tr>
                <th>ov1.5</th>
                <th>und1.5</th>
            </tr>
            <tr>
                <td><button id='o15_{game_id}' class='hid_g'>{over_one_odd}</button></td>
                <td><button id='u15_{game_id}' class='hid_g'>{under_one_odd}</button></td>
            </tr>

            <!-- Over 2.5 Section -->
            <tr>
                <th>ov2.5</th>
                <th>und2.5</th>
            </tr>
            <tr>
                <td><button id='o25_{game_id}' class='hid_g'>{over_two_odd}</button></td>
                <td><button id='u25_{game_id}' class='hid_g'>{under_two_odd}</button></td>
            </tr>
        </table>
    </div>
</div>
                    '''
                
                # Append the generated match data to the page
                new_page += match_data
            
            else:
                pass
    return new_page



sc_file = find_file('today.csv')
live_file = find_file('live_data.csv')

def remove_if_started(source_file=sc_file,ids_file=live_file):
    # Step 1: Read IDs from the ids_file
    ids_to_remove = set()
    
    with open(ids_file, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  # Ensure the row is not empty
                ids_to_remove.add(row[0])  # Assuming ID is the first column
    
    # Step 2: Read the source file and filter out the rows with IDs in ids_to_remove
    filtered_rows = []
    headers = None
    
    with open(source_file, mode='r') as file:
        csv_reader = csv.reader(file)
        #headers = next(csv_reader)  # Read the headers
        
        for row in csv_reader:
            if row and row[0] not in ids_to_remove and row != []:
                filtered_rows.append(row)
    
    # Step 3: Write the filtered rows to the source file
    with open(source_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        headers=['Game_id','match','home_odd','draw_odd','away_odd','gg','ngg','o1.5','u1.5','o2.5','u2.5','date']
        #csv_writer.writerow(headers)  # Write headers first
        csv_writer.writerows(filtered_rows)  # Write filtered rows


#single user login auth
# Path to the CSV file where mobile numbers and IP addresses are stored
CSV_FILE_PATH = find_file('ip.csv')

def add_mobile_ip_to_csv(mobile_number, ip_address):
    """
    Adds a mobile number and IP address pair to the CSV file if it doesn't already exist.
    """
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([mobile_number, ip_address])
    
def check_mobile_ip_match(mobile_number, ip_address):
    """
    Check if the given mobile number matches the provided IP address in the CSV file.
    Returns True if the match is found, otherwise False.
    """
    try:
        with open(CSV_FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_mobile, stored_ip = row
                if stored_mobile == mobile_number and stored_ip == ip_address:
                    return True
        return False
    except FileNotFoundError:
        # If the CSV file doesn't exist, treat it as no match
        return False
    
#to reassign another ip to user

def update_mobile_ip_in_csv(mobile_number, new_ip_address):
    """
    Updates the IP address for the given mobile number in the CSV file.
    If the mobile number exists, update its IP address. If it doesn't exist, append it.
    """
    temp_file_path = 'temp_user_data.csv'  # Temporary file to store updated data
    
    updated = False  # To check if we found the mobile number to update
    try:
        with open(CSV_FILE_PATH, mode='r') as infile, open(temp_file_path, mode='w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Read through the original CSV and update the matching mobile number's IP
            for row in reader:
                stored_mobile, stored_ip = row
                if stored_mobile == mobile_number:
                    # Update the IP for this mobile number
                    writer.writerow([mobile_number, new_ip_address])
                    updated = True
                else:
                    # Write the unchanged rows to the temp file
                    writer.writerow(row)
            
            # If the mobile number wasn't found, append it as a new entry
            if not updated:
                writer.writerow([mobile_number, new_ip_address])
    
        # Replace the old CSV with the updated one
        os.replace(temp_file_path, CSV_FILE_PATH)

    except FileNotFoundError:
        # If the CSV file doesn't exist, create it and add the mobile-IP pair
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([mobile_number, new_ip_address])

#func to change user ip
def change_ip_view(request):
    """
    Allow users to change their IP address manually.
    """
    mobile_number = request.POST.get('mobile_number')
    new_ip_address = request.POST.get('new_ip_address')

    # Update the IP address in the CSV
    update_mobile_ip_in_csv(mobile_number, new_ip_address)

    return HttpResponse(f"Your IP address has been updated to {new_ip_address}")


#block user funcs
block_file=find_file('blocked.csv')

def check_2_block_user(mobile,payload,data_check,reply_func,msg):
      for ch in payload:
            if ch not in data_check:
                  print(f'invalid..{payload}')
                  print(f'blocking user..{mobile}')
                  block=[mobile,f'payload:{payload}']
                  check_add(block_file,block)
                  return reply_func({'info':msg})
            else:
                  pass
            
def block_user(mobile,payload):
    payl=[mobile,payload]
    check_add(block_file,payl)

def check_if_blocked(mobile):
    f_data=(read(block_file))
    for l in f_data:
        if l[0]==mobile:
            return True
        else:
            pass
    return False
    

#checking received slips for any modification
# Function to load CSV data into a dictionary
def load_csv_data(file_path):
    game_data = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Using Game_id as the key for easy lookup
            game_data[row['Game_id']] = {
                'match': row['match'],
                'home_odd': float(row['home_odd']),
                'draw_odd': float(row['draw_odd']),
                'away_odd': float(row['away_odd']),
                'gg': float(row['gg']),
                'ngg': float(row['ngg']),
                'o1.5': float(row['o1.5']),
                'u1.5': float(row['u1.5']),
                'o2.5': float(row['o2.5']),
                'u2.5': float(row['u2.5']),
                'date': row['date']
            }
    return game_data

# Function to validate the picks from the frontend against the original CSV data
def validate_picks(picks, csv_data):
    for game_id, pick in picks.items():
        if game_id not in csv_data:
            return False, f"Game_id {game_id} not found in the original data."

        game_info = csv_data[game_id]
        
        # Validate the odds (you can add more checks for other fields if necessary)
        if pick['home_odd'] != game_info['home_odd'] or \
           pick['draw_odd'] != game_info['draw_odd'] or \
           pick['away_odd'] != game_info['away_odd']:
            return False, f"Odds mismatch for Game_id {game_id}. Received odds do not match the original."

    return True, "All picks are valid."

from encron.tools import encrypt_web
def changing_hash(mobile,amnt):
    str_f=f'{amnt}/{mobile}'
    hash=encrypt_web(str_f,mobile)
    return hash

import hashlib

def generate_hash(mobile, amount):
    # Convert the mobile and amount to strings and concatenate them
    input_data = f"{mobile}/{amount}"
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    # Encode the input data to bytes and update the hash object
    hash_object.update(input_data.encode('utf-8'))
    # Generate the hexadecimal hash
    hash_hex = hash_object.hexdigest()
    return hash_hex


#ADD CLIENTS BALANCE
def update_amount(mobile, amount_to_add,file_path=find_file('clients.csv')):
    """
    Updates the amount for a user based on their mobile number in the CSV file.

    Parameters:
        file_path (str): Path to the CSV file.
        mobile (str): The mobile number to search for.
        amount_to_add (float): The amount to add to the existing amount.
    
    Returns:
        str: Success or error message.
    """
    updated = False
    rows = []

    try:
        # Read the CSV file
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if the mobile number matches
                if row[3] == mobile:
                    try:
                        # Update the amount at the 4th index (convert to float first)
                        current_amount = float(row[4])
                        row[4] = str(current_amount + amount_to_add)
                        updated = True
                    except ValueError:
                        return f"Error: Invalid amount in the file for mobile {mobile}."
                rows.append(row)

        # Write the updated data back to the file
        if updated:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            return f"Successfully updated the amount for mobile {mobile}."
        else:
            return f"Mobile number {mobile} not found in the file."

    except FileNotFoundError:
        return "Error: The specified file does not exist."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


#take out old matches
from datetime import datetime, timedelta

new_pg='clean.csv'

def remove_past_matches(file_path):
    """
    Removes rows from the CSV file where the match time is earlier than the current time in Kenya.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Get the current UTC time and add 3 hours for Kenya's time (UTC+3)
    current_time = datetime.utcnow() + timedelta(hours=3)
    current_hour_minute = current_time.strftime("%H:%M")  # Extract hour and minute as a string

    updated_rows = []

    # Read the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        updated_rows.append(header)  # Keep the header row

        for row in csv_reader:
            match_time_str = row[-1]  # The last column is the match time (e.g., 15:30)

            # Compare match time with current Kenya time
            if match_time_str >= current_hour_minute:
                updated_rows.append(row)

    # Write the filtered rows back to the file
    with open(find_file('clean.csv'), 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(updated_rows)


#reverse today list

def reverse_csv_rows(input_file=find_file('today.csv'), output_file=find_file('today.csv')):
    """
    Reverses the rows of a CSV file, keeping the header at the top.
    
    Parameters:
    - input_file: str, path to the input CSV file.
    - output_file: str, path to save the reversed CSV file.
    """
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Ensure there are at least header and one row of data
        if len(rows) > 1:
            header = rows[0]  # First line is the header
            data = rows[1:]   # Remaining lines are the data
            
            # Reverse the data rows
            data.reverse()
            
            # Combine header and reversed data
            reversed_rows = [header] + data
        else:
            reversed_rows = rows  # If no data, keep original rows

    # Write the reversed rows to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(reversed_rows)
 


def remove_home_away(file):
    input_file=file
    output_file=file
    """
    Removes rows containing 'Home - Away' in the 'match' column from a CSV file.
    """
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        # Ensure there is a header
        if len(rows) > 0:
            header = rows[0]
            filtered_data = [header]  # Initialize with the header
            
            # Filter out rows where the 'match' column contains 'Home - Away'
            for row in rows[1:]:
                if len(row) > 1 and row[1] != "Home - Away":
                    filtered_data.append(row)
        else:
            filtered_data = rows  # If no data, keep the original rows

    # Write the filtered data to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(filtered_data)


