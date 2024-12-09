from .mydb import read
from encron.tools import find_file

import csv
import json

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

# Updated process_slip function with the check
def process_slip(request):
    if request.method == 'POST':
        try:
            # Decode the request body to a string
            data = request.body.decode('utf-8')
            # Parse the JSON string to a dictionary
            datas = json.loads(data)

            # Access picks and other details
            picks_str = datas['picks']
            mobile = datas['mobile']
            possible_win = datas['possible']
            odds = datas['odds']
            bet_amount = datas['bet_amount']
            max_time = datas['max_time']
            balance = get_balance(mobile)
            bt_amount = float(bet_amount)
            bal = float(balance)

            if bt_amount > bal:
                print(bt_amount, '>', bal)
                return JsonResponse({'info': 'deny'})
            if bt_amount <= bal:
                new_balance = bal - bt_amount
                update_balance(mobile, new_balance, bt_amount)

                # Parse the picks string to a dictionary
                picks = json.loads(picks_str)

                # Load original CSV data to validate picks
                csv_data = load_csv_data(find_file('today.csv'))  # Provide the correct path to the CSV file
                is_valid, validation_message = validate_picks(picks, csv_data)

                if not is_valid:
                    return JsonResponse({'info': 'invalid', 'message': validation_message})

                # Set default status for each pick to 'pending'
                for key in picks:
                    picks[key]['status'] = 'pending'

                # The payload should be counter checked in the database for authenticity
                pending = find_file('pending_slips.csv')
                nw = [mobile, possible_win, json.dumps(picks), odds, max_time, 'waiting']
                print(f'new: {nw}')
                print('arguments ok..')

                # Add to the database
                add_to_db(pending, nw)
                print('added to db')
                return JsonResponse({'info': 'rec'})

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'info': 'error', 'message': str(e)})