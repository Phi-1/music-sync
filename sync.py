#!/usr/bin/env python3
#called on the raspi while server is online on main pc
#mainframe ip is 1.92

import json
import requests
import backend.fs as fs
import os
from dotenv import load_dotenv

# path is relative to music folder
def get_music_file(music_folder: str, path: str, url: str):
    res = requests.request("get", f"{url}/music", data=path.decode())
    with open(f"{music_folder}{path}", "bw") as file:
        file.write(res.content)

def get_missing_music(music_folder: str, index, url: str):
    for filename in index["index"]:
        #check if folder exists
        os.makedirs(os.path.dirname(music_folder + filename), exist_ok=True)
        get_music_file(music_folder, filename, url)

def get_missing_music_index(index: str, url: str):
    # send fs to server, get back list of missing music paths
    res = requests.request("get", f"{url}/index/missing", data=index)
    if not res.status_code == 200:
        print("Something went wrong fetching missing music index")
        return None
    missing_index = json.loads(res.content)
    return missing_index

def create_index_json(folder: str) -> str:
    index = fs.create_directory_index(folder)
    return json.dumps({ "index": index })

def main():
    load_dotenv()
    music_folder = os.environ.get("MUSIC_FOLDER")
    mainframe_url = "http://192.168.1.92:7777"
    index = create_index_json(music_folder)
    missing_index = get_missing_music_index(index, mainframe_url)
    if missing_index == None:
        return
    if len(missing_index["index"]) == 0:
        print("Not missing any music files")
        return
    print(f"Missing the following files: {missing_index['index']}")
    get_missing_music(music_folder, missing_index, mainframe_url)

if __name__ == "__main__":
    main()