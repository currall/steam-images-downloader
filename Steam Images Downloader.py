# Steam Images Downloader

import os
import urllib.request

def library():
    # get owned games - steam api

    f = open("config.txt","r")
    config = f.readlines()
    f.close()

    def clean_string(input,remove):
        output = input.replace(remove.lower(),"")
        output = output.replace(":","")
        output = output.replace(" ","")
        output = output.replace("\n","")
        return output

    api_key = clean_string(config[0],"api key")
    steam_id = clean_string(config[1],"steam id")

    library_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+api_key+"&steamid="+steam_id+"&format=json&include_appinfo=1"
    print(library_url)
    urllib.request.urlretrieve(library_url,"steam_library.json") # downloads steam library to json

    steam_games = []

    with open('steam_library.json') as f:
        steam_lib = f.readlines()
        steam_lib = steam_lib[0]

    for i in range(len(steam_lib)):   
        if steam_lib[i:i+7] == '"appid"': # finds string appid
            j = i
            while steam_lib[j] != ",": # finds comma representing end of id
                j+=1
                
            game_id = steam_lib[i+8:j]

            k = j+9 
            while steam_lib[k] != '"': # starts from end of "name:"
                k+=1
            game_name = steam_lib[j+9:k]
            game_name = game_name.replace("â„¢","")
            game_name = game_name.replace("Â®","")
                    
            steam_games.append([game_name,game_id]) # adds name and id to array
            
    return steam_games

def download_box_arts():

    steam_library = library()
    current_dir = os.getcwd()
    try:
        os.mkdir("steam images")
    except:
        pass
    os.chdir("steam images")
    
    for i in range(len(steam_library)):
        image_url = "https://cdn.cloudflare.steamstatic.com/steam/apps/"+steam_library[i][1]+"/header.jpg?t=1646985712"
        urllib.request.urlretrieve(image_url,steam_library[i][1]+".jpg")

download_box_arts()