import serial
from pyubx2 import UBXReader, UBX_PROTOCOL, NMEA_PROTOCOL, RTCM3_PROTOCOL

port = "COM9"
baudrate = 38400

ser = serial.Serial(port, baudrate, timeout=1)

ubr = UBXReader(
    ser,
    protfilter=UBX_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL
)

try:
    while True:
        raw, msg = ubr.read()
        if msg:
            print(msg)

except KeyboardInterrupt:
    print("Streaming stopped")

finally:
    ser.close()
