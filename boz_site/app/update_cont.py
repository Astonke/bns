import os
from my_func import *
from mydb import *
from encron.tools import *

# Get the directory path
#dir_path = os.path.dirname(os.path.realpath(__file__))
pathx='/home/aston/bozbet/bozbet/zsite/boz_site'
# File paths
file_path = f'{pathx}/media/shell_scripts/use.txt'
html_path = f'{pathx}/app/templates'

# Get total lines in the input file
total_lines = len(open(file_path).readlines())

def today_init():
    fl = find_file('today.csv')
    clf=find_file('clean.csv')
    print(f'file path: {fl}')
    os.system(f"echo '' > {fl}")
    os.system(f"echo '' > {clf}")    
    header = ['Game_id','match','home_odd','draw_odd','away_odd','gg','ngg','o1.5','u1.5','o2.5','u2.5','date']
    check_add(fl, header)

today_init()

# Extract data from the input file
times_data = extract_data(file_path, pattern=':')
games_data = extract_data(file_path, pattern='-')
odds_data = file_to_list('odds.txt')
ids_data = file_to_list('ids.txt')

# Check minimum length for all lists
min_length = min(len(times_data), len(games_data), len(odds_data) // 3, len(ids_data))

new_page = ''

# Process data line by line
if times_data:  # Check if times_data is not empty
    for i in range(1, min(total_lines // 6 + 1, min_length + 1)):
        date = times_data[i - 1]
        game_id = ids_data[i - 1]
        game = (games_data[i - 1])

        home_odd, draw_odd, away_odd = odds_data[3 * (i - 1): 3 * i]

        # Generate additional data
        gg_odd = generate_odd(min_value=1.40, max_value=1.75)
        ngg_odd = generate_odd(min_value=1.50, max_value=1.90)

        over_one_odd = generate_odd(min_value=1.09, max_value=1.25)
        under_one_odd = generate_odd(min_value=1.41, max_value=2.11)

        over_two_odd = generate_odd(min_value=1.29, max_value=2.01)
        under_two_odd = generate_odd(min_value=1.28, max_value=1.82)

        # Construct match data
        match_data = f'''\n
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
    <!-- GG Section -->
    <label for="gg" class="button-label">GG</label>
    <button id='gg_{game_id}' class='hid_g'>{gg_odd}</button>
    <label for="ngg" class="button-label">NGG</label>
    <button id='ngg_{game_id}' class='hid_g'>{ngg_odd}</button>
    <br>

    <!-- Over 1.5 Section -->
    <label for="o15" class="button-label">ov1.5</label>
    <button id='o15_{game_id}' class='hid_g'>{over_one_odd}</button>
    <label for="u15" class="button-label">und1.5</label>
    <button id='u15_{game_id}' class='hid_g'>{under_one_odd}</button>
    <br>

    <!-- Over 2.5 Section -->
    <label for="o25" class="button-label">ov2.5</label>
    <button id='o25_{game_id}' class='hid_g'>{over_two_odd}</button>
    <label for="u25" class="button-label">und2.5</label>
    <button id='u25_{game_id}' class='hid_g'>{under_two_odd}</button>
</div>
</div>

        '''
        #new_page += match_data
        home_score='0'
        away_score='0'
        appen_today = [game_id,game,home_odd,draw_odd,away_odd,gg_odd,ngg_odd,over_one_odd,under_one_odd,over_two_odd,under_two_odd,date]
        check_add(find_file('today.csv'),appen_today)
        

# Insert HTML content into the template
#insert_html(f'{html_path}/temp.html', '<!--start-->', new_page)
#reverse today to start with the popular
reverse_csv_rows()
remove_home_away(find_file('today.csv'))
