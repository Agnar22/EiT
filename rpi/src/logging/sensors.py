
from sense_hat import SenseHat
import adafruit_gps
import serial

import time
from datetime import datetime
from logger import DataLogger

class SensorReader():

    def __init__(self):
        
        self.logger = DataLogger()

        self.sense = SenseHat()
        self.sense.set_imu_config(True, True, False)

        self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)
        # Turn on the basic GGA and RMC info
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Set update rate to 1 Hz
        self.gps.send_command(b"PMTK220,1000")

    def read_gyro(self):
        return self.sense.get_orientation_degrees()
    
    def read_acc(self):
        return self.sense.accel_raw

    def read_timestamp(self):
        return str(datetime.utcnow())

    def read_pos(self):
        if self.gps.update():
            if self.gps.has_fix:
                return {"longitude": self.gps.longitude, "latitude": self.gps.latitude}

        return {"longitude": None, "latitude": None}

    def _pack_data(self, data, timestamp, acc_data, gyro_data, gps_data):
        data.setdefault("timestamp", []).append(timestamp)
        data.setdefault("g-force_x", []).append(acc_data["x"])
        data.setdefault("g-force_y", []).append(acc_data["y"])
        data.setdefault("g-force_z", []).append(acc_data["z"])
        data.setdefault("orientation_roll", []).append(gyro_data["roll"])
        data.setdefault("orientation_pitch", []).append(gyro_data["pitch"])
        data.setdefault("orientation_yaw", []).append(gyro_data["yaw"])
        data.setdefault("position_longitude", []).append(None)
        data.setdefault("position_latitude", []).append(None)

        return data
        

    def run(self, freq=1000, sync_size=600):
        sensor_data = {}
        while True:
            timestamp = self.read_timestamp()
            acc = self.read_acc()
            gyro = self.read_gyro()
            pos = self.read_pos()

            sensor_data = self._pack_data(sensor_data, timestamp, acc, gyro, None)

            if len(sensor_data["timestamp"])%sync_size == 0 and len(sensor_data["timestamp"]) != 0:
                print("Logging")
                self.logger.log(sensor_data)
                sensor_data={}

            time.sleep(1/freq)

if __name__ == "__main__":

    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    sensor_reader = SensorReader()
    sensor_reader.run(freq=10)
