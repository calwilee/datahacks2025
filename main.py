import os
from dotenv import load_dotenv
import base64 #importing libraries
from requests import post, get
import json

load_dotenv() #calls function

client_id = os.getenv("CLIENT_ID") #values
client_secret = os.getenv("CLIENT_SECRET")

def get_token(): # def is define
    auth_string = client_id + ":" + client_secret #concatenating strings
    auth_bytes = auth_string.encode("utf-8") #encoding
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #encoding

    url = "https://accounts.spotify.com/api/token" #url
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) #post request
    json_result = json.loads(result.content)
    token = json_result["access_token"] #access token
    return token #returning token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}  #function to get auth header

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers) #get request
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0: #length of json_result
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token) #send requests
    result = get(url, headers=headers) #get request
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token() #calling function
result = search_for_artist(token, "BEACH HOUSE")
artist_id = result["id"] # the artist id
songs = get_songs_by_artist(token, artist_id) # retrieve songs by artist

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")