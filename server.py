import json
from dotenv import load_dotenv
from flask import Flask, send_file, make_response, request
import os
import backend.fs as fs

app = Flask(__name__)

@app.route("/music", methods=["GET"])
def get_music_file():
    relative_music_file_path = request.data.decode()
    return send_file(f"{os.environ.get("MUSIC_FOLDER")}{relative_music_file_path}")

@app.route("/index/missing", methods=["GET"])
def get_missing_index():
    pi_index = json.loads(request.data)
    missing_index = []
    index = {}
    with open("./index.json") as file:
        index = json.loads(file.read())
    for path in index["index"]:
        if path not in pi_index["index"]:
            missing_index.append(path)
    response = make_response(json.dumps({ "index": missing_index }), 200)
    return response

def main():
    load_dotenv()
    index = fs.create_filesystem_index("C:/Users/Phi/Music") 
    with open("./index.json", "w") as file:
        file.write(json.dumps({ "index": index }))
    app.run("0.0.0.0", port=7777, load_dotenv=False, threaded=True)

if __name__ == "__main__":
    main()