import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import threading, time

app = Flask(__name__)
latest_track = {"artist": None, "title": None}

def fetch_loop():
    global latest_track
    while True:
        try:
            resp = requests.get("https://nowplaying.jameswragg.com/", timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            track = soup.select_one(".np")
            if track:
                artist = track.select_one(".artist").get_text(strip=True)
                title = track.select_one(".title").get_text(strip=True)
                if artist and title:
                    latest_track = {"artist": artist, "title": title}
        except Exception as e:
            print("Fetch error:", e)
        time.sleep(30)

threading.Thread(target=fetch_loop, daemon=True).start()

@app.route("/nowplaying")
def nowplaying():
    return jsonify(latest_track)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
