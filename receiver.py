from flask import Flask, render_template
from flask_socketio import SocketIO
import pynmea2
import meshtastic.serial_interface
from pubsub import pub
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

PORT = "COM12"
interface = meshtastic.serial_interface.SerialInterface(devPath=PORT, noNodes=True)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("send_message")
def handle_send_message(data):
    text = data.get("text", "")

    if text:
        print("[Button]", text)
        interface.sendText(text)

def parse_with_lib(sentence):
    try:
        msg = pynmea2.parse(sentence)
        if msg.sentence_type == "GGA":
            return msg.latitude, msg.longitude
    except pynmea2.ParseError:
        print("[PARSE ERROR] Invalid NMEA:", sentence)
    return None, None, None

def on_receive(packet, interface=None):

    sentence = packet['decoded']['text']

    lat, lon = parse_with_lib(sentence)

    print(f"[PARSED] Lat: {lat:.6f}, Lon: {lon:.6f}")
    socketio.emit("gps_update", {"lat": lat, "lon": lon})

pub.subscribe(on_receive, "meshtastic.receive.text")

def heartbeat():
    while True:
        time.sleep(5)

if __name__ == "__main__":
    import threading
    threading.Thread(target=heartbeat, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000, use_reloader=False, allow_unsafe_werkzeug=True)