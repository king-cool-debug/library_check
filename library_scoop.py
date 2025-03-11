#!/usr/bin/env python

from bs4 import BeautifulSoup
import subprocess
import pandas as pd
import os.path
import requests

Page = ['https://whitby.bibliocommons.com/explore/recent_arrivals?f_on_order=true&formats=BLURAY',
'https://whitby.bibliocommons.com/explore/recent_arrivals?f_on_order=false&formats=BLURAY',
'https://oshlib.bibliocommons.com/explore/recent_arrivals?f_on_order=false&formats=BLURAY',
'https://oshlib.bibliocommons.com/explore/recent_arrivals?f_on_order=true&formats=BLURAY']
Status = ['On Order','In Stock','In Stock','On Order']
Location = ['Whitby','Whitby','Oshawa','Oshawa']
Setup_df = pd.DataFrame({'Page':Page,'Status':Status,'Location':Location})

def get_list(url):
    result = subprocess.run(["curl",url], capture_output=True, text=True)
    output = BeautifulSoup(result.stdout,'html.parser')
    soup = output.find_all('a')
    titles = []
    for temp in soup:
        title = temp.get('title')
        if title != None:
            print(title)
            titles.append(title)
    return titles

def do_list():
    df = pd.DataFrame(columns=['Status','Location'])
    df.index.name = 'Title'
    
    full_list = []
    for index, row in Setup_df.iterrows():
        full_list += get_list(row.Page)
        for title in full_list:
            if title not in df.index:
                df.loc[title] = {'Status':row.Status, 'Location':row.Location}
    return df            

def get_diff():
    if os.path.isfile('titles.csv'):
        existing_df = pd.read_csv('titles.csv',index_col='Title')
        existing_df.index = 'Title'
        current_df = do_list()
    else:
        current_df = do_list()
        current_df.to_csv('titles.csv')
        existing_df = current_df

    new_titles = 'New Titles!:\n'
    diff = (set(current_df.index()) - set(existing_df.index()))
    for index,row in diff.iterrows():
        new_titles += (f'{index} {row.Status} at {row.Location} Location \n') 
    
    return new_titles

def ping_discord(new_titles):
    webhook_url = 'https://discord.com/api/webhooks/1349098820847272107/J4mPvTwuJiKAHbJT99sc71egvHC_iknhclc8-h7nAZXRp_u03IKhQ5OkcyegBbicsWIM'
    if new_titles != '':
        message = {
            "content": new_titles 
            }
    
        # Send the POST request to the webhook URL
        response = requests.post(webhook_url, json=message)
    
        # Check if the request was successful
        if response.status_code == 204:
            print("Message sent successfully!")
            return 200
        else:
            print(f"Failed to send message: {response.status_code}")
            return 500
    else:
        print("No new titles :(")
        return 200

def execute()
    new_titles = get_diff()
    status_code = ping_discord(new_titles)
    return status_code

if __name__ == "__main__":
    execute()
    
