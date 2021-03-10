
import time

class DataLogger():

    def __init__(self, data_path="../../data/"):
        self.data_path = data_path

        self.num_measurements = len(self.measurements)

    def _pack(self, sensor_data: dict):
        log_entry = []

        for sensor, data in sensor_data.items():
            if sensor in self.measurements:

                




if __name__ == "__main__":
    import os

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)