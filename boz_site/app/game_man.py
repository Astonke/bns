import csv
from django.shortcuts import render
from .forms import GameForm
from encron.tools import find_file

def game_update(action, game_data=None, game_id=None):
    """
    Function to add, modify, or delete game data in today.csv.
    
    Parameters:
    - action (str): 'add', 'modify', or 'delete'.
    - game_data (dict): Dictionary containing game details (required for 'add' and 'modify').
    - game_id (str): The Game_id to identify the record (required for 'modify' and 'delete').
    """
    filename = find_file("today.csv")
    
    # Read the current content of the CSV
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    if action == 'add':
        # Ensure game_data has all required fields
        if not game_data or not all(field in game_data for field in fieldnames):
            return "Invalid game_data. All fields are required."
        
        # Add the new game to the rows
        rows.append(game_data)
    
    elif action == 'modify':
        if not game_id or not game_data:
            return "game_id and game_data are required for modification."
        
        # Find the row to modify and update it
        for row in rows:
            if row['Game_id'] == game_id:
                row.update(game_data)
                break
        else:
            return f"Game with Game_id {game_id} not found."
    
    elif action == 'delete':
        if not game_id:
            return "game_id is required for deletion."
        
        # Remove the row with the specified Game_id
        rows = [row for row in rows if row['Game_id'] != game_id]
    
    else:
        return "Invalid action. Use 'add', 'modify', or 'delete'."
    
    # Write the updated content back to the CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return f"Action '{action}' completed successfully."

#from forms import GameForm

def manage_game(request,ckey):
      # Your static key for comparison
    static_key = 'hacker404'
    static_key2='gKLS90o9B_qtL0gt67zDHh-sEueeYwJLHNiZz_9MBNqo7FInBkB7r51xgtU5KzcRPZ3k'

    # Check if the key is valid
    if ckey == static_key or ckey == static_key2:
        # If valid, pass the encrypted key to the template
        if ckey == static_key2:
            endp='no_red'
        else:
            endp=static_key2

    else:
        # If the key is invalid, return 404
        return render(request,'access_denied.html')
    
    games = []
    with open(find_file('today.csv'), mode='r') as file:
        reader = csv.DictReader(file)
        games = list(reader)
    message = None
    if request.method == 'POST':
        action = request.POST.get('action')
        game_id = request.POST.get('Game_id')
        form = GameForm(request.POST)
        
        if form.is_valid() and action in ['add', 'modify', 'delete']:
            if action == 'delete':
                message = game_update('delete', game_id=game_id)
            else:
                message = game_update(action, game_data=form.cleaned_data, game_id=game_id)
        else:
            message = "Invalid input."

    form = GameForm()
    #return render(request, 'manage_game.html', {'form': form, 'message': message})
    return render(request, 'manage_game.html', {'games': games, 'message': message})

"""
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Helper function to read games from the CSV file
def read_games(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

# Helper function to write games to the CSV file
def write_games(file_path, games):
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ["Game_id", "match", "home_odd", "draw_odd", "away_odd", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)

def manage_game(request,ckey):
    if ckey == 'hacker404':
       pass
    else:
       return render(request,'access_denied.html')
    file_path = find_file('today.csv')  # Ensure this path is correct
    games = read_games(file_path)
    message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        # Adding a new game
        if action == 'add':
            new_game = {
                "Game_id": request.POST.get('Game_id'),
                "match": request.POST.get('match'),
                "home_odd": request.POST.get('home_odd'),
                "draw_odd": request.POST.get('draw_odd'),
                "away_odd": request.POST.get('away_odd'),
                "date": request.POST.get('date'),
            }
            games.append(new_game)
            write_games(file_path, games)
            message = "Game added successfully!"

        # Modifying an existing game
        elif action == 'modify':
            game_id = request.POST.get('Game_id')
            for game in games:
                if game["Game_id"] == game_id:
                    game.update({
                        "match": request.POST.get('match'),
                        "home_odd": request.POST.get('home_odd'),
                        "draw_odd": request.POST.get('draw_odd'),
                        "away_odd": request.POST.get('away_odd'),
                        "date": request.POST.get('date'),
                    })
                    break
            write_games(file_path, games)
            message = f"Game {game_id} updated successfully!"

        # Deleting an existing game
        elif action == 'delete':
            game_id = request.POST.get('Game_id')
            games = [game for game in games if game["Game_id"] != game_id]
            write_games(file_path, games)
            message = f"Game {game_id} deleted successfully!"

        return redirect('manage_game')

    return render(request, 'manage_game.html', {'games': games, 'message': message})
"""


import csv
from django.shortcuts import render
from django.http import JsonResponse

# File path to the CSV file
FILE_PATH = find_file('today.csv')
"""
# Helper to read CSV data
def read_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

# Helper to write to CSV
def write_csv(file_path, data):
    if data:
        headers = data[0].keys()
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

# View function
def manage_game(request,ckey):
    if ckey == 'hacker404':
       pass
    else:
       return render(request,'access_denied.html')

    if request.method == 'POST':
        action = request.POST.get('action')
        games = read_csv(FILE_PATH)

        if action == 'add':
            # Add a new game
            new_game = {
                "Game_id": request.POST.get('Game_id'),
                "match": request.POST.get('match'),
                "home_odd": request.POST.get('home_odd'),
                "draw_odd": request.POST.get('draw_odd'),
                "away_odd": request.POST.get('away_odd'),
                "date": request.POST.get('date'),
            }
            games.append(new_game)

        elif action == 'edit':
            # Edit an existing game
            game_id = request.POST.get('Game_id')
            for game in games:
                if game["Game_id"] == game_id:
                    game.update({
                        "match": request.POST.get('match'),
                        "home_odd": request.POST.get('home_odd'),
                        "draw_odd": request.POST.get('draw_odd'),
                        "away_odd": request.POST.get('away_odd'),
                        "date": request.POST.get('date'),
                    })
                    break

        elif action == 'delete':
            # Delete a game
            game_id = request.POST.get('Game_id')
            games = [game for game in games if game["Game_id"] != game_id]

        # Write updated data to CSV
        write_csv(FILE_PATH, games)

        # Return success response
        return JsonResponse({"success": True, "games": games})

    # For GET requests, render the page with game data
    games = read_csv(FILE_PATH)
    return render(request, 'manage_game.html', {'games': games})
"""
"""
# Helper to read CSV data
def read_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

# Helper to write to CSV
def write_csv(file_path, data):
    if data:
        headers = data[0].keys()
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

# View function
def manage_game(request,ckey):
    if ckey == 'hacker404':
       pass
    else:
       return render(request,'access_denied.html')

    if request.method == 'POST':
        action = request.POST.get('action')
        games = read_csv(FILE_PATH)

        if action == 'add':
            new_game = {
                "Game_id": request.POST.get('Game_id'),
                "match": request.POST.get('match'),
                "home_odd": request.POST.get('home_odd'),
                "draw_odd": request.POST.get('draw_odd'),
                "away_odd": request.POST.get('away_odd'),
                "gg": request.POST.get('gg'),
                "ngg": request.POST.get('ngg'),
                "o1.5": request.POST.get('o1_5'),
                "u1.5": request.POST.get('u1_5'),
                "o2.5": request.POST.get('o2_5'),
                "u2.5": request.POST.get('u2_5'),
                "date": request.POST.get('date'),
            }
            games.append(new_game)
        elif action == 'edit':
            game_id = request.POST.get('Game_id')
            for game in games:
                if game["Game_id"] == game_id:
                    game.update({
                        "match": request.POST.get('match'),
                        "home_odd": request.POST.get('home_odd'),
                        "draw_odd": request.POST.get('draw_odd'),
                        "away_odd": request.POST.get('away_odd'),
                        "gg": request.POST.get('gg'),
                        "ngg": request.POST.get('ngg'),
                        "o1.5": request.POST.get('o1_5'),
                        "u1.5": request.POST.get('u1_5'),
                        "o2.5": request.POST.get('o2_5'),
                        "u2.5": request.POST.get('u2_5'),
                        "date": request.POST.get('date'),
                    })
                    break
        elif action == 'delete':
            game_id = request.POST.get('Game_id')
  """
