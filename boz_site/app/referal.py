import csv
import os
from encron.tools import find_file

CSV_FILE_PATH = find_file('referrals.csv')

# Function to read referral data from the CSV file
def read_referral_data():
    if not os.path.exists(CSV_FILE_PATH):
        return {}  # Return an empty dictionary if the file doesn't exist
    
    data = {}
    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row['mobile_number']] = int(row['referral_count'])
    return data

# Function to write referral data to the CSV file
def write_referral_data(data):
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['mobile_number', 'referral_count'])
        writer.writeheader()
        for mobile_number, referral_count in data.items():
            writer.writerow({'mobile_number': mobile_number, 'referral_count': referral_count})

# Function to update referral count or add a new entry
def update_referral_count(mobile_number):
    data = read_referral_data()
    
    # Check if the mobile number already exists in the data
    if mobile_number in data:
        data[mobile_number] += 1  # Increment referral count
    else:
        data[mobile_number] = 1  # Initialize referral count if not exists

    write_referral_data(data)
    return data[mobile_number]  # Return the updated referral count
