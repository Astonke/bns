import os

def delete_csv_files(directory="."):
  """Deletes only valid CSV files from the specified directory."""
  csv_filenames = ["accounts.csv", "betslips.csv", "user_data.csv",'README.md','devserver.sh','mysite']

  # Informative messages for non-standard filenames
  for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if filename.startswith("<coolcsv.mydb.mydb object at"):
      print(f"del non-standard file: {filename} (might not be a real file)")
      os.remove(filepath)
    elif filename in csv_filenames:
      print(f"{filename}  Skipping deletion for safety.")
      pass

# Example usage (replace "." with the actual directory path if needed)
delete_csv_files()
