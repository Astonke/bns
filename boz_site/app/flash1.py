import requests
from bs4 import BeautifulSoup
import csv
import time

# Function to scrape football data
def scrape_football_data():
    url = 'https://www.flashscore.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Fetch the page
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find football matches
        matches = soup.find_all('div', class_='event__match')
        
        football_data = []
        
        for match in matches:
            # Extract team names, odds, ids, etc.
            home_team = match.find('div', class_='event__participant--home').text.strip()
            away_team = match.find('div', class_='event__participant--away').text.strip()
            odds = match.find('div', class_='event__odd').text.strip()
            match_id = match['id'].replace('g_1_', '')  # Example adjustment for match id
            
            # Example data structure
            football_data.append({
                'Home Team': home_team,
                'Away Team': away_team,
                'Odds': odds,
                'Match ID': match_id,
                'Home Score': '',
                'Away Score': ''
            })
        
        return football_data
    
    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch page: {e}')
        return None

# Function to log data to CSV
def log_to_csv(data, filename='football_data.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Home Team', 'Away Team', 'Odds', 'Match ID', 'Home Score', 'Away Score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)

# Function to update scores in CSV
def update_scores_in_csv(filename='football_data.csv'):
    # Simulating score update process
    updated_data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Simulate updating scores
            row['Home Score'] = '2'  # Example updated score
            row['Away Score'] = '1'  # Example updated score
            updated_data.append(row)
    
    # Write updated data back to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Home Team', 'Away Team', 'Odds', 'Match ID', 'Home Score', 'Away Score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in updated_data:
            writer.writerow(item)

# Example usage:
if __name__ == '__main__':
    # Scraping football data
    football_data = scrape_football_data()
    
    if football_data:
        # Logging data to CSV
        log_to_csv(football_data)
        
        # Simulate waiting for the match to finish (e.g., sleep for 1 minute)
        time.sleep(60)
        
        # Updating scores in CSV
        update_scores_in_csv()
        print('CSV updated with scores.')
    else:
        print('No football data scraped.')
