from flask import Flask, render_template
from flask_socketio import SocketIO
import pynmea2
import meshtastic.serial_interface


app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

interface = meshtastic.serial_interface.SerialInterface()

@app.route("/")
def index():
    return render_template("index.html")


def parse_with_lib(sentence):
    try:
        msg = pynmea2.parse(sentence)

        if msg.sentence_type == "GGA":
            return msg.latitude, msg.longitude

    except pynmea2.ParseError:
        return None, None

    return None, None


def on_receive(packet, interface):
    if 'decoded' in packet and 'text' in packet['decoded']:
        sentence = packet['decoded']['text']

        lat, lon = parse_with_lib(sentence)

        if lat is not None and lon is not None:
            print("Sending:", lat, lon)

            socketio.emit("gps_update", {
                "lat": lat,
                "lon": lon
            })


# Attach callback
interface.onReceive = on_receive


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000)