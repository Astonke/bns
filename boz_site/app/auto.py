import subprocess
import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from encron.tools import find_file

#f tools
def execute_bash(command):
    try:
        result = subprocess.run(
            command, 
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the command: {e}")
        return e.stderr.strip()

def check_install_driver():
    g_v = execute_bash('google-chrome --version')
    g_lst = g_v.split()
    vr = g_lst[2]
    chrome_driver_path = find_file('net_drive')
    if not chrome_driver_path or not os.path.isfile(chrome_driver_path):
        print(f'Installing ChromeDriver {vr}')
        inst = execute_bash(
            f'https://storage.googleapis.com/chrome-for-testing-public/{vr}/linux64/chrome-linux64.zip; '
            f'unzip chromedriver_linux64.zip; '
            f'mv chromedriver net_drive; '
            f'chmod +x net_drive; '
            f'rm chromedriver_linux64.zip'
            f'rm -r chromedriver_linux64'
        )
        print(inst)
        chrome_driver_path = 'net_drive'
    else:
        print('net_drive installed..')
    return chrome_driver_path

# Create ChromeOptions instance with headless flag
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Specify the path to the ChromeDriver executable
def executable(binary):
    chrome_driver_path = find_file(binary)
    chrome_options.add_argument(f"executable_path={chrome_driver_path}")
    #return chrome_driver_path

# Set the path to the ChromeDriver executable in the PATH environment variable
def browser_binary(bin='/bin/google-chrome'):
    chrome_options.binary_location = bin

def headless():
    return chrome_options.add_argument("--headless")

driver=''
    
def init(driver_name='net_drive',browser_bin='/bin/google-chrome',background=True):
    #install net_drive if absent
    #check_install_driver()
    # Create a new instance of the Chrome driver with headless options
    if background:
        chrome_options.add_argument("--headless")
    executable(driver_name)
    browser_binary(browser_bin)
    # replace with the actual path to your Chrome browser if needed
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    

def go(url_path):
    driver.get(url_path)
    
def exec(script):
    result=driver.execute_script(script)
    return result

def find_click(xpath):
    ob=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ob.click()

def db_click(xpath):
    ob=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ob.click()
    ob.click()
    
def clear_input(xpath,data):
    ob=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ob.click()
    ob.clear()
    ob.send_keys(data)
    
def click_btn(xpath):
    bt=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def extract_text(xpath):
    ob=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return ob.text

#to refresh the page
def refresh():
    driver.refresh()