import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import certifi
import time

load_dotenv()

API_BASE_URL = 'https://demo.credy.in/api/v1/maya/movies/'

def fetch_movies(page=1):
    username = os.getenv('API_USERNAME')
    password = os.getenv('API_PASSWORD')
   
    auth = HTTPBasicAuth(username, password)
    params={'page':page}

    retries=3

    while retries>0:
        try:
            response = requests.get(API_BASE_URL, auth=auth, params=params, verify=False)
            response.raise_for_status()
            # print(len(response.json().get('results')))
            return response.json()
        except requests.exceptions.RequestException as e:
            # print(e)
            # print("retries ##########################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",retries)
            retries-=1
    return None
    
# print(fetch_movies())

# def fetch_all_movies():
#     page=1
#     max_retries=3
#     all_movies=[]

#     while True:
#         try:
#             response=fetch_movies(page)
#             if not response:
#                 break
#             print("response ##########################",response)
#             all_movies.extend(response.get('results', []))

#             next_page=response.get('next')
#             if not next_page:
#                 break
#             page=page+1
#         except requests.exceptions.RequestException as e:
#             max_retries-=1

#             print("retries ##########################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",max_retries)
#             if max_retries <= 0:
#                 print(f"Max retries exceeded. Error: {e}")
#                 break
#             print(f"Retrying after error: {e}")
#             time.sleep(5)

#     print("all_movies ##########################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",all_movies)    

#     return all_movies

# print(fetch_all_movies())
    
