import os
import json
from typing import List

def create_file_object(name: str):
    return {
        "name": name,
        "type": "file"
    }

def create_directory_object(path: str, name: str):
    object = {
        "name": name,
        "type": "directory",
        "children": []
    }
    for item in os.listdir(path):
        if os.path.isfile(f"{path}/{item}"):
            object["children"].append(create_file_object(item))
        else:
            object["children"].append(create_directory_object(f"{path}/{item}", name))
    
    return object

def create_filesystem(root_folder: str):
    fs = { "fs": [] }
    for item in os.listdir(root_folder):
        if item == "desktop.ini":
            continue
        if os.path.isfile(f"{root_folder}/{item}"):
            fs["fs"].append(create_file_object(item))
        else:
            fs["fs"].append(create_directory_object(f"{root_folder}/{item}", item))
    
    return fs

def create_filesystem_json(root_folder: str):
    return json.dumps(create_filesystem(root_folder))

def create_directory_index(path: str) -> List[str]:
    index: List[str] = []
    relative_path = path.split("Music")[-1] if "Music" in path else path.split("music")[-1]
    for item in os.listdir(path):
        full_item_path = f"{path}/{item}"
        if os.path.isdir(full_item_path):
            nested_index = create_directory_index(full_item_path)
            index.extend(nested_index)
            continue
        if item == "desktop.ini":
            continue
        index.append(f"{relative_path}/{item}")

    return index

def create_filesystem_index(root_folder: str):
    index = create_directory_index(root_folder)
    return index