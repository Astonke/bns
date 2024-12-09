import csv
import os
import json
from time import sleep

def write_data(data, filename):
  """Writes data to a CSV file.

  Args:
    data: A list of lists, where each inner list represents a row.
    filename: The name of the CSV file.
  """
  dir_path=os.path.dirname(os.path.realpath(__file__))
  with open(f'{dir_path}/{filename}', "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


def append_data(data, filename):
  """Appends data to an existing CSV file.

  Args:
    data: A list representing a new row to be appended.
    filename: The name of the CSV file.
  """
  dir_path=os.path.dirname(os.path.realpath(__file__))
  with open(f'{dir_path}/{filename}', "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)



def read_data(filename):
  """Reads data from a CSV file into a list of lists.

  Args:
    filename: The name of the CSV file.

  Returns:
    A list of lists containing the CSV data.
  """
  data = []
  dir_path=os.path.dirname(os.path.realpath(__file__))
  with open(f'{dir_path}/{filename}', "r") as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)
  return data


def get_column(data, column_index):
  """Retrieves a specific column from the CSV data.

  Args:
    data: A list of lists containing the CSV data.
    column_index: The index of the column to retrieve (0-based indexing).

  Returns:
    A list containing the values from the specified column.
  """
  return [row[column_index] for row in data]


def get_row(data, row_index):
  """Retrieves a specific row from the CSV data.

  Args:
    data: A list of lists containing the CSV data.
    row_index: The index of the row to retrieve (0-based indexing).

  Returns:
    A list representing the retrieved row.
  """
  return data[row_index]


def get_user_data(data, header, value):
  """Retrieves all rows where a specific header-value pair exists.

  Args:
    data: A list of lists containing the CSV data.
    header: The name of the header to search.
    value: The value to search for.

  Returns:
    A list of lists containing matching rows.
  """
  matching_data = []
  matching_lists=[]
  header_index = data[0].index(header)
 
  for row in data[1:]:
    if value in row:
      matching_lists.append(row)
    else:
      pass
  for list in matching_lists:
    if  list[header_index] == value:
      matching_data=(list)
      return matching_data
    else:
      pass
  if matching_data == []:
    return False


def remove_row(data, row_index):
  """Removes a row from the CSV data (in-memory).

  Args:
    data: A list of lists containing the CSV data.
    row_index: The index of the row to remove (0-based indexing).
  """
  del data[row_index]


def remove_column(data, column_index):
  """Removes a column from the CSV data (in-memory).

  Args:
    data: A list of lists containing the CSV data.
    column_index: The index of the column to remove (0-based indexing).
  """
  for row in data:
    del row[column_index]


def update_data(data, filename):
  """Writes the updated CSV data back to the file.

  Args:
    data: A list of lists containing the updated CSV data.
    filename: The name of the CSV file.
  """
  write_data(data, filename)
  
def append_to_csv_column(filename, column_name, new_data):
  """
  Appends data to a specific column in a CSV file.

  Args:
      filename (str): The path to the CSV file.
      column_name (str): The name of the column to append data to.
      new_data (list): A list of new values to append to the column.
  """
  # Read the CSV data
  with open(filename, "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

  # Find the index of the column to modify
  try:
    column_index = data[0].index(column_name)
  except ValueError:
    print(f"Column '{column_name}' not found in the CSV file.")
    return

  # Append new data to the specified column
  for row in data[1:]:
    row.insert(column_index, "")  # Add empty slots for new data
  for i, value in enumerate(new_data):
    data[i+1][column_index] = value

  # Write the modified data to a new CSV file
  with open("modified_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
    
def check_in_db(mobile_no):
  client_list=get_user_data(read_data('data.csv'), "mobile", mobile_no)
  if (client_list[0]==mobile_no):
    return True
  else:
    return False
  
  
def get_page(file):
    from encron.tools import find_file
    f_path=find_file(file)
    with open(f'{f_path}', "r") as f:
     content = f.read() 
    return content
  
def take_json(data):
   start=data.find('{')+1
   end=data.find('}')
   for x in data:
      return data[start:end]

def make_dict(data):
   tdict={}
   pairs =[item.strip() for item in data.replace('"','').split(',')]
   for pair in pairs:
      key, value =pair.split(":")
      tdict[key] = value
   return tdict

def j_data(json_datax):
   respo=json.dumps(json_datax)
   http_respo=(
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(respo)}\r\n"
        "\r\n"
        f"""{respo}"""
   )
   return (http_respo.encode('utf-8'))

def responder(j_data,session_data):
    response_data=json.dumps(j_data)
    http_cors=(
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Content-Type: */*\r\n"
        f"Content-Length: {len(response_data)}\r\n"
        "\r\n"
        f"""{response_data}"""
    )
    session_data.sendall(http_cors.encode('utf-8'))
 
import os
import tempfile
import subprocess
import random

import re

def append_after(hfile,comment,new_data):
    new=hfile.replace(comment,comment+f'\n{new_data}')
    return new

def insert_html(html_file, comment_text, div_content):
  """
  Inserts a div container with specified content after a comment tag
  with the given text in the provided HTML file, overwriting the original content.

  Args:
      html_file (str): Path to the HTML file.
      comment_text (str): Text of the comment tag to serve as the insertion point.
      div_content (str): Content to be placed inside the div tag.

  Raises:
      FileNotFoundError: If the specified HTML file is not found.
  """
  # Read the HTML file
  try:
    with open(html_file, 'r', encoding='utf-8') as file:  # Open in read mode with UTF-8 encoding
      html_string = file.read()
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: HTML file '{html_file}' not found.")
  
  #find the comment tag then append data
  new_html=append_after(hfile=html_string,comment=comment_text,new_data=div_content)
  
  # Overwrite the original file with the modified HTML content
  with open(html_file, 'w', encoding='utf-8') as file:
    file.write(new_html)
  

def extract_data(file_path, pattern):
    """
    Extracts lines containing the specified pattern from the file.

    Args:
        file_path (str): Path to the input file.
        pattern (str): Regular expression pattern to match.

    Returns:
        list: List of lines containing the pattern.
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if pattern in line]


def generate_odd(min_value, max_value):
    """
    Simulates generating an odd value within a range (replace with actual logic).

    Args:
        min_value (float): Minimum possible odd value.
        max_value (float): Maximum possible odd value.

    Returns:
        float: A random value between min_value and max_value.
    """
    # Replace this with your actual odd generation logic (e.g., calling odd_gen.py)
    # This is just a placeholder for demonstration purposes
    return round(random.uniform(min_value, max_value), 2)
  
def run_shell(command):
  """
  Runs a shell command and returns its output as a string.

  Args:
      command (str): The shell command to execute.

  Returns:
      str: The output of the command, or None if an error occurred.
  """

  try:
    # Run the command with capture to get the output
    result = subprocess.run(command.split(), capture_output=True, text=True)  # Ensure text output
    return result.stdout.strip()  # Remove leading/trailing whitespace
  except subprocess.CalledProcessError as e:
    print(f"Error running command '{command}': {e}")
    return None


def file_to_list(f_name):
    d_path=os.path.dirname(os.path.realpath(__file__))
    dir_path=f'{d_path}/../media/shell_scripts'
    with open(f'{dir_path}/{f_name}','r') as fl:
        lines=fl.readlines()
    
    # Remove trailing newline characters from each line (optional)
    lines = [line.strip() for line in lines]
    return lines
  

# Function to ensure max length for match id
def check_game_length(game):
    game_out = ''
    c_game = len(game)
    if c_game > 28:
        dif = c_game - 28
        take = int((dif) / 2)
        hm, aw = game.split('-')
        dif_z = 0
        home_len = len(hm)
        away_len = len(aw)
        # Balance the length strings if caused by one side
        if len(hm) > len(aw):
            dif_z = (len(hm) - len(aw))
            if dif_z > dif:
                home_len = hm[0:(len(hm) - (dif_z - dif))]
        else:
            dif_z = (len(aw) - len(hm))
            if dif_z > dif:
                away_len = aw[0:(len(aw) - (dif_z - dif))]
        # If still greater then take from both
        n_game = f'{home_len}-{away_len}'
        if len(n_game) > dif:
            nhm = hm[0:(len(hm) - take)]
            naw = aw[0:(len(aw) - take)]
            return f'{nhm}-{naw}'
        else:
            return n_game
    else:
        return game
  