from flask import Flask, render_template
from flask_socketio import SocketIO
import random

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

@app.route("/")
def index():
    return render_template("index.html")

def gps_stream():
    lat = 43.0018
    lon = -78.7895

    while True:
        lat += random.uniform(-0.0001, 0.0001)
        lon += random.uniform(-0.0001, 0.0001)

        print("Sending:", lat, lon)

        socketio.emit("gps_update", {"lat": lat, "lon": lon})
        socketio.sleep(2)

if __name__ == "__main__":
    socketio.start_background_task(gps_stream)
    socketio.run(app, host="127.0.0.1", port=5000)
