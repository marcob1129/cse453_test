import serial
import meshtastic.serial_interface
import time

GPS_PORT = "COM7"
MESHTASTIC_PORT = "COM11"
GPS_BAUD = 9600       # try 115200 if no data comes through
MESH_BAUD = 115200

gps = serial.Serial(GPS_PORT, GPS_BAUD, timeout=1)

interface = meshtastic.serial_interface.SerialInterface(devPath=MESHTASTIC_PORT)

def is_gga(line):
    return line.startswith("$GPGGA") or line.startswith("$GNGGA")

while True:
    try:
        line = gps.readline().decode(errors="ignore").strip()

        if not line:
            continue

        if is_gga(line):
            print(f"[SEND] {line}")
            interface.sendText(line)
            time.sleep(2)  # rate limit to avoid flooding mesh

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(1)