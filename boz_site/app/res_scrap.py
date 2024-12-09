import requests
from auto import *
from time import sleep

url='https://odibets.com/live/'

init()

go(url)

#search button
find_click('/html/body/div[1]/div/div[2]/div[1]/div[3]')

#input area
find_click('//*[@id="modal"]/div/div[1]/input')

#enter code
clear_input('//*[@id="modal"]/div/div[1]/input','5070')

#teams
home=extract_text('/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/a/div[1]')
away=extract_text('/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/a/div[2]')

#scores
home_score=extract_text('/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/span[1]')
away_score=extract_text('/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/span[2]')

print(f'{home}-{away}')
print(f'scores: {home_score}-{away_score}')

#get current xodds

sleep(10000)